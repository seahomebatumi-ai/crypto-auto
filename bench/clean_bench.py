#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""clean_bench.py — proves the dead-code cleanup removed ONLY dead code.

  python3 bench/clean_bench.py <before.html> <after.html>

Checks, in order of severity:
  1. <script> is byte-identical            -> no logic changed, at all
  2. body markup is byte-identical         -> no element changed
  3. every kept CSS rule is byte-identical -> no surviving style changed
  4. every removed selector is unreachable -> nothing on screen loses styling,
     including class names built by string concatenation at run time
  5. no comment left behind mentions a removed name
  6. no @keyframes / CSS custom property is left orphaned
"""
import io, re, sys

fail = []


def ok(name, cond, info=''):
    if not cond:
        fail.append(name + (('  [' + info + ']') if info else ''))


def split(path):
    s = io.open(path, encoding='utf-8').read()
    style = re.search(r'<style>(.*?)</style>', s, re.S).group(1)
    script = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
    body = s[:s.index('<style>')] + s[s.index('</style>') + 8:s.index('<script>')] \
         + s[s.index('</script>') + 9:]
    return s, style, script, body


def rules(style):
    noc = re.sub(r'/\*.*?\*/', lambda m: ' ' * len(m.group(0)), style, flags=re.S)
    out, i = [], 0
    while True:
        br = noc.find('{', i)
        if br < 0:
            return out
        sel = noc[i:br].strip()
        depth, j = 1, br + 1
        while j < len(noc) and depth:
            if noc[j] == '{':
                depth += 1
            elif noc[j] == '}':
                depth -= 1
            j += 1
        out.append((re.sub(r'\s+', ' ', sel), style[br:j].strip()))
        i = j


bef_path, aft_path = sys.argv[1], sys.argv[2]
bs, b_style, b_script, b_body = split(bef_path)
as_, a_style, a_script, a_body = split(aft_path)

# 1-2. nothing outside <style> may move, except three declarations of globals
# that the whole document never reads (they are listed explicitly, so a fourth
# unannounced edit to the script would fail this check).
DROPPED = ['var L_BASE', 'var SHOW_LEVS', 'var STRESS_NAME']
import difflib
diff = [l for l in difflib.unified_diff(b_script.split('\n'), a_script.split('\n'), n=0)
        if l[:1] in '+-' and l[:3] not in ('+++', '---')]
ok('script changed only by the declared removals',
   all(l.startswith('-') and any(d in l for d in DROPPED) for l in diff)
   and len(diff) == len(DROPPED),
   ' | '.join(l.strip()[:60] for l in diff[:5]))
ok('body markup byte-identical', b_body == a_body,
   'len %d -> %d' % (len(b_body), len(a_body)))

# 3. kept rules untouched, and kept order preserved
br, ar = rules(b_style), rules(a_style)
a_map = {}
for sel, body in ar:
    a_map.setdefault(sel, []).append(body)
removed = []
kept_bad = []
seq = []
for sel, body in br:
    if sel in a_map and a_map[sel]:
        if a_map[sel][0] != body:
            kept_bad.append(sel)
        a_map[sel].pop(0)
        seq.append(sel)
    else:
        removed.append(sel)
ok('kept rules byte-identical', not kept_bad, ', '.join(kept_bad[:4]))
ok('no rule invented', all(not v for v in a_map.values()),
   ', '.join(k for k, v in a_map.items() if v))
ok('kept order preserved', seq == [s for s, _ in ar], 'reordered')
print('removed rules: %d' % len(removed))
for r in removed:
    print('   - ' + r)

# 4. every removed selector must be unreachable from the live document
live_names = set(re.findall(r'class="([^"]*)"', a_body))
tokens = set()
for c in live_names:
    tokens.update(c.split())
# class names the script writes, literal and concatenated
tokens.update(re.findall(r"class=\\?[\"']([\w\- ]+)", a_script))
tokens.update(re.findall(r"className\s*=\s*'([\w\- ]+)'", a_script))
flat = set()
for t in tokens:
    flat.update(t.split())
# Class names built by concatenation at run time, e.g. 'side-btn' + ' a-' + mode.
# Each site is resolved against the enum of ITS OWN loop, not a pooled one:
# pooling side modes with stress modes invents 's-long' and hides real orphans.
built = set()
for m in re.finditer(r"'\s*([a-z][\w]*-)'\s*\+\s*(\w+)", a_script):
    pref = m.group(1)
    win = a_script[max(0, m.start() - 800):m.start()]
    arr = None
    for am in re.finditer(r"\[\s*\[\s*'([^']+)'[^\]]*\](?:\s*,\s*\[\s*'([^']+)'[^\]]*\])*\s*\]", win):
        arr = am
    if arr:
        built.update(pref + v for v in re.findall(r"\[\s*'([^']+)'", arr.group(0)))
reachable = flat | built
print('reachable class tokens: %d (of which built at run time: %d)'
      % (len(reachable), len(built)))
for sel in removed:
    if sel.startswith('@'):
        continue
    for cls in re.findall(r'\.([A-Za-z][\w-]*)', sel):
        ok('removed .%s is unreachable' % cls, cls not in reachable,
           'still referenced')

# 5. no stale comment mentions a removed name
removed_names = set()
for sel in removed:
    removed_names.update(re.findall(r'\.([A-Za-z][\w-]*)', sel))
    if sel.startswith('@keyframes'):
        removed_names.add(sel.split()[1])
for c in re.findall(r'/\*.*?\*/', a_style, re.S):
    for n in removed_names:
        ok('no stale comment about %s' % n,
           not re.search(r'(?<![\w-])' + re.escape(n) + r'(?![\w-])', c),
           c.strip().replace('\n', ' ')[:70])

# 6. nothing left orphaned by the removal
a_noc = re.sub(r'/\*.*?\*/', ' ', a_style, flags=re.S)
for kf in re.findall(r'@keyframes\s+([\w-]+)', a_noc):
    ok('keyframe %s still used' % kf,
       len(re.findall(r'animation[^;]*?(?<![\w-])' + re.escape(kf) + r'(?![\w-])', a_noc)) > 0)
for var in set(re.findall(r'(--[\w-]+)\s*:', a_noc)):
    ok('css var %s still used' % var, ('var(' + var) in a_noc or ('var(' + var) in a_script)

# unused globals must be gone and unreferenced
for g in ['L_BASE', 'SHOW_LEVS', 'STRESS_NAME']:
    ok('%s removed' % g,
       not re.search(r'(?<![\w$.])' + g + r'(?![\w$])', as_), 'still present')

print('\nFAIL %d' % len(fail))
for f in fail:
    print('  ' + f)
sys.exit(1 if fail else 0)
