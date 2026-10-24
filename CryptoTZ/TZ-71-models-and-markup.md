# TZ-71 — The hunter and the page reader on the current models; the bot renders tap-to-copy prices, fenced blocks and folding quotes

**Canonical filename:** `CryptoTZ/TZ-71-models-and-markup.md`
**Report:** `CryptoReports/TZ-71-models-and-markup-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the run unit. **A0 stops BLOCKED on any other
machine**, because A2 reads the two model ids with the run's own Claude login, which lives there.
**Class:** branch TZ (contract §8) — it modifies three files under `vps/**` and nothing else.
**Branch:** `tz-71-models-and-markup`, from `origin/main` · **Model:** Opus
**Trigger:** `EXECUTE TZ-71`, with nothing under it: no credential arrives.
**Written against:** contract v31, map `2026-10-24-c` and methodology `2026-10-24-c`, uploaded with this TZ, and `main`
at `15b29b9` — its `vps` tree `0eeac7c1b7310e86a454c72c4201246b1c96b97a` — read by the Architect from the repository
on 24.10.2026, where §11's patch was built, applied and run through the selftest and the four controls of V3.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-24-c.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-24-c.**` |
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
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | its version line reads `**Version 31.**` — a lower version is BLOCKED; lines and MD5 reported |
| `vps/run.py` | 364 | `988f6f4955072f6429def95d3957d974` | equal, or A1 stops: §11's patch is written against these bytes |
| `vps/bot.py` | 442 | `d1ebb118c78413f62418dd1c331f9196` | equal, or A1 stops, on the same ground |
| `vps/selftest.py` | 2207 | `55eed34fa003c2e7ea51826d438b55ce` | equal, or A1 stops, on the same ground |

The map itself: 2800 lines, MD5 `167140f2528337adda68fe103403b38c` — reported, not enforced.

---

## 1. Credentials

**None arrives.** A2 is the one step that touches a credential: the run's own Claude login,
`/etc/crypto-auto/credentials/claude-oauth-token`, reaches each of A2's two transient units as a systemd credential
(`LoadCredential=`) under the run's own user, and is read inside the unit into the environment of the `claude` child
alone. **No value is printed, logged, committed or quoted** — in the report, a commit, a check's label or the chat —
and no other credential is read: neither the deploy key, nor the bot's token, nor any other. Nothing is sent to
Telegram from the branch.

---

## 2. Contract, map and methodology text this TZ obeys

> **Contract §7 item 15:** «An implementation session never enables, starts or leaves running a persistent unit,
> timer or service from a branch; it may start TRANSIENT units from its branch for a measurement its TZ names, and its
> report proves none is left behind.»

> **Contract §7 item 6:** «A unit that runs a model session runs as its own unprivileged user, never root, and holds
> exactly two credentials: its own Claude login and the deploy key» — A2's units hold one of the two, the login, and
> run as `cryptorun`, the run unit's own user (`vps/units/crypto-run.service`, `User=cryptorun`).

> **Contract §9:** «Any TZ touching CI requires a **negative test**: force a real failure in the working tree, confirm
> the job turns red, revert, confirm the tree is clean. A gate never proven to fail is not a gate.» — this TZ touches no
> workflow; V3 holds the selftest to the same standard.

> **Map §10 row «Two model pins lag a generation»:** «`vps/run.py` pins the hunter to `claude-sonnet-5` and the CLI's
> page reader to `claude-haiku-4-5-20251001` (TZ-66, TZ-67), while the trader and the sheriff run `claude-opus-5-5`; the
> current generation of the two is `claude-sonnet-5-5` and `claude-haiku-5-5`, and TZ-71 reads both ids on the VPS
> before any constant moves.»

> **Map §10 row «The answer's markup is bold and headings only»:** «Telegram's HTML also carries `<code>` — a price the
> owner taps to copy into his order — and `<blockquote expandable>`, a block that opens on a tap, which would fold the
> ETF days, the positions and the BTC ladder under one line each. The methodology uses neither before the bot renders
> them.»

> **Telegram Bot API, «Formatting options», as mirrored by grammY's reference (`grammy.dev/ref/types/parsemode`, read
> 24.10.2026):** `<blockquote>` and `<blockquote expandable>`, `<code>`, `<pre>`; «bold, italic, underline,
> strikethrough, and spoiler entities can contain and can be part of any other entities, except pre and code»;
> «blockquote and expandable_blockquote entities can't be nested»; all other entities can't contain each other. **So a
> code span is never placed inside a quote or a bold span**, and §11's `quote_block` drops a span's backticks inside a
> quote rather than nesting it.

---

## 3. What is built, and why

**A — the two pins.** `vps/run.py`: `HUNTER_MODEL` `claude-sonnet-5` → `claude-sonnet-5-5`, `HELPER_MODEL`
`claude-haiku-4-5-20251001` → `claude-haiku-5-5`; `PINS` is built from them and is not touched. The owner's audit of
24.10.2026 asked whether the agents' models suffice: the trader and the sheriff run the current Opus at `high`; the
hunter and the page reader every fetched page passes through run a generation behind. **An id is pinned only after A2
read it answering on this host, under the run's own login, through the alias the session resolves** — the hunter's
Agent call names `sonnet`, and `ANTHROPIC_DEFAULT_SONNET_MODEL` turns it into the pin (TZ-66). Where either id does not
answer, part A is not applied at all — §11's `vps/run.py` hunk and section O's three hunks stay out — and part B goes on
alone.

**B — the markup.** `vps/bot.py`'s conversion (TZ-54 §12.3) gains four forms and loses none: a code span `` `…` `` →
`<code>…</code>`, which Telegram copies on a tap; a fenced block between two ```` ``` ```` lines → one `<pre>`; a run of
lines opening `> ` → one `<blockquote>`; a run opening `>> ` → one `<blockquote expandable>`. A block longer than the
chunk limit splits at its own line breaks, every piece rendered whole, so no tag is left open across two chunks — the
rule tables already follow, now one helper, `_block`, for all three. A fence with no closing fence is a plain line, an
empty fenced block prints nothing, and a code span inside a quote keeps its text and loses its backticks (§2). **Every
existing conversion is unchanged:** selftest section D's block converts byte for byte as before. The methodology prints
none of the new forms until a revision after this merge (map row above); until then the answer looks as it does today.

---

## 4. Scope

### Files to Create
- `CryptoReports/TZ-71-models-and-markup-report.md` — on `main` (contract §8).

### Files to Modify
- `vps/run.py` — §11's hunk: the two pins and their comment. Part A only.
- `vps/bot.py` — §11's hunks: `_CODE`, `FENCE`, `QUOTE`, `FOLD`, `_quote_kind`, `_inline`, `quote_block`, `_block`, and
  `_units` and `convert_line` calling them.
- `vps/selftest.py` — §11's hunks: the module docstring, section O's three expectations of the pins (part A only), and
  section Z with its entry in `SECTIONS`.

### Files to Delete
- None.

### On the VPS, outside the repository — authorised, and nothing else
- A2's two transient units, each collected when it exits, and A3's one version read. Nothing is installed, enabled,
  started or restarted; the deployer installs the merge, as it installs every merge (contract §7 item 15).

### On `main`
- The report only.

---

## 5. What this TZ does not decide and does not build

- No methodology text: `ANALYST-INSTRUCTIONS.md` is the Architect's, and no TZ writes it (contract §7 item 14).
- No change to the trader's model or effort (`MODEL`, `EFFORT`), to the sheriff, to the chunk limit, to the HTML →
  plain fallback, or to anything `run.py` does but the two constants.
- No message is sent to Telegram from the branch, and the bot's token is not read: the forms are tested offline, and
  Telegram's own refusal of a chunk already falls back to plain text (`send_chunk`, TZ-54).
- No other model id is probed, and no probe runs more than one turn.

---

## 6. Rules — binding in every stage

- **The patch of §11 is the implementation.** Apply it as it stands; a hunk that does not apply, or a validation item
  that fails with it applied, is reported — never repaired by a change of your own design (contract §6).
- **Minimal diff:** three files, §11's hunks and nothing else (V5).
- **No credential printed** (§1). A2's command prints one summary line per unit built from the JSON result, never the
  result whole, and never the environment.
- **Nothing persistent from the branch** (contract §7 item 15); the report proves both transient units gone (V6).
- **The selftest is never edited to make it pass** (contract §7 item 2): section O's three hunks change the pins it
  expects because part A changes the pins, and nothing else of any section moves.

---

## 7. Stage A — readings, no writes

- **A0. The host.** `systemctl cat crypto-run.service` prints `User=cryptorun` and the line
  `LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token`. Either absent → BLOCKED.
- **A1. The baseline.** `git fetch --all --prune`; the fingerprints of §0 at `origin/main`, and
  `git rev-parse origin/main:vps` equal to `0eeac7c1b7310e86a454c72c4201246b1c96b97a`. A different `vps` tree or a
  different value for any of the three `vps` files → STOP, BLOCKED, the found values in the report: §11 is written
  against these bytes. `python3 vps/selftest.py` at `origin/main` prints its last line
  `selftest: sections 25 checks 511 failed 0 empty 0` (the Architect's reading of 24.10.2026); another line is
  recorded and reported, and decides nothing by itself.
- **A2. The two ids, read on this host.** Two transient units, one per id, each run once:

  ```
  systemd-run --wait --pipe --collect --quiet --unit=tz71-probe-<n> \
    -p User=cryptorun -p Group=cryptorun -p WorkingDirectory=/var/lib/cryptorun \
    -p Environment=HOME=/var/lib/cryptorun -p Environment=DISABLE_AUTOUPDATER=1 \
    -p "Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin" \
    -p Environment=<PIN>=<id> \
    -p LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token \
    /bin/sh -c 'CLAUDE_CODE_OAUTH_TOKEN="$(cat "$CREDENTIALS_DIRECTORY/claude-oauth-token")" exec claude -p "Reply with the one word: ok" --output-format json --max-turns 1 --model <alias>' \
    | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("is_error"), d.get("subtype"), sorted((d.get("modelUsage") or {}).keys()), d.get("total_cost_usd"))'
  ```

  `n` 1: `<PIN>` `ANTHROPIC_DEFAULT_SONNET_MODEL`, `<id>` `claude-sonnet-5-5`, `<alias>` `sonnet`; `n` 2: `<PIN>`
  `ANTHROPIC_DEFAULT_HAIKU_MODEL`, `<id>` `claude-haiku-5-5`, `<alias>` `haiku`. **An id answers** where its line
  prints `False`, a subtype and a list naming the id. The report carries both commands as run, both printed lines,
  both exit codes, and `systemctl list-units --all 'tz71-probe-*'` printing no unit afterwards. **Either id not
  answering leaves part A out** (§3), and the report names the line that decided it.
- **A3. The CLI.** `runuser -u cryptorun -- env HOME=/var/lib/cryptorun claude --version`, recorded verbatim.

---

## 8. Stage B — the code, on the branch

- **B1.** Branch `tz-71-models-and-markup` from `origin/main`; `git apply` §11's patch — whole where A2 read both ids,
  without its `vps/run.py` hunk and section O's three hunks otherwise (`git apply --exclude`, or the hunks removed from
  a copy of the patch, the command recorded).
- **B2.** Validation (§9), then one implementation commit with §12's message, the branch pushed, a pull request opened
  — or contract §8's fallback.
- **B3.** The report on `main` (§10), then the closing message (contract §11).

---

## 9. Validation

Every item names its command and its known answer; each answer was derived where it says.

- **V1.** `python3 -m py_compile vps/run.py vps/bot.py vps/selftest.py` → exit 0.
- **V2.** `python3 vps/selftest.py` → exit 0 and the last line `selftest: sections 26 checks 534 failed 0 empty 0`;
  section D `checks 13 failed 0`, section E `checks 12 failed 0`, section O `checks 33 failed 0`, section Z
  `checks 23 failed 0`. *Derived: the Architect's run of §11's patch on `15b29b9`, 24.10.2026; part A out leaves every
  figure the same, because section O keeps its count and its expectations stay those of the pins in place.*
- **V3. Four controls, each on the committed branch, each reverted before the next** — apply, run the selftest, record
  the section's line and the exit code, then `git checkout -- vps/` and `git status --porcelain` printing nothing:
  - C1 `sed -i 's/tag = "<blockquote expandable>" if kind == "fold" else "<blockquote>"/tag = "<blockquote>"/' vps/bot.py`
    → `section Z: checks 23 failed 4`, exit non-zero;
  - C2 `sed -i 's/^HUNTER_MODEL = "claude-sonnet-5-5"/HUNTER_MODEL = "claude-sonnet-5"/' vps/run.py`
    → `section O: checks 33 failed 2`, exit non-zero (part A applied only);
  - C3 `sed -i 's/^HELPER_MODEL = "claude-haiku-5-5"/HELPER_MODEL = "claude-haiku-4-5-20251001"/' vps/run.py`
    → `section O: checks 33 failed 1`, exit non-zero (part A applied only);
  - C4 `sed -i 's/out.append("<code>" + m.group(1) + "<\/code>")/out.append(m.group(1))/' vps/bot.py`
    → `section Z: checks 23 failed 2`, exit non-zero.
  *Derived: the Architect's runs of the four controls on the patched tree, 24.10.2026.* A control that leaves the
  selftest green fails this item.
- **V4.** The three files after B1, lines and MD5 — with the whole patch: `vps/run.py` 365
  `84fe8282238df76f7c2ff6dc67b5ff6a`, `vps/bot.py` 496 `2bf99362c01bf0fc638c7352c64aea91`, `vps/selftest.py` 2265
  `c6ba603ec1e4c953e4be8139e236c956`. *Derived: the Architect's build.* With part A out, `vps/run.py` keeps §0's pair
  and `vps/selftest.py`'s pair is reported as found. A different value is a finding: the patch applied differently.
- **V5.** `git diff --stat origin/main...HEAD` names `vps/bot.py`, `vps/run.py` and `vps/selftest.py` and nothing else.
- **V6.** A2's two lines and exit codes, and the empty unit listing after them.
- **V7. The answer's form, offline:**
  `python3 -c 'import sys; sys.path.insert(0, "vps"); import bot; print(bot.convert("Вход `$1.231` · **стоп** `$1.3593`\n>> ETF 23.10 · 22.10\n>> BTC -137.9 · -635.5"))'`
  → `['Вход <code>$1.231</code> · <b>стоп</b> <code>$1.3593</code>', '<blockquote expandable>ETF 23.10 · 22.10\nBTC -137.9 · -635.5</blockquote>']`.
  *Derived: §11's `_inline` and `quote_block` on that input.*
- **No regression:** section D unchanged byte for byte (V2), every other section's count and result as at A1.

---

## 10. The report

`CryptoReports/TZ-71-models-and-markup-report.md`, in contract §10's format, committed to `main`. `## Fingerprints`
carries the map, §0's four files at the required revision, and the four files §0's gate adds — and per anchor the
command and the text the match returned, with the anchor table's row count beside the number compared (contract §5).
`## Implementation Summary` says whether part A was applied, in one line, with A2's deciding line. `## Remaining Risks`
names what this TZ could not measure from the branch: Telegram's acceptance of the new tags is read on the first answer
the methodology prints in them, and a refusal there falls back to plain text, chunk by chunk.

---

## Commit Message

```
TZ-71: vps — the hunter and the CLI's page reader on the current models (claude-sonnet-5-5, claude-haiku-5-5), each read on this host first; the bot renders code spans, fenced blocks, quotes and folding quotes, every block split whole
```

(Without part A: `TZ-71: vps — the bot renders code spans, fenced blocks, quotes and folding quotes, every block split whole; the model pins stay, A2 did not read both ids`.)

---

## 11. The patch

Built and verified by the Architect on `15b29b9` (24.10.2026): `git apply --check` clean, selftest 26 / 534 / 0, the
four controls of V3 red as registered. Applied with `git apply`; its own hunks are the whole of the change. The fence is four backticks because the patch
carries three.

````diff
diff --git a/vps/bot.py b/vps/bot.py
index c5e4ccc..7d796cc 100644
--- a/vps/bot.py
+++ b/vps/bot.py
@@ -40,9 +40,12 @@ DEAD_SUFFIX = ".dead"                 # TZ-55 B3: outbox_files() never lists it;
 STOP_WORDS = ("stop", "/stop", "\u0441\u0442\u043e\u043f")   # TZ-60 §12.6
 
 
-# --- TZ-54 §12.3: conversion ---------------------------------------------------
+# --- TZ-54 §12.3: conversion; TZ-71 adds code spans, fenced blocks and quotes -----
 _HEADER = re.compile(r"^#{1,6} (.+)$")
 _BOLD = re.compile(r"\*\*(.+?)\*\*")
+_CODE = re.compile(r"`([^`]+)`")    # TZ-71: a code span -- Telegram copies its text on a tap
+FENCE = "```"                       # TZ-71: a fenced block, its lines verbatim in one <pre>
+QUOTE, FOLD = "> ", ">> "           # TZ-71: a quote, and a quote that opens on a tap
 
 
 def _escape(text):
@@ -53,18 +56,46 @@ def _is_table(line):
     return line.lstrip(" \t").startswith("|")
 
 
+def _quote_kind(line):
+    """'fold' for a line opening with FOLD, 'quote' for one opening with QUOTE, None otherwise."""
+    if line.startswith(FOLD):
+        return "fold"
+    if line.startswith(QUOTE):
+        return "quote"
+    return None
+
+
+def _inline(escaped):
+    """Code spans first, their text kept as it stands; bold in the text between them. Telegram
+    nests no entity inside a code span, so a bold span never crosses one."""
+    out, pos = [], 0
+    for m in _CODE.finditer(escaped):
+        out.append(_BOLD.sub(r"<b>\1</b>", escaped[pos:m.start()]))
+        out.append("<code>" + m.group(1) + "</code>")
+        pos = m.end()
+    out.append(_BOLD.sub(r"<b>\1</b>", escaped[pos:]))
+    return "".join(out)
+
+
 def convert_line(line):
     escaped = _escape(line)
     head = _HEADER.match(escaped)
     if head:
         return "<b>" + head.group(1).replace("**", "") + "</b>"
-    return _BOLD.sub(r"<b>\1</b>", escaped)
+    return _inline(escaped)
 
 
 def pre_block(lines):
     return "<pre>" + "\n".join(_escape(line) for line in lines) + "</pre>"
 
 
+def quote_block(lines, kind):
+    """One quote of lines whose marker is already removed. Telegram nests no code span inside a
+    quote, so a span keeps its text and loses its backticks; bold converts as on a plain line."""
+    tag = "<blockquote expandable>" if kind == "fold" else "<blockquote>"
+    return tag + "\n".join(_BOLD.sub(r"<b>\1</b>", _CODE.sub(r"\1", _escape(line))) for line in lines) + "</blockquote>"
+
+
 def visible_len(unit_html):
     """Length with tags removed and &lt; &gt; &amp; read as one character each."""
     text = re.sub(r"<[^>]*>", "", unit_html)
@@ -76,31 +107,54 @@ def convert(text):
     return [html_ for html_, _ in _units(text.split("\n"), None)]
 
 
+def _block(out, block, render, limit):
+    """One block as one unit, or, where it is longer than the limit, split at its own line breaks
+    with every piece rendered whole -- a tag is never left open across two chunks."""
+    if limit is None or visible_len(render(block)) <= limit:
+        out.append((render(block), "\n".join(block)))
+        return
+    group = []
+    for line in block:
+        for piece in _cut(line, limit):
+            if group and visible_len(render(group + [piece])) > limit:
+                out.append((render(group), "\n".join(group)))
+                group = []
+            group.append(piece)
+    if group:
+        out.append((render(group), "\n".join(group)))
+
+
 def _units(lines, limit):
-    """Units in order: a maximal run of table lines is one <pre> block, every
-    other line is one unit. With a limit, a <pre> block longer than it is split
-    at its own line breaks, and a longer plain line is cut in its source text
-    before conversion. Each unit is (html, source)."""
+    """Units in order: a fenced block's lines are one <pre> block (TZ-71), a maximal run of table
+    lines is one <pre> block, a maximal run of quote lines of one kind is one quote (TZ-71), and
+    every other line is one unit. With a limit, a block longer than it is split at its own line
+    breaks, and a longer plain line is cut in its source text before conversion. A fence with no
+    closing fence is a plain line. Each unit is (html, source)."""
     out = []
     i = 0
     while i < len(lines):
+        if lines[i].rstrip().startswith(FENCE):
+            close = next((k for k in range(i + 1, len(lines)) if lines[k].strip() == FENCE), None)
+            if close is not None:
+                if close > i + 1:
+                    _block(out, lines[i + 1:close], pre_block, limit)
+                i = close + 1
+                continue
         if _is_table(lines[i]):
             j = i
             while j < len(lines) and _is_table(lines[j]):
                 j += 1
-            block = lines[i:j]
-            if limit is None or visible_len(pre_block(block)) <= limit:
-                out.append((pre_block(block), "\n".join(block)))
-            else:
-                group = []
-                for line in block:
-                    for piece in _cut(line, limit):
-                        if group and visible_len(pre_block(group + [piece])) > limit:
-                            out.append((pre_block(group), "\n".join(group)))
-                            group = []
-                        group.append(piece)
-                if group:
-                    out.append((pre_block(group), "\n".join(group)))
+            _block(out, lines[i:j], pre_block, limit)
+            i = j
+            continue
+        kind = _quote_kind(lines[i])
+        if kind:
+            marker = FOLD if kind == "fold" else QUOTE
+            j = i
+            while j < len(lines) and _quote_kind(lines[j]) == kind:
+                j += 1
+            _block(out, [line[len(marker):] for line in lines[i:j]],
+                   lambda block, k=kind: quote_block(block, k), limit)
             i = j
             continue
         line = lines[i]
diff --git a/vps/run.py b/vps/run.py
index 3e5bfb5..c0b3614 100644
--- a/vps/run.py
+++ b/vps/run.py
@@ -52,10 +52,11 @@ EFFORT = "high"
 # TZ-66: each alias a subagent call can name resolves to one full id in the session's environment. The Agent
 # tool's per-call model outranks any agent definition (Claude Code docs, "Subagents", read 19.10.2026), and the
 # methodology names the hunter's as `sonnet`; the sheriff runs on MODEL, the session's own.
-HUNTER_MODEL = "claude-sonnet-5"
+# TZ-71: the hunter and the CLI's page reader move to the current generation, each id read on this host first.
+HUNTER_MODEL = "claude-sonnet-5-5"
 # TZ-67: the CLI's own helper model -- the one that reads every fetched page for the hunter -- named by
-# TZ-66's A3 in every run since 09.10.2026 and pinned to that id.
-HELPER_MODEL = "claude-haiku-4-5-20251001"
+# TZ-66's A3 in every run since 09.10.2026 and pinned to that id; TZ-71 moves the pin.
+HELPER_MODEL = "claude-haiku-5-5"
 PINS = {"ANTHROPIC_DEFAULT_OPUS_MODEL": MODEL, "ANTHROPIC_DEFAULT_SONNET_MODEL": HUNTER_MODEL,
         "ANTHROPIC_DEFAULT_HAIKU_MODEL": HELPER_MODEL}
 CLAUDE = ["claude", "-p", PROMPT,
diff --git a/vps/selftest.py b/vps/selftest.py
index 8cb551d..806d97a 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -1,7 +1,7 @@
 #!/usr/bin/env python3
 """The VPS assistant's selftest (TZ-54 B10, TZ-55 B7, TZ-56 B5, TZ-57 B5, TZ-58 B3, TZ-60 B7,
-TZ-62 B2, TZ-64 B4, TZ-65 B1, TZ-69 B1): the sections of TZ-54 §12.14 with TZ-55 §12.7's, TZ-56 §12.6's,
-TZ-57 §12.8's, TZ-58 §12.7's, TZ-60 §12.11's, TZ-62 §12.4's, TZ-64's, TZ-65's and TZ-69's changed and new ones, each printing
+TZ-62 B2, TZ-64 B4, TZ-65 B1, TZ-69 B1, TZ-71 B2): the sections of TZ-54 §12.14 with TZ-55 §12.7's, TZ-56 §12.6's,
+TZ-57 §12.8's, TZ-58 §12.7's, TZ-60 §12.11's, TZ-62 §12.4's, TZ-64's, TZ-65's, TZ-69's and TZ-71's changed and new ones, each printing
 `section <X>: checks <n> failed <m>`, then the total.
 
     python3 vps/selftest.py
@@ -566,11 +566,11 @@ def section_o(s):
             any(cmd[i] == "--effort" and cmd[i + 1] == "high" for i in range(len(cmd) - 1)))
     s.check("no element of run.CLAUDE equals opus", "opus" not in cmd)
     # TZ-66: each alias a subagent call can name is pinned to one full id.
-    s.check("run.PINS resolves sonnet to claude-sonnet-5",
-            run.PINS.get("ANTHROPIC_DEFAULT_SONNET_MODEL") == "claude-sonnet-5")
+    s.check("run.PINS resolves sonnet to claude-sonnet-5-5",
+            run.PINS.get("ANTHROPIC_DEFAULT_SONNET_MODEL") == "claude-sonnet-5-5")
     s.check("run.PINS resolves opus to run.MODEL", run.PINS.get("ANTHROPIC_DEFAULT_OPUS_MODEL") == run.MODEL)
-    s.check("run.PINS resolves haiku to claude-haiku-4-5-20251001",
-            run.PINS.get("ANTHROPIC_DEFAULT_HAIKU_MODEL") == "claude-haiku-4-5-20251001")
+    s.check("run.PINS resolves haiku to claude-haiku-5-5",
+            run.PINS.get("ANTHROPIC_DEFAULT_HAIKU_MODEL") == "claude-haiku-5-5")
     tmp = tempfile.mkdtemp(prefix="vps-selftest-o.")
     env_keys = ("PATH", "CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", run.LOGIN_ENV,
                 "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW", "SELFTEST_O_RESULT",
@@ -599,7 +599,7 @@ def section_o(s):
                            "ANTHROPIC_DEFAULT_OPUS_MODEL": "selftest-decoy-opus",
                            "ANTHROPIC_DEFAULT_SONNET_MODEL": "selftest-decoy-sonnet",
                            "ANTHROPIC_DEFAULT_HAIKU_MODEL": "selftest-decoy-haiku",
-                           "SELFTEST_O_MODELS": json.dumps({"claude-opus-5-5": {}, "claude-sonnet-5": {},
+                           "SELFTEST_O_MODELS": json.dumps({"claude-opus-5-5": {}, "claude-sonnet-5-5": {},
                                                             "claude-haiku-selftest": {}})})
         common.OUTBOX_DIR, common.REQUESTS_DIR = paths["outbox"], paths["requests"]
         run.WRITER = os.path.join(paths["bin"], "writer-stub.py")
@@ -629,7 +629,7 @@ def section_o(s):
         second = [l for l in summary.splitlines() if l.startswith("crypto-run: models=")]
         s.check("the second summary line names every id used, then the one outside run.PINS",
                 len(second) == 1 and second[0].startswith(
-                    "crypto-run: models=claude-haiku-selftest,claude-opus-5-5,claude-sonnet-5 "
+                    "crypto-run: models=claude-haiku-selftest,claude-opus-5-5,claude-sonnet-5-5 "
                     "unpinned=claude-haiku-selftest denied_tools="))
         # TZ-56 §12.4: the third summary line carries the stub's usage and cost.
         third = [l for l in summary.splitlines() if l.startswith("crypto-run: memory_max=")]
@@ -2178,12 +2178,70 @@ def section_y(s):
     s.check("the manifest does not list crypto-etf.service", "crypto-etf.service" not in listed)
 
 
+# --- Z: TZ-71's code spans, fenced blocks, quotes and folding quotes ---------------------
+Z_INPUT = ("Price `$1.231` \u00b7 **stop** `$1.3593`\n"
+           "```\n"
+           "BTC  -635.5  +528.4\n"
+           "ETH  -110.5   +15.0\n"
+           "```\n"
+           "> first **bold** line\n"
+           "> second `code`\n"
+           ">> folded 1\n"
+           ">> folded 2\n"
+           "R&D <x> ` one backtick\n"
+           "```\n"
+           "unclosed")
+Z_EXPECTED = ("Price <code>$1.231</code> \u00b7 <b>stop</b> <code>$1.3593</code>\n"
+              "<pre>BTC  -635.5  +528.4\nETH  -110.5   +15.0</pre>\n"
+              "<blockquote>first <b>bold</b> line\nsecond code</blockquote>\n"
+              "<blockquote expandable>folded 1\nfolded 2</blockquote>\n"
+              "R&amp;D &lt;x&gt; ` one backtick\n"
+              "```\n"
+              "unclosed")
+
+
+def section_z(s):
+    got = "\n".join(bot.convert(Z_INPUT))
+    s.check("the expected block, byte for byte", got.encode("utf-8") == Z_EXPECTED.encode("utf-8"))
+    got_lines, want_lines = got.split("\n"), Z_EXPECTED.split("\n")
+    s.check("line count", len(got_lines) == len(want_lines))
+    for k, want in enumerate(want_lines):
+        s.check("line %d" % (k + 1), k < len(got_lines) and got_lines[k] == want)
+    s.check("section D's input converts as before", "\n".join(bot.convert(D_INPUT)) == D_EXPECTED)
+    s.check("an empty fenced block prints nothing", bot.convert("a\n```\n```\nb") == ["a", "b"])
+    s.check("a fenced block's plain fallback is its own lines",
+            bot.chunk("```\nx y\n```")[0] == ("<pre>x y</pre>", "x y"))
+    limit = 4000
+    quote = "\n".join("> %03d " % k + "q" * 80 for k in range(120))
+    chunks = bot.chunk(quote, limit)
+    s.check("a quote longer than the limit splits into several", len(chunks) >= 2)
+    s.check("every piece opens and closes its own quote",
+            all(c[0].startswith("<blockquote>") and c[0].endswith("</blockquote>")
+                and c[0].count("<blockquote>") == 1 for c in chunks))
+    s.check("every piece within the limit", all(bot.visible_len(c[0]) <= limit for c in chunks))
+    s.check("no quote line lost or reordered",
+            "\n".join(c[1] for c in chunks) == "\n".join("%03d " % k + "q" * 80 for k in range(120)))
+    fold = "\n".join(">> %02d " % k + "f" * 60 for k in range(20))
+    chunks = bot.chunk(fold, limit)
+    s.check("a folding quote within the limit is one unit",
+            len(chunks) == 1 and chunks[0][0].startswith("<blockquote expandable>")
+            and chunks[0][0].count("</blockquote>") == 1)
+    s.check("a quote's visible length counts its text alone",
+            bot.visible_len(bot.quote_block(["ab", "cd"], "fold")) == 5)
+    s.check("a quote carries no code span -- Telegram nests none inside one",
+            bot.convert("> `x` and **y**") == ["<blockquote>x and <b>y</b></blockquote>"])
+    mixed = "> one\n>> two\n> three"
+    s.check("a change of kind starts a new quote",
+            bot.convert(mixed) == ["<blockquote>one</blockquote>", "<blockquote expandable>two</blockquote>",
+                                   "<blockquote>three</blockquote>"])
+
+
 SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
             ("F", section_f), ("G", section_g), ("H", section_h), ("I", section_i), ("J", section_j),
             ("K", section_k), ("L", section_l), ("M", section_m), ("N", section_n), ("O", section_o),
             ("P", section_p), ("Q", section_q), ("R", section_r), ("S", section_s),
             ("T", section_t), ("U", section_u), ("V", section_v), ("W", section_w), ("X", section_x),
-            ("Y", section_y))
+            ("Y", section_y), ("Z", section_z))
 
 
 def main():
````
