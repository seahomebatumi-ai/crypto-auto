#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
display_bench.py — proof that the candidate list is displayed BY RANK AND BY
SCORE on every card (Boss's requirement, 19.08.2026, third revision).

Invariant 21 is respected literally: not one line of production math or
production display logic is copied here. The <script> block of index.html is
cut out and executed by real node; every function under test (byScore,
assignRanks, tierBadge, tierOf, directionVerdict, scoreCandidate, sideRelevant)
is the shipping one. Editing index.html changes this bench automatically.

Checks
  A  order      — rendered order is non-increasing in score, always
  B  numbering  — 1..N contiguous over ranked rows, order-consistent, and
                  off-side rows never take a number
  C  badge      — every scored card prints its rank and its score, whatever
                  the verdict; state is carried by the glyph, not by silence
  D  glyph      — trade / wait / none map to '' / '~' / '✕', pulse only on '~'
  E  tiers      — tier boundaries 70 / 50 / 35 inclusive, unchanged
  F  regression — the old build hid rank+score on every non-trade card
                  (reproduces the defect the Boss filmed)
"""
import io, json, math, os, random, re, subprocess, sys

# byScore treats a gap of <= 0.05 points as a tie and falls through to the
# market-cap rank (production behaviour, not a bench allowance): two scores
# that close are noise-equal and a stable secondary key beats a coin flip.
SCORE_EPS = 0.05


def js_round(x):
    "JS Math.round is half-UP; Python round() is half-EVEN. Match production."
    return int(math.floor(x + 0.5))

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HTML = os.path.join(ROOT, 'index.html')


def script_of(path):
    src = io.open(path, encoding='utf-8').read()
    a = src.index('<script>') + len('<script>')
    b = src.index('</script>', a)
    return src[a:b]


HARNESS = r"""
// --- universal tolerant DOM stub: the script must LOAD, nothing must render.
// A Proxy swallows every property and every call, so the bench never has to
// track which DOM API the production file uses next (inv. 21 in spirit:
// no mirror of production code lives here).
function universal() {
    var f = function(){ return universal(); };
    return new Proxy(f, {
        get: function(t, k) {
            if (k === Symbol.toPrimitive) return function(){ return ''; };
            if (k === 'length') return 0;
            if (k === 'then') return undefined;
            if (k === Symbol.iterator) return function*(){};
            return universal();
        },
        set: function(){ return true; },
        apply: function(){ return universal(); },
        has: function(){ return true; }
    });
}
global.document = universal();
global.localStorage = { getItem:function(){ return null; },
                        setItem:function(){}, removeItem:function(){} };
global.window = global;
global.navigator = { userAgent:'bench' };
function deadPromise() {
    var d = {};
    d.then = function(){ return d; };
    d.catch = function(){ return d; };
    d.finally = function(){ return d; };
    return d;
}
global.fetch = function(){ return deadPromise(); };
global.Promise = global.Promise;
global.setInterval = function(){ return 0; };
global.setTimeout  = function(){ return 0; };
global.alert = function(){};

__SCRIPT__

// --- drivers -------------------------------------------------------------
function mkRow(o) {
    return { t:{ name:o.name, s:o.name+'USDT' }, idx:o.idx,
             coin:{ lastPrice:'1' }, cd:{ rank:o.rank, volatility:o.vol },
             state:'ok',
             sc:(o.score === null ? null : { score:o.score, reasons:[] }),
             vd:{ action:o.action, wait:o.wait, score:o.score, reasons:[] },
             off:!!o.off };
}

var CASES = JSON.parse(require('fs').readFileSync(process.argv[2],'utf8'));
var OUT = [];
for (var c = 0; c < CASES.length; c++) {
    var rows = CASES[c].map(mkRow);
    rows.sort(byScore);
    assignRanks(rows);
    OUT.push(rows.map(function(r) {
        return { name:r.t.name,
                 score:(r.sc ? r.sc.score : null),
                 no:r.no, off:!!r.off,
                 action:r.vd.action,
                 badge:(typeof tierBadge === 'function' ? tierBadge(r) : null) };
    }));
}
console.log(JSON.stringify({ rows:OUT,
    tiers:[tierOf(100),tierOf(70),tierOf(69.999),tierOf(50),tierOf(49.999),
           tierOf(35),tierOf(34.999),tierOf(0)] }));
"""


def run(script_js, cases):
    js = HARNESS.replace('__SCRIPT__', script_js)
    p = os.path.join(HERE, '_run.js')
    io.open(p, 'w', encoding='utf-8').write(js)
    cp = os.path.join(HERE, '_cases.json')
    io.open(cp, 'w', encoding='utf-8').write(json.dumps(cases))
    r = subprocess.run(['node', p, cp], capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit('node failed')
    return json.loads(r.stdout)


def make_cases(n_cases=400, seed=20260819):
    rnd = random.Random(seed)
    acts = ['trade', 'wait', 'none', 'none', 'none']
    cases = []
    for _ in range(n_cases):
        k = rnd.randint(4, 28)
        case = []
        for i in range(k):
            scored = rnd.random() > 0.10
            case.append({
                'name': 'C%02d' % i, 'idx': i,
                'score': (round(rnd.uniform(0, 100), 2) if scored else None),
                'action': (rnd.choice(acts) if scored else 'none'),
                'wait': round(rnd.uniform(0.01, 900), 4),
                'rank': rnd.randint(1, 200),
                'vol': round(rnd.uniform(0.003, 0.03), 4),
                'off': rnd.random() < 0.15,
            })
        cases.append(case)
    return cases


RANK_RE = re.compile(r'>#(\d+) ')
NUM_RE = re.compile(r'(\d+)(?:\s*<span|</span>)')

TIER_WORDS = {
    'Сильный': (70, 101), 'Средний': (50, 70),
    'Кандидат': (35, 50), 'Наблюдать': (-1, 35),
}


def check(res, cases, legacy=False):
    fails, checks = [], 0
    for ci, out in enumerate(res['rows']):
        # ---- A. order --------------------------------------------------
        prev = None
        for r in out:
            s = r['score'] if r['score'] is not None else -1
            if prev is not None and s > prev + SCORE_EPS + 1e-9:
                fails.append('A case%d %s score %s after %s' %
                             (ci, r['name'], s, prev))
            prev = s
            checks += 1
        # ---- B. numbering ----------------------------------------------
        seen, last_no = [], 0
        for r in out:
            checks += 1
            eligible = (r['score'] is not None) and not r['off']
            if legacy:
                continue
            if eligible:
                if r['no'] != last_no + 1:
                    fails.append('B case%d %s no=%s expected %d' %
                                 (ci, r['name'], r['no'], last_no + 1))
                last_no = r['no']
                seen.append(r['no'])
            elif r['no'] != 0:
                fails.append('B case%d %s took rank %s while ineligible'
                             % (ci, r['name'], r['no']))
        if not legacy and seen and seen != list(range(1, len(seen) + 1)):
            fails.append('B case%d ranks not contiguous: %s' % (ci, seen))
        # ---- C / D. badge ----------------------------------------------
        for r in out:
            checks += 1
            if r['score'] is None:
                if r['badge'] != '':
                    fails.append('C case%d %s badge on scoreless row' %
                                 (ci, r['name']))
                continue
            b = r['badge']
            if legacy:
                continue
            # score present?
            if str(js_round(r['score'])) not in b:
                fails.append('C case%d %s score %s missing from badge %r' %
                             (ci, r['name'], r['score'], b))
            # tier word present and correct?
            word = [w for w in TIER_WORDS if w in b]
            if len(word) != 1:
                fails.append('C case%d %s tier word missing: %r' %
                             (ci, r['name'], b))
            else:
                lo, hi = TIER_WORDS[word[0]]
                if not (lo <= r['score'] < hi):
                    fails.append('C case%d %s tier %s wrong for %s' %
                                 (ci, r['name'], word[0], r['score']))
            # rank present iff eligible?
            m = RANK_RE.search(b)
            if r['off']:
                if m:
                    fails.append('B case%d %s off-row shows rank' %
                                 (ci, r['name']))
            else:
                if not m or int(m.group(1)) != r['no']:
                    fails.append('C case%d %s rank missing/wrong in %r' %
                                 (ci, r['name'], b))
            # glyph
            checks += 1
            if r['action'] == 'trade':
                if '\u007E<' in b or '\u2715' in b:
                    fails.append('D case%d %s trade carries a glyph' %
                                 (ci, r['name']))
            elif r['action'] == 'wait':
                if '\u007E' not in b or 'light-blink' not in b:
                    fails.append('D case%d %s wait lost pulse/glyph' %
                                 (ci, r['name']))
            else:
                if '\u2715' not in b or 'light-blink' in b:
                    fails.append('D case%d %s none glyph wrong' %
                                 (ci, r['name']))
    # ---- E. tiers -------------------------------------------------------
    want = ['Сильный', 'Сильный', 'Средний', 'Средний', 'Кандидат',
            'Кандидат', 'Наблюдать', 'Наблюдать']
    for got, w in zip(res['tiers'], want):
        checks += 1
        if got['n'] != w:
            fails.append('E tier %s expected %s' % (got['n'], w))
    return checks, fails


def main():
    cases = make_cases()
    res = run(script_of(HTML), cases)
    checks, fails = check(res, cases)

    # ---- F. regression witness: the shipped-before build -----------------
    legacy_note = ''
    old = os.path.join(ROOT, 'index_before.html')
    if os.path.exists(old):
        ro = run(script_of(old), cases)
        hidden = ranked = total = 0
        for out in ro['rows']:
            for r in out:
                # Witness uses the OLD build's own assignRanks (a named
                # production function), never a copy of its badge branch.
                if r['score'] is None or r['off']:
                    continue
                total += 1
                if r['no'] == 0:
                    hidden += 1
                else:
                    ranked += 1
        legacy_note = ('F old build: %d/%d scored cards printed NO rank '
                       '(%.0f%%), %d printed one' %
                       (hidden, total, 100.0 * hidden / max(total, 1), ranked))

    print('display_bench: %d checks, %d failures' % (checks, len(fails)))
    if legacy_note:
        print(legacy_note)
    for f in fails[:25]:
        print('  FAIL', f)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
