#!/usr/bin/env python3
"""EXECUTOR-KIT.py -- the mechanical half of the standard blocks of EXECUTOR-INSTRUCTIONS.md (contract section 15).

Written by the Architect, uploaded by the Boss, pinned by SHA-256 in the contract. RUN it, never read it:

    python3 -I EXECUTOR-KIT.py <mode> [arguments]

    open TZ-NN            self, ready, number, fingerprint and the shipped files' bytes; host when the TZ names the VPS
    stage TZ-NN           the TZ's branch, its patch applied to the index, every resulting file against the manifest
    log NAME [--tail N] [--grep RE] [--sh] -- CMD...
                          CMD's whole output to $KIT_DIR/NAME.log; prints exit, lines, SHA-256 and the tail
    map PART...           prints only the named parts of the map: 11, 3.12, inv.21, row:<item of a table>
    usage TZ-NN | --session ID | --since ISO-8601 [--dir PATH]
                          tokens of Claude Code transcripts, per model: input, cache creation, cache read, output
    close TZ-NN           secrets, report, caps and units, on the report about to be committed
    clean [TZ-NN]         the tree clean, main and the TZ's branch equal to their remotes
    ready [TZ-NN] · number TZ-NN · fingerprint TZ-NN · host [vps] · units · secrets [BASE] [FILE...] · caps FILE...
    grow OLD NEW · report PATH · self
                          one block each

Exit 0 PASS · 1 FAIL · 2 wrong arguments · 3 a defect of this kit (contract section 15 says what follows).
Every mode first checks this file against the contract's pin. Python 3.11+ standard library only.
"""
import hashlib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import traceback

MAP = "SYSTEM-MAP-CRYPTOCALCUL.md"
CONTRACT = "EXECUTOR-INSTRUCTIONS.md"
PIN = re.compile(r"\*\*Kit:\*\* `EXECUTOR-KIT\.py`, SHA-256 `([0-9a-f]{64})`")
VERSION = re.compile(r"^\*\*Version (\d+)\.\*\*", re.M)
REVISION = re.compile(r"\*\*Revision (\d{4}-\d{2}-\d{2}(?:-[a-z])?)\.\*\*")
CRED_DIR = "/etc/crypto-auto/credentials"
VPS_MARKERS = (CRED_DIR, "/var/lib/crypto-auto", "/srv/crypto-auto", "/var/lib/cryptorun")
TZ_CAP, REPORT_CAP, BLOCKED_CAP = 20000, 25000, 5000
FIRST_CAPPED_CONTRACT = 32
SECTIONS = ("Status", "Inbound Filing", "Scope Executed", "Files Created", "Files Modified", "Files Renamed",
            "Files Deleted", "Implementation Summary", "Validation", "Test Results", "Deviations",
            "Pre-existing Issues", "Remaining Risks", "Commit", "Pull Request", "CI Execution",
            "Final Repository State", "Fingerprints", "Tokens")
REPORT_ONLY_LINE = "None — report-only TZ; direct push on the CryptoReports/** path (§8)."
BANNED = (("main carries this report", re.compile(r"\bmain\W+carries\W+this\W+report", re.I)),
          ("a forecast of the gate", re.compile(r"expected\s+to\s+have\s+(fired|run|passed)", re.I)))
PATTERNS = (("anthropic key", re.compile(rb"sk-ant-[A-Za-z0-9_-]{20,}")),
            ("github token", re.compile(rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})")),
            ("private key", re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
            ("telegram token", re.compile(rb"\b\d{8,10}:[A-Za-z0-9_-]{35}\b")))
NOT_TZ = re.compile(r"[^A-Za-z0-9]")


class Fail(Exception):
    """A block's own FAIL: printed as its verdict line."""


# ------------------------------------------------------------------ plumbing

def say(block, text):
    print("%s: %s" % (block, text), flush=True)


def sh(args, cwd=None, check=False):
    """(exit, stdout+stderr as text) of a command; never a shell."""
    p = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    text = p.stdout.decode("utf-8", "replace")
    if check and p.returncode != 0:
        raise Fail("%s exited %d: %s" % (" ".join(args[:3]), p.returncode, tail(text, 3)))
    return p.returncode, text


def git(root, *args, check=False):
    return sh(["git", "-C", root] + list(args), check=check)


def gitout(root, *args):
    return git(root, *args, check=True)[1].strip()


def tail(text, n):
    return " | ".join(text.strip().splitlines()[-n:])


def blob(path):
    with open(path, "rb") as fh:
        return fh.read()


def text_of(path):
    return blob(path).decode("utf-8", "replace")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def md5(data):
    return hashlib.md5(data).hexdigest()


def lines_of(data):
    return data.count(b"\n")


def repo_root():
    code, out = sh(["git", "rev-parse", "--show-toplevel"])
    if code != 0:
        raise Fail("not inside a git repository")
    return out.strip()


def tz_number(arg):
    m = re.fullmatch(r"(?:TZ-?)?0*(\d+)", arg.strip(), re.I)
    if not m:
        raise Fail("not a TZ number: %r" % arg)
    return int(m.group(1))


# ------------------------------------------------------------------ markdown

def split_row(line):
    """Cells of one Markdown table row; a | inside backticks stays inside its cell."""
    cells, cur, code = [], [], False
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    for ch in body:
        if ch == "`":
            code = not code
        if ch == "|" and not code:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur).strip())
    return cells


def tables(lines):
    """Every table in lines: (header cells, [row cells], first row's index). Cut by structure alone."""
    out, i = [], 0
    while i + 1 < len(lines):
        if lines[i].lstrip().startswith("|") and re.fullmatch(r"\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*",
                                                               lines[i + 1]):
            head, rows, j = split_row(lines[i]), [], i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            out.append((head, rows, i + 2))
            i = j
        else:
            i += 1
    return out


def table_with(lines, *names):
    """The first table whose header starts with these cell names."""
    want = [n.lower() for n in names]
    for head, rows, at in tables(lines):
        if [h.lower() for h in head[:len(want)]] == want:
            return head, rows, at
    return None


def literal(cell):
    """The exact string a cell quotes: between its first and last backtick, else the cell."""
    a, b = cell.find("`"), cell.rfind("`")
    return cell[a + 1:b] if 0 <= a < b else cell.strip()


def section(lines, heading_re):
    """Lines of the section whose heading matches, up to the next heading of the same or a higher level."""
    rx = re.compile(heading_re)
    for i, line in enumerate(lines):
        m = re.match(r"(#{1,6}) ", line)
        if m and rx.match(line):
            level, j = len(m.group(1)), i + 1
            while j < len(lines):
                n = re.match(r"(#{1,6}) ", lines[j])
                if n and len(n.group(1)) <= level:
                    break
                j += 1
            return i, lines[i:j]
    return None, []


def header(text):
    """The **Key:** value lines above a TZ's first ## heading."""
    out = {}
    for line in text.split("\n"):
        if line.startswith("## "):
            break
        m = re.match(r"\*\*([A-Za-z -]+):\*\*\s*(.*)", line)
        if m:
            out[m.group(1).strip().lower()] = m.group(2).strip()
    return out


# ------------------------------------------------------------------ blocks

def block_self(root):
    contract = os.path.join(root, CONTRACT)
    text = text_of(contract)
    pins = PIN.findall(text)
    mine = sha256(blob(os.path.abspath(__file__)))
    version = VERSION.search(text)
    if len(pins) != 1:
        raise Fail("the contract carries %d kit pin lines, not one" % len(pins))
    if pins[0] != mine:
        raise Fail("this kit hashes %s, the contract pins %s" % (mine[:16], pins[0][:16]))
    return "PASS kit sha256 %s = pin of contract v%s" % (mine[:16], version.group(1) if version else "?")


def find_tz(root, nn):
    """Paths in the working tree whose name carries TZ-nn in any spelling and ends in .md."""
    rx = re.compile(r"(?:^|/)TZ[-_ ]0*%d(?!\d)[^/]*\.md$" % nn)
    code, out = git(root, "ls-files", "-z")
    names = [n for n in out.split("\0") if n and rx.search(n) and not n.startswith("CryptoReports/")]
    return sorted(names)


def tz_file(root, nn):
    found = find_tz(root, nn)
    if not found:
        raise Fail("no TZ-%d file in CryptoTZ/ or the root of this tree" % nn)
    canon = [f for f in found if re.fullmatch(r"CryptoTZ/TZ-%d-[a-z0-9-]+\.md" % nn, f)]
    path = canon[0] if canon else found[0]
    return path, text_of(os.path.join(root, path))


def block_ready(root, nn=None):
    notes = []
    code, out = git(root, "fetch", "--all", "--prune")
    if code != 0:
        raise Fail("git fetch --all --prune exited %d: %s" % (code, tail(out, 2)))
    if gitout(root, "rev-parse", "--is-shallow-repository") == "true":
        git(root, "fetch", "--unshallow", check=True)
        notes.append("unshallowed")
    dirty = gitout(root, "status", "--porcelain", "--untracked-files=no")
    if dirty:
        raise Fail("tracked files modified: %s" % ", ".join(l[3:] for l in dirty.splitlines()[:10]))
    loose = gitout(root, "ls-files", "--others", "--exclude-standard").splitlines()
    if loose:
        say("ready", "WARN untracked, pre-existing, for the report: %s" % ", ".join(loose[:10]))
    branch = gitout(root, "rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        git(root, "switch", "-q", "main", check=True)
        notes.append("switched from %s to main" % branch)
    ahead = int(gitout(root, "rev-list", "--count", "origin/main..HEAD"))
    if ahead:
        raise Fail("local main is %d commit(s) ahead of origin/main" % ahead)
    behind = int(gitout(root, "rev-list", "--count", "HEAD..origin/main"))
    if behind:
        git(root, "merge", "-q", "--ff-only", "origin/main", check=True)
        notes.append("fast-forwarded %d" % behind)
    head = gitout(root, "rev-parse", "--short=7", "HEAD")
    unmerged = [b.strip() for b in gitout(root, "branch", "-r", "--no-merged", "origin/main").splitlines() if b.strip()]
    prev = "-"
    if nn is not None:
        nums = sorted({int(m.group(1)) for f in os.listdir(os.path.join(root, "CryptoTZ"))
                       for m in [re.match(r"TZ-(\d+)-", f)] if m and int(m.group(1)) < nn})
        if nums:
            p = nums[-1]
            rx = re.compile(r"(?:^|/)tz-0*%d-" % p)
            bs = [b.strip() for b in gitout(root, "branch", "-r").splitlines() if rx.search(b.strip())]
            if not bs:
                prev = "TZ-%d no branch" % p
            else:
                merged = [b for b in bs if git(root, "merge-base", "--is-ancestor", b, "origin/main")[0] == 0]
                prev = "TZ-%d %s" % (p, "merged" if len(merged) == len(bs) else "NOT MERGED: " + ", ".join(
                    b for b in bs if b not in merged))
    say("ready", "main at %s = origin/main%s" % (head, (" (" + "; ".join(notes) + ")") if notes else ""))
    if unmerged:
        say("ready", "remote branches not in main: %s" % ", ".join(unmerged))
    return "PASS main %s = origin/main · tracked tree clean · clone complete · previous %s · %d branch(es) ahead" % (
        head, prev, len(unmerged))


def elsewhere(root, nn):
    """Remote branches other than main whose tree holds a file naming TZ-nn."""
    rx = re.compile(r"(?:^|/)TZ[-_ ]0*%d(?!\d)[^/]*\.md$" % nn)
    hits = []
    for b in gitout(root, "branch", "-r").splitlines():
        b = b.strip()
        if not b or "->" in b or b == "origin/main":
            continue
        code, out = git(root, "ls-tree", "-r", "--name-only", b)
        hits += ["%s:%s" % (b, n) for n in out.splitlines() if rx.search(n)]
    return hits


def block_number(root, nn):
    found = find_tz(root, nn)
    if not found:
        other = elsewhere(root, nn)
        raise Fail("no file names TZ-%d on main%s" % (nn, ("; on other branches: " + ", ".join(other)) if other else
                                                       ", in its root or on any other branch -- BLOCKED, expected "
                                                       "CryptoTZ/TZ-%d-<short-name>.md" % nn))
    path, text = tz_file(root, nn)
    head = header(text)
    canon = literal(head.get("canonical filename", ""))
    if not re.fullmatch(r"CryptoTZ/TZ-%d-[a-z0-9-]+\.md" % nn, canon):
        raise Fail("header names no canonical filename CryptoTZ/TZ-%d-<short-name>.md (%r)" % (nn, canon[:80]))
    bodies = {}
    for f in found:
        bodies.setdefault(sha256(blob(os.path.join(root, f))), []).append(f)
    if len(bodies) > 1:
        raise Fail("%d different TZ-%d files: %s -- the correct content wins (contract section 3)" % (
            len(bodies), nn, ", ".join(found)))
    for f in found:
        if f != canon:
            say("number", "file it: git mv '%s' '%s'" % (f, canon) if canon not in found else
                "duplicate of the canonical copy: %s" % f)
    nums = {int(m.group(1)) for f in os.listdir(os.path.join(root, "CryptoTZ"))
            for m in [re.match(r"TZ-(\d+)[-_ ]", f)] if m}
    newest = max(nums) if nums else nn
    if newest > nn:
        say("number", "WARN TZ-%d exists: this is not the newest TZ" % newest)
    reports = sorted(f for f in os.listdir(os.path.join(root, "CryptoReports"))
                     if re.match(r"TZ-%d-.*-report(-\d+)?\.md$" % nn, f))
    want = literal(head.get("report", "")) or "CryptoReports/TZ-%d-<short-name>-report.md" % nn
    if reports:
        k = 2
        stem = want[:-3] if want.endswith(".md") else want
        while os.path.basename("%s-%d.md" % (stem, k)) in reports:
            k += 1
        want = "%s-%d.md" % (stem, k)
        say("number", "WARN executed already: %s; a re-run writes %s" % (", ".join(reports), want))
    return "PASS %s · the report to write %s" % (canon, want)


def block_fingerprint(root, nn):
    mtext = text_of(os.path.join(root, MAP))
    mlines = mtext.split("\n")
    _, sec0 = section(mlines, r"## 0\. Fingerprint")
    if not sec0:
        raise Fail("the map has no '## 0. Fingerprint' section")
    mrev = REVISION.search("\n".join(sec0))
    mapt = table_with(sec0, "Anchor", "Exact string that must be present")
    files = table_with(sec0, "File", "Lines", "MD5")
    if not mapt or not mrev:
        raise Fail("the map's section 0 carries no anchor table or no revision line")
    path, text = tz_file(root, nn)
    _, tz0 = section(text.split("\n"), r"## 0\. Fingerprint")
    tzt = table_with(tz0, "Anchor", "Exact string that must be present")
    if not tzt:
        raise Fail("%s has no anchor table under '## 0. Fingerprint required'" % path)
    want = [(r[0], literal(r[1])) for r in mapt[1] if len(r) >= 2]
    got = [(r[0], literal(r[1])) for r in tzt[1] if len(r) >= 2]
    bad = []
    for name, s in want:
        pos = mtext.find(s)
        quoted = (name, s) in got
        say("fingerprint", "anchor %-20s map line %s · quoted %s · matched `%s`" % (
            name, mtext.count("\n", 0, pos) + 1 if pos >= 0 else "ABSENT", "yes" if quoted else "NO",
            mtext[pos:pos + len(s)] if pos >= 0 else ""))
        if pos < 0 or not quoted:
            bad.append(name)
    extra = [n for n, s in got if (n, s) not in want]
    if extra:
        bad.append("not in the map's table: " + ", ".join(extra))
    say("fingerprint", "map table rows %d · header rows %d · compared %d" % (len(mapt[1]), len(tzt[1]), len(want)))
    differ = []
    if files:
        for r in files[1]:
            f = literal(r[0])
            p = os.path.join(root, f)
            if not os.path.isfile(p):
                differ.append(f + " absent")
                continue
            data = blob(p)
            ok = str(lines_of(data)) == r[1].replace(" ", "") and md5(data) == literal(r[2])
            say("fingerprint", "file %s %d %s %s" % (f, lines_of(data), md5(data), "= map" if ok else
                                                     "DIFFERS from map %s %s" % (r[1], literal(r[2]))))
            if not ok:
                differ.append(f)
        tzf = table_with(tz0, "File", "Lines", "MD5")
        if not tzf or [[literal(c) for c in r[:3]] for r in tzf[1]] != [[literal(c) for c in r[:3]] for r in files[1]]:
            say("fingerprint", "WARN the header's file table is not the map's")
    added = table_with(tz0, "Added file", "Lines", "MD5")
    if added:
        for r in added[1]:
            f = literal(r[0])
            p = os.path.join(root, f)
            req = (r[3] if len(r) > 3 else "").strip().lower()
            if not os.path.isfile(p):
                say("fingerprint", "added %s ABSENT" % f)
                if req.startswith("equal"):
                    bad.append(f + " absent")
                continue
            data = blob(p)
            ok = str(lines_of(data)) == r[1].replace(" ", "") and md5(data) == literal(r[2])
            say("fingerprint", "added %s %d %s %s" % (f, lines_of(data), md5(data), "= header" if ok else "DIFFERS"))
            if not ok and req.startswith("equal"):
                bad.append(f)
    head = header(text)
    cv = re.search(r"v(\d+)", head.get("contract", ""))
    have = VERSION.search(text_of(os.path.join(root, CONTRACT)))
    if cv:
        if not have or int(have.group(1)) != int(cv.group(1)):
            bad.append("contract v%s required, v%s present" % (cv.group(1), have.group(1) if have else "?"))
    mdata = blob(os.path.join(root, MAP))
    say("fingerprint", "map %d lines md5 %s revision %s" % (lines_of(mdata), md5(mdata), mrev.group(1)))
    if differ:
        say("fingerprint", "reported, not enforced (contract section 5): %s" % ", ".join(differ))
    if bad:
        raise Fail("BLOCKED -- %s" % "; ".join(bad))
    return "PASS revision %s · anchors %d of %d rows · files %d measured, %d differ · map md5 %s" % (
        mrev.group(1), len(want), len(mapt[1]), len(files[1]) if files else 0, len(differ), md5(mdata)[:8])


def manifest(text):
    """(shipped rows, result rows) of the TZ's Shipped section."""
    lines = text.split("\n")
    _, sec = section(lines, r"## \d+\. Shipped")
    ship = table_with(sec, "File", "Bytes", "SHA-256", "Use")
    res = table_with(sec, "Path", "Lines", "SHA-256")
    return (ship[1] if ship else []), (res[1] if res else [])


def locate(root, rel):
    """rel, or the one file of the same directory whose name equals it once spaces and underscores read as hyphens."""
    p = os.path.join(root, rel)
    if os.path.isfile(p):
        return rel
    d, base = os.path.split(rel)
    key = re.sub(r"[ _]", "-", base)
    try:
        hits = [f for f in os.listdir(os.path.join(root, d or ".")) if re.sub(r"[ _]", "-", f) == key]
    except FileNotFoundError:
        hits = []
    return os.path.join(d, hits[0]) if len(hits) == 1 else None


def check_shipped(root, nn, text, block="open"):
    ship, res = manifest(text)
    if not ship:
        return None, [], res
    out, altered = [], []
    for r in ship:
        if len(r) < 4:
            raise Fail("a Shipped row has %d cells, not 4" % len(r))
        rel, size, digest, use = literal(r[0]), r[1].replace(" ", ""), literal(r[2]), r[3].strip().lower()
        at = locate(root, rel)
        if at is None:
            raise Fail("shipped file %s is not in the tree" % rel)
        if at != rel:
            say(block, "file it: git mv '%s' '%s'" % (at, rel))
        data = blob(os.path.join(root, at))
        same = str(len(data)) == size and sha256(data) == digest
        say(block, "shipped %s %d bytes sha256 %s %s" % (rel, len(data), sha256(data)[:16],
                                                          "= manifest" if same else "DIFFERS from manifest"))
        if not same:
            if use != "apply":
                raise Fail("%s is run as shipped and arrived altered" % rel)
            altered.append(rel)
        out.append((at, use))
    return out, altered, res


def block_open(root, nn):
    path, text = tz_file(root, nn)
    head = header(text)
    results = []
    steps = [("ready", lambda: block_ready(root, nn)), ("number", lambda: block_number(root, nn)),
             ("fingerprint", lambda: block_fingerprint(root, nn))]
    if "vps" in head.get("host", "").lower():
        steps.append(("host", lambda: block_host(["vps"])))
    for name, fn in steps:
        try:
            say(name, fn())
            results.append(True)
        except Fail as e:
            say(name, "FAIL %s" % e)
            results.append(False)
    shipped, altered, res = check_shipped(root, nn, tz_file(root, nn)[1])
    if shipped is None:
        say("open", "no Shipped section: an old-form TZ, its own text says how its code arrives")
    elif altered:
        say("open", "WARN arrived altered, the result decides at stage: %s" % ", ".join(altered))
    say("open", "model %s" % (head.get("model") or "not named in the header"))
    if not all(results):
        raise Fail("a block failed -- BLOCKED before any work")
    return "PASS %s · %s" % (path, "shipped %d file(s)" % len(shipped) if shipped else "nothing shipped")


def block_stage(root, nn):
    path, text = tz_file(root, nn)
    head = header(text)
    branch = literal(head.get("branch", ""))
    if not branch:
        raise Fail("the header names no branch")
    if gitout(root, "status", "--porcelain", "--untracked-files=no"):
        raise Fail("tracked files modified before staging")
    cur = gitout(root, "rev-parse", "--abbrev-ref", "HEAD")
    created = cur != branch
    if created:
        if git(root, "rev-parse", "--verify", "-q", "origin/" + branch)[0] == 0:
            raise Fail("origin/%s exists already: a second execution is the Architect's to order" % branch)
        git(root, "switch", "-q", "-c", branch, "origin/main", check=True)
    try:
        return stage_on_branch(root, nn, branch)
    except Fail:
        if created:
            # the branch this call made goes, so that the BLOCKED report is written on a clean main
            git(root, "reset", "-q", "--hard")
            git(root, "switch", "-q", "main")
            git(root, "branch", "-q", "-D", branch)
            say("stage", "the branch %s this call made is removed; main is clean" % branch)
        raise


def stage_on_branch(root, nn, branch):
    # the hashes are read on the branch's own checkout, the one the patch is applied from
    path, text = tz_file(root, nn)
    shipped, altered, res = check_shipped(root, nn, text, "stage")
    if not shipped:
        raise Fail("the TZ ships no file")
    for at, use in shipped:
        if use != "apply":
            continue
        code, out = git(root, "apply", "--check", "--whitespace=nowarn", os.path.join(root, at))
        if code != 0:
            raise Fail("git apply --check %s: %s" % (at, tail(out, 6)))
        git(root, "apply", "--index", "--whitespace=nowarn", os.path.join(root, at), check=True)
    touched = set(gitout(root, "diff", "--cached", "--name-only").splitlines())
    listed, bad = set(), []
    for r in res:
        rel = literal(r[0])
        listed.add(rel)
        p = os.path.join(root, rel)
        if r[1].strip().lower() == "deleted":
            ok = not os.path.exists(p)
            say("stage", "result %s %s" % (rel, "deleted" if ok else "STILL PRESENT"))
        elif not os.path.isfile(p):
            ok = False
            say("stage", "result %s ABSENT" % rel)
        else:
            data = blob(p)
            ok = str(lines_of(data)) == r[1].replace(" ", "") and sha256(data) == literal(r[2])
            say("stage", "result %s %d lines sha256 %s %s" % (rel, lines_of(data), sha256(data)[:16],
                                                              "= manifest" if ok else "DIFFERS"))
        if not ok:
            bad.append(rel)
    if touched - listed:
        bad.append("touched outside the manifest: " + ", ".join(sorted(touched - listed)))
    if bad:
        raise Fail("BLOCKED -- the patch did not arrive as written, and no hand edit replaces it: %s" % "; ".join(bad))
    return "PASS branch %s · %d file(s) staged = manifest%s" % (
        branch, len(touched), " · the patch arrived altered and the result matched" if altered else "")


def block_log(argv):
    if len(argv) < 3 or "--" not in argv:
        raise Usage("log NAME [--tail N] [--grep RE] [--sh] -- CMD...")
    name, rest = argv[0], argv[1:]
    cut = rest.index("--")
    opts, cmd = rest[:cut], rest[cut + 1:]
    n, pat, shell, i = 40, None, False, 0
    while i < len(opts):
        if opts[i] == "--tail":
            n, i = int(opts[i + 1]), i + 2
        elif opts[i] == "--grep":
            pat, i = re.compile(opts[i + 1]), i + 2
        elif opts[i] == "--sh":
            shell, i = True, i + 1
        else:
            raise Usage("unknown log option %s" % opts[i])
    if not cmd:
        raise Usage("log: no command after --")
    d = os.environ.get("KIT_DIR") or "/tmp/kit"
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, re.sub(r"[^A-Za-z0-9.-]", "-", name) + ".log")
    args = ["bash", "-o", "pipefail", "-c", " ".join(cmd)] if shell else cmd
    with open(path, "wb") as fh:
        code = subprocess.run(args, stdout=fh, stderr=subprocess.STDOUT).returncode
    data = blob(path)
    rows = data.decode("utf-8", "replace").splitlines()
    say("log", "%s exit %d lines %d bytes %d sha256 %s at %s" % (name, code, len(rows), len(data), sha256(data),
                                                                path))
    shown = [r for r in rows if pat.search(r)] if pat else rows
    if pat:
        say("log", "%s lines match %s: %d" % (name, pat.pattern, len(shown)))
    for r in shown[-n:] if n > 0 else []:
        print(r[:400])
    return code


def block_map(root, parts):
    lines = text_of(os.path.join(root, MAP)).split("\n")
    _, inv = section(lines, r"## 4\. Invariants")
    for part in parts:
        p = part.strip()
        m = re.fullmatch(r"(?:inv\.?\s*)(\d+)", p, re.I)
        if m:
            n, got = m.group(1), []
            for line in inv:
                if got and (re.match(r"\d+\. \*\*", line) or line.startswith("#")):
                    break
                if got or line.startswith(n + ". **"):
                    got.append(line)
            out = got
        elif p.lower().startswith("row:"):
            key = norm(p[4:])
            out = [l for l in lines if l.startswith("| ") and norm(split_row(l)[0]) == key]
        else:
            sid = re.escape(p.lstrip("§").rstrip("."))
            _, out = section(lines, r"#{2,4} %s(?:\.|\s)" % sid)
        print("=== map %s: %d lines" % (p, len(out)))
        print("\n".join(out).rstrip())
        if not out:
            raise Fail("%s is not in the map" % p)
    return 0


def norm(s):
    return re.sub(r"[*`«»\s]+", " ", s).strip().lower()


def transcripts(root, given=None):
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
    proj = os.path.join(base, "projects")
    if given:
        dirs = [given]
    else:
        own = os.path.join(proj, NOT_TZ.sub("-", root))
        dirs = [own] if os.path.isdir(own) else []
        if not dirs and os.path.isdir(proj):
            tag = NOT_TZ.sub("-", os.path.basename(root))
            dirs = [os.path.join(proj, d) for d in os.listdir(proj) if d.endswith(tag)]
    files = []
    for d in dirs:
        for top, _, names in os.walk(d):
            files += [os.path.join(top, n) for n in names if n.endswith(".jsonl")]
    return dirs, sorted(files)


def user_text(msg):
    c = (msg or {}).get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return " ".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
    return ""


def block_usage(root, argv):
    sel, val, given, i = None, None, None, 0
    while i < len(argv):
        a = argv[i]
        if a == "--dir":
            given, i = argv[i + 1], i + 2
        elif a in ("--session", "--since"):
            sel, val, i = a[2:], argv[i + 1], i + 2
        else:
            sel, val, i = "tz", tz_number(a), i + 1
    if sel is None:
        raise Usage("usage TZ-NN | --session ID | --since ISO-8601 [--dir PATH]")
    dirs, files = transcripts(root, given)
    say("usage", "transcripts %d file(s) under %s" % (len(files), ", ".join(dirs) or "no project directory"))
    rows, skipped = [], 0
    for f in files:
        with open(f, "rb") as fh:
            for k, raw in enumerate(fh):
                try:
                    o = json.loads(raw)
                except ValueError:
                    skipped += 1
                    continue
                if isinstance(o, dict):
                    rows.append((str(o.get("sessionId") or os.path.basename(f)), str(o.get("timestamp") or ""), f, k, o))
    rows.sort(key=lambda r: (r[0], r[1], r[2], r[3]))
    calls, current, last_sid, sessions, orphans = {}, None, None, set(), 0
    trig = re.compile(r"EXECUTE\s+TZ-0*(\d+)(?!\d)")
    for sid, ts, f, k, o in rows:
        if sid != last_sid:
            current, last_sid = None, sid
        msg = o.get("message") if isinstance(o.get("message"), dict) else {}
        if o.get("type") == "user" and not o.get("isSidechain"):
            m = trig.search(user_text(msg))
            if m:
                current = int(m.group(1))
        if o.get("type") != "assistant" or not isinstance(msg.get("usage"), dict):
            continue
        take = ((sel == "tz" and current == val) or (sel == "session" and sid.startswith(val))
                or (sel == "since" and ts >= val))
        if not take:
            if sel == "tz" and current is None and o.get("isSidechain"):
                orphans += 1
            continue
        key = (sid, msg.get("id") or o.get("uuid") or "%s:%d" % (f, k), o.get("requestId") or "")
        u = msg["usage"]
        rec = calls.setdefault(key, {"model": msg.get("model") or "-", "side": bool(o.get("isSidechain")), "ts": ts,
                                     "in": 0, "cc": 0, "cr": 0, "out": 0})
        for name, field in (("in", "input_tokens"), ("cc", "cache_creation_input_tokens"),
                            ("cr", "cache_read_input_tokens"), ("out", "output_tokens")):
            v = u.get(field)
            if isinstance(v, int) and v > rec[name]:
                rec[name] = v
        sessions.add(sid)
    say("usage", "selector %s %s · sessions %d · records %d · unreadable lines %d · subagent calls of no trigger %d" % (
        sel, "TZ-%d" % val if sel == "tz" else val, len(sessions), len(rows), skipped, orphans))
    if not calls:
        raise Fail("no assistant usage matches -- the measurement is absent, and the report says so")
    per, main, peak = {}, 0, 0
    for rec in calls.values():
        if rec["model"] == "<synthetic>":
            continue
        t = per.setdefault(rec["model"], [0, 0, 0, 0, 0])
        t[0] += 1
        t[1] += rec["in"]
        t[2] += rec["cc"]
        t[3] += rec["cr"]
        t[4] += rec["out"]
        if not rec["side"]:
            main += 1
            peak = max(peak, rec["in"] + rec["cc"] + rec["cr"])
    tot = [sum(v[j] for v in per.values()) for j in range(5)]
    for model, t in sorted(per.items()):
        say("usage", "%s calls %d input %d cache_creation %d cache_read %d output %d" % ((model,) + tuple(t)))
    first = min(r["ts"] for r in calls.values())
    last = max(r["ts"] for r in calls.values())
    return ("PASS calls %d (main chain %d) input %d cache_creation %d cache_read %d output %d · peak context %d · "
            "%s to %s" % (tot[0], main, tot[1], tot[2], tot[3], tot[4], peak, first, last))


def written(root, base, refs):
    """(label, bytes) of everything this session wrote: each ref's files changed since base, read from the ref, and
    the working tree's modified, staged and untracked files."""
    out = []
    for ref in refs:
        code, names = git(root, "diff", "--name-only", "--diff-filter=d", "%s...%s" % (base, ref))
        for n in (names.splitlines() if code == 0 else []):
            p = subprocess.run(["git", "-C", root, "show", "%s:%s" % (ref, n)], stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL)
            if p.returncode == 0:
                out.append(("%s:%s" % (ref, n), p.stdout))
    local = set()
    for args in (("diff", "--name-only"), ("diff", "--name-only", "--cached"),
                 ("ls-files", "--others", "--exclude-standard")):
        code, names = git(root, *args)
        local.update(n for n in (names.splitlines() if code == 0 else []) if n.strip())
    for n in sorted(local):
        if os.path.isfile(os.path.join(root, n)):
            out.append((n, blob(os.path.join(root, n))))
    return out


def block_secrets(root, argv):
    base, refs, extra = "origin/main", ["HEAD"], []
    for a in argv:
        if a.startswith("--ref="):
            refs.append(a[6:])
        elif os.path.exists(os.path.join(root, a)) or os.path.exists(a):
            extra.append(a)
        else:
            base = a
    values = []
    if os.path.isdir(CRED_DIR):
        for name in sorted(os.listdir(CRED_DIR)):
            p = os.path.join(CRED_DIR, name)
            if os.path.isfile(p):
                for part in [blob(p).strip()] + blob(p).split(b"\n"):
                    part = part.strip()
                    if len(part) >= 16 and not part.startswith(b"-----") and (name, part) not in values:
                        values.append((name, part))
        say("secrets", "credential values %d from %d file(s), compared, never printed" % (
            len(values), len({n for n, _ in values})))
    else:
        say("secrets", "no %s on this host: no value to compare; patterns only" % CRED_DIR)
    items = written(root, base, refs)
    for a in extra:
        p = a if os.path.isabs(a) else os.path.join(root, a)
        if os.path.isfile(p):
            items.append((os.path.relpath(p, root), blob(p)))
    d = os.environ.get("KIT_DIR") or "/tmp/kit"
    if os.path.isdir(d):
        items += [(os.path.join(d, f), blob(os.path.join(d, f))) for f in sorted(os.listdir(d)) if f.endswith(".log")]
    hits, warns, seen = [], [], set()
    for label_p, data in items:
        if label_p in seen:
            continue
        seen.add(label_p)
        for name, v in values:
            if v in data:
                hits.append("%s holds the value of %s" % (label_p, name))
        for label, rx in PATTERNS:
            n = len(rx.findall(data))
            if n:
                warns.append("%s: %d %s pattern(s)" % (label_p, n, label))
    scanned = len(seen)
    for w in warns:
        say("secrets", "WARN review %s" % w)
    if hits:
        raise Fail("a credential value is written: %s -- revoke and replace it (contract section 7 item 6)" %
                   "; ".join(hits))
    return "PASS files %d scanned · values %d · 0 value hits · %d pattern warning(s)" % (scanned, len(values),
                                                                                         len(warns))


def cap_of(path, text):
    rel = path.replace("\\", "/")
    if re.search(r"(^|/)CryptoReports/TZ-\d+-.*-report(-\d+)?\.md$", rel):
        _, st = section(text.split("\n"), r"## Status")
        status = " ".join(st[1:]).strip()
        return (BLOCKED_CAP, "BLOCKED report") if "BLOCKED" in status[:80] else (REPORT_CAP, "report")
    if re.search(r"(^|/)CryptoTZ/TZ-\d+-[^/]*\.md$", rel):
        cv = re.search(r"v(\d+)", header(text).get("contract", ""))
        if cv and int(cv.group(1)) >= FIRST_CAPPED_CONTRACT:
            return TZ_CAP, "TZ"
        return None, "old-form TZ"
    return None, "no cap for this path"


def block_caps(root, files):
    if not files:
        raise Usage("caps FILE...")
    bad = []
    for f in files:
        p = f if os.path.isabs(f) else os.path.join(root, f)
        data = blob(p)
        cap, kind = cap_of(os.path.relpath(p, root), data.decode("utf-8", "replace"))
        if cap is None:
            say("caps", "%s %d bytes · %s" % (f, len(data), kind))
            continue
        ok = len(data) <= cap
        say("caps", "%s %d bytes · %s cap %d · %s" % (f, len(data), kind, cap, "within" if ok else "OVER"))
        if not ok:
            bad.append(f)
    if bad:
        raise Fail("over its cap: %s" % ", ".join(bad))
    return "PASS %d file(s)" % len(files)


def block_grow(old, new):
    a, b = len(blob(old)), len(blob(new))
    say("grow", "%s %d bytes -> %s %d bytes (%+d)" % (old, a, new, b, b - a))
    if b > a:
        raise Fail("inv. 73: the delivery is %d bytes larger than the file it replaces" % (b - a))
    return "PASS %d <= %d" % (b, a)


def block_report(root, path):
    p = path if os.path.isabs(path) else os.path.join(root, path)
    text = text_of(p)
    lines = text.split("\n")
    bad = []
    m = re.match(r"# Implementation Report — TZ-(\d+)\s*$", lines[0] if lines else "")
    if not m:
        bad.append("first line is not '# Implementation Report — TZ-NN'")
    heads = [l[3:].split("←")[0].strip() for l in lines if l.startswith("## ")]
    for s in SECTIONS:
        if heads.count(s) != 1:
            bad.append("section '%s' appears %d times" % (s, heads.count(s)))
    order = [h for h in heads if h in SECTIONS]
    if order != [s for s in SECTIONS if s in order]:
        bad.append("sections out of the contract's order")
    _, st = section(lines, r"## Status")
    status = next((l.strip() for l in st[1:] if l.strip()), "")
    if not re.match(r"\**(COMPLETED|PARTIAL|BLOCKED)\b", status):
        bad.append("Status opens with neither COMPLETED, PARTIAL nor BLOCKED")
    for label, rx in BANNED:
        if rx.search(text):
            bad.append("carries %s" % label)
    _, pr = section(lines, r"## Pull Request")
    _, fs = section(lines, r"## Final Repository State")
    report_only = REPORT_ONLY_LINE in "\n".join(pr)
    sentence = "NOT IN EFFECT UNTIL MERGED" in "\n".join(fs)
    if not status.lstrip("*").startswith("BLOCKED"):
        if report_only and sentence:
            bad.append("a report-only TZ's report states NOT IN EFFECT UNTIL MERGED")
        if not report_only and not sentence:
            bad.append("a branch TZ's Final Repository State lacks NOT IN EFFECT UNTIL MERGED")
    _, tk = section(lines, r"## Tokens")
    if not any(l.startswith("usage: ") for l in tk):
        bad.append("Tokens carries no 'usage:' line of this kit")
    cap, kind = cap_of(os.path.relpath(p, root), text)
    size = len(text.encode("utf-8"))
    if cap and size > cap:
        bad.append("%d bytes over the %s cap of %d" % (size, kind, cap))
    if bad:
        raise Fail("; ".join(bad))
    return "PASS %s · %d sections in order · %d bytes of %s" % (os.path.relpath(p, root), len(SECTIONS), size, cap)


def block_close(root, nn):
    _, text = tz_file(root, nn)
    head = header(text)
    want = literal(head.get("report", ""))
    reports = sorted(f for f in os.listdir(os.path.join(root, "CryptoReports"))
                     if re.match(r"TZ-%d-.*-report(-\d+)?\.md$" % nn, f))
    status = gitout(root, "status", "--porcelain")
    fresh = [l[3:].strip() for l in status.splitlines() if l[3:].strip().startswith("CryptoReports/")]
    path = fresh[-1] if fresh else (want if want and os.path.isfile(os.path.join(root, want)) else None)
    if not path and reports:
        path = "CryptoReports/" + reports[-1]
    if not path:
        raise Fail("no report of TZ-%d in the tree" % nn)
    branch = literal(head.get("branch", ""))
    refs = ["--ref=origin/" + branch] if branch and git(root, "rev-parse", "--verify", "-q", "origin/" + branch)[0] == 0 \
        else []
    ok = True
    for name, fn in (("secrets", lambda: block_secrets(root, [path] + refs)),
                     ("report", lambda: block_report(root, path)),
                     ("caps", lambda: block_caps(root, [path])), ("units", block_units)):
        try:
            say(name, fn())
        except Fail as e:
            say(name, "FAIL %s" % e)
            ok = False
    if not ok:
        raise Fail("fix the report before its commit")
    return "PASS %s" % path


def block_clean(root, nn=None):
    status = gitout(root, "status", "--porcelain", "--untracked-files=no")
    if status:
        raise Fail("tracked files modified: %s" % ", ".join(l[3:] for l in status.splitlines()[:20]))
    loose = gitout(root, "ls-files", "--others", "--exclude-standard").splitlines()
    if loose:
        say("clean", "WARN untracked: %s -- remove what this session made" % ", ".join(loose[:20]))
    git(root, "fetch", "-q", "origin")
    branch = gitout(root, "rev-parse", "--abbrev-ref", "HEAD")
    note = "on %s" % branch
    want = [branch]
    if nn is not None:
        b = literal(header(tz_file(root, nn)[1]).get("branch", ""))
        if b and b not in want:
            want.append(b)
    for b in want:
        if git(root, "rev-parse", "--verify", "-q", "origin/" + b)[0] != 0:
            raise Fail("origin/%s does not exist: %s is not pushed" % (b, b))
        if git(root, "rev-parse", "--verify", "-q", b)[0] == 0 and \
                gitout(root, "rev-parse", b) != gitout(root, "rev-parse", "origin/" + b):
            raise Fail("%s differs from origin/%s: not pushed" % (b, b))
        note += " · %s = origin/%s" % (b, b)
    return "PASS tree clean · %s" % note


def block_units():
    if not shutil.which("systemctl"):
        return "PASS no systemctl on this host: no unit to read"
    code, out = sh(["systemctl", "list-units", "--all", "--plain", "--no-legend", "crypto*"])
    left, seen = [], 0
    for line in out.splitlines():
        unit = line.split()[0] if line.split() else ""
        if not unit or "." not in unit:
            continue
        seen += 1
        if sh(["systemctl", "show", "-p", "Transient", "--value", unit])[1].strip() == "yes":
            left.append(unit)
    if left:
        raise Fail("transient unit(s) left: %s" % ", ".join(left))
    return "PASS %d crypto unit(s) read · none transient" % seen


def block_host(argv):
    facts = ["hostname %s" % socket.gethostname(), "uid %d" % os.getuid(), "python %s" % sys.version.split()[0]]
    try:
        osr = dict(l.split("=", 1) for l in text_of("/etc/os-release").splitlines() if "=" in l)
        facts.append("os %s" % osr.get("PRETTY_NAME", "?").strip('"'))
    except OSError:
        pass
    facts.append("git %s" % sh(["git", "--version"])[1].strip().split()[-1])
    facts.append("systemd %s" % ("yes" if shutil.which("systemctl") else "no"))
    present = [m for m in VPS_MARKERS if os.path.isdir(m)]
    facts.append("vps markers %d of %d" % (len(present), len(VPS_MARKERS)))
    say("host", " · ".join(facts))
    if argv and argv[0] == "vps" and len(present) != len(VPS_MARKERS):
        raise Fail("not the VPS: absent %s" % ", ".join(m for m in VPS_MARKERS if m not in present))
    return "PASS %s" % ("the VPS" if len(present) == len(VPS_MARKERS) else "not the VPS, and none was required")


# ------------------------------------------------------------------ dispatch

class Usage(Exception):
    pass


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        raise Usage(__doc__.split("\n\n")[2].strip())
    mode, args = argv[0], argv[1:]
    root = repo_root()
    say("self", block_self(root))
    if mode == "self":
        return 0
    if mode == "log":
        return 0 if block_log(args) == 0 else 1
    if mode == "map":
        if not args:
            raise Usage("map PART...")
        return block_map(root, args)
    one = {"open": lambda: block_open(root, tz_number(args[0])),
           "stage": lambda: block_stage(root, tz_number(args[0])),
           "ready": lambda: block_ready(root, tz_number(args[0]) if args else None),
           "number": lambda: block_number(root, tz_number(args[0])),
           "fingerprint": lambda: block_fingerprint(root, tz_number(args[0])),
           "usage": lambda: block_usage(root, args),
           "close": lambda: block_close(root, tz_number(args[0])),
           "clean": lambda: block_clean(root, tz_number(args[0]) if args else None),
           "host": lambda: block_host(args),
           "units": block_units,
           "secrets": lambda: block_secrets(root, args),
           "caps": lambda: block_caps(root, args),
           "grow": lambda: block_grow(args[0], args[1]),
           "report": lambda: block_report(root, args[0])}
    if mode not in one:
        raise Usage("unknown mode %s" % mode)
    if mode in ("open", "stage", "number", "fingerprint", "close", "grow", "report", "usage", "caps") and not args:
        raise Usage("%s needs an argument" % mode)
    if mode == "grow" and len(args) != 2:
        raise Usage("grow OLD NEW")
    say(mode, one[mode]())
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Fail as e:
        mode = sys.argv[1] if len(sys.argv) > 1 else "kit"
        say(mode, "FAIL %s" % e)
        sys.exit(1)
    except Usage as e:
        print("kit: %s" % e)
        sys.exit(2)
    except Exception:
        print("kit: DEFECT -- the kit itself failed; contract section 15: the block is done by hand and reported")
        print("\n".join(traceback.format_exc().strip().splitlines()[-8:]))
        sys.exit(3)
