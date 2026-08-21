#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_bench.py — end-to-end audit of the CARD LIST as the Boss actually sees
it. display_bench.py proves byScore / assignRanks / tierBadge in isolation;
this one proves the whole render path: real update(), real DOM string, real
order, on data shaped exactly like coeffs.json + the Binance ticker.

Invariant 21: no production logic is copied. The <script> block of index.html
is executed by node behind a tolerant DOM stub that RECORDS what update()
writes into #results, and the emitted HTML is then parsed and audited.

Checks per scenario
  1  update() completes without throwing
  2  card order is non-increasing in score (0.05 tie window, as in byScore)
  3  ranks run 1..N, contiguous, in list order
  4  every card carrying a score prints BOTH its rank and its score
  5  the state glyph matches the verdict, and only 'wait' pulses
  6  degraded rows (no pair / dead market / no bot metrics) take no rank
     and print no badge, and never abort the render

Scenarios: LONG and SHORT x {normal book, degraded rows present,
off-side rows expanded}, plus an empty-bot-data run.
"""
import io, json, math, os, random, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HTML = os.path.join(ROOT, 'index.html')

SCORE_EPS = 0.05          # byScore tie window — production, not a tolerance


def script_of(path):
    src = io.open(path, encoding='utf-8').read()
    a = src.index('<script>') + len('<script>')
    return src[a:src.index('</script>', a)]


HARNESS = r"""
// ── DOM stub that RECORDS instead of rendering ─────────────────────────────
var CAPTURED = {};
function recEl(id) {
    var e = { _id:id, style:{}, innerText:'', value:'', className:'',
              classList:{ add:function(){}, remove:function(){} },
              addEventListener:function(){}, appendChild:function(){},
              setAttribute:function(){}, getAttribute:function(){ return null; },
              oninput:null, onclick:null, onchange:null, checked:false,
              scrollIntoView:function(){}, focus:function(){}, blur:function(){},
              remove:function(){}, querySelector:function(){ return recEl('q'); },
              querySelectorAll:function(){ return []; },
              getElementsByClassName:function(){ return []; },
              getBoundingClientRect:function(){
                  return { top:0, left:0, width:0, height:0, bottom:0, right:0 }; },
              scrollTop:0, scrollHeight:0, offsetTop:0, offsetHeight:0,
              parentNode:null, children:[] };
    Object.defineProperty(e, 'innerHTML', {
        get:function(){ return CAPTURED[id] || ''; },
        set:function(v){ CAPTURED[id] = String(v); }
    });
    return e;
}
var EL_CACHE = {};
global.document = {
    getElementById:function(id){
        if (!EL_CACHE[id]) EL_CACHE[id] = recEl(id);
        return EL_CACHE[id];
    },
    addEventListener:function(){},
    querySelector:function(){ return recEl('q'); },
    querySelectorAll:function(){ return []; },
    createElement:function(){ return recEl('new'); },
    body:recEl('body')
};
global.localStorage = { getItem:function(){ return null; },
                        setItem:function(){}, removeItem:function(){} };
global.window = global;
global.navigator = { userAgent:'bench' };
function deadPromise(){ var d={}; d.then=function(){return d;};
    d.catch=function(){return d;}; d.finally=function(){return d;}; return d; }
global.fetch = function(){ return deadPromise(); };
global.setInterval = function(){ return 0; };
global.setTimeout  = function(){ return 0; };
global.alert = function(){};

__SCRIPT__

// ── driver ────────────────────────────────────────────────────────────────
var SC = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));
var OUT = [];
for (var i = 0; i < SC.length; i++) {
    var s = SC[i];
    var rec = { name:s.name, ok:true, err:null, html:'', rows:[] };
    try {
        botData          = s.botData;
        cachedMarketData = s.market;
        cachedFutTickers = s.fut || {};
        cachedFunding    = s.funding || {};
        currentSide      = s.side;
        currentStress    = 'normal';
        currentLev       = 3;
        showOff          = !!s.showOff;
        boardSym         = null;
        entryState       = {};
        document.getElementById('slider').value = String(s.target);
        CAPTURED['results'] = '';
        update();
        rec.html = CAPTURED['results'] || '';
        // lastShownSyms / lastRows are production state, not a bench copy.
        for (var r = 0; r < lastRows.length; r++) {
            var row = lastRows[r];
            rec.rows.push({ name:row.t.name, state:row.state,
                            score:(row.sc ? row.sc.score : null),
                            no:row.no || 0, off:!!row.off,
                            action:(row.vd ? row.vd.action : null) });
        }
        rec.shown = lastShownSyms.slice(0);
        // Доска — вторая поверхность того же вердикта. Открываем её по каждой
        // показанной монете и снимаем то, что она реально печатает.
        rec.boards = [];
        if (s.side !== 'none') {
            boardSide = s.side;
            for (var b = 0; b < lastShownSyms.length; b++) {
                boardSym = lastShownSyms[b];
                CAPTURED['board'] = '';
                renderBoard();
                rec.boards.push({ sym:boardSym, html:CAPTURED['board'] || '' });
            }
            boardSym = null;
        }
    } catch (e) {
        rec.ok = false;
        rec.err = String(e && e.stack || e);
    }
    OUT.push(rec);
}
console.log(JSON.stringify(OUT));
"""


def run(cases):
    js = HARNESS.replace('__SCRIPT__', script_of(HTML))
    rp = os.path.join(HERE, '_render_run.js')
    cp = os.path.join(HERE, '_render_cases.json')
    io.open(rp, 'w', encoding='utf-8').write(js)
    io.open(cp, 'w', encoding='utf-8').write(json.dumps(cases))
    r = subprocess.run(['node', rp, cp], capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit('node failed')
    return json.loads(r.stdout)


# ── synthetic book, shaped like coeffs.json ────────────────────────────────
SYMS = ['SUI', 'ONDO', 'LINK', 'RENDER', 'NEAR', 'YFI', 'AAVE', 'AVAX',
        'FET', 'ENA', 'TAO', 'GRAM', 'XRP', 'ADA', 'TRX', 'SOL', 'BCH',
        'HYPE', 'SKY', 'ETH', 'HBAR', 'XLM', 'ALGO', 'BNB', 'ZEC', 'UNI',
        'LIT', 'DOGE']


def coin_row(rnd, sym, broken=False):
    price = round(rnd.uniform(0.05, 900), 4)
    lo = price * rnd.uniform(0.35, 0.92)
    hi = price * rnd.uniform(1.08, 3.0)
    if broken:
        return {'symbol': sym, 'error': True}
    b = round(rnd.uniform(0.2, 2.0), 3)
    return {
        'symbol': sym, 'error': False,
        'up_beta': b, 'up_r2': round(rnd.uniform(0.02, 0.9), 3),
        'down_beta': round(b * rnd.uniform(0.7, 1.3), 3),
        'down_r2': round(rnd.uniform(0.02, 0.9), 3),
        'up_beta_90': round(b * rnd.uniform(0.8, 1.2), 3),
        'up_r2_90': round(rnd.uniform(0.02, 0.9), 3),
        'down_beta_90': round(b * rnd.uniform(0.8, 1.2), 3),
        'down_r2_90': round(rnd.uniform(0.02, 0.9), 3),
        'corr_90': round(rnd.uniform(0.2, 0.95), 3),
        'r7': round(rnd.uniform(-0.25, 0.25), 4),
        'r14': round(rnd.uniform(-0.35, 0.35), 4),
        'r30': round(rnd.uniform(-0.5, 0.5), 4),
        'vol7': round(rnd.uniform(0.004, 0.03), 4),
        'eff14': round(rnd.uniform(-2, 2), 3),
        'vol_ratio': round(rnd.uniform(0.6, 1.7), 3),
        'volatility': round(rnd.uniform(0.003, 0.028), 4),
        'min_price': round(lo, 6), 'max_price': round(hi, 6),
        'min30': round(lo * 1.05, 6), 'max30': round(hi * 0.95, 6),
        'price_pos': round(rnd.uniform(0, 100), 1),
        'rank': rnd.randint(1, 200),
        'rank_prev': rnd.randint(1, 200),
        'fdv_mc': round(rnd.uniform(1.0, 4.5), 2),
        '_price': price,
    }


def ticker(sym, price, rnd, dead=False):
    return {
        'symbol': sym + 'USDT',
        'lastPrice': str(price),
        'priceChangePercent': str(round(rnd.uniform(-9, 9), 2)),
        'quoteVolume': str(round(rnd.uniform(2e6, 9e8), 2)),
        'highPrice': str(round(price * rnd.uniform(1.001, 1.09), 6)),
        'lowPrice': str(round(price * rnd.uniform(0.91, 0.999), 6)),
        'count': '0' if dead else str(rnd.randint(20000, 900000)),
        'bidPrice': '0' if dead else str(round(price * 0.999, 6)),
        'askPrice': '0' if dead else str(round(price * 1.001, 6)),
    }


def build(seed, side, degraded=False, show_off=False, empty_bot=False):
    rnd = random.Random(seed)
    btc = 68000.0
    rows, market, fut, funding = [], [], {}, {}
    market.append(ticker('BTC', btc, rnd))
    for i, s in enumerate(SYMS):
        broken = degraded and i % 9 == 3
        cr = coin_row(rnd, s, broken=broken)
        rows.append({k: v for k, v in cr.items() if k != '_price'})
        price = cr.get('_price', round(rnd.uniform(0.05, 900), 4))
        dead = degraded and i % 9 == 5
        nopair = degraded and i % 9 == 7
        if nopair:
            continue
        t = ticker(s, price, rnd, dead=dead)
        if s == 'HYPE':
            fut[s + 'USDT'] = t
        else:
            market.append(t)
        funding[s + 'USDT'] = round(rnd.uniform(-0.0009, 0.0009), 6)
    bot = {'generated_at': '2026-08-19T17:00:00Z',
           'btc': {'min_price': 58244.0, 'max_price': 77847.0,
                   'volatility': 0.0102, 'r7': round(rnd.uniform(-.08, .08), 4),
                   'r14': round(rnd.uniform(-.12, .12), 4)},
           'analysis_data': rows}
    if empty_bot:
        bot = {'generated_at': None, 'analysis_data': []}
    tag = '%s%s%s%s' % (side, '-degraded' if degraded else '',
                        '-showoff' if show_off else '',
                        '-nobot' if empty_bot else '')
    return {'name': 'seed%d-%s' % (seed, tag), 'side': side,
            'botData': bot, 'market': market, 'fut': fut, 'funding': funding,
            'target': round(btc * (1 + rnd.uniform(-0.05, 0.05)), 2),
            'showOff': show_off}


BADGE_RE = re.compile(
    r'<span class="tier-badge" style="color:([^"]+);">(.*?)</span>\s*</span>|'
    r'<span class="tier-badge" style="color:([^"]+);">([^<]*)</span>')
CARD_BADGE_RE = re.compile(r'<span class="tier-badge"[^>]*>(.*?)(?=<div|<span class="rank-badge"|$)',
                           re.S)


def badges(html):
    """Pull the tier badges out of the rendered list, in DOM order."""
    out = []
    for m in re.finditer(r'<span class="tier-badge" style="color:([^"]*?);">', html):
        start = m.end()
        # badge ends at the first </span> that is not opened inside it
        depth, i = 1, start
        while depth and i < len(html):
            nxt_open = html.find('<span', i)
            nxt_close = html.find('</span>', i)
            if nxt_close == -1:
                break
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                i = nxt_open + 5
            else:
                depth -= 1
                i = nxt_close + 7
        out.append((m.group(1), html[start:i - 7]))
    return out


# Badge layout, invariants 33-34, edition 20.08.2026:
#     <tier> [#<no>] \u2014 <round(score)><glyph>
# The rank sits AFTER the tier word and before the em dash. The earlier
# expectation put it first, which was the 19.08 (3) layout; invariant 34
# reversed that on the same day and the expectation was never updated. The
# lowest tier word is 'Фон', not 'Наблюдать': the word names the ATTENTION
# QUEUE, not a trade recommendation.
NUM_RE = re.compile(r'^(\S+)(?: #(\d+))? \u2014 (\d+)')
TIER_WORDS = {'Сильный': (70, 1e9), 'Средний': (50, 70),
              'Кандидат': (35, 50), 'Фон': (-1, 35)}


def js_round(x):
    return int(math.floor(x + 0.5))


def audit(rec):
    fails, checks = [], 0
    if not rec['ok']:
        return 1, ['%s: update() threw\n%s' % (rec['name'], rec['err'])]

    scored = [r for r in rec['rows'] if r['score'] is not None]
    ranked = [r for r in rec['rows'] if r['no'] > 0]

    # 3. ranks contiguous over the shown, scored, on-side rows
    # Display order is lastShownSyms, NOT lastRows order: with the off-side
    # block expanded the two differ, and auditing the wrong one compares a
    # badge against a different coin.
    by_name = dict((r['name'], r) for r in rec['rows'])
    shown = [by_name[n] for n in rec['shown'] if n in by_name]
    order = [r for r in shown if r['score'] is not None and not r['off']]
    checks += 1
    if [r['no'] for r in order] != list(range(1, len(order) + 1)):
        fails.append('%s: ranks not 1..N in order: %s'
                     % (rec['name'], [r['no'] for r in order]))
    checks += 1
    if any(r['no'] != 0 for r in rec['rows']
           if r['score'] is None or r['off']):
        fails.append('%s: a scoreless or off-side row took a rank' % rec['name'])

    # 2. order non-increasing in score
    prev = None
    for r in order:
        checks += 1
        if prev is not None and r['score'] > prev + SCORE_EPS + 1e-9:
            fails.append('%s: %s score %.2f after %.2f'
                         % (rec['name'], r['name'], r['score'], prev))
        prev = r['score']

    # 4/5. badges: one per scored shown row, carrying rank + score + glyph
    bl = badges(rec['html'])
    want = [r for r in shown if r['score'] is not None]
    checks += 1
    if len(bl) != len(want):
        fails.append('%s: %d badges for %d scored cards'
                     % (rec['name'], len(bl), len(want)))
        return checks, fails
    for (color, body), r in zip(bl, want):
        checks += 2
        txt = re.sub(r'<[^>]+>', '', body).strip()
        m = NUM_RE.match(txt)
        if not m:
            fails.append('%s: unparsable badge %r' % (rec['name'], txt))
            continue
        word, no, val = m.group(1), m.group(2), int(m.group(3))
        if r['off']:
            if no is not None:
                fails.append('%s: off row %s shows rank' % (rec['name'], r['name']))
        elif no is None or int(no) != r['no']:
            fails.append('%s: %s rank %s in badge, %s in model'
                         % (rec['name'], r['name'], no, r['no']))
        if val != js_round(r['score']):
            fails.append('%s: %s score %s in badge, %.2f in model'
                         % (rec['name'], r['name'], val, r['score']))
        checks += 1
        if word not in TIER_WORDS:
            fails.append('%s: %s unknown tier word %r' % (rec['name'], r['name'], word))
        else:
            lo, hi = TIER_WORDS[word]
            if not (lo <= r['score'] < hi):
                fails.append('%s: %s tier %s wrong for %.2f'
                             % (rec['name'], r['name'], word, r['score']))
        checks += 1
        act = r['action']
        if act == 'trade' and ('\u2715' in body or '\u007e' in body):
            fails.append('%s: %s tradable card carries a glyph' % (rec['name'], r['name']))
        if act == 'wait' and ('\u007e' not in body or 'light-blink' not in body):
            fails.append('%s: %s wait lost its pulse' % (rec['name'], r['name']))
        if act == 'none' and ('\u2715' not in body or 'light-blink' in body):
            fails.append('%s: %s refusal glyph wrong' % (rec['name'], r['name']))

    # 7. board: same rank, same score, same glyph, verdict stated in words
    # Anchor on the score line's own key, not on the first bd-v in the board.
    BD_RE = re.compile(
        r'\u041e\u0446\u0435\u043d\u043a\u0430 \u043a\u0430\u043a[^<]*</span>'
        r'\s*<span class="bd-v" style="color:([^"]*?);">(.*?)</span></div>', re.S)
    for bd in rec.get('boards', []):
        r = by_name.get(bd['sym'])
        if r is None or r['score'] is None:
            continue
        m = BD_RE.search(bd['html'])
        checks += 1
        if not m:
            fails.append('%s: board for %s prints no score line'
                         % (rec['name'], bd['sym']))
            continue
        body = m.group(2)
        txt = re.sub(r'<[^>]+>', '', body)
        parts = [p.strip() for p in txt.split('\u00b7')]
        checks += 3
        if r['no'] > 0 and ('#%d' % r['no']) not in txt:
            fails.append('%s: board for %s lost rank #%d (%r)'
                         % (rec['name'], bd['sym'], r['no'], txt))
        if str(js_round(r['score'])) not in txt:
            fails.append('%s: board for %s lost score (%r)'
                         % (rec['name'], bd['sym'], txt))
        act = r['action']
        if act == 'wait' and '\u007e' not in body:
            fails.append('%s: board for %s lost the wait glyph' % (rec['name'], bd['sym']))
        if act == 'none' and '\u2715' not in body:
            fails.append('%s: board for %s lost the refusal glyph' % (rec['name'], bd['sym']))
        if act == 'trade' and ('\u2715' in body or '\u007e' in body):
            fails.append('%s: board for %s shows a glyph on a tradable coin'
                         % (rec['name'], bd['sym']))
        checks += 1
        if act == 'none' and 'bd-bad' not in bd['html']:
            fails.append('%s: board for %s never says there is no trade'
                         % (rec['name'], bd['sym']))

    # 6. degraded rows produce a no-data card and no badge
    for r in rec['rows']:
        if r['state'] in ('nopair', 'dead', 'nodata'):
            checks += 1
            if r['no'] != 0 or r['score'] is not None:
                fails.append('%s: degraded row %s got a rank/score'
                             % (rec['name'], r['name']))
    return checks, fails


def main():
    cases = []
    for seed in range(11, 31):
        for side in ('long', 'short'):
            cases.append(build(seed, side))
            cases.append(build(seed + 100, side, degraded=True))
            cases.append(build(seed + 200, side, show_off=True))
    cases.append(build(999, 'long', empty_bot=True))
    cases.append(build(999, 'short', empty_bot=True))
    cases.append(build(998, 'none'))

    recs = run(cases)
    total, fails = 0, []
    for rec in recs:
        c, f = audit(rec)
        total += c
        fails += f
    print('render_bench: %d scenarios, %d checks, %d failures'
          % (len(recs), total, len(fails)))
    for f in fails[:20]:
        print('  FAIL', f)
    # Invariant 22: a validator that passes with no data is a failed validator.
    # Required before this bench may stand in the gate (contract 7.12).
    if total == 0:
        print('  FAIL bench compared nothing')
        return 1
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
