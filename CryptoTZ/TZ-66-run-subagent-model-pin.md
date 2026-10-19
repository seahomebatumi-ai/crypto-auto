# TZ-66 — On the VPS: the hunter and the sheriff on pinned model ids

**Canonical filename:** `CryptoTZ/TZ-66-run-subagent-model-pin.md`
**Report:** `CryptoReports/TZ-66-run-subagent-model-pin-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the run unit. **A0 stops BLOCKED on any other
machine, before the gate and before any other work.**
**Class:** branch TZ (contract §8) — it modifies two files under `vps/**`.
**Branch:** `tz-66-run-subagent-model-pin` · **Model:** Sonnet
**Previous TZ:** TZ-65, COMPLETED; merged with TZ-64 at `373a6cf` (pull request #53).
**Written against:** contract v30, map `2026-10-19-b`, methodology `2026-10-19-a`, and `main` at `c625bf4` — its
`vps` tree `8b2b6d8c5106eb1cada9c9437780cc59b5a1385a` — read by the Architect from the repository on 19.10.2026,
with the map as delivered for upload beside this TZ. Map §10 row «The hunter runs on a model alias» is what this
TZ executes.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-19-b.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-19-b.**` |
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
| `EXECUTOR-INSTRUCTIONS.md` | 858 | `25fac2ff37d2cb12f4bf0e35ce9c9b06` | its version line reads `**Version 30.**` — a lower version is BLOCKED (inv. 59); lines and MD5 reported |
| `vps/run.py` | 351 | `41161832221abd8a6d4f026c6b7b21d8` | reported; a different file is a finding, never a block — B1's `git apply --check` is the block |
| `vps/selftest.py` | 1807 | `04d484d41ac49a466ec60c0df3c17dda` | reported; as above |

The map itself: 2788 lines, MD5 `5be2e6e013a7288b8ed03a7593ab8970` — reported, not enforced. The tree
`origin/main:vps` is reported beside them; `8b2b6d8c5106eb1cada9c9437780cc59b5a1385a` is the one this TZ was written
against, and a different one is a finding, never a block.

---

## 1. Credentials

None arrives, none is read and none is written. **No model session is opened and the `claude` binary is never
executed:** A2 reads its bytes with `grep` and its version from its package file, and the code under change runs
offline in the selftest against a stub session.

---

## 2. Contract, map, methodology and code text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section or file named.

> **Decided at `2026-10-19-b`, on Claude Code's pages «Subagents», «Model configuration» and «Environment variables», read 19.10.2026:** a subagent's model is the per-call `model` first and its definition's second, so a named agent with a full id would lose to the `sonnet` the methodology passes, and `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_OPUS_MODEL` are the ids those two aliases resolve to.

— map §10, row «The hunter runs on a model alias». §11's patch builds exactly this and nothing beside it.

> **The hunter.** One Agent call, `subagent_type` `general-purpose`, `model` `sonnet`

> **The sheriff.** One Agent call, `subagent_type` `general-purpose`, the session's model

— methodology §15. Neither moves: inside the run, `sonnet` and `opus` now name one full id each.

> It passes one of the three full-cycle strings, verbatim, as the prompt of a headless session, beside one appended system-prompt sentence that names this file as the session's contract; it passes nothing else, because any further instruction in a unit's prompt is a second methodology written into a unit file.

— contract §4. The pins are environment, never instruction: `run.PROMPT`, `run.APPEND` and `run.CLAUDE` do not
move (V3).

> the run's program hands its own Claude login to the session it starts and to nothing else.

— contract §7 item 6. The pins join the environment the login already travels in; the writer's does not change.

> Code under `vps/` runs on the VPS only from `main`: the deployer fast-forwards its own clone and installs what changed, and nothing else installs anything.

— contract §7 item 15. The merge installs the change; this session restarts nothing.

> a TZ with a stage on the VPS names its host in its header, and its first stage stops BLOCKED on any other machine before any work

— map §10, row «The assistant's build sequence».

---

## 3. What is built and what is read

**The defect** (the map's row named in the header): `vps/run.py` pins the session — `--model claude-opus-5-5
--effort high` — but the methodology launches the hunter with the Agent tool's `model` `sonnet`, an alias the
installed CLI resolves. Every logged hunt reported `claude-sonnet-5` (`analyst/log/2026-10-10.md`,
`2026-10-15.md`, `2026-10-19.md`); a newer CLI on the host resolves the same word to another model, and nothing
records the change.

**The mechanism, read on 19.10.2026 from Claude Code's own documentation:** «Subagents» resolves a subagent's model
in this order — the per-invocation `model` parameter, the definition's `model`, `CLAUDE_CODE_SUBAGENT_MODEL`, the main
conversation's model; «Environment variables» defines `ANTHROPIC_DEFAULT_SONNET_MODEL` as the model id the `sonnet`
alias resolves to, and `ANTHROPIC_DEFAULT_OPUS_MODEL` the same for `opus`. A named agent carrying a full id is
therefore outranked by the `sonnet` the trader passes, while the variable governs exactly that word.

**Built** (§11's patch):

1. `run.HUNTER_MODEL = "claude-sonnet-5"` and `run.PINS`, mapping `ANTHROPIC_DEFAULT_OPUS_MODEL` to `run.MODEL` and
   `ANTHROPIC_DEFAULT_SONNET_MODEL` to `run.HUNTER_MODEL`; `run.claude_env` sets both over any value the unit's
   environment carries, in the claude child's environment alone.
2. The journal's second summary line gains `unpinned=` after `models=`: every id of `result.json`'s `modelUsage`
   outside `run.PINS`'s values, comma-separated, or `-`.
3. `vps/selftest.py` section O: five checks — the two pins, the stub session seeing both over planted values,
   `run.py`'s own environment untouched, and the second line's two fields.

*[Architect's decision, TZ-66: the hunter is pinned to `claude-sonnet-5`, the model every logged hunt ran on, so the
pin changes nothing a run does today and removes only the silent switch. Discarded: Sonnet 5.5 — Claude Code's
«Model configuration» requires v2.1.284 for it and the host read 2.1.282 on 03.10.2026, so it would be a model change
and a host change in one step, and a model change is decided on its own measurement.]*

**Read on the VPS, read-only:** the program the run unit starts (A2), and every id each run since 09.10.2026 used
(A3) — the ids the first press after the merge is compared against.

---

## 4. Scope

### Files to Create

None.

### Files to Modify

```
vps/run.py    vps/selftest.py
```

### Files to Delete

None.

### On the VPS, outside the repository — authorised, and nothing else

- the scratch directory `/root/tz66`, mode `0700`, holding §11's patch, and gone at the end;
- reading, never writing or executing: the file the run unit's `PATH` resolves `claude` to and the `package.json` two
  levels above it; the run unit's journal; `/var/lib/crypto-auto/deployed-vps-tree`; `systemctl` state.

**No unit is started, stopped, restarted, enabled or disabled. No run is started, requested or stopped, and nothing
under `/etc/crypto-auto/`, `/etc/systemd/`, `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto` or
`/var/spool/crypto-auto` is written.**

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **The session.** `run.PROMPT`, `run.APPEND`, `run.CLAUDE`, `run.MODEL` and `run.EFFORT` do not move.
- **The methodology and the contract.** The hunter is still launched with `sonnet` and the sheriff on the session's
  model (§2); what changes is what those words mean inside the run.
- **Sonnet 5.5, and any other change of model** (§3).
- **An id outside the pins** — a helper model the CLI uses on its own, if A3 shows one — is named by `unpinned=` and
  not pinned; the map decides on A3's reading.
- **Whether the pins hold on this program.** No model session is opened here: the first press after the merge
  measures it — its journal's `unpinned=` and the day log's model lines — read by the next TZ that reads the journal.
- **Installing the change** — the deployer does it after the merge, behind the selftest (§2).

---

## 6. Rules — binding in every stage

1. **No model session**, and the `claude` binary is never executed: A2 reads it with `readlink`, `ls`, `grep`, and
   `python3` reading its package file.
2. **No unit changes state** because of this session: `systemctl` and `journalctl` are used to read.
3. **The session's own network reads are `git`'s and `gh`'s, and nothing else.**
4. **§11's patch is extracted byte for byte, never retyped** — by the one command B1 gives.
5. **Python 3.12's standard library and bash only.**
6. **Time is UTC everywhere.**
7. **Model ids are printed in full** — they are this TZ's subject, and the day logs on `main` already carry them.

---

## 7. Stage A — readings, no writes

- **A0. The host — first, before contract §4a's gate and before anything else:** `hostname`;
  `systemctl is-active crypto-bot.service crypto-exchange.service`; `test -d /srv/crypto-auto/.git && echo clone`;
  `id -u cryptorun`. **Known answers:** `vultr`; `active` twice; `clone`; `995`. **Derived:** TZ-64's report read
  exactly these on this host on 16.10.2026, and TZ-63's on 09.10.2026. **Any other answer: BLOCKED.** The session
  writes a report carrying A0's lines and its own `hostname`, commits it to `main`, and does nothing else (§2).
- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git rev-parse origin/main:vps` and `cat /var/lib/crypto-auto/deployed-vps-tree`. **Known answer:** both
     `8b2b6d8c5106eb1cada9c9437780cc59b5a1385a`. **Derived:** the Architect's session read `git rev-parse` of
     `373a6cf:vps` and `c625bf4:vps` equal to it, and the paper-test recorder, which only that merge's install
     runs, has committed under `analyst/paper/` since 17.10.2026 (`6dd51f4` onward). A different value is a finding,
     never a block.
  2. `systemctl show crypto-run.service -p ActiveState -p NRestarts` and
     `systemctl list-unit-files 'crypto-*' --no-pager` — the values V5 compares. Not registered.
  3. `python3 vps/selftest.py` on `origin/main`'s tree before any edit. **Known answer:** exit 0 and
     `selftest: sections 23 checks 432 failed 0 empty 0`. **Derived:** TZ-65's V1 read exactly this on this tree,
     and the Architect's session read the same line at `c625bf4`.
- **A2. The program the run unit starts**, read and never executed — `claude` resolved under the unit's own `PATH`,
  copied from `vps/units/crypto-run.service` line 15:

  ```
  p="$(readlink -f "$(env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin sh -c 'command -v claude')")"
  echo "$p"; ls -l "$p"
  python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["version"])' "$(dirname "$(dirname "$p")")/package.json"
  for v in ANTHROPIC_DEFAULT_SONNET_MODEL ANTHROPIC_DEFAULT_OPUS_MODEL; do printf '%s ' "$v"; grep -a -c -F "$v" "$p"; done
  grep -a -o -E 'claude-(opus|sonnet|haiku)-[0-9]+(-[0-9]+)*' "$p" | sort | uniq -c
  ```

  **Not registered:** no session of the Architect has read this file. Compared, never required: TZ-63's C1 read
  `/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`, 238767288 bytes, on 09.10.2026, and TZ-58 the
  version `2.1.282` on 03.10.2026. The report records the path, the size, the version, both counts and the id list.
  A count of `0` is a finding the audit decides on, and the code is built regardless: a variable the program never
  reads changes nothing in the run.
- **A3. Every id the runs used since TZ-63's install:**

  ```
  journalctl -u crypto-run.service --since '2026-10-09 00:00:00 UTC' -o short-iso-precise --no-pager | grep -E 'crypto-run: (requests|models)='
  ```

  Printed verbatim (§6 rule 7). **Not registered:** the day logs of 10.10, 15.10 and 19.10.2026 record the hunter's
  own word, `claude-sonnet-5`, and the sheriff on `claude-opus-5-5`; a completed run's `models=` is the CLI's own
  count of the same session. The report states per invocation its `claude_exit`, its ids, and each id that is
  neither `claude-opus-5-5` nor `claude-sonnet-5`.

---

## 8. Stage B — the code, on the branch

- **B1.** `git checkout -b tz-66-run-subagent-model-pin origin/main`, then:

  ```
  install -d -m 0700 /root/tz66
  git show origin/main:CryptoTZ/TZ-66-run-subagent-model-pin.md \
      | awk '/^<!-- TZ-66 PATCH BEGIN -->$/{f=1;next} /^<!-- TZ-66 PATCH END -->$/{f=0} f' \
      | sed '1d;$d' > /root/tz66/tz66.patch
  md5sum /root/tz66/tz66.patch; wc -l < /root/tz66/tz66.patch
  git apply --check /root/tz66/tz66.patch && git apply /root/tz66/tz66.patch
  ```

  **Known answer:** the patch's MD5 is `c5cc1d197d912fd61e55d364e7628a25` (132 lines), and both `git apply` commands exit 0.
  **Derived:** the Architect's session extracted the patch from this file with exactly these commands and applied it
  to a clean checkout of `c625bf4`. A different digest means the upload changed the file: BLOCKED, nothing applied.
- **B2.** `md5sum` and `wc -l` of the two files. **Known answer:**

  | File | Lines | MD5 |
  |---|---:|---|
  | `vps/run.py` | 360 | `07f672e5bcea06be27508db66aa3a8e0` |
  | `vps/selftest.py` | 1830 | `ce6220cdf2a45709bd1f09596e209ee9` |

  **Derived:** the same application in the Architect's session. Any difference: BLOCKED.
- **B3.** `git diff --summary origin/main` prints no mode line: both files stay `100644`.
- **B4.** `rm -r /root/tz66` once the patch is applied.

---

## 9. Validation

- **V1. Selftest.** `python3 vps/selftest.py` on the branch: exit 0,
  `selftest: sections 23 checks 437 failed 0 empty 0` and `section O: checks 32 failed 0`. **Derived:** A1.3's 432
  checks plus section O's five new ones, read by the Architect's session on §11's files under Python 3.11, 3.12 and
  3.13. **Negative controls** (inv. 68), each applied alone, then reverted, B2's digests restored and V1 green again —
  in each, every other check of all twenty-three sections stays green:
  1. in `vps/run.py`, the line `    env.update(PINS)` deleted: exit non-zero,
     `selftest: sections 23 checks 437 failed 1 empty 0`, and **exactly 1** check of section O fails —
     `the stub claude sees every pin of run.PINS, not the unit's own values`;
  2. in `vps/run.py`, `HUNTER_MODEL = "claude-sonnet-5"` → `HUNTER_MODEL = "sonnet"`: exit non-zero,
     `selftest: sections 23 checks 437 failed 2 empty 0`, and **exactly 2** fail —
     `run.PINS resolves sonnet to claude-sonnet-5` and
     `the second summary line names every id used, then the one outside run.PINS`;
  3. in `vps/run.py`, `    extra["unpinned"] = ",".join(m for m in used if m not in PINS.values()) or "-"` →
     `    extra["unpinned"] = ",".join(m for m in used if m not in PINS) or "-"`: exit non-zero,
     `selftest: sections 23 checks 437 failed 1 empty 0`, and **exactly 1** fails —
     `the second summary line names every id used, then the one outside run.PINS`;
  4. in `vps/run.py`, the two lines `    env = writer_env()` and `    env.update(PINS)` of `claude_env` →
     `    os.environ.update(PINS)` and `    env = writer_env()`: exit non-zero,
     `selftest: sections 23 checks 437 failed 1 empty 0`, and **exactly 1** fails —
     `run.py put no pin into its own environment`.

  **Derived:** the Architect's session ran all four on §11's files under Python 3.12 and 3.13 and read exactly these
  partitions.
- **V2. Syntax.** `python3 -m py_compile vps/run.py vps/selftest.py`.
- **V3. The pins, and a command line that does not move.** On the branch:

  ```
  python3 -c 'import sys; sys.path.insert(0, "vps"); import run; print(run.PINS); print(run.CLAUDE == ["claude", "-p", run.PROMPT, "--output-format", "json", "--model", "claude-opus-5-5", "--effort", "high", "--allowedTools", "Bash Read Write Edit Glob Grep WebSearch WebFetch", "--append-system-prompt", run.APPEND])'
  ```

  **Known answer:** `{'ANTHROPIC_DEFAULT_OPUS_MODEL': 'claude-opus-5-5', 'ANTHROPIC_DEFAULT_SONNET_MODEL': 'claude-sonnet-5'}`
  and `True`. **Derived:** the Architect's session ran it on §11's files, and the second line prints `True` on
  `c625bf4` as well — `run.CLAUDE` is the TZ-59 list, unchanged.
- **V4. Scope.** `git diff --name-only origin/main...HEAD` lists exactly `vps/run.py` and `vps/selftest.py`.
- **V5. Nothing touched.** After B, `systemctl show crypto-run.service -p ActiveState -p NRestarts` and
  `systemctl list-unit-files 'crypto-*' --no-pager` equal A1.2's.
- **V6. Pushes.** The branch pushed and a pull request opened (or contract §8's fallback); `main` receives nothing
  from this session but its report.

No regression: every section of `vps/selftest.py` at `origin/main` keeps its checks green — section O's 27 earlier
ones unchanged, and sections S and U, which run `run.main` and read the methodology, at their counts.

---

## 10. The report

Contract §10's template. **The first four lines after `## Status`:**

1. **The code** — B1's patch digest, B2's two digests, V1's total and the four controls' partitions.
2. **The program** — A2's path, size, version, both counts and the id list.
3. **The ids the runs used** — A3's lines; per invocation its `claude_exit`, its ids, and those outside the pins.
4. **The tree** — A1.1's two values.

---

## Commit Message

Implementation, on the branch:

```
TZ-66: vps — the hunter and the sheriff on pinned model ids: the session's environment resolves sonnet and opus to full ids, and the journal names every id outside them
```

Report, on `main`:

```
TZ-66: report — the hunter and the sheriff on pinned model ids
```

---

## 11. The patch

Against `c625bf4`. B1 extracts the lines between the two markers, drops the fence lines, and applies the rest.

<!-- TZ-66 PATCH BEGIN -->
```diff
diff --git a/vps/run.py b/vps/run.py
index b012c03..bd79c60 100644
--- a/vps/run.py
+++ b/vps/run.py
@@ -49,6 +49,11 @@ APPEND = ("Read EXECUTOR-INSTRUCTIONS.md at the repository root in full before a
           "it is your contract, and the user message is a trigger from its \u00a74.")
 MODEL  = "claude-opus-5-5"
 EFFORT = "high"
+# TZ-66: each alias a subagent call can name resolves to one full id in the session's environment. The Agent
+# tool's per-call model outranks any agent definition (Claude Code docs, "Subagents", read 19.10.2026), and the
+# methodology names the hunter's as `sonnet`; the sheriff runs on MODEL, the session's own.
+HUNTER_MODEL = "claude-sonnet-5"
+PINS = {"ANTHROPIC_DEFAULT_OPUS_MODEL": MODEL, "ANTHROPIC_DEFAULT_SONNET_MODEL": HUNTER_MODEL}
 CLAUDE = ["claude", "-p", PROMPT,
           "--output-format", "json", "--model", MODEL, "--effort", EFFORT,
           "--allowedTools", "Bash Read Write Edit Glob Grep WebSearch WebFetch",
@@ -191,10 +196,12 @@ def writer_env():
 
 
 def claude_env():
-    """The environment of the claude child alone: this unit's, plus the run's own
-    Claude login read from $CREDENTIALS_DIRECTORY (TZ-55 B2.3). Raises
-    common.CredentialMissing when the login is absent."""
+    """The environment of the claude child alone: this unit's, the model pins over any
+    value it carries (TZ-66), and the run's own Claude login read from
+    $CREDENTIALS_DIRECTORY (TZ-55 B2.3). Raises common.CredentialMissing when the
+    login is absent."""
     env = writer_env()
+    env.update(PINS)
     env[LOGIN_ENV] = common.load_credential(LOGIN_CREDENTIAL)
     return env
 
@@ -242,7 +249,7 @@ def main(argv=None):
     tree = os.path.abspath(args.tree)
     line = {"requests": 0, "admitted": "no", "waited_s": 0, "writer_exit": "-", "claude_exit": "-",
             "is_error": "true", "num_turns": 0, "duration_ms": 0, "denials": 0, "answer_chars": 0}
-    extra = {"models": "-", "denied_tools": "-"}
+    extra = {"models": "-", "unpinned": "-", "denied_tools": "-"}
     extra.update((name, "-") for name in RESULT_CATEGORIES)
     # TZ-56 12.4: the limits the run ran under, its peaks and its token usage.
     seen = {"memory_max": None, "memory_swap_max": None, "mem_available": "-", "swap_free": "-"}
@@ -257,8 +264,8 @@ def main(argv=None):
                    "answer_chars=%(answer_chars)s" % line)
         # Model ids, denied tool names and result.json's categorical fields (TZ-54 §14,
         # TZ-55 B2.4); never the answer.
-        common.log("crypto-run: models=%(models)s denied_tools=%(denied_tools)s subtype=%(subtype)s "
-                   "api_error_status=%(api_error_status)s terminal_reason=%(terminal_reason)s "
+        common.log("crypto-run: models=%(models)s unpinned=%(unpinned)s denied_tools=%(denied_tools)s "
+                   "subtype=%(subtype)s api_error_status=%(api_error_status)s terminal_reason=%(terminal_reason)s "
                    "stop_reason=%(stop_reason)s" % extra)
         # TZ-56 12.4, every path; never `result`.
         common.log("crypto-run: memory_max=%s memory_swap_max=%s mem_available=%s swap_free=%s memory_peak=%s "
@@ -321,7 +328,9 @@ def main(argv=None):
     line["num_turns"] = doc.get("num_turns", 0)
     line["duration_ms"] = doc.get("duration_ms", 0)
     line["denials"] = len(denials)
-    extra["models"] = ",".join(sorted(doc.get("modelUsage") or {})) or "-"
+    used = sorted(doc.get("modelUsage") or {})
+    extra["models"] = ",".join(used) or "-"
+    extra["unpinned"] = ",".join(m for m in used if m not in PINS.values()) or "-"
     extra["denied_tools"] = ",".join(sorted({str(d.get("tool_name")) for d in denials if isinstance(d, dict)})) or "-"
     for name in RESULT_CATEGORIES:
         extra[name] = category(doc.get(name))
diff --git a/vps/selftest.py b/vps/selftest.py
index e3378da..46a9505 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -506,9 +506,12 @@ STUB_CLAUDE = """#!/usr/bin/env python3
 import json, os, sys
 with open(os.environ["SELFTEST_O_CLAUDE_SAW"], "w") as fh:
     fh.write(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "<absent>"))
+with open(os.environ["SELFTEST_O_CLAUDE_SAW"] + "-pins", "w") as fh:
+    json.dump({k: os.environ.get(k) for k in ("ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL")}, fh)
 json.dump({"type": "result", "subtype": "stub_subtype", "is_error": False, "result": os.environ["SELFTEST_O_RESULT"],
            "num_turns": 3, "duration_ms": 1234, "api_error_status": 418, "terminal_reason": "stub_terminal",
-           "stop_reason": "stub_stop", "modelUsage": {}, "permission_denials": [],
+           "stop_reason": "stub_stop", "modelUsage": json.loads(os.environ.get("SELFTEST_O_MODELS", "{}")),
+           "permission_denials": [],
            "usage": {"input_tokens": 11, "output_tokens": 22, "cache_read_input_tokens": 33,
                      "cache_creation_input_tokens": 44}, "total_cost_usd": 0.5}, sys.stdout)
 """
@@ -557,9 +560,14 @@ def section_o(s):
     s.check("run.CLAUDE carries --effort immediately followed by high",
             any(cmd[i] == "--effort" and cmd[i + 1] == "high" for i in range(len(cmd) - 1)))
     s.check("no element of run.CLAUDE equals opus", "opus" not in cmd)
+    # TZ-66: each alias a subagent call can name is pinned to one full id.
+    s.check("run.PINS resolves sonnet to claude-sonnet-5",
+            run.PINS.get("ANTHROPIC_DEFAULT_SONNET_MODEL") == "claude-sonnet-5")
+    s.check("run.PINS resolves opus to run.MODEL", run.PINS.get("ANTHROPIC_DEFAULT_OPUS_MODEL") == run.MODEL)
     tmp = tempfile.mkdtemp(prefix="vps-selftest-o.")
     env_keys = ("PATH", "CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", run.LOGIN_ENV,
-                "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW", "SELFTEST_O_RESULT")
+                "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW", "SELFTEST_O_RESULT",
+                "SELFTEST_O_MODELS") + tuple(run.PINS)
     saved_env = {k: os.environ.get(k) for k in env_keys}
     patched = [(common, "OUTBOX_DIR"), (common, "REQUESTS_DIR"), (run, "WRITER"), (run, "own_memory_max"),
                (run, "own_swap_max"), (run, "mem_available"), (run, "swap_free"), (run, "ADMISSION_POLL_S"),
@@ -579,7 +587,12 @@ def section_o(s):
                            run.LOGIN_ENV: decoy,          # a value already in the unit's environment is not the login
                            "SELFTEST_O_CLAUDE_SAW": claude_saw, "SELFTEST_O_WRITER_SAW": writer_saw,
                            # TZ-63: the stub's final message is an answer, opening with run's own head.
-                           "SELFTEST_O_RESULT": run.ANSWER_HEAD + " SELFTEST-O-RESULT-TEXT"})
+                           "SELFTEST_O_RESULT": run.ANSWER_HEAD + " SELFTEST-O-RESULT-TEXT",
+                           # TZ-66: a value already in the unit's environment is not the pin.
+                           "ANTHROPIC_DEFAULT_OPUS_MODEL": "selftest-decoy-opus",
+                           "ANTHROPIC_DEFAULT_SONNET_MODEL": "selftest-decoy-sonnet",
+                           "SELFTEST_O_MODELS": json.dumps({"claude-opus-5-5": {}, "claude-sonnet-5": {},
+                                                            "claude-haiku-selftest": {}})})
         common.OUTBOX_DIR, common.REQUESTS_DIR = paths["outbox"], paths["requests"]
         run.WRITER = os.path.join(paths["bin"], "writer-stub.py")
         run.own_memory_max = run.own_swap_max = lambda: None
@@ -596,10 +609,20 @@ def section_o(s):
         s.check("the stub writer holds neither value under any name",
                 not any(planted in v or decoy in v for v in writer_env.values()))
         s.check("run.py put no login into its own environment", os.environ.get(run.LOGIN_ENV) == decoy)
+        with open(claude_saw + "-pins") as fh:
+            pins_seen = json.load(fh)
+        s.check("the stub claude sees every pin of run.PINS, not the unit's own values", pins_seen == run.PINS)
+        s.check("run.py put no pin into its own environment",
+                os.environ.get("ANTHROPIC_DEFAULT_SONNET_MODEL") == "selftest-decoy-sonnet")
         for field, value in (("subtype", "stub_subtype"), ("api_error_status", "418"),
                              ("terminal_reason", "stub_terminal"), ("stop_reason", "stub_stop")):
             s.check("the summary carries %s=%s" % (field, value), (" %s=%s" % (field, value)) in summary)
         s.check("the summary never carries the result", "SELFTEST-O-RESULT-TEXT" not in summary)
+        second = [l for l in summary.splitlines() if l.startswith("crypto-run: models=")]
+        s.check("the second summary line names every id used, then the one outside run.PINS",
+                len(second) == 1 and second[0].startswith(
+                    "crypto-run: models=claude-haiku-selftest,claude-opus-5-5,claude-sonnet-5 "
+                    "unpinned=claude-haiku-selftest denied_tools="))
         # TZ-56 §12.4: the third summary line carries the stub's usage and cost.
         third = [l for l in summary.splitlines() if l.startswith("crypto-run: memory_max=")]
         s.check("one third summary line", len(third) == 1)
```
<!-- TZ-66 PATCH END -->
