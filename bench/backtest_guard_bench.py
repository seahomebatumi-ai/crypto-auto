#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""backtest_guard_bench.py — offline garrison for backtest_bench.py.

backtest_bench.py runs under backtest_bench.yml, which needs the archive and a
warm cache, so four of its rules had no executing control at all. This bench is
the control, and it is in the gate:

  A  the four JS bundles BUILD and CLOSE against the checkout's index.html —
     the residual of inv. 62. `verify_bench.py` proves the module imports; only
     a build proves that `extract_js` still finds what it cuts.
  B  the archive coverage census: `_vision_rows` refills every absent month,
     never crosses instruments, stops at the last complete hour; `census`,
     `census_of_doc` and `_cov_hit` measure what they say.
  C  the splice rule (inv. 63) — admissibility is arithmetic, its bar is the
     legs' own extremes, and split-then-splice reproduces the original.
  D  the `--target` arm gate — what the gate DOES with a class. Which cell
     earns which class is `verify_bench.py`'s, not this bench's (inv. 20).

Nothing here re-implements a rule it checks (inv. 21, 38): every assertion
calls the production function by name and compares its return, and every
fixture is synthetic input to that function. No network — `requests` is
stubbed and the archive is built in memory. No writes outside a temporary
directory: `backtest_bench.HERE` is redirected there, so the bridge files the
real builders write land in the scratch tree and leave with it.

  python3 bench/backtest_guard_bench.py [path/to/backtest_bench.py] [path/to/index.html]
"""
import io, os, re, sys, types, shutil, zipfile, calendar, tempfile
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'backtest_bench.py')
HTML = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'index.html')

sys.path.insert(0, os.path.dirname(os.path.abspath(BENCH)))
import importlib.util
spec = importlib.util.spec_from_file_location('bb', BENCH)
bb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bb)

HOUR = bb.HOUR_MS
DAY = bb.DAY_MS

fails = []
checks = [0]


def ok(name, cond, info=''):
    checks[0] += 1
    if not cond:
        fails.append(name + (('  [' + str(info)[:220] + ']') if info else ''))


def caught(fn):
    """Run `fn` with its printing swallowed. Returns (exception type name or
    None, message). A control that must raise is read off this pair, so a
    control that raised the WRONG thing cannot be mistaken for a pass."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            fn()
        return None, buf.getvalue()
    except Exception as e:                                  # noqa: BLE001
        return type(e).__name__, str(e)


tmp = tempfile.mkdtemp(prefix='guardbench_')
bb.HERE = tmp                    # every bridge file the real builders write

# ═══════════════════════════════════════════════════════════════════════════
# A. The four bundles build and close  (inv. 62 residual)
# ═══════════════════════════════════════════════════════════════════════════
BUNDLES = [
    ('_score_bridge.js', lambda: bb.JsScorer(HTML)),
    ('_inv_bridge.js', lambda: bb._extract_js_set(
        HTML, bb.INV_JS_FUNCS, bb.INV_JS_VARS, bb.INV_DRIVER, '_inv_bridge.js')),
    ('_res_bridge.js', lambda: bb._extract_js_set(
        HTML, bb.RES_JS_FUNCS, bb.RES_JS_VARS, bb.RES_DRIVER, '_res_bridge.js')),
    ('_tgt_bridge.js', lambda: bb._extract_js_set(
        HTML, bb.TARGET_JS_FUNCS, bb.TARGET_JS_VARS, bb.TARGET_DRIVER,
        '_tgt_bridge.js')),
]

for label, build in BUNDLES:
    buf = io.StringIO()
    err = None
    try:
        with contextlib.redirect_stdout(buf):
            build()
    except Exception as e:                                  # noqa: BLE001
        err = type(e).__name__ + ': ' + str(e)[:200]
    out = buf.getvalue()
    # Both builders run `node --check` on what they wrote, so a bundle that
    # gets here is also syntactically valid JavaScript.
    ok('%s builds from index.html without raising' % label, err is None, err)
    m = re.search(r'замкнутость ' + re.escape(label) + r': сверено (\d+) обращений',
                  out)
    ok('%s closure check compared something (inv. 22)' % label,
       m is not None and int(m.group(1)) > 0, out[-200:] or err)

# ── negative control (inv. 23, 60): the check must RAISE when a name is lost.
# Both halves of `known` are exercised, because it is the union of two texts
# and a check only ever proved on one of them is unproved on the other.
#
# The controls need a real bundle to mutilate. When the cut itself has fallen
# behind index.html there is none, and that is exactly the run this bench
# exists to catch — so the absence is a NAMED failure here rather than a
# traceback that never reaches the summary line.
score_bundle = None
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        score_bundle = bb.extract_js(HTML)
except Exception:                                           # noqa: BLE001
    score_bundle = None
ok('the negative controls have a real bundle to work on',
   score_bundle is not None and 'function ' in (score_bundle or ''),
   'extract_js did not return a bundle')
score_bundle = score_bundle or ''


def drop_first_function(bundle):
    """Remove the first function the assembled bundle DECLARES, and return its
    name with the mutilated text. The name is read off the bundle, never typed:
    a typed name goes stale the day production renames a helper, which is the
    class of defect section A exists to catch."""
    scan = bb._strip_js_noise(bundle)
    m = re.search(r'\bfunction\s+([A-Za-z_$][\w$]*)\s*\(', scan)
    if not m:
        return None, bundle
    b = scan.index('{', m.end())
    end = bb._skip_to_matching_brace(scan, b)
    return m.group(1), bundle[:m.start()] + bundle[end:]


name_a, bundle_a = drop_first_function(score_bundle)
t, msg = caught(lambda: bb._assert_js_closed(bundle_a, bb.JS_DRIVER, '_ctl_a.js'))
ok('control a: a bundle missing a definition it calls RAISES',
   t == 'RuntimeError', '%s / %s' % (t, msg[:160]))
ok('control a: the raise names the lost identifier %r' % name_a,
   t == 'RuntimeError' and name_a is not None and name_a in msg, msg[:200])
ok('control a: the removal was real, not a no-op',
   name_a is not None and len(bundle_a) < len(score_bundle)
   and name_a in score_bundle, '%d vs %d' % (len(bundle_a), len(score_bundle)))

# The driver half. No real bundle references a driver-declared name in a form
# the scan collects (measured: for all four bundles the set of names resolved
# ONLY by the driver is empty), so the reference is appended to the real bundle
# and the NAME is still read off the driver's own text — the first `var` it
# declares. With the declaration present the check must pass, and only then
# does its absence prove the driver half of `known` is load-bearing.
dscan = bb._strip_js_noise(bb.JS_DRIVER)
name_b = re.search(r'\bvar\s+([A-Za-z_$][\w$]*)', dscan).group(1)
dm = re.search(r'\bvar\s+' + re.escape(name_b) + r'\b[^;]*;', dscan)
driver_minus = bb.JS_DRIVER[:dm.start()] + bb.JS_DRIVER[dm.end():]
bundle_b = score_bundle + '\nvar _guard_probe = ' + name_b + '(0);\n'

t, msg = caught(lambda: bb._assert_js_closed(bundle_b, bb.JS_DRIVER, '_ctl_b.js'))
ok('control b: the driver declaration of %r resolves the read' % name_b,
   t is None, '%s / %s' % (t, msg[:160]))
t, msg = caught(lambda: bb._assert_js_closed(bundle_b, driver_minus, '_ctl_b.js'))
ok('control b: removing that declaration from the driver RAISES',
   t == 'RuntimeError', '%s / %s' % (t, msg[:160]))
ok('control b: the raise names %r' % name_b,
   t == 'RuntimeError' and name_b in msg, msg[:200])

t, msg = caught(lambda: bb._assert_js_closed('', '', '_ctl_c.js'))
ok('control c: an empty bundle RAISES rather than passing silently',
   t == 'RuntimeError', '%s / %s' % (t, msg[:160]))
ok('control c: the raise is the inv. 22 message',
   t == 'RuntimeError' and 'сверено 0 идентификаторов' in msg, msg[:200])

# ═══════════════════════════════════════════════════════════════════════════
# B. The coverage census
# ═══════════════════════════════════════════════════════════════════════════


def kline(t, close=100.0):
    """One row in the twelve-column layout `_rows_from_zip` and the REST
    endpoint both return."""
    return [t, close, close, close, close, 1.0,
            t + HOUR - 1, 1000.0, 10, 0.5, 500.0, 0]


def zip_bytes(rows):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        z.writestr('k.csv',
                   '\n'.join(','.join(str(c) for c in r) for r in rows))
    return buf.getvalue()


def month_start(mo):
    y, m = int(mo[:4]), int(mo[5:7])
    return calendar.timegm((y, m, 1, 0, 0, 0, 0, 1, 0)) * 1000


def month_hours(mo):
    y, m = int(mo[:4]), int(mo[5:7])
    return calendar.monthrange(y, m)[1] * 24


class Archive(object):
    """A synthetic data.binance.vision that RECORDS every URL it was asked for.

    Half the rules below are about a request that must NOT be made, and a row
    count cannot tell «not fetched» from «fetched and empty» (inv. 22). Only
    the recorded list can, so it is the assertion target."""

    def __init__(self, monthly=None, daily=None, rest=None):
        self.monthly = monthly or {}          # "YYYY-MM"    -> rows | None=404
        self.daily = daily or {}              # "YYYY-MM-DD" -> rows | None=404
        self.rest = rest or []                # klines the mirror offers
        self.urls = []

    def get(self, url, **kw):
        self.urls.append(url)
        m = re.search(r'-1h-(\d{4}-\d{2}-\d{2})\.zip$', url)
        if m:
            rows = self.daily.get(m.group(1))
            return _Resp(200, zip_bytes(rows)) if rows else _Resp(404)
        m = re.search(r'-1h-(\d{4}-\d{2})\.zip$', url)
        if m:
            rows = self.monthly.get(m.group(1))
            return _Resp(200, zip_bytes(rows)) if rows else _Resp(404)
        if url.endswith('/api/v3/klines'):
            p = kw.get('params') or {}
            beg, end = int(p['startTime']), int(p['endTime'])
            out = [k for k in self.rest if beg <= int(k[0]) <= end][:int(p['limit'])]
            return _Resp(200, payload=out)
        return _Resp(404)

    def install(self):
        fake = types.ModuleType('requests')
        fake.get = self.get
        sys.modules['requests'] = fake
        return self


class _Resp(object):
    def __init__(self, status, content=b'', payload=None):
        self.status_code = status
        self.content = content
        self._payload = payload

    def json(self):
        return self._payload


def hostset(urls):
    return set(re.sub(r'^https?://([^/]+)/.*$', r'\1', u) for u in urls)


# ── B1. `_vision_rows` offline ──────────────────────────────────────────────
# Four consecutive months. The first is pre-listing (404 and no daily files),
# the second and fourth are published monthly, the third exists only as
# dailies — the shape measured on BTCUSDT on 05.09.2026 and the whole reason
# `months[-1]` alone was not enough.
PRE, FIRST, GAPMO, LAST = '2026-05', '2026-06', '2026-07', '2026-08'
t_beg = month_start(PRE)
t_end = month_start(LAST) + (month_hours(LAST) - 1) * HOUR      # last archived hour

arch = Archive(
    monthly={FIRST: [kline(month_start(FIRST) + i * HOUR)
                     for i in range(month_hours(FIRST))],
             LAST: [kline(month_start(LAST) + i * HOUR)
                    for i in range(month_hours(LAST))]},
    daily=dict(('%s-%02d' % (GAPMO, d + 1),
                [kline(month_start(GAPMO) + (d * 24 + h) * HOUR)
                 for h in range(24)])
               for d in range(month_hours(GAPMO) // 24)),
).install()

rows, gone, note = bb._vision_rows('AAAUSDT', False, t_beg, t_end)
got = set(int(r[0]) for r in rows)
gap_hours = set(month_start(GAPMO) + i * HOUR for i in range(month_hours(GAPMO)))
ok('1. the interior absent month is refilled from its dailies',
   gap_hours <= got, '%d of %d hours of %s' %
   (len(gap_hours & got), len(gap_hours), GAPMO))
ok('1. its daily paths were actually requested',
   any('/daily/klines/' in u and ('-1h-' + GAPMO + '-') in u for u in arch.urls),
   [u for u in arch.urls if '/daily/' in u][:2])
ok('2. the pre-listing month produces NO daily request',
   not any('/daily/klines/' in u and ('-1h-' + PRE + '-') in u for u in arch.urls),
   [u for u in arch.urls if PRE in u][:3])
ok('2. and no hour of it entered the series',
   not any(month_start(PRE) <= t < month_start(FIRST) for t in got))
ok('3. `gone` counts every month whose monthly ZIP was absent',
   gone == 2, gone)
ok('3. including the one the dailies then covered',
   gone == 2 and gap_hours <= got, '%s / %s' % (gone, len(gap_hours & got)))
ok('B1 fixture is not empty', len(rows) == month_hours(FIRST) + month_hours(GAPMO)
   + month_hours(LAST), len(rows))
ok('a complete archive needs no top-up', note == '' and
   not any('data-api' in u for u in arch.urls), note)

# ── inv. 64: a perpetual is never topped up from the spot mirror ────────────
SHORT = '2026-08'
short_rows = [kline(month_start(SHORT) + i * HOUR) for i in range(20 * 24)]
t_beg2 = month_start(SHORT)
t_end2 = month_start(SHORT) + (month_hours(SHORT) - 1) * HOUR
mirror = [kline(month_start(SHORT) + i * HOUR)
          for i in range(20 * 24, month_hours(SHORT))]

arch = Archive(monthly={SHORT: short_rows}, rest=mirror).install()
rows_f, gone_f, note_f = bb._vision_rows('AAAUSDT', True, t_beg2, t_end2)
ok('4. a perp tail is not topped up from the spot mirror (inv. 64)',
   not any('data-api.binance.vision' in u for u in arch.urls),
   [u for u in arch.urls if 'data-api' in u][:2])
ok('4. and never from fapi in any form (inv. 24)',
   not any('fapi' in u for u in arch.urls),
   [u for u in arch.urls if 'fapi' in u][:2])
ok('4. the archive lag is REPORTED instead', bool(note_f), repr(note_f))
ok('4. the perp read the futures root', all('/data/futures/um/' in u
                                            for u in arch.urls), arch.urls[:2])
ok('4. the fixture really was short of the last complete hour',
   max(int(r[0]) for r in rows_f) + HOUR < (t_end2 // HOUR) * HOUR,
   '%d rows' % len(rows_f))

arch = Archive(monthly={SHORT: short_rows}, rest=mirror).install()
rows_s, gone_s, note_s = bb._vision_rows('AAAUSDT', False, t_beg2, t_end2)
ok('5. a spot tail IS topped up, from data-api.binance.vision',
   any(u.startswith('https://data-api.binance.vision/api/v3/klines')
       for u in arch.urls), arch.urls[-2:])
ok('5. and from no other host',
   hostset(arch.urls) == set(['data.binance.vision', 'data-api.binance.vision']),
   sorted(hostset(arch.urls)))
ok('5. the top-up actually extended the series',
   len(rows_s) > len(rows_f) and note_s == '',
   '%d vs %d / %r' % (len(rows_s), len(rows_f), note_s))

# t_end inside an hour: the mirror offers the hour IN PROGRESS and it must not
# enter the series — a partial bar would be read as an hourly close.
t_end3 = (t_end2 // HOUR) * HOUR + 1800 * 1000
lch3 = (t_end3 // HOUR) * HOUR
mirror3 = mirror + [kline(lch3)]
arch = Archive(monthly={SHORT: short_rows}, rest=mirror3).install()
rows_h, _g, _n = bb._vision_rows('AAAUSDT', False, t_beg2, t_end3)
ok('6. the fixture offered the hour in progress',
   any(int(k[0]) == lch3 for k in mirror3))
ok('6. no returned row is stamped at or after the last complete hour',
   max(int(r[0]) for r in rows_h) < lch3,
   '%s vs %s' % (max(int(r[0]) for r in rows_h), lch3))

sys.modules.pop('requests', None)

# ── B2. census · census_of_doc · _cov_hit ───────────────────────────────────


def buckets(spans):
    """{hour_bucket: [stamp_ms, value]} — the dict both fetchers build. The
    stamp is the END of the hour, exactly as `_series_from_rows` writes it."""
    P = {}
    for b0, n in spans:
        for i in range(n):
            P[b0 + i] = [(b0 + i) * HOUR + HOUR, 100.0 + b0 + i]
    return P


P = buckets([(0, 50)])
last_b = max(P)
ref = (last_b + 5) * HOUR
c1 = bb.census(P, ref + 1)
c2 = bb.census(P, ref + HOUR - 1)
ok('7. the tail is counted to the last COMPLETE hour', c1['tail'] == 4, c1['tail'])
ok('7. moving t_ref inside one hour does not move it',
   c1['tail'] == c2['tail'], '%s vs %s' % (c1['tail'], c2['tail']))
ok('7. and the rest of the census does not move either', c1 == c2)

G = buckets([(0, 10), (20, 10), (35, 5)])
cg = bb.census(G, (max(G) + 1) * HOUR)
ok('8. an interior gap carries its own start, end and length',
   cg['gaps'][0] == [11 * HOUR, 20 * HOUR, 10], cg['gaps'][:1])
ok('8. n_gaps counts gaps', cg['n_gaps'] == 2, cg['n_gaps'])
ok('8. `inside` sums their hours', cg['inside'] == 15, cg['inside'])
ok('8. max_gap is the longest of them', cg['max_gap'] == [11 * HOUR, 20 * HOUR, 10],
   cg['max_gap'])

cn = bb.census(P, (max(P) + 1) * HOUR)
ok('9. a series with no gap reports none',
   (cn['n_gaps'], cn['inside'], cn['max_gap']) == (0, 0, None),
   (cn['n_gaps'], cn['inside'], cn['max_gap']))
ok('9. on a non-empty series', cn['hours'] == 50, cn['hours'])

doc = {'prices': [G[k] for k in sorted(G)]}
ok('10. census_of_doc reproduces census on the same buckets',
   bb.census_of_doc(doc, (max(G) + 1) * HOUR) == cg)

ct = bb.census(P, ref)
ok('11. a tail deficit is reported whatever the window',
   all(bb._cov_hit(ct, w, ct['last']) and 'хвост' in bb._cov_hit(ct, w, ct['last'])
       for w in (1, 7, 90, 3650)), ct['tail'])

# One gap and no tail, so the only thing that can move the answer is the
# window: the two cases below differ by one day on either side of the hour the
# gap ends, and nothing else.
H = buckets([(0, 10), (200, 300)])
ch = bb.census(H, (max(H) + 1) * HOUR)
t_last = ch['last']
end_of_gap = ch['gaps'][0][1]
inside_d = (t_last - end_of_gap) / float(DAY) + 1.0
outside_d = (t_last - end_of_gap) / float(DAY) - 1.0
ok('12. the boundary case has no tail deficit and exactly one gap',
   ch['tail'] == 0 and ch['n_gaps'] == 1, (ch['tail'], ch['n_gaps']))
ok('12. a gap ending INSIDE the window is named',
   bb._cov_hit(ch, inside_d, t_last) is not None and
   'дыра' in bb._cov_hit(ch, inside_d, t_last), bb._cov_hit(ch, inside_d, t_last))
ok('12. a gap ending BEFORE the window is not',
   bb._cov_hit(ch, outside_d, t_last) is None, bb._cov_hit(ch, outside_d, t_last))
ok('12. the two cases sit on either side of one boundary',
   0 < outside_d < inside_d, (outside_d, inside_d))
ok('13. no census at all is not a hit', bb._cov_hit(None, 90, t_last) is None)

# ═══════════════════════════════════════════════════════════════════════════
# C. The splice rule (inv. 63)
# ═══════════════════════════════════════════════════════════════════════════


def walk(b0, n, p0=100.0, seed=5, step=0.004):
    """Deterministic hourly rows. No RNG: the same bytes on every machine."""
    out, p, s = [], p0, seed
    for i in range(n):
        s = (s * 1103515245 + 12345) % 2147483648
        p *= 1.0 + step * ((s / 2147483648.0) - 0.5)
        out.append(kline((b0 + i) * HOUR, round(p, 8)))
    return out


old = walk(0, 10, 100.0, seed=5)
new = walk(10, 10, old[-1][4] * 1.001, seed=11)
sp = bb._splice(old, new)
ok('14. an ordinary joint is ADMITTED', sp['ok'] is True, sp['why'])
ok('14. and the admission is named', 'внутри' in sp['why'], sp['why'])
ok('14. rows are the pre-cut old leg followed by the whole new leg',
   sp['rows'] == old + new, len(sp['rows']))

far = walk(11, 10, 100.0 * 4200.0, seed=13)          # redenomination shape
spf = bb._splice(walk(0, 10, 100.0, seed=5), far)
ok('15. a joint outside the legs\' own extremes is REFUSED', spf['ok'] is False,
   spf['why'])
ok('15. and the refusal is named', 'ВНЕ' in spf['why'], spf['why'])
ok('15. rows are the new leg alone, unmodified', spf['rows'] == far, len(spf['rows']))

# 16. The one clause with no other witness: the extremes are taken INSIDE each
# leg. Here the legs are hour-ADJACENT, so an implementation that scanned the
# merged series would find the joint's own return among the pairs and admit it.
adj_old = walk(0, 10, 100.0, seed=5)
adj_new = walk(10, 10, 100.0 * 30.0, seed=17)
spa = bb._splice(adj_old, adj_new)
ok('16. the legs are hour-adjacent across the joint',
   int(adj_new[0][0]) // HOUR - int(adj_old[-1][0]) // HOUR == 1)
ok('16. the joint would be admitted if its own return counted',
   spa['r'] is not None and not (spa['lo'] <= spa['r'] <= spa['hi']),
   (spa['lo'], spa['r'], spa['hi']))
ok('16. it is REFUSED, so the extremes never crossed the joint',
   spa['ok'] is False, spa['why'])

ov_old = walk(0, 15, 100.0, seed=5)
ov_new = walk(10, 10, ov_old[10][4], seed=19)
spo = bb._splice(ov_old, ov_new)
ok('17. `cut` is read off the new leg, not declared',
   spo['cut'] == 10 * HOUR + HOUR, spo['cut'])
ok('17. the overlapping old hours are dropped', spo['old_h'] == 10, spo['old_h'])

sp18a = bb._splice(old, [])
ok('18. no new leg is refused with its own reason',
   sp18a['ok'] is False and 'новой пары' in sp18a['why'], sp18a['why'])
sp18b = bb._splice(walk(20, 5, 100.0), walk(10, 5, 100.0))
ok('18. no pre-cut old leg is refused with its own reason',
   sp18b['ok'] is False and 'плеча до переименования' in sp18b['why'], sp18b['why'])
zero_old = walk(0, 10, 100.0)
zero_old[-1][4] = 0.0
sp18c = bb._splice(zero_old, walk(10, 10, 100.0))
ok('18. a non-positive price at the joint is refused',
   sp18c['ok'] is False and 'нулевая цена' in sp18c['why'], sp18c['why'])

sparse_old = [kline(0 * HOUR, 100.0), kline(2 * HOUR, 101.0)]
sparse_new = [kline(10 * HOUR, 102.0), kline(12 * HOUR, 103.0)]
sp19 = bb._splice(sparse_old, sparse_new)
ok('19. no adjacent hourly pair in either leg is refused', sp19['ok'] is False,
   sp19['why'])
ok('19. with the inv. 22 reason', 'сравнивать не с чем' in sp19['why'], sp19['why'])
ok('19. and the fixture really had nothing to compare', sp19['n'] == 0, sp19['n'])

# 20. Identity (inv. 45). The first two hours carry the series' extremes, so
# the interior joint is an ordinary return of the very series being cut.
whole = walk(0, 100, 100.0, seed=23)
whole[1][4] = round(float(whole[0][4]) * 1.05, 8)
whole[2][4] = round(float(whole[1][4]) * 0.95, 8)
K = 50
sp20 = bb._splice(whole[:K], whole[K:])
ok('20. split-then-splice admits the joint', sp20['ok'] is True, sp20['why'])
ok('20. and reproduces the original series row for row',
   sp20['rows'] == whole, '%d vs %d' % (len(sp20['rows']), len(whole)))

# ═══════════════════════════════════════════════════════════════════════════
# D. The `--target` arm gate
# ═══════════════════════════════════════════════════════════════════════════
# What earns which class is locked by verify_bench.py cases 9 and 10. What is
# locked here is what the gate DOES with a class — a second control over one
# rule is the defect inv. 20 names.
CLEAN, UNREC, ABSENT = 'CLEAN', 'UNREC', 'ABSENT'
by_class = dict((cl, 'C%d' % i) for i, cl in enumerate(bb.CLASSES))
sym_class = dict((sy, cl) for cl, sy in by_class.items())
sym_class[CLEAN] = 'clean'
sym_class[ABSENT] = bb.HARD_CLASSES[0]          # failing, but not in the cache
cache = sorted(list(by_class.values()) + [CLEAN, UNREC])

ok('21. the case table names every class the production list carries',
   set(by_class) == set(bb.CLASSES), (sorted(by_class), list(bb.CLASSES)))
ok('21. it also carries a clean symbol and an unreconciled one',
   sym_class[CLEAN] == 'clean' and UNREC in cache and UNREC not in sym_class)
ok('21. and a failing symbol absent from the cache',
   sym_class[ABSENT] in bb.HARD_CLASSES and ABSENT not in cache)

# The gate's membership rule moves with HARD_CLASSES by design, so the two
# anchors below are the only thing in section D that does NOT: a failing set
# that had swallowed every class would leave §3.14's reference lane with
# nowhere to go, and --verify would then be red on two clean coins after a
# fully successful repair (inv. 58). That is a fact about the constants, not
# about the gate, and it cannot be allowed to move with them.
ok('22. every failing class is a class the classifier can produce',
   set(bb.HARD_CLASSES) <= set(bb.CLASSES),
   (list(bb.HARD_CLASSES), list(bb.CLASSES)))
ok('22. and the failing set is PROPER — the reference lane of §3.14 survives',
   bool(set(bb.CLASSES) - set(bb.HARD_CLASSES)),
   sorted(set(bb.CLASSES) - set(bb.HARD_CLASSES)))

before_sc = dict((k, v) for k, v in sym_class.items())
before_ca = list(cache)
excluded, unrec = bb.target_gate(sym_class, cache)

for cl in bb.CLASSES:
    sy = by_class[cl]
    if cl in bb.HARD_CLASSES:
        ok('22. %s is excluded' % cl, sy in excluded, sorted(excluded))
        ok('22. %s carries its class as the value' % cl,
           excluded.get(sy) == cl, excluded.get(sy))
    else:
        ok('22. %s is kept' % cl, sy not in excluded, sorted(excluded))
ok('22. a clean symbol is kept', CLEAN not in excluded, sorted(excluded))

ok('23. a failing symbol absent from the cache is not excluded',
   ABSENT not in excluded, sorted(excluded))
ok('23. nor named as unreconciled', ABSENT not in unrec, unrec)
ok('24. a cached symbol with no reconciliation row is named', UNREC in unrec, unrec)
ok('24. and kept, never silently excluded', UNREC not in excluded, sorted(excluded))
ok('24. nothing else is named', list(unrec) == [UNREC], unrec)

ok('25. target_gate does not mutate sym_class', sym_class == before_sc)
ok('25. target_gate does not mutate the symbol list', cache == before_ca)

ok('26. an empty exclusion set prints the «ничего» wording',
   'ничего' in bb._excl_line({'excluded': {}}), bb._excl_line({'excluded': {}}))
line = bb._excl_line({'excluded': excluded})
for cl in bb.HARD_CLASSES:
    n = len([1 for c in excluded.values() if c == cl])
    ok('26. the line names %s with its count' % cl, ('%s %d' % (cl, n)) in line, line)
for sy in excluded:
    ok('26. the line names the symbol %s it removed' % sy, sy in line, line)
ok('26. a withheld verdict reads as «removed by the reconciliation»',
   line.startswith('снято сверкой:') and 'ничего' not in line, line)

# ═══════════════════════════════════════════════════════════════════════════
shutil.rmtree(tmp, ignore_errors=True)
for f in os.listdir(HERE):
    if f.startswith('_') and f.endswith('_bridge.js'):
        os.remove(os.path.join(HERE, f))

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
