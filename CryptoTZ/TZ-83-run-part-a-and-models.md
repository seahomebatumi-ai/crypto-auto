# TZ-83 — TZ-82's scope under contract v33: the run reads its own part of the contract and logs its tokens per model; the trader on `xhigh`, the page reader on Sonnet 5.5; the selftest's head check repaired

**Contract:** v33 — `EXECUTOR-INSTRUCTIONS.md` at the repository root, read in full before the sections below.
**Canonical filename:** `CryptoTZ/TZ-83-run-part-a-and-models.md`
**Report:** `CryptoReports/TZ-83-run-part-a-and-models-report.md`
**Class:** branch TZ (contract §8) — it authorises two repository files besides its report.
**Branch:** `claude/tz-83-run-part-a-and-models`
**Host:** the VPS — stage 4's readings exist only there.
**Model:** Sonnet 5.5 · medium — the code is §6's patch, written and run by the Architect; the session applies it, runs
the checks and takes three readings, and judges nothing.
**Base:** `main` at `69462d8` with this delivery's uploads — the map `2026-11-26-b`, contract v33 and its kit, the
methodology `2026-11-26-a`; `vps/` unchanged since `5db65c0`.
**Rests on:** map §10 rows «Sessions read text they never use», «The run spends its account on reading» and «A run
that leaves no log»; inv. 54, 59 and 73.
**Previous TZ:** TZ-82, BLOCKED at `kit open` on 26.11.2026 — the session's linked worktree could not check out `main`;
this TZ carries its scope. TZ-81, accepted 16.11.2026, merged at `5db65c0` (pull request #67).
**Trigger:** `EXECUTE TZ-83`, with nothing under it: no credential arrives and the Boss is asked for nothing.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-11-26-b.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-11-26-b.**` |
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

The map itself: 2783 lines, MD5 `4ac1ebf55b6a03ac6e73215410fdc5e2` — reported, not enforced.

---

## 1. Goal and scope

**Step 2's first TZ** (map §10, row «The run spends its account on reading»), **TZ-82's scope unchanged**, which
stopped before any work because contract v32's kit could not run from the linked worktree the remote client gives a
session; v33's kit does:

- **The run reads the contract's Part A alone** — 31 688 of its 52 023 bytes — where `vps/run.py`'s appended sentence
  asks today for the whole file, on every turn of a press.
- **The trader runs at `xhigh` and the CLI's page reader on `claude-sonnet-5-5`** — the owner's proposal of
  25.11.2026. The hunter stays on Sonnet 5.5; the sheriff's `xhigh` is named in methodology `2026-11-26-a` §15's call,
  never in code.
- **The run logs its tokens per model** — one journal line per id of `result.json`'s `modelUsage`, thinking tokens
  included: the line step 2's target is read from.
- **The selftest's head check repaired.** Since the methodology of 18.11.2026 the skeleton opens with its title and the
  head «Время анализа:» follows it, so section U's check — the first line after a three-backtick fence — fails on `main`
  (G1), and **`vps/install.sh` installs no `vps` tree while the selftest is red**. What fails is a stale expectation; the
  unit's `is_answer` reads every line and delivered every answer since.
- **Three readings on the VPS:** the pinned CLI's `--effort` values; the run unit's journal since 01.11.2026 — each
  press's tokens, and what the run of 23.11.2026 left (row «A run that leaves no log»); and the Executor's own sessions
  of TZ-80, TZ-81 and TZ-82 beside this one's.

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
| G1 | Baseline, on the base before `stage`'s patch: `selftest: sections 28 checks 807 failed 1 empty 0`, the one FAIL `section U: ANALYST-INSTRUCTIONS.md section 2's skeleton opens with run.ANSWER_HEAD` | the Architect's run of the base — `69462d8` with this delivery's six uploads — under Python 3.11, 3.12 and 3.13 |
| G2 | After it: `selftest: sections 28 checks 813 failed 0 empty 0` — `section O: checks 39 failed 0`, `section U: checks 18 failed 0` | the same run on the patched tree |
| G3 | Head line altered → `813 failed 1`, the FAIL in section U alone; the contract's `# PART B — ROLE 1 ONLY` line altered → `813 failed 1`, the FAIL in section O alone | the same run, each alteration made in a copy of the tree |
| G4 | R1 prints exactly two lines, the second `(low, medium, high, xhigh, max)` | the pinned build run by the Architect on 26.11.2026 — npm's `claude-code-linux-x64` 2.1.308, SHA-256 `356733f185fa988e…` = `vps/install.sh`'s pin: its `--help` prints `--effort <level> … Effort level for the current session` and wraps the levels onto the next line, which a grep on `effort` alone misses |
| G5 | R2 and R3 register nothing | they are readings: an absence is their result |

---

## 3. Run order

1. **`kit open TZ-83`.** Any FAIL is BLOCKED (contract §4a step 3). In a linked worktree `ready` takes a detached
   `HEAD` at `origin/main` and says so in its PASS line.
2. **Baseline:** `kit log selftest-base -- python3 vps/selftest.py` — G1.
3. **`kit stage TZ-83`**, then V1–V4 (§4), then a commit with §7's message — local, not yet pushed.
4. **R1–R3**, below.
5. Push; a pull request titled `TZ-83: vps — the run reads its part and logs its tokens per model`, its body naming this
   TZ and TZ-82 — or contract §8's fallback.
6. `kit usage TZ-83` and `kit units`; back on step 1's checkout (contract §4a step 7); the report; `kit close TZ-83`;
   the report to `main` by `git push origin HEAD:main`; `kit clean TZ-83`; the closing message.

**R1 — the CLI.** `kit log cli-help --grep 'effort|xhigh' -- /usr/local/libexec/crypto-auto/claude-code/2.1.308/claude
--help`. The report carries the matched lines, against G4.

**R2 — the run unit's journal.** `kit log run-journal --grep 'crypto-run: (requests|memory_max)=' --tail 80 --sh --
'journalctl -u crypto-run.service --since 2026-11-01 --no-pager -o short-iso'`, then `kit log run-journal-1123 --tail
80 --sh -- 'journalctl -u crypto-run.service --since "2026-11-23 00:00" --until "2026-11-24 00:00" --no-pager -o
short-iso'`. The report carries one row per press since 01.11.2026 — its time, `claude_exit`, `is_error`,
`num_turns`, `answer_chars` and the five token and cost fields — and for 23.11.2026 every `crypto-run:` line verbatim,
with the one sentence that names which of them shows why no day log followed, or that none does. No line of either
log is a credential (`common.log` redacts), and `kit close` scans both.

**R3 — the old form against the new.** One log over every Claude Code project directory of this repository on the VPS:
`kit log usage-old --sh -- 'for d in "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/projects/*crypto-auto*; do for n in 80 81
82; do echo "== TZ-$n $d"; python3 -I EXECUTOR-KIT.py usage TZ-$n --dir "$d"; done; done'`. Under `## Tokens` the
report carries, per TZ, its `usage:` PASS line and the directory it was found in, beside step 6's `kit usage TZ-83`,
each with the bytes of the documents its TZ asked to be read in full: TZ-80 143 638 and TZ-81 120 517, each with
contract v31's 57 581; TZ-82 10 912 with contract v32's 52 031; TZ-83 this file and contract v33's 52 023. A TZ found
in no directory is that line's FAIL, stated, with the directories listed.

---

## 4. Validation

- **V1.** `kit stage TZ-83` — PASS, both files of §6's second table at their lines and SHA-256.
- **V2.** `kit log pycompile -- python3 -m py_compile vps/run.py vps/selftest.py` — exit 0.
- **V3.** `kit log selftest -- python3 vps/selftest.py` — exit 0, G2's last line and its sections O and U.
- **V4.** G3's two negative controls, in a copy of the tree and never in it — `cp -a . /tmp/tz83-neg`, the line
  altered there with `sed -i`, `kit log neg-head -- python3 /tmp/tz83-neg/vps/selftest.py`, a fresh copy for the second
  — then `rm -rf /tmp/tz83-neg` and `git status --porcelain --untracked-files=no` listing only `vps/run.py` and
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
opening block, its lines from the first fence of three or more backticks to the first blank line. TZ-82's patch with
its comments naming TZ-83.

---

## 6. Shipped

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CryptoTZ/TZ-83-run-part-a-and-models.patch` | 12072 | `b582511b77145d435e13a77d785f7eaeef29b1aa0037e5ce09b1a768f113bd5a` | apply |

| Path | Lines | SHA-256 |
|---|---:|---|
| `vps/run.py` | 394 | `f039b2594d0c99888216050f5c5437293f7cff2b2a6925ebf1e5d49fd2af9d0a` |
| `vps/selftest.py` | 4130 | `7db8e7c9d3c918bd16f451a64fa5b1d54774403ef1818c4118cbc78dbab41431` |

---

## 7. Commit Message

```
TZ-83: vps — the run reads the contract's Part A and logs its tokens per model; the trader on xhigh, the page reader on Sonnet 5.5; the selftest's head check repaired (TZ-82's scope)
```

---

## 8. Pre-send checks

Run by the Architect before this file was sent:

- `kit caps` on this file — within 20 000 bytes.
- On a fresh clone of `main` at `69462d8` with this delivery's six uploads committed to a local origin, from a linked
  worktree whose `main` the primary clone holds: `kit open TZ-83` PASS, `kit stage TZ-83` PASS, and G1–G3 measured
  under Python 3.11, 3.12 and 3.13; the v32 kit on the same tree reproduces TZ-82's `ready` FAIL.
- `kit grow` on the map, the contract and the methodology against the files they replace — PASS for each.
- G4's two lines read off the pinned build's `--help` on this machine.
