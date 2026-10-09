# TZ-63 — On the VPS: the run delivers an answer or a notice, never a status, and its subagents cannot leave the foreground

**Canonical filename:** `CryptoTZ/TZ-63-vps-run-answer-only.md`
**Report:** `CryptoReports/TZ-63-vps-run-answer-only-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the run unit. **A0 stops BLOCKED on any other
machine, before the gate and before any other work.**
**Class:** branch TZ (contract §8) — it modifies three files under `vps/**`.
**Branch:** `tz-63-vps-run-answer-only` · **Model:** Sonnet
**Previous TZ:** TZ-62, COMPLETED, merged at `d446a6b` (pull request #50).
**Written against:** contract v28, map `2026-10-09-e`, methodology `2026-10-09-b`, and `main` at `ef89542` — its
`vps` tree `d65dfbd5d1830b477a084e2f288a851e377d6947` — read by the Architect from the repository on 09.10.2026,
with the contract, the methodology and the map as delivered for upload beside this TZ. Map §10 row «A headless
run delivered a status as its answer» is what this TZ executes.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-09-e.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-09-e.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` |

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Files this TZ's gate adds:

| Added file | Lines | MD5 | Required |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 1028 | `5f50e8785755b340d2e8f07425432f44` | its version line reads `**Version 28.**` — a lower version is BLOCKED (inv. 59); lines and MD5 reported |
| `ANALYST-INSTRUCTIONS.md` | 4738 | `918a86d648a80e09c72c8c0f4660fbe8` | its revision line reads `**Revision 2026-10-09-b.**` or a later one — an earlier one is BLOCKED, because section U reads its §2 and the run reads its §15; lines and MD5 reported |
| `vps/run.py` | 336 | `beb420d158630b8e5801badf26aee2b4` | reported; a different file is a finding, never a block |
| `vps/selftest.py` | 1107 | `53045fb9aafcf1c26252a4f76da2babe` | reported; as above |
| `vps/units/crypto-run.service` | 37 | `dc6ac1073c42b03c1a2f3b754e28bca0` | reported; as above |

The map itself: 3365 lines, MD5 `a3d99eb9bcbd9965a18f80cfc0fbb281` — reported, not enforced. The tree `origin/main:vps` is reported beside
them; `d65dfbd5d1830b477a084e2f288a851e377d6947` is the one this TZ was written against, and a different one is a
finding, never a block.

---

## 1. Credentials

None arrives, none is read and none is written. **No model session is opened and the `claude` binary is never
executed:** C1 reads its bytes with `grep`, and the code under change runs offline in the selftest against stub
sessions.

---

## 2. Contract, map, methodology and code text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section or file named.

> **A final message carrying no line that opens with «Время анализа:» — the answer's first line, `ANALYST-INSTRUCTIONS.md` §2 — is not an answer: the unit delivers the notice «Анализ не завершён.» in its place, and never the message** (since v28).

— contract §4. §12.1–§12.3 build exactly this test, and nothing beside it.

> Code under `vps/` runs on the VPS only from `main`: the deployer fast-forwards its own clone and installs what changed, and nothing else installs anything.

— contract §7 item 15. The merge installs the change; this session restarts nothing.

> a TZ with a stage on the VPS names its host in its header, and its first stage stops BLOCKED on any other machine before any work

— map §10, row «The assistant's build sequence».

> Время анализа: ЧЧ:ММ Тбилиси · ЧЧ:ММ UTC · ЧЧ:ММ ET · Binance Futures

— methodology §2, the skeleton's first line: the head `run.ANSWER_HEAD` carries, and the line section U checks
the methodology against.

> **The run is ONE turn, and its last message is the answer** (contract §4).

— methodology §15. §12.4 keeps the Agent tool from sending a subagent to the background; what the session does
is the methodology's, and this TZ changes none of it.

> Never prints the answer.

— `vps/run.py`'s docstring. §12.3's journal line carries the message's length, never its text.

---

## 3. What is built and what is read

**The defect, measured on 09.10.2026** (the map's row named in the header): the press whose writer committed
`ef89542` ran methodology `2026-10-09-a`; the trader launched the hunter through the Agent tool, the tool ran it
in the background, and the trader ended its turn on a status in English — «The hunter is still running the
catalyst, unlock and positioning hunt…». `run.main` handed that status to the outbox as the answer, because its
one test was a non-empty result, and the owner received it in place of an analysis. No state and no log reached
`main`.

**Built:** (1) the run unit's environment carries `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` beside
`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` (§12.4) — the variable third-party documentation of Claude Code names as the
one that keeps a subagent from running in the background; (2) `run.is_answer`, and `run.main` delivering a final
message only where a line of it opens with `run.ANSWER_HEAD`, «Время анализа:», once leading whitespace and
markdown marks are set aside — and notice S7, «Анализ не завершён.», in its place otherwise, with one journal line
carrying the message's length (§12.1–§12.3); (3) the selftest: section O's stub answers with `run`'s own head,
because under the delivery test its old result is not an answer — control 4 shows exactly that (§12.5) — and
section U, 18 checks, with the methodology's skeleton among them (§12.6). **Read on the VPS, read-only:** the
installed CLI for the variable's name (C1), and the delivery test over every day-log answer on `main` (C2).

---

## 4. Scope

### Files to Modify

```
vps/run.py    vps/selftest.py    vps/units/crypto-run.service
```

### Files to Create

None.

### Files to Delete

None.

### On the VPS, outside the repository — authorised, and nothing else

- the scratch directory `/root/tz63`, mode `0700`, holding §12.7's script, and gone at the end;
- reading, never writing or executing: the file `command -v claude` resolves to, and the directory two levels
  above it where C1 says so; `/var/lib/crypto-auto/deployed-vps-tree`; `systemctl` state.

**No unit is started, stopped, restarted, enabled or disabled. No run is started, requested or stopped, and
nothing under `/etc/crypto-auto/`, `/etc/systemd/`, `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto`
or `/var/spool/crypto-auto` is written.**

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **The session.** `run.CLAUDE`, `run.PROMPT`, `run.APPEND`, the model and the effort do not move; what the session
  does is the methodology's (§2).
- **The notice.** `common.S7` does not move; it is what the owner receives for a final message that is not an
  answer, as for a session that failed.
- **The bot.** `vps/bot.py`'s delivery and chunking do not move.
- **Whether the variable works.** C1 reads its name in the installed CLI; the first press after the merge measures
  it, read from the run unit's journal by the next TZ (the map's row).
- **Installing the change** — the deployer does it after the merge, behind the selftest and
  `systemd-analyze verify` (§2).

---

## 6. Rules — binding in every stage

1. **No model session**, and the `claude` binary is never executed: C1 reads it with `readlink`, `ls` and `grep`.
2. **No unit changes state** because of this session: `systemctl` is used to read.
3. **The session's own network reads are `git`'s and `gh`'s, and nothing else.**
4. **§12.7's script prints counts and file names, never an answer's text.**
5. **Python 3.12's standard library and bash only.**
6. **Time is UTC everywhere.**
7. **§12's blocks are copied byte for byte, never retyped:** each block is the lines between its opening fence and
   the next closing fence, each ending in a newline, blank lines included. Every block is ASCII; the head's
   Russian is written as the escape `vps/common.py` uses for its Russian strings.

---

## 7. Stage A — readings, no writes

- **A0. The host — first, before contract §4a's gate and before anything else:** `hostname`;
  `systemctl is-active crypto-bot.service crypto-exchange.service`; `test -d /srv/crypto-auto/.git && echo clone`;
  `id -u cryptorun`. **Known answers:** `vultr`; `active` twice; `clone`; `995`. **Derived:** TZ-62's report read
  exactly these on this host at 2026-10-09T06:03:44Z. **Any other answer: BLOCKED.** The session writes a report
  carrying A0's lines and its own `hostname`, commits it to `main`, and does nothing else (§2).
- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git rev-parse origin/main:vps` and `cat /var/lib/crypto-auto/deployed-vps-tree`. **Known answer:** both
     `d65dfbd5d1830b477a084e2f288a851e377d6947`. **Derived:** the Architect's session read `git rev-parse` of
     `d446a6b:vps` and `ef89542:vps` equal to it and `git log --oneline d446a6b..ef89542 -- vps/` empty, and the
     map records TZ-62's merge at `d446a6b` with this tree and its first alert at 2026-10-09T07:00Z. A different
     value is a finding, never a block.
  2. On `origin/main`, `grep -c -F` of each line §12 edits at — in `vps/run.py`:
     `RESULT_CATEGORIES = ("subtype", "api_error_status", "terminal_reason", "stop_reason")`, `def category(value):`
     and `    answered =(not is_error) and isinstance(result, str) and result.strip() != ""`; in
     `vps/units/crypto-run.service`: `Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`; in `vps/selftest.py`:
     `"is_error": False, "result": "SELFTEST-O-RESULT-TEXT",`,
     `                "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW")`,
     `                           "SELFTEST_O_CLAUDE_SAW": claude_saw, "SELFTEST_O_WRITER_SAW": writer_saw})`,
     `SECTIONS = (("A", section_a),` and `            ("T", section_t))`. **Known answer:** `1` each.
     **Derived:** the Architect's session applied §12 to `ef89542` with a script asserting exactly one occurrence
     of each. **Any other count: BLOCKED** — §12 is written against those lines.
  3. `systemctl show crypto-run.service -p ActiveState -p NRestarts` and
     `systemctl list-unit-files 'crypto-*' --no-pager` — the values V5 compares. Not registered.
  4. `python3 vps/selftest.py` on the branch before any edit. **Known answer:** exit 0 and
     `selftest: sections 20 checks 296 failed 0 empty 0`. **Derived:** TZ-62 registered exactly this as its V1 for
     the tree `d65dfbd5…`, and the Architect's session read the same line on that tree.

---

## 8. Stage B — the code, on the branch

- **B1. `vps/run.py`** — §12.1, §12.2 and §12.3.
- **B2. `vps/units/crypto-run.service`** — §12.4.
- **B3. `vps/selftest.py`** — §12.5 and §12.6.
- **B4.** `md5sum vps/run.py vps/selftest.py vps/units/crypto-run.service` and `wc -l` of the three. **Known
  answer:** `41161832221abd8a6d4f026c6b7b21d8` at 351 lines, `e7fb68d609bd36965f76145528d2575e` at 1186 lines and
  `9355ee94131624ff3fcdafe409183f38` at 38 lines. **Derived:** the Architect's session applied §12 to these three
  files at `ef89542` and read these values. A different digest means a block was not copied byte for byte: the
  session copies it again, and does not go on until the three match.

---

## 9. Stage C — on the VPS, on the branch's code, read-only

- **C1. The CLI the run unit starts**, read and never executed:

  ```
  p="$(readlink -f "$(command -v claude)")"; echo "$p"; ls -l "$p"
  grep -a -c -F CLAUDE_CODE_DISABLE_BACKGROUND_TASKS "$p"
  grep -a -c -F run_in_background "$p"
  ```

  and, only where both counts are `0` and the file is smaller than 1 MiB — a launcher, not the program —
  `grep -r -a -l -F` of each of the two names over the directory two levels above `$p`, listing the files that
  carry it. **Not registered:** no session of the Architect has read this file. The report records the path, the
  size and both counts, or the listed files; a variable absent from the program is a finding the map decides on,
  and the methodology's foreground rule and §12.3's delivery test stand without it.
- **C2. The delivery test on the record:** §12.7's script copied into `/root/tz63`, then
  `python3 /root/tz63/tz63_record.py "$PWD"` from the branch's checkout. **Known answer:**
  `answers N refused 0` — `N` the number of files `analyst/log/*.md` in the checkout that do not end in
  `.hunt.md`, 48 at `ef89542` — and `status refused`. **Derived:** the Architect's session ran the script with the
  branch's `vps/run.py` at `ef89542` and read `answers 48 refused 0` and `status refused`. A log added after
  `ef89542` is read the same way. **Any refused file: BLOCKED** — the branch is pushed, no pull request is opened,
  and the report names the file first: a delivery test that refuses a real answer is never installed.

---

## 10. Validation

- **V1. Selftest.** `python3 vps/selftest.py` on the branch: exit 0,
  `selftest: sections 21 checks 314 failed 0 empty 0`, `section O: checks 27 failed 0` and
  `section U: checks 18 failed 0`. **Derived:** A1.4's 296 checks plus section U's 18 — one on the methodology's
  skeleton, ten `is_answer` cases, six on `run.main` with a status as the final message and one on the unit — read
  by the Architect's session on §12's files. **Negative controls** (inv. 68), each applied alone, then reverted,
  B4's digest restored and V1 green again:
  1. in `vps/run.py`, `    answered = (not is_error) and is_answer(result)` →
     `    answered = (not is_error) and isinstance(result, str) and result.strip() != ""`: exit non-zero, and
     **exactly 5** checks of section U fail — `a status as the final message: exit 1`,
     `a status as the final message: one notice S7`, `a status as the final message: no answer in the outbox`,
     `one line crypto-run: final message is not an answer chars=171` and `the summary carries answer_chars=0`;
  2. in `vps/run.py`, `ANSWER_MARKS = " \t*_#>"` → `ANSWER_MARKS = ""`: **exactly 2** fail —
     `is_answer: an answer after blank lines and indentation is True` and
     `is_answer: an answer under emphasis is True`;
  3. the line `Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` deleted from `vps/units/crypto-run.service`:
     **exactly 1** fails — `exactly one Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`;
  4. in `vps/selftest.py`, `"result": os.environ["SELFTEST_O_RESULT"],` → `"result": "SELFTEST-O-RESULT-TEXT",`:
     **exactly 2** checks of section O fail — `the run answered: exit 0` and `the answer went to the outbox` —
     which is why §12.5 moves section O's stub: under the delivery test its old result is not an answer.

  In each, every other check of all twenty-one sections stays green. **Derived:** the Architect's session ran all
  four on §12's files and read exactly these partitions.
- **V2. Syntax.** `python3 -m py_compile vps/run.py vps/selftest.py`.
- **V3. The units.** `systemd-analyze verify vps/units/*` from the branch: exit 0. **Derived:** TZ-60's C1 read
  exit 0 with no output on this host's units, and the installer runs the same command before every install and
  installed the tree `d65dfbd5…`; on a machine where both trees print one identical message about a host path, the
  Architect's session read byte-identical output for `main`'s units and the branch's — the added line adds nothing
  to verify.
- **V4. Scope.** `git diff --name-only origin/main...HEAD` lists exactly the three files of §4.
- **V5. Nothing touched.** After C, `systemctl show crypto-run.service -p ActiveState -p NRestarts` and
  `systemctl list-unit-files 'crypto-*' --no-pager` equal A1.3's.
- **V6. Pushes.** The branch pushed and a pull request opened (or contract §8's fallback), unless C2 blocked;
  `main` receives nothing from this session but its report.

No regression: every section of `vps/selftest.py` at `origin/main` stays green with its own checks unchanged,
section O's 27 included; section U is the only new one.

---

## 11. The report

Contract §10's template. **The first four lines after `## Status`:**

1. **The delivery test** — built, V1's total, section U's count, and the four controls' partitions.
2. **The variable** — §12.4 in the unit, and C1's path, size and counts.
3. **The record** — C2's two lines.
4. **The tree** — A1.1's two values.

---

## 12. Dictated blocks

### 12.1 `vps/run.py` — inserted after the line `RESULT_CATEGORIES = ("subtype", "api_error_status", "terminal_reason", "stop_reason")`

```
# TZ-63: the market answer's first line opens with this head (ANALYST-INSTRUCTIONS.md section 2,
# contract v28 section 4); a final message with no line opening with it is not an answer.
ANSWER_HEAD = "\u0412\u0440\u0435\u043c\u044f \u0430\u043d\u0430\u043b\u0438\u0437\u0430:"
ANSWER_MARKS = " \t*_#>"   # set aside before the head: indentation and markdown emphasis or heading
```

### 12.2 `vps/run.py` — inserted before the line `def category(value):`

The block ends with two blank lines.

```
def is_answer(result):
    """TZ-63: True when result is a market answer -- a string with a line that opens with
    ANSWER_HEAD once leading whitespace and markdown marks are set aside. A status, a plan,
    a one-line refusal or an empty string is not an answer, and the run never delivers one."""
    if not isinstance(result, str):
        return False
    return any(line.lstrip(ANSWER_MARKS).startswith(ANSWER_HEAD) for line in result.splitlines())


```

### 12.3 `vps/run.py` — replaces the one line `    answered =(not is_error) and isinstance(result, str) and result.strip() != ""`

```
    answered = (not is_error) and is_answer(result)
    if not is_error and isinstance(result, str) and result.strip() != "" and not answered:
        common.log("crypto-run: final message is not an answer chars=%d" % len(result))
```

### 12.4 `vps/units/crypto-run.service` — inserted after the line `Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`

```
Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1
```

### 12.5 `vps/selftest.py` — section O: three lines replaced

The line

```
json.dump({"type": "result", "subtype": "stub_subtype", "is_error": False, "result": "SELFTEST-O-RESULT-TEXT",
```

becomes

```
json.dump({"type": "result", "subtype": "stub_subtype", "is_error": False, "result": os.environ["SELFTEST_O_RESULT"],
```

the line

```
                "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW")
```

becomes

```
                "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW", "SELFTEST_O_RESULT")
```

and the line

```
                           "SELFTEST_O_CLAUDE_SAW": claude_saw, "SELFTEST_O_WRITER_SAW": writer_saw})
```

becomes the three lines

```
                           "SELFTEST_O_CLAUDE_SAW": claude_saw, "SELFTEST_O_WRITER_SAW": writer_saw,
                           # TZ-63: the stub's final message is an answer, opening with run's own head.
                           "SELFTEST_O_RESULT": run.ANSWER_HEAD + " SELFTEST-O-RESULT-TEXT"})
```

### 12.6 `vps/selftest.py` — section U, inserted before the line beginning `SECTIONS = (("A", section_a),`

The block ends with two blank lines.

```
# --- U: the delivery test (TZ-63) ----------------------------------------------------
STUB_CLAUDE_U = """#!/usr/bin/env python3
import json, os, sys
json.dump({"type": "result", "subtype": "success", "is_error": False, "result": os.environ["SELFTEST_U_RESULT"],
           "num_turns": 2, "duration_ms": 10, "modelUsage": {}, "permission_denials": [], "usage": {},
           "total_cost_usd": 0.1}, sys.stdout)
"""
# The final message the run of 09.10.2026 delivered, two of its lines verbatim.
U_STATUS = ("The hunter is still running the catalyst, unlock and positioning hunt. Here's where the run stands:\n"
            "\n"
            "When the report arrives, I'll read it and do my four allowed lookups.\n")


def section_u(s):
    head = run.ANSWER_HEAD
    with open(os.path.join(REPO, "ANALYST-INSTRUCTIONS.md"), encoding="utf-8") as fh:
        lines = [line.rstrip("\n") for line in fh]
    starts = [i for i, line in enumerate(lines) if line.startswith("## 2. ")]
    fence = None
    if len(starts) == 1:
        fence = next((i for i in range(starts[0] + 1, len(lines)) if lines[i] == "`" * 3), None)
    s.check("ANALYST-INSTRUCTIONS.md section 2's skeleton opens with run.ANSWER_HEAD",
            fence is not None and fence + 1 < len(lines) and lines[fence + 1].startswith(head + " "))
    cases = ((head + " 22:59 Tbilisi\n\n# R\n", True, "an answer"),
             ("\n\n  " + head + " 22:59\n", True, "an answer after blank lines and indentation"),
             ("**" + head + "** 22:59\n", True, "an answer under emphasis"),
             ("Note.\n\n" + head + " 22:59\n", True, "an answer after a line before it"),
             (U_STATUS, False, "the status the run of 09.10.2026 delivered"),
             (common.S7, False, "notice S7"),
             ("Soon: " + head + " 22:59\n", False, "the head inside a line"),
             ("", False, "an empty string"),
             (None, False, "None"),
             (42, False, "a number"))
    for result, want, label in cases:
        s.check("is_answer: %s is %s" % (label, want), run.is_answer(result) is want)
    tmp = tempfile.mkdtemp(prefix="vps-selftest-u.")
    env_keys = ("PATH", "CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", "SELFTEST_O_WRITER_SAW", "SELFTEST_U_RESULT")
    saved_env = {k: os.environ.get(k) for k in env_keys}
    patched = [(common, "OUTBOX_DIR"), (common, "REQUESTS_DIR"), (run, "WRITER"), (run, "own_memory_max"),
               (run, "own_swap_max")]
    saved_attrs = [(mod, name, getattr(mod, name)) for mod, name in patched]
    saved_term = signal.getsignal(signal.SIGTERM)
    want_line = "crypto-run: final message is not an answer chars=%d" % len(U_STATUS)
    try:
        paths, tree, _ = o_fixtures(tmp, STUB_CLAUDE_U, "sk-ant-oat01-selftest-planted-" + os.urandom(6).hex())
        os.environ.update({"PATH": paths["bin"] + os.pathsep + (saved_env["PATH"] or ""),
                           "CREDENTIALS_DIRECTORY": paths["creds"], "RUNTIME_DIRECTORY": paths["runtime"],
                           "SELFTEST_O_WRITER_SAW": os.path.join(tmp, "writer-saw"), "SELFTEST_U_RESULT": U_STATUS})
        common.OUTBOX_DIR, common.REQUESTS_DIR = paths["outbox"], paths["requests"]
        run.WRITER = os.path.join(paths["bin"], "writer-stub.py")
        run.own_memory_max = run.own_swap_max = lambda: None
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = run.main(["--tree", tree])
        summary = out.getvalue()
        s.check("a status as the final message: exit 1", code == 1)
        s.check("a status as the final message: one notice S7", notices(paths["outbox"]) == [common.S7])
        s.check("a status as the final message: no answer in the outbox",
                [n for n in os.listdir(paths["outbox"]) if "-answer-" in n] == [])
        s.check("one line " + want_line, summary.splitlines().count(want_line) == 1)
        s.check("the summary carries answer_chars=0", " answer_chars=0" in summary)
        s.check("the summary never carries the status", "The hunter is still running" not in summary)
    finally:
        signal.signal(signal.SIGTERM, saved_term)
        for mod, name, value in saved_attrs:
            setattr(mod, name, value)
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(tmp, ignore_errors=True)
    with open(os.path.join(HERE, "units", "crypto-run.service"), encoding="utf-8") as fh:
        unit_lines = [line.rstrip("\n") for line in fh]
    s.check("exactly one Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1",
            unit_lines.count("Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1") == 1)


```

and the line

```
            ("T", section_t))
```

becomes

```
            ("T", section_t), ("U", section_u))
```

### 12.7 The record — `/root/tz63/tz63_record.py`

```
#!/usr/bin/env python3
"""TZ-63 C2: the delivery test over every day log's answer in a checkout (argv[1]), with that
checkout's vps/run.py. Prints counts and file names, never an answer's text."""
import glob
import os
import sys

REPO = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(REPO, "vps"))
import run  # noqa: E402

# The final message the run of 09.10.2026 delivered, two of its lines verbatim.
STATUS = ("The hunter is still running the catalyst, unlock and positioning hunt. Here's where the run stands:\n"
          "\n"
          "When the report arrives, I'll read it and do my four allowed lookups.\n")
FENCE = "`" * 3
answers, refused = 0, []
for path in sorted(glob.glob(os.path.join(REPO, "analyst", "log", "*.md"))):
    if path.endswith(".hunt.md"):
        continue
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    cut = text.find("\n" + FENCE + "\nINTERNAL APPENDIX")
    if cut < 0:
        cut = text.find(FENCE)
    answer = text[:cut] if cut >= 0 else text
    if run.is_answer(answer):
        answers += 1
    else:
        refused.append(os.path.basename(path))
print("answers %d refused %d" % (answers, len(refused)))
for name in refused:
    print("refused", name)
print("status", "answer" if run.is_answer(STATUS) else "refused")
```

---

## 13. Commit messages

Implementation, on the branch:

```
TZ-63: vps — the run delivers an answer or the notice, never a status; subagents cannot leave the foreground
```

Report, on `main`:

```
TZ-63: report — the delivery test, the variable, and the record read through it
```
