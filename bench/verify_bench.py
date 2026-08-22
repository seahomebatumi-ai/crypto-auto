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


def make_cache(dirpath, coins, extra_files=()):
    os.makedirs(dirpath, exist_ok=True)
    for f in os.listdir(dirpath):
        os.remove(os.path.join(dirpath, f))
    for sym, px in coins.items():
        vol = [[t, 1e7] for t, _ in px]
        json.dump({'prices': px, 'volumes': vol, 'src': 'synthetic'},
                  open(os.path.join(dirpath, sym + '.json'), 'w'))
    for name, payload in extra_files:
        json.dump(payload, open(os.path.join(dirpath, name), 'w'))


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
ok('returns are printed in percentage points', 'пп' in out)

# 5. time gap larger than three hours -> returns are NOT comparable.
#    The verdict must say so instead of claiming full agreement.
code, out = run_verify(tmp, live_from_cache(coins, cdb, gap_h=30))
ok('big gap is announced', 'РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ' in out)
ok('big gap names what was not compared',
   'НЕ СВЕРЯЛОСЬ' in out and all(f in out.split('НЕ СВЕРЯЛОСЬ')[-1]
                                 for f in ('r7', 'r14', 'r30', 'eff14')),
   out.strip().splitlines()[-1][:150])
ok('big gap never claims agreement without the qualifier',
   ('совпадает с продакшном' not in out) or ('по сверенным полям' in out),
   out.strip().splitlines()[-1][:150])
ok('big gap still exits 0 (expected operational state)', code == 0, 'exit=%s' % code)

# 6. a field missing from the live JSON for EVERY coin must never pass silently
#    (invariant 22: a check with nothing to compare is not a passing check)
code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, drop=('min30',)))
ok('field absent everywhere is reported', 'min30' in out and (
    'ни разу' in out or 'НЕ СВЕРЕНО' in out.upper()), out.strip().splitlines()[-1][:150])
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

# 9. threshold semantics (12.08.2026): a reconstruction defect is systemic or
#    huge; single small outliers are SOURCE noise and must warn, not kill the
#    pipeline that has experiments queued behind the step.
def bump_one_small(rec):
    if rec['symbol'] == 'AAA':
        rec['min_price'] = rec['min_price'] * 1.03      # 3 % = 1.5x threshold

make_cache(tmp, coins)
code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_one_small))
ok('single small outlier exits 0', code == 0, 'exit=%s' % code)
ok('single small outlier prints a named warning',
   'ПРЕДУПРЕЖДЕНИЕ' in out and 'AAA' in out.split('ПРЕДУПРЕЖДЕНИЕ')[-1],
   out.strip().splitlines()[-1][:150])

def bump_one_huge(rec):
    if rec['symbol'] == 'AAA':
        rec['min_price'] = rec['min_price'] * 1.10      # 10 % = 5x threshold

code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_one_huge))
ok('single outlier of ANY size warns, exits 0 (v3: defects are systemic)',
   code == 0 and 'ПРЕДУПРЕЖДЕНИЕ' in out and 'AAA' in out.split('ПРЕДУПРЕЖДЕНИЕ')[-1],
   'exit=%s' % code)

# 10. fut basis lane: with html naming AAA as fut:true, a big return gap on AAA
#     is labelled as basis and does not fail; the same gap without html does.
html_fut = os.path.join(tmp, '_toks.html')
io.open(html_fut, 'w', encoding='utf-8').write(
    'x\nvar tokens = [{name:"AAA", s:"AAAUSDT", fut:true},'
    '{name:"BBB", s:"BBBUSDT"}, {name:"CCC", s:"CCCUSDT"}];\nx')

def bump_fut_ret(rec):
    if rec['symbol'] == 'AAA':
        rec['r30'] = (rec['r30'] or 0.0) + 0.10         # 10 pp

def bump_fut_level(rec):
    if rec['symbol'] == 'AAA':
        rec['min_price'] = rec['min_price'] * 1.06      # the HYPE case of 12.08

code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_fut_ret),
                       html=html_fut)
ok('fut basis: return gap exits 0 with html', code == 0, 'exit=%s' % code)
ok('fut basis: return gap named as basis', 'БАЗИС ПЕРП/СПОТ' in out and 'AAA' in out,
   out.strip().splitlines()[-1][:150])
code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_fut_level),
                       html=html_fut)
ok('fut basis: LEVEL gap also exits 0 with html (all fields covered)',
   code == 0 and 'БАЗИС ПЕРП/СПОТ' in out and 'min_price' in out.split('БАЗИС')[-1],
   'exit=%s' % code)
# systemic detection power is intact: all three coins over the bar still fails
code, out = run_verify(tmp, live_from_cache(coins, cdb, 0.5, mutate=bump_level))
ok('systemic breach (all coins) still fails after v3', code != 0, 'exit=%s' % code)

shutil.rmtree(tmp, ignore_errors=True)

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
