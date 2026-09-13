#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_bench.py — offline test suite for backtest_bench.py --verify.

--verify is the only mode that can be wrong in the dangerous direction: it can
print a pass. Everything here runs without network: `requests` is stubbed, the
cache is synthetic, and the "live" coeffs.json is built by the bench's own
CdBuilder so a clean run matches exactly and every failure below is injected
on purpose.

  python3 bench/verify_bench.py [path/to/backtest_bench.py] [path/to/main.py]
"""
import io, os, sys, json, math, types, shutil, tempfile, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'backtest_bench.py')
BOT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'main.py')

sys.path.insert(0, os.path.dirname(BENCH))
import importlib.util
spec = importlib.util.spec_from_file_location('bb', BENCH)
bb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bb)

HOUR = 3600 * 1000
fails = []
checks = [0]


def ok(name, cond, info=''):
    checks[0] += 1
    if not cond:
        fails.append(name + (('  [' + info + ']') if info else ''))


def series(n=2600, seed=5, drift=0.0):
    """Deterministic hourly walk. No numpy RNG: the same bytes on every machine."""
    px, p, s = [], 100.0, seed
    t0 = 1700000000000
    for i in range(n):
        s = (s * 1103515245 + 12345) % 2147483648
        p *= math.exp(drift + 0.004 * ((s / 2147483648.0) - 0.5))
        px.append([t0 + i * HOUR, round(p, 6)])
    return px


def make_cache(dirpath, coins, extra_files=(), venues=None):
    """Fixture cache documents, each carrying an OBSERVED census (TZ-35 §2.1).

    The census is built by PRODUCTION — `bb.census_of_doc` on the document just
    assembled — and is never written out as a literal here: a hand-made census
    is a second implementation of a production function and drifts from it
    without saying so (inv. 21, 38).

    `t_ref` is the document's own last bar, so `tail` is 0 and `gaps` is empty.
    That is not decoration: `_cov_hit` reads exactly those two fields, and a
    fixture that accidentally reported a tail deficit would move case 9's cell
    out of `unexplained` into `coverage` and pass for the wrong reason.

    The venue is the one fact `census_of_doc` cannot recover from `prices`, so
    the fixture states it per symbol and defaults to spot. A fixture DECLARING
    the world it tests is not the defaulting TZ-34 §2.2 forbids — that
    prohibition is on production inventing an observation it never made. The
    values come from production's own names (inv. 65); a venue string copied
    into this file is a constant that stops moving with the thing it judges."""
    venues = venues or {}
    os.makedirs(dirpath, exist_ok=True)
    for f in os.listdir(dirpath):
        os.remove(os.path.join(dirpath, f))
    for sym, px in coins.items():
        vol = [[t, 1e7] for t, _ in px]
        doc = {'prices': px, 'volumes': vol, 'src': 'synthetic'}
        cov = bb.census_of_doc(doc, px[-1][0])
        cov['venue'] = venues.get(sym, bb.VENUE_SPOT)
        doc['cov'] = cov
        json.dump(doc, open(os.path.join(dirpath, sym + '.json'), 'w'))
    for name, payload in extra_files:
        json.dump(payload, open(os.path.join(dirpath, name), 'w'))


def last_line(text, n=150):
    """The last printed line, for an `ok(...)` info argument (TZ-35 §2.3).

    Python evaluates that argument BEFORE `ok` is called, so
    `text.strip().splitlines()[-1]` raises `IndexError` on empty output — on a
    check that was about to PASS — and the bench dies mid-run, losing every
    check after it. `checks[0]` is then smaller, the summary prints the smaller
    number, and nothing distinguishes a bench that shrank from a bench that
    crashed. A count that can silently shrink is not a count (inv. 43)."""
    lines = text.strip().splitlines()
    return lines[-1][:n] if lines else ''


def live_from_cache(coins, cdb, gap_h=0.5, mutate=None, drop=()):
    """Build the coeffs.json the bot WOULD have written for this cache."""
    data, last = [], 0
    for sym, px in coins.items():
        cd = cdb.build(px, [[t, 1e7] for t, _ in px], len(px) - 1)
        rec = {'symbol': sym, 'error': None}
        for k in ('min_price', 'max_price', 'min30', 'max30', 'volatility',
                  'vol7', 'r7', 'r14', 'r30', 'eff14', 'vol_ratio'):
            if k in drop:
                continue
            rec[k] = cd[k]
        if mutate:
            mutate(rec)
        data.append(rec)
        last = max(last, px[-1][0])
    gen = bb.time.strftime('%Y-%m-%dT%H:%M:%S',
                           bb.time.gmtime(last / 1000.0 + gap_h * 3600))
    return {'generated_at': gen, 'analysis_data': data}


class FakeResp(object):
    def __init__(self, payload):
        self._p = payload
        self.status_code = 200

    def json(self):
        return self._p


def run_verify(cache_dir, live, html=None):
    """Executes --verify offline; returns (exit_code, printed_text)."""
    fake = types.ModuleType('requests')
    fake.get = lambda *a, **k: FakeResp(live)
    sys.modules['requests'] = fake
    old_cache = bb.CACHE
    bb.CACHE = cache_dir
    buf = io.StringIO()
    code = 0
    try:
        with contextlib.redirect_stdout(buf):
            code = bb.verify_against_live(BOT, html)
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else 1
    except Exception as e:
        bb.CACHE = old_cache
        return ('CRASH:' + type(e).__name__ + ':' + str(e)[:120], buf.getvalue())
    bb.CACHE = old_cache
    return (code or 0, buf.getvalue())


# ── fixtures ────────────────────────────────────────────────────────────────
tmp = tempfile.mkdtemp(prefix='vbench_')
# The HTML fixtures live OUTSIDE the cache directory, because `make_cache`
# empties that directory on every call and the token list is not a cache
# document. Keeping them in `tmp` made a later `make_cache` delete the
# declaration the lanes of case 10 exist to vary, and all three lanes then
# passed with no declaration present at all — green while asserting nothing.
tmp_in = tempfile.mkdtemp(prefix='vbench_in_')
coins = {'AAA': series(2600, 5), 'BBB': series(2600, 9), 'CCC': series(2600, 17)}
cdb = bb.CdBuilder(BOT)

# 1. clean run inside the time gap -> pass, exit 0
make_cache(tmp, coins)
code, out = run_verify(tmp, live_from_cache(coins, cdb, gap_h=0.5))
ok('clean run exits 0', code == 0, str(code))
ok('clean run reports a pass', 'совпадает с продакшном' in out, out[-200:])
ok('clean run compared 3 coins', 'сверено монет: 3' in out)

# 2. a price level off by 5 % -> must fail loudly AND exit non-zero
def bump_level(rec):
    rec['min_price'] = rec['min_price'] * 1.05

code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_level))
ok('level mismatch is named', 'ВЫШЛИ ЗА ПОРОГ' in out and 'min_price' in out.split('ВЫШЛИ ЗА ПОРОГ')[-1])
ok('level mismatch exits non-zero', code != 0,
   'exit=%s — a failed verification looked green' % code)

# 3. a return field off by 5 pp, gap small -> must fail
def bump_ret(rec):
    rec['r7'] = (rec['r7'] or 0) + 0.05

code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_ret))
ok('return mismatch is named', 'ВЫШЛИ ЗА ПОРОГ' in out and 'r7' in out.split('ВЫШЛИ ЗА ПОРОГ')[-1])
ok('return mismatch exits non-zero', code != 0, 'exit=%s' % code)

# 4. the metric must be chosen by field type, not one rule for everything:
#    a relative %% error on a field that crosses zero is meaningless (r14 = 0.001
#    against 0.0155 prints as 1449 %% while the real gap is 1.4 points).
import re as _re
_spec = _re.search(r'SPEC = \[(.+?)\]\n', io.open(BENCH, encoding='utf-8').read(), _re.S).group(1)
for f, want in (('min_price', 'rel'), ('max_price', 'rel'), ('min30', 'rel'),
                ('max30', 'rel'), ('volatility', 'rel'), ('vol7', 'rel'),
                ('r7', 'pp'), ('r14', 'pp'), ('r30', 'pp'), ('eff14', 'abs')):
    ok('%s is compared as %s' % (f, want),
       _re.search(r'\("%s",\s*"%s"' % (f, want), _spec) is not None,
       'wrong metric for a %s field' % ('level' if want == 'rel' else 'return'))

def half_point(rec):
    rec['r14'] = (rec['r14'] or 0.0) + 0.005      # exactly 0.5 percentage points

code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=half_point))
ok('half a point on a return passes', code == 0,
   'exit=%s — a 0.5 pp gap must be inside the 2.0 pp threshold' % code)
ok('returns are printed in SIGNED percentage points',
   _re.search(r'[+-]\s*\d+\.\d\d пп', out) is not None, out[:300])

# 5. time gap larger than three hours -> returns are NOT comparable.
#    The verdict must say so instead of claiming full agreement.
code, out = run_verify(tmp, live_from_cache(coins, cdb, gap_h=30))
ok('big gap is announced', 'РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ' in out)
ok('big gap names what was not compared',
   'НЕ СВЕРЯЛОСЬ' in out and all(f in out.split('НЕ СВЕРЯЛОСЬ')[-1]
                                 for f in ('r7', 'r14', 'r30', 'eff14')),
   last_line(out))
ok('big gap never claims agreement without the qualifier',
   ('совпадает с продакшном' not in out) or ('по сверенным полям' in out),
   last_line(out))
ok('big gap still exits 0 (expected operational state)', code == 0, 'exit=%s' % code)

# 6. a field missing from the live JSON for EVERY coin must never pass silently
#    (invariant 22: a check with nothing to compare is not a passing check)
code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, drop=('min30',)))
ok('field absent everywhere is reported', 'min30' in out and (
    'ни разу' in out or 'НЕ СВЕРЕНО' in out.upper()), last_line(out))
ok('field absent everywhere exits non-zero', code != 0,
   'exit=%s — zero comparisons were reported as agreement' % code)

# 7. a side file in the cache must not crash the run (--run --quality-const
#    legitimately stores _quality_today.json there)
make_cache(tmp, coins, extra_files=[('_quality_today.json', {'AAA': {'rank': 5, 'qv': 1e8}})])
code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5))
ok('side file in cache does not crash', not str(code).startswith('CRASH'), str(code))
ok('side file is ignored, 3 coins still compared', 'сверено монет: 3' in out, out[:200])

# 8. empty cache must fail, never pass
make_cache(tmp, {})
code, out = run_verify(tmp, {'generated_at': '2026-08-11T10:00:00', 'analysis_data': []})
ok('empty cache exits non-zero', code != 0, 'exit=%s' % code)

# 9. threshold semantics, re-registered by TZ-29 §2.5. The v3 rule of
#    12.08.2026 let a single coin over the bar exit 0 at ANY magnitude,
#    because ONE threshold table was reporting three causes as one verdict and
#    the pipeline had experiments queued behind the step. The causes are now
#    separated by class: `venue-basis` is reference, `coverage` and
#    `unexplained` return non-zero and name themselves. The pipeline is
#    protected where it belongs instead — --target excludes the symbol whose
#    reconciliation failed (§2.6) rather than the run swallowing the
#    disagreement. So a single unexplained outlier is RED, and it says which
#    coin, which field, in which direction and by how much.
def bump_one_small(rec):
    if rec['symbol'] == 'AAA':
        rec['min_price'] = rec['min_price'] * 1.03      # 3 % = 1.5x threshold

make_cache(tmp, coins)
code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_one_small))
ok('single outlier exits non-zero and is classified unexplained',
   code != 0 and 'AAA unexplained' in out and 'BBB clean' in out, 'exit=%s' % code)
ok('the failing cell carries symbol, field and a SIGNED deviation',
   _re.search(r'AAA\s+min_price\s+[+-]\d', out) is not None,
   last_line(out))

def bump_one_huge(rec):
    if rec['symbol'] == 'AAA':
        rec['min_price'] = rec['min_price'] * 1.10      # 10 % = 5x threshold

code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_one_huge))
ok('an outlier of ANY size is red, and only its own coin is dirty',
   code != 0 and 'AAA unexplained' in out and 'CCC clean' in out
   and _re.search(r'unexplained\s+1\b', out) is not None, 'exit=%s' % code)

# 10. The venue-basis licence has TWO inputs and only ONE of them decides
#     (TZ-34 §2.3, re-registered here by TZ-35 §2.2). The lane that existed
#     before tested one cell of a two-by-two: declared `fut:true` AND cached on
#     the perpetual. Three lanes now vary the two inputs independently, all
#     under the SAME over-threshold mutation:
#
#       lane   declared fut:true   series venue   class          exit
#         A          yes               perp       venue-basis      0
#         B          yes               spot       unexplained    non-zero
#         C          no                perp       venue-basis      0
#
#     B is the behaviour TZ-34 introduced: a declaration no longer buys a
#     licence. C is the case the whole line of work exists for — a coin never
#     declared, silently cached on the perpetual, earns the licence instead of
#     falling into `unexplained`; it is the UNI/XLM/ZEC shape. The strongest
#     assertion is neither: A and C must agree exactly, because the declaration
#     is the ONLY thing that differs between them and it must make no
#     difference at all. Two separate green checks would not say that.
html_fut = os.path.join(tmp_in, 'toks_fut.html')
io.open(html_fut, 'w', encoding='utf-8').write(
    'x\nvar tokens = [{name:"AAA", s:"AAAUSDT", fut:true},'
    '{name:"BBB", s:"BBBUSDT"}, {name:"CCC", s:"CCCUSDT"}];\nx')
# The same three tokens with AAA NOT declared. Lane C uses this rather than
# `html=None` so the declaration is the only difference from lane A: with no
# file at all the parse path itself would differ, and the equality below would
# no longer isolate the declaration.
html_nofut = os.path.join(tmp_in, 'toks_nofut.html')
io.open(html_nofut, 'w', encoding='utf-8').write(
    'x\nvar tokens = [{name:"AAA", s:"AAAUSDT"},'
    '{name:"BBB", s:"BBBUSDT"}, {name:"CCC", s:"CCCUSDT"}];\nx')

def bump_fut_ret(rec):
    if rec['symbol'] == 'AAA':
        rec['r30'] = (rec['r30'] or 0.0) + 0.10         # 10 pp

def bump_fut_level(rec):
    if rec['symbol'] == 'AAA':
        rec['min_price'] = rec['min_price'] * 1.06      # the HYPE case of 12.08

def basis_sets(text):
    """The two sets that must be the SAME object: what the classifier put in
    `venue-basis`, and what the «БАЗИС ПЕРП/СПОТ» line names. The class is READ
    from that calculation, never from a field-family label written by hand, and
    a classifier never shown to reproduce the note it is derived from supports
    no claim about a new reading (inv. 45)."""
    cls, note, block = set(), set(), False
    for ln in text.splitlines():
        if ln.startswith('  venue-basis'):
            block = True; continue
        if block:
            m = _re.match(r'\s+(\w+)\s+(\w+)\s+[+-]', ln)
            if m:
                cls.add(m.group(1, 2)); continue
            block = False
        if 'БАЗИС ПЕРП/СПОТ' in ln:
            for part in ln.split(':', 1)[1].split('·'):
                sy, fs = part.split(':')
                for f in fs.split(','):
                    note.add((sy.strip(), f.strip().split()[0]))
    return cls, note

# ── lane A: declared fut:true, series ON the perpetual ──────────────────────
make_cache(tmp, coins, venues={'AAA': bb.VENUE_PERP})
code_a, out_a = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_fut_ret),
                           html=html_fut)
code, out = code_a, out_a
ok('fut basis: return gap exits 0 with html', code == 0, 'exit=%s' % code)
ok('fut basis: return gap named as basis and classified venue-basis',
   'БАЗИС ПЕРП/СПОТ' in out and 'AAA' in out and basis_sets(out)[0] == basis_sets(out)[1]
   and len(basis_sets(out)[0]) > 0, last_line(out))
code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_fut_level),
                       html=html_fut)
ok('fut basis: LEVEL gap also exits 0, and the class set IS the basis note',
   code == 0 and 'БАЗИС ПЕРП/СПОТ' in out and 'min_price' in out.split('БАЗИС')[-1]
   and basis_sets(out)[0] == basis_sets(out)[1] == {('AAA', 'min_price')},
   'exit=%s · %r' % (code, basis_sets(out)))

# ── lane C: NOT declared, same series on the perpetual ──────────────────────
#    Same cache as lane A, same mutation; only the declaration is withdrawn.
code_c, out_c = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_fut_ret),
                           html=html_nofut)
ok('lane C: an UNDECLARED coin cached on the perpetual still exits 0',
   code_c == 0, 'exit=%s' % code_c)
ok('lane C: it is classified venue-basis and named in the basis note',
   'БАЗИС ПЕРП/СПОТ' in out_c
   and basis_sets(out_c)[0] == basis_sets(out_c)[1] == {('AAA', 'r30')},
   last_line(out_c))

# The equality is the point of the pair, not the two greens above it: an
# equality that HOLDS across a varied input is what «this input no longer
# decides» means. The non-emptiness clause keeps it from passing on two empty
# sets (inv. 22).
ok('lanes A and C agree exactly — the declaration decides nothing',
   code_a == code_c and basis_sets(out_a)[0] == basis_sets(out_c)[0]
   and len(basis_sets(out_a)[0]) > 0,
   'A exit=%s %r · C exit=%s %r' % (code_a, basis_sets(out_a)[0],
                                    code_c, basis_sets(out_c)[0]))

# ── lane B: declared fut:true, series on SPOT ───────────────────────────────
make_cache(tmp, coins)
code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_fut_ret),
                       html=html_fut)
ok('lane B: a declaration over a SPOT series buys no licence — exits non-zero',
   code != 0, 'exit=%s — the declaration granted a licence again' % code)
ok('lane B: the cell is unexplained and no basis note is printed',
   'AAA unexplained' in out and basis_sets(out)[0] == set()
   and 'БАЗИС ПЕРП/СПОТ' not in out, last_line(out))

# systemic detection power is intact: all three coins over the bar still fails
code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_level))
ok('systemic breach (all coins) still fails after v3', code != 0, 'exit=%s' % code)

# 11. Comparability per SYMBOL and before the class (ТЗ-43 §5). A cell is
#     compared only where both sides were built over one window, decided from
#     the symbol's OWN end instant against production's stamp — never from the
#     cache-wide gap and never after the threshold. An incomparable cell is
#     printed and named, and carries no class, no count of agreement and no
#     exclusion from --target. Lane L5 is retired and keeps its number, so this
#     block reads against ТЗ-42's report.
RET = bb.RET_FIELDS
LEVELS = ('min_price', 'max_price', 'min30', 'max30', 'volatility', 'vol7')


def run_lane(cache_dir, live, html=None):
    """--verify's exit and text, and the reconciliation behind them on the same
    stubbed input: (exit, text, R, class sets, symbol classes, excluded)."""
    code, out = run_verify(cache_dir, live, html)
    fake = types.ModuleType('requests')
    fake.get = lambda *a, **k: FakeResp(live)
    sys.modules['requests'] = fake
    old_cache, bb.CACHE = bb.CACHE, cache_dir
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            R = bb.reconcile(BOT, html)
    except (Exception, SystemExit):                       # noqa: BLE001
        return code, out, {'nocmp': [], 'seen': {}}, {}, {}, {}
    finally:
        bb.CACHE = old_cache
    cls = dict((c, sorted((s, k) for s, k, _, _ in R['classes'][c]))
               for c in bb.CLASSES)
    excl = bb.target_gate(R['sym_class'], sorted(R['sym_class']))[0]
    return code, out, R, cls, dict(R['sym_class']), excl


def nocmp_set(R):
    return set((s, k) for s, k, _, _ in R['nocmp'])


def agreed(text):
    """The fields the agreement line names; None where it is not printed."""
    for ln in text.splitlines():
        if ln.startswith('совпадает с продакшном по сверенным полям:'):
            return [f.strip() for f in ln.split(':', 1)[1].split(',') if f.strip()]
    return None


def not_compared(text):
    """The «НЕ СВЕРЯЛОСЬ (окно не совпадает)» line and the coin lines under it."""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith('НЕ СВЕРЯЛОСЬ (окно не совпадает)'):
            j = i + 1
            while j < len(lines) and lines[j].startswith('  '):
                j += 1
            return lines[i:j]
    return []


def bump_aaa_ret(rec):
    if rec['symbol'] == 'AAA':
        rec['r7'] = (rec['r7'] or 0) + 0.05            # 5 pp


# ── L1 · L2: ±30 h, r7 over the bar on every coin ───────────────────────────
make_cache(tmp, coins)
L1 = run_lane(tmp, live_from_cache(coins, cdb, gap_h=30, mutate=bump_ret))
L2 = run_lane(tmp, live_from_cache(coins, cdb, gap_h=-30, mutate=bump_ret))
ok('L1. +30 h, r7 over the bar on every coin: exits 0', L1[0] == 0, 'exit=%s' % L1[0])
ok('L1. every class list is empty',
   len(L1[3]) == len(bb.CLASSES) and all(v == [] for v in L1[3].values()), L1[3])
_blk = not_compared(L1[1])
ok('L1. «НЕ СВЕРЯЛОСЬ» names every return field and every coin',
   len(_blk) == 1 + len(coins) and all(f in _blk[0] for f in RET)
   and sorted(ln.split()[0] for ln in _blk[1:]) == sorted(coins), _blk)
ok('L1. no symbol is excluded from --target, and each reads unverified',
   L1[5] == {} and L1[4] == dict((s, bb.UNVERIFIED) for s in coins), (L1[5], L1[4]))
ok('L2. -30 h: L1\'s exit and L1\'s class sets exactly — the sign decides nothing',
   (L2[0], L2[3], L2[4], L2[5]) == (L1[0], L1[3], L1[4], L1[5])
   and len(L1[4]) == len(coins), (L2[0], L2[3], L2[4], L2[5]))
ok('L2. the -30 h gap is announced',
   'РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ у 3 монет из 3' in L2[1], last_line(L2[1]))

# ── L3 · L4: 0.5 h cache-wide, AAA's own series ending 20 h earlier ─────────
# The shortening is BUILT, never written into a census: make_cache runs
# production's census_of_doc on the short series, so its `tail` stays 0 and the
# lane proves the decision is taken on the INSTANT, not on `cov`.
short = dict(coins)
short['AAA'] = coins['AAA'][:-20]
make_cache(tmp, short, venues={'AAA': bb.VENUE_PERP})
L3a = run_lane(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_aaa_ret))
L3b = run_lane(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_fut_level))
ok('L3a. the perp coin 20 h short: its return is not compared',
   ('AAA', 'r7') in nocmp_set(L3a[2])
   and set(s for s, _ in nocmp_set(L3a[2])) == {'AAA'}, sorted(nocmp_set(L3a[2])))
ok('L3a. not venue-basis, not in the basis note, exits 0, AAA reads unverified',
   L3a[0] == 0 and L3a[3].get('venue-basis') == [] and 'БАЗИС ПЕРП/СПОТ' not in L3a[1]
   and L3a[4] == {'AAA': bb.UNVERIFIED, 'BBB': 'clean', 'CCC': 'clean'},
   (L3a[0], L3a[3], L3a[4]))
ok('L3b. its LEVEL over the bar: still venue-basis, named in the basis note, exits 0',
   L3b[0] == 0 and basis_sets(L3b[1])[0] == basis_sets(L3b[1])[1]
   == {('AAA', 'min_price')}, (L3b[0], basis_sets(L3b[1])))
ok('L3. the pair: the licence keeps the level and loses the return',
   (L3a[0], L3b[0]) == (0, 0)
   and (basis_sets(L3a[1])[0], basis_sets(L3b[1])[0]) == (set(), {('AAA', 'min_price')}),
   (basis_sets(L3a[1]), basis_sets(L3b[1])))
make_cache(tmp, short)
L4 = run_lane(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_aaa_ret))
ok('L4. the same coin on SPOT: L3a\'s exit and class sets exactly — no venue is read',
   (L4[0], L4[3], L4[4], L4[5]) == (L3a[0], L3a[3], L3a[4], L3a[5])
   and L4[4].get('AAA') == bb.UNVERIFIED, (L4[0], L4[3], L4[4]))

# ── L6: the boundary, stated ────────────────────────────────────────────────
make_cache(tmp, coins)
L6 = [run_lane(tmp, live_from_cache(coins, cdb, gap_h=g, mutate=bump_ret))
      for g in (3.0, -3.0, 3.1)]
_r7 = [('AAA', 'r7'), ('BBB', 'r7'), ('CCC', 'r7')]
ok('L6. +3.0 h, -3.0 h, +3.1 h: compared, compared, not compared',
   [L[2]['seen'].get('r7') for L in L6] == [3, 3, 0]
   and [('AAA', 'r7') in nocmp_set(L[2]) for L in L6] == [False, False, True],
   [L[2]['seen'].get('r7') for L in L6])
ok('L6. the compared boundary meets the threshold; the other carries no class',
   [L[0] for L in L6] == [1, 1, 0] and L6[0][3].get('unexplained') == _r7
   and L6[1][3].get('unexplained') == _r7 and L6[2][3].get('unexplained') == [],
   [(L[0], L[3].get('unexplained')) for L in L6])

# ── L7 · L7b: generated_at unparseable ─────────────────────────────────────
_lv7 = live_from_cache(coins, cdb, 0.5)
_lv7['generated_at'] = 'not a stamp'
L7 = run_lane(tmp, _lv7)
ok('L7. an unparseable stamp: every return cell is not compared, for an unknown gap',
   len(L7[2]['nocmp']) == len(coins) * len(RET)
   and all(w == 'разрыв во времени неизвестен' and g is None
           for _, _, w, g in L7[2]['nocmp']), L7[2]['nocmp'][:2])
ok('L7. the unknown-gap announcement is printed and «БОЛЬШЕ ТРЁХ ЧАСОВ» is absent',
   'РАЗРЫВ ВО ВРЕМЕНИ НЕИЗВЕСТЕН у 3 монет из 3' in L7[1]
   and 'БОЛЬШЕ ТРЁХ ЧАСОВ' not in L7[1], last_line(L7[1]))
ok('L7. the levels are still compared, and the run exits 0',
   L7[0] == 0 and all(L7[2]['seen'].get(k) == len(coins) for k in LEVELS),
   (L7[0], L7[2]['seen']))
_lv7b = live_from_cache(coins, cdb, 0.5, mutate=bump_fut_level)
_lv7b['generated_at'] = 'not a stamp'
L7b = run_lane(tmp, _lv7b)
ok('L7b. an unknown gap does not excuse a level: exit 1, unexplained, AAA excluded',
   L7b[0] == 1 and L7b[3].get('unexplained') == [('AAA', 'min_price')]
   and L7b[5] == {'AAA': 'unexplained'}, (L7b[0], L7b[3], L7b[5]))

# ── L8: the claim that must not be made, asserted directly (L1's world) ─────
_ag = agreed(L1[1])
ok('L8. the agreement line names no return field',
   _ag is not None and len(_ag) > 0 and not (set(_ag) & set(RET)), _ag)
ok('L8. each return field reads «сверок 0 из 3»',
   all(_re.search(r'^\s+%s\s+сверок\s+0 из\s+%d\b' % (f, len(coins)), L1[1], _re.M)
       for f in RET), last_line(L1[1]))

shutil.rmtree(tmp, ignore_errors=True)
shutil.rmtree(tmp_in, ignore_errors=True)

print('checks run: %d   FAIL %d' % (checks[0], len(fails)))
for f in fails:
    print('  FAIL: ' + f)
# Invariant 22: a validator that passes with no data is a failed validator. The
# guard sits after the summary so a red run still prints its own numbers, and it
# may only ever make this bench redder.
if checks[0] == 0:
    print('  FAIL bench compared nothing')
    sys.exit(1)
sys.exit(1 if fails else 0)
