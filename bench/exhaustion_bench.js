// bench/exhaustion_bench.js
// TZ-10 — the list-level exhaustion measure.
//
// No formula is copied here (invariant 21): dayRangeRatio, sigmaDay,
// listExhaustion and regimeBanner are pulled out of the <script> block of
// index.html at runtime and executed as the production functions. The only
// arithmetic written in this file is the CLOSED FORM the TZ specifies as the
// independent reference for the identity case — that is the assertion, not a
// second implementation of the rule.
//
// SCOPE AT THIS REVISION. TZ-10 Stage C is not implemented: the archive
// calibration (Stage B) could not run, so DAY_RANGE_ABNORMAL does not exist
// and listExhaustion().abnormal is permanently false. The two §5.2 cases that
// depend on it — the threshold edge, and the eight banner cases with
// abnormal === true — are therefore NOT written here: a bench cannot assert
// against code that does not exist, and inventing a threshold to test against
// would be exactly the retune inv. 23 forbids. What this file does instead is
// pin every case that IS well-defined today, and add one the final revision
// will not need: that the new measure is INERT — it reaches no consumer, so
// the board is unchanged. When Stage C lands, sections D2 and E extend.
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const HTML = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const src = HTML.slice(HTML.indexOf('<script>') + 8, HTML.lastIndexOf('</script>'));

// Minimal DOM/browser shims: the module body only needs these to evaluate.
const stub = new Proxy(function () {}, {
    get: () => stub, set: () => true, apply: () => stub, construct: () => stub
});
const sandbox = {
    document: { getElementById: () => stub, querySelector: () => stub,
                querySelectorAll: () => [], addEventListener: () => {},
                createElement: () => stub, body: stub, head: stub },
    window: {}, localStorage: { getItem: () => null, setItem: () => {} },
    navigator: { userAgent: 'node' }, location: { href: '' },
    fetch: () => Promise.resolve({ json: () => ({}) }),
    setTimeout: () => 0, clearTimeout: () => {}, setInterval: () => 0,
    clearInterval: () => {}, requestAnimationFrame: () => 0,
    console, Math, Date, JSON, parseFloat, parseInt, isFinite, isNaN
};
sandbox.window = sandbox;
vm.createContext(sandbox);
vm.runInContext(src, sandbox, { filename: 'index.html:<script>' });

const P = sandbox;   // production namespace

['dayRangeRatio', 'sigmaDay', 'listExhaustion', 'regimeBanner', 'marketRegime'].forEach(function (f) {
    if (typeof P[f] !== 'function') {
        console.log('FAIL ' + f + ' is not defined in index.html');
        process.exit(1);
    }
});

// Per-section counters. The gate total is a SUM of these, never an estimate
// (inv. 43), and each one counts comparisons actually made at its own site.
const N = { identity: 0, nulls: 0, quorum: 0, venue: 0, banner: 0, stress: 0, inert: 0,
            purity: 0, control: 0, wiring: 0 };
let section = 'identity';
let checks = 0, fails = 0;

function eq(name, got, want) {
    checks++; N[section]++;
    if (got !== want) {
        fails++;
        if (fails < 15) console.log('  FAIL ' + name + ': got ' + JSON.stringify(got) + ' want ' + JSON.stringify(want));
    }
}
function near(name, got, want, tol) {
    checks++; N[section]++;
    const ok = typeof got === 'number' && typeof want === 'number'
             && Math.abs(got - want) <= tol;
    if (!ok) {
        fails++;
        if (fails < 15) console.log('  FAIL ' + name + ': got ' + JSON.stringify(got) + ' want ' + JSON.stringify(want));
    }
}
function ok(name, cond) { eq(name, !!cond, true); }

// Deterministic PRNG so any failure is reproducible from the seed alone.
let seed = 20260823;
function rnd() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; }
function span(a, b) { return a + rnd() * (b - a); }

// ───────────────────────────────────────────────────────────────────────────
console.log('=== A. Identity: dayRangeRatio against the closed form ===');
// The reference is the TZ's own expression, evaluated independently of the
// production code path. sigmaDay is NOT called here on purpose: if production
// ever stopped routing through it (inv. 20), this reference would still hold
// and section A would stay green — so section A is not the guard for that.
// Section A1 below is.
const K = Math.sqrt(8 / Math.PI);
const ID_N = 200000;
for (let i = 0; i < ID_N; i++) {
    const cur = span(1e-4, 1e5);
    const vol = span(1e-6, 0.25);
    const lo  = span(1e-6, cur * 2);
    const hi  = lo + span(1e-9, cur);
    const got = P.dayRangeRatio(hi, lo, cur, vol);
    const want = (hi - lo) / (cur * vol * Math.sqrt(24) * K);
    // Relative tolerance: the TZ's 1e-12 is an equality statement about the
    // same arithmetic in a different association order, not about magnitude.
    near('identity#' + i, got, want, Math.abs(want) * 1e-12 + 1e-300);
}
console.log('  compared: ' + N.identity);

console.log('=== A1. The daily-sigma conversion goes through sigmaDay (inv. 20) ===');
// dayRangeRatio must not recompute vol * sqrt(24) of its own. Proven by
// behaviour, not by reading the source: swap the production sigmaDay for a
// scaled one and the ratio must move by exactly the inverse factor.
{
    const before = P.dayRangeRatio(110, 100, 105, 0.01);
    const real = P.sigmaDay;
    P.sigmaDay = function (v) { return real(v) * 4; };
    const after = P.dayRangeRatio(110, 100, 105, 0.01);
    P.sigmaDay = real;
    near('dayRangeRatio routes through sigmaDay', after, before / 4, Math.abs(before / 4) * 1e-12);
    near('sigmaDay restored', P.dayRangeRatio(110, 100, 105, 0.01), before, 0);
}
console.log('  compared: ' + (N.identity - ID_N));

// ───────────────────────────────────────────────────────────────────────────
section = 'nulls';
console.log('=== B. Nulls: a missing measurement is never a number ===');
// Strict === null: 0 and Infinity both fail this, which is the whole point.
const NULL_CASES = [
    ['vol null',        [110, 100, 105, null]],
    ['vol undefined',   [110, 100, 105, undefined]],
    ['vol 0',           [110, 100, 105, 0]],
    ['vol NaN',         [110, 100, 105, NaN]],
    ['vol negative',    [110, 100, 105, -0.01]],
    ['vol Infinity',    [110, 100, 105, Infinity]],
    ['cur 0',           [110, 100, 0, 0.01]],
    ['cur negative',    [110, 100, -105, 0.01]],
    ['cur null',        [110, 100, null, 0.01]],
    ['cur undefined',   [110, 100, undefined, 0.01]],
    ['cur NaN',         [110, 100, NaN, 0.01]],
    ['cur Infinity',    [110, 100, Infinity, 0.01]],
    ['hi < lo',         [90, 100, 105, 0.01]],
    ['hi === lo',       [100, 100, 105, 0.01]],
    ['hi null',         [null, 100, 105, 0.01]],
    ['hi undefined',    [undefined, 100, 105, 0.01]],
    ['hi NaN',          [NaN, 100, 105, 0.01]],
    ['hi Infinity',     [Infinity, 100, 105, 0.01]],
    ['lo null',         [110, null, 105, 0.01]],
    ['lo undefined',    [110, undefined, 105, 0.01]],
    ['lo NaN',          [110, NaN, 105, 0.01]],
    ['lo -Infinity',    [110, -Infinity, 105, 0.01]],
    ['all undefined',   [undefined, undefined, undefined, undefined]],
    ['no arguments',    []],
    ['strings',         ['110', '100', '105', '0.01']]
];
NULL_CASES.forEach(function (c) {
    eq('null: ' + c[0], P.dayRangeRatio(c[1][0], c[1][1], c[1][2], c[1][3]), null);
});
// Underflow must not become Infinity: a denominator that rounds to zero is a
// missing measurement, not an infinitely abnormal day.
eq('null: denominator underflows to 0', P.dayRangeRatio(1e-320, 0, 5e-324, 5e-324), null);
// Overflow of the numerator likewise.
eq('null: ratio overflows to Infinity', P.dayRangeRatio(1.7e308, -1.7e308, 1e-300, 1e-300), null);

// Randomised out-of-domain fuzz: every invalid combination, always null.
const FUZZ_N = 20000;
for (let i = 0; i < FUZZ_N; i++) {
    const pick = [0, null, undefined, NaN, Infinity, -Infinity, -span(1, 100)];
    const cur = rnd() < 0.5 ? pick[Math.floor(rnd() * pick.length)] : span(1, 100);
    const vol = rnd() < 0.5 ? pick[Math.floor(rnd() * pick.length)] : span(1e-4, 0.1);
    const lo  = rnd() < 0.5 ? pick[Math.floor(rnd() * pick.length)] : span(1, 100);
    const hi  = rnd() < 0.5 ? pick[Math.floor(rnd() * pick.length)] : span(1, 100);
    const r = P.dayRangeRatio(hi, lo, cur, vol);
    const valid = typeof hi === 'number' && isFinite(hi)
               && typeof lo === 'number' && isFinite(lo)
               && typeof cur === 'number' && isFinite(cur) && cur > 0
               && typeof vol === 'number' && isFinite(vol) && vol > 0
               && hi > lo;
    if (valid) ok('fuzz#' + i + ' valid input returns a finite number',
                  typeof r === 'number' && isFinite(r) && r > 0);
    else eq('fuzz#' + i + ' invalid input returns null', r, null);
}
console.log('  compared: ' + N.nulls);

// ───────────────────────────────────────────────────────────────────────────
section = 'quorum';
console.log('=== C. listExhaustion: median, exclusion and the quorum of 8 ===');
function row(hi, lo, cur, vol) { return { hi24: hi, lo24: lo, cur: cur, cd: { volatility: vol } }; }
// A row whose ratio is exactly r, built from the production function itself so
// the fixture cannot drift from the measure it feeds.
function rowFor(r) {
    const cur = 100, vol = 0.01, lo = 100;
    const hi = lo + r * (cur * P.sigmaDay(vol) * Math.sqrt(8 / Math.PI));
    return row(hi, lo, cur, vol);
}
function med(rows) { return P.listExhaustion(rows).median; }

// Fixture sanity: rowFor really produces the ratio it claims.
[0.5, 1, 2.43, 7].forEach(function (r) {
    near('rowFor(' + r + ') round-trips', P.dayRangeRatio.apply(null,
        (function (x) { return [x.hi24, x.lo24, x.cur, x.cd.volatility]; })(rowFor(r))), r, r * 1e-12);
});

// Odd n: the middle value.
{
    const rows = [3, 1, 2, 5, 4, 6, 7, 9, 8].map(rowFor);
    eq('odd n = 9', P.listExhaustion(rows).n, 9);
    near('odd n median is the middle value', med(rows), 5, 1e-12);
}
// Even n: the mean of the two middle values.
{
    const rows = [1, 2, 3, 4, 5, 6, 7, 10].map(rowFor);
    eq('even n = 8', P.listExhaustion(rows).n, 8);
    near('even n median averages the two middles', med(rows), 4.5, 1e-12);
}
// Order must not matter.
{
    const asc  = [1, 2, 3, 4, 5, 6, 7, 8].map(rowFor);
    const desc = [8, 7, 6, 5, 4, 3, 2, 1].map(rowFor);
    near('median is order-independent', med(desc), med(asc), 1e-12);
}
// Sorting is numeric, not lexicographic: 10 must not sort between 1 and 2.
{
    const rows = [10, 9, 8, 7, 6, 5, 4, 3, 2].map(rowFor);
    near('numeric sort, not lexicographic', med(rows), 6, 1e-12);
}
// Rows with a null ratio are excluded from BOTH median and n.
{
    const good = [1, 2, 3, 4, 5, 6, 7, 8].map(rowFor);
    const bad = [
        { hi24: 110, lo24: 100, cur: 105, cd: { volatility: 0 } },   // vol 0
        { hi24: 100, lo24: 100, cur: 105, cd: { volatility: 0.01 } }, // hi === lo
        { hi24: 110, lo24: 100, cur: 105, cd: {} },                   // no volatility
        { hi24: 110, lo24: 100, cur: 105, cd: null },                 // nodata row
        { state: 'nopair', cd: null },                                // no pair
        { state: 'dead', cd: null },                                  // dead market
        null,
        undefined
    ];
    const mixed = P.listExhaustion(bad.slice(0, 4).concat(good).concat(bad.slice(4)));
    eq('null rows excluded from n', mixed.n, 8);
    near('null rows excluded from median', mixed.median, med(good), 1e-12);
    ok('a null ratio never became a zero', mixed.median > 4);
}
// Quorum: below 8 contributing rows there is no verdict, whatever the values.
for (let k = 0; k <= 12; k++) {
    const rows = [];
    for (let i = 0; i < k; i++) rows.push(rowFor(9 + i));   // all extreme
    const r = P.listExhaustion(rows);
    eq('n reported truthfully at k=' + k, r.n, k);
    if (k < 8) {
        eq('k=' + k + ' below quorum -> median null', r.median, null);
        eq('k=' + k + ' below quorum -> abnormal false', r.abnormal, false);
    } else {
        ok('k=' + k + ' at or above quorum -> median is a number',
           typeof r.median === 'number' && isFinite(r.median));
    }
}
// Degenerate inputs.
[[[], 0], [null, 0], [undefined, 0]].forEach(function (c) {
    const r = P.listExhaustion(c[0]);
    eq('degenerate n', r.n, c[1]);
    eq('degenerate median', r.median, null);
    eq('degenerate abnormal', r.abnormal, false);
});
// Shape contract: always the same three keys, always those types.
{
    const r = P.listExhaustion([1, 2, 3, 4, 5, 6, 7, 8].map(rowFor));
    eq('shape keys', Object.keys(r).sort().join(','), 'abnormal,median,n');
    eq('n is an integer', r.n === Math.floor(r.n), true);
    eq('abnormal is a boolean', typeof r.abnormal, 'boolean');
}
// Stage A contract: abnormal is permanently false, at any magnitude.
[0.01, 1, 2.43, 5, 100, 1e6].forEach(function (r) {
    const rows = [];
    for (let i = 0; i < 25; i++) rows.push(rowFor(r));
    eq('abnormal stays false at median ' + r, P.listExhaustion(rows).abnormal, false);
});
console.log('  compared: ' + N.quorum);

// ───────────────────────────────────────────────────────────────────────────
section = 'venue';
console.log('=== C1. Venue: the declaration is read, the host is not (TZ-12 B) ===');
// §3.14 / inv. 41. The three fut:true assets take their range from the
// perpetual and their volatility from a spot index, so pooling them makes the
// live estimator a different estimator from the one every calibration and every
// journal replay measured on the 25 spot assets (§3.16, inv. 47).
// A row exactly as production builds it: t is the entry from tokens[].
function vrow(r, fut, name) {
    const x = rowFor(r);
    x.t = { name: name || 'SPOT', s: (name || 'SPOT') + 'USDT' };
    if (fut) x.t.fut = true;
    return x;
}
// C1.1 — a mixed list must equal the same list with the fut rows physically
// removed, in BOTH median and n. The fut values are chosen far outside the
// spot ones so their presence would move both if they were counted.
{
    const spot = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4].map(function (r, i) {
        return vrow(r, false, 'S' + i);
    });
    const fut = [9.0, 9.5, 12.0].map(function (r, i) { return vrow(r, true, 'F' + i); });
    // Interleaved, so the exclusion cannot be an artefact of position.
    const mixed = [fut[0]].concat(spot.slice(0, 4), [fut[1]], spot.slice(4), [fut[2]]);
    const a = P.listExhaustion(mixed);
    const b = P.listExhaustion(spot);
    eq('mixed n equals the spot count', a.n, 9);
    eq('spot-only n equals the spot count', b.n, 9);
    near('mixed median equals spot-only median', a.median, b.median, 1e-12);
    near('median is the middle spot value', a.median, 1.0, 1e-12);
    eq('abnormal untouched by the exclusion', a.abnormal, false);
    // The control on the control: counting them WOULD have moved both.
    const naive = mixed.map(function (x) { const y = {}; for (const k in x) y[k] = x[k]; delete y.t; return y; });
    const c = P.listExhaustion(naive);
    eq('without the declaration the same list counts 12', c.n, 12);
    ok('without the declaration the median moves', Math.abs(c.median - b.median) > 1e-9,
       c.median + ' vs ' + b.median);
}
// C1.2 — the quorum is applied AFTER the exclusion: a list that reaches eight
// only by counting fut rows has no verdict at all.
{
    const spot = [1, 2, 3, 4, 5].map(function (r, i) { return vrow(r, false, 'S' + i); });
    const fut  = [1, 2, 3, 4, 5].map(function (r, i) { return vrow(r, true, 'F' + i); });
    const r = P.listExhaustion(spot.concat(fut));
    eq('below-quorum after exclusion -> n is the spot count', r.n, 5);
    eq('below-quorum after exclusion -> median null', r.median, null);
    eq('below-quorum after exclusion -> abnormal false', r.abnormal, false);
    // Same rows, declaration dropped: quorum would have been met. That is the
    // defect this stage closes, stated as an assertion rather than a comment.
    const naive = spot.concat(fut).map(function (x) { const y = {}; for (const k in x) y[k] = x[k]; delete y.t; return y; });
    eq('the same list reaches quorum without the declaration', P.listExhaustion(naive).n, 10);
    ok('and would have produced a median', typeof P.listExhaustion(naive).median === 'number');
}
// C1.3 — the venue test short-circuits BEFORE the cd test: a fut row may not be
// read at all, whatever fields it carries. Proven by a throwing accessor, which
// is the only way to observe "was not read" rather than "was read and ignored".
{
    let touched = 0;
    const trap = { t: { name: 'XMR', s: 'XMRUSDT', fut: true }, hi24: 200, lo24: 100, cur: 150 };
    Object.defineProperty(trap, 'cd', {
        enumerable: true,
        get: function () { touched++; throw new Error('cd read on a fut:true row'); }
    });
    const spot = [1, 2, 3, 4, 5, 6, 7, 8].map(function (r, i) { return vrow(r, false, 'S' + i); });
    let threw = null;
    let out = null;
    try { out = P.listExhaustion([trap].concat(spot)); } catch (e) { threw = e.message; }
    eq('no exception: the fut row was skipped before cd', threw, null);
    eq('the cd of a fut row was never read', touched, 0);
    eq('n counts spot rows only', out ? out.n : -1, 8);
    // And the trap really does fire when the declaration is absent — the probe
    // must be able to detect a read, or it proves nothing (inv. 23).
    const bare = { hi24: 200, lo24: 100, cur: 150 };
    Object.defineProperty(bare, 'cd', {
        enumerable: true,
        get: function () { touched++; throw new Error('read'); }
    });
    let threw2 = null;
    try { P.listExhaustion([bare].concat(spot)); } catch (e) { threw2 = e.message; }
    eq('the probe can detect a cd read', threw2, 'read');
    eq('and it fired exactly once', touched, 1);
}
// C1.4 — fut:false and a missing fut field are both spot; only fut === true
// (and any other truthy value production could carry) excludes.
{
    const base = [1, 2, 3, 4, 5, 6, 7, 8].map(function (r, i) { return vrow(r, false, 'S' + i); });
    const want = P.listExhaustion(base);
    [[undefined, 9], [false, 9], [0, 9], [null, 9], [true, 8]].forEach(function (c) {
        const extra = rowFor(3.5);
        extra.t = { name: 'X', s: 'XUSDT' };
        if (c[0] !== undefined) extra.t.fut = c[0];
        eq('fut=' + JSON.stringify(c[0]) + ' -> n', P.listExhaustion(base.concat([extra])).n, c[1]);
    });
    // A row with no t at all is still counted: the declaration is absent, not
    // negative, and the bench fixtures of TZ-10 have exactly that shape.
    eq('a row with no t is still counted', want.n, 8);
}
// C1.5 — the exclusion is not a length trick: 25 spot + 3 fut, the live shape.
{
    const rows = [];
    for (let i = 0; i < 25; i++) rows.push(vrow(0.5 + i * 0.1, false, 'S' + i));
    ['XMR', 'LIT', 'HYPE'].forEach(function (nm) { rows.push(vrow(20, true, nm)); });
    const r = P.listExhaustion(rows);
    eq('live shape: 28 rows, 25 counted', r.n, 25);
    near('live shape: median is the 13th spot value', r.median, 0.5 + 12 * 0.1, 1e-12);
}
console.log('  compared: ' + N.venue);

// ───────────────────────────────────────────────────────────────────────────
section = 'banner';
console.log('=== D. regimeBanner: every abnormal === false case ===');
// The four banner branches, with trend split by direction because the branch
// picks a different colour on each: five states x isLong = ten combinations,
// a superset of the eight §5.2 requires to be byte-identical to today's
// output. The matching abnormal === true half arrives with Stage C.
const STATES = [
    ['unknown', { known: false, mode: 'range',  dir: 0 }, '#888'],
    ['stress',  { known: true,  mode: 'stress', dir: 0 }, 'var(--red)'],
    ['trend+',  { known: true,  mode: 'trend',  dir: 1 }, null],
    ['trend-',  { known: true,  mode: 'trend',  dir: -1 }, null],
    ['range',   { known: true,  mode: 'range',  dir: 0 }, 'var(--accent)']
];
// The word that distinguishes the exhaustion clause of Stage C. Written as
// escapes, like every Russian string that lives inside JavaScript here.
const CLAUSE = '\u0410\u041D\u041E\u041C\u0410\u041B\u042C\u041D\u042B\u0419';
const seen = {};
STATES.forEach(function (s) {
    [true, false].forEach(function (isLong) {
        const out = P.regimeBanner(JSON.parse(JSON.stringify(s[1])), isLong);
        const key = s[0] + '/' + (isLong ? 'long' : 'short');
        seen[key] = out;
        ok(key + ' renders a div', out.indexOf('<div style=') === 0 && out.slice(-6) === '</div>');
        eq(key + ' carries no exhaustion clause', out.indexOf(CLAUSE), -1);
        if (s[2]) ok(key + ' colour ' + s[2], out.indexOf('border-left:3px solid ' + s[2]) !== -1);
        else {
            // trend: green when the side matches the trend, red when it does not.
            const up = s[1].dir > 0;
            const want = (up === isLong) ? 'var(--green)' : 'var(--red)';
            ok(key + ' colour ' + want, out.indexOf('border-left:3px solid ' + want) !== -1);
        }
        ok(key + ' colour is applied to text as well as border',
           out.indexOf(';color:') !== -1);
    });
});
// Amber is Stage C's colour and must not appear anywhere yet.
Object.keys(seen).forEach(function (k) {
    eq(k + ' is not amber yet', seen[k].indexOf('#e0a02a'), -1);
});
// Red belongs to stress, and stress alone must never be softened away from it.
ok('stress/long is red', seen['stress/long'].indexOf('var(--red)') !== -1);
ok('stress/short is red', seen['stress/short'].indexOf('var(--red)') !== -1);
console.log('  compared: ' + N.banner);

// ───────────────────────────────────────────────────────────────────────────
section = 'stress';
console.log('=== D2. Symmetric stress: five banner states, byte-identical (TZ-12 A) ===');
// The whole banner surface, written out. Not a substring match and not a
// property: the exact bytes production must emit, so a re-worded string is a
// failure and not a silent pass. The four texts that predate TZ-12 are copied
// from the released board; OVERHEAT is the one string this stage adds.
const UNKNOWN  = '\u0420\u0415\u0416\u0418\u041c \u041d\u0415\u0418\u0417\u0412\u0415\u0421\u0422\u0415\u041d \u2014 \u043d\u0435\u0442 \u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0438 BTC';   // РЕЖИМ НЕИЗВЕСТЕН — нет статистики BTC
const STRESS   = '\u0421\u0422\u0420\u0415\u0421\u0421 \u0420\u042b\u041d\u041a\u0410 \u2014 \u0441\u0434\u0435\u043b\u043e\u043a \u043d\u0435\u0442 \u043d\u0438 \u043d\u0430 \u043e\u0434\u043d\u043e\u0439 \u0441\u0442\u043e\u0440\u043e\u043d\u0435';   // СТРЕСС РЫНКА — сделок нет ни на одной стороне
const OVERHEAT = '\u0420\u042b\u041d\u041e\u041a \u041f\u0415\u0420\u0415\u0413\u0420\u0415\u0422 \u2014 \u0441\u0434\u0435\u043b\u043e\u043a \u043d\u0435\u0442 \u043d\u0438 \u043d\u0430 \u043e\u0434\u043d\u043e\u0439 \u0441\u0442\u043e\u0440\u043e\u043d\u0435';   // РЫНОК ПЕРЕГРЕТ — сделок нет ни на одной стороне
const TRUP     = '\u0422\u0420\u0415\u041d\u0414 \u0412\u0412\u0415\u0420\u0425';   // ТРЕНД ВВЕРХ
const TRDN     = '\u0422\u0420\u0415\u041d\u0414 \u0412\u041d\u0418\u0417';   // ТРЕНД ВНИЗ
const WITH     = ' \u2014 \u0441\u0447\u0451\u0442 \u043f\u043e \u043a\u0430\u043d\u0430\u043b\u0443 \u0438\u043c\u043f\u0443\u043b\u044c\u0441\u0430';   //  — счёт по каналу импульса
const AGAINST  = ' \u2014 \u0432\u0441\u044f \u044d\u0442\u0430 \u0441\u0442\u043e\u0440\u043e\u043d\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0430, \u0441\u0447\u0451\u0442 \u2014 \u0442\u043e\u043b\u044c\u043a\u043e \u043e\u0447\u0435\u0440\u0435\u0434\u044c \u0432\u043d\u0438\u043c\u0430\u043d\u0438\u044f';   //  — вся эта сторона закрыта, счёт — только очередь внимания
const RANGE    = '\u0414\u0418\u0410\u041f\u0410\u0417\u041e\u041d \u2014 \u0441\u0447\u0451\u0442 \u043f\u043e \u043a\u0430\u043d\u0430\u043b\u0443 \u0432\u043e\u0437\u0432\u0440\u0430\u0442\u0430';   // ДИАПАЗОН — счёт по каналу возврата

// The wrapper is production's, so a change to it is caught here too.
function bannerHtml(txt, col) {
    return '<div style="margin:2px 0 8px;padding:6px 10px;border-left:3px solid ' + col
         + ';font-size:0.82em;letter-spacing:0.04em;color:' + col + ';">' + txt + '</div>';
}
const RED = 'var(--red)', GREEN = 'var(--green)', GREY = '#888', ACC = 'var(--accent)';
const Z = P.REG_STRESS_Z;
ok('REG_STRESS_Z is a positive number in production', typeof Z === 'number' && Z > 0);

// state, reg, expected [long, short] as full bytes.
const TABLE = [
    ['unknown',          { known: false, mode: 'range',  dir: 0, z: null },
        bannerHtml(UNKNOWN, GREY),            bannerHtml(UNKNOWN, GREY)],
    ['stress z null',    { known: true,  mode: 'stress', dir: 0, z: null },
        bannerHtml(STRESS, RED),              bannerHtml(STRESS, RED)],
    ['stress z -4.06',   { known: true,  mode: 'stress', dir: 0, z: -4.06 },
        bannerHtml(STRESS, RED),              bannerHtml(STRESS, RED)],
    ['stress z -Z',      { known: true,  mode: 'stress', dir: 0, z: -Z },
        bannerHtml(STRESS, RED),              bannerHtml(STRESS, RED)],
    ['stress z 0',       { known: true,  mode: 'stress', dir: 0, z: 0 },
        bannerHtml(STRESS, RED),              bannerHtml(STRESS, RED)],
    ['stress z +Z-eps',  { known: true,  mode: 'stress', dir: 0, z: Z - 1e-9 },
        bannerHtml(STRESS, RED),              bannerHtml(STRESS, RED)],
    ['overheat z +Z',    { known: true,  mode: 'stress', dir: 0, z: Z },
        bannerHtml(OVERHEAT, RED),            bannerHtml(OVERHEAT, RED)],
    ['overheat z +4.06', { known: true,  mode: 'stress', dir: 0, z: 4.06 },
        bannerHtml(OVERHEAT, RED),            bannerHtml(OVERHEAT, RED)],
    ['trend up',         { known: true,  mode: 'trend',  dir: 1, z: 0.4 },
        bannerHtml(TRUP + WITH, GREEN),       bannerHtml(TRUP + AGAINST, RED)],
    ['trend down',       { known: true,  mode: 'trend',  dir: -1, z: -0.4 },
        bannerHtml(TRDN + AGAINST, RED),      bannerHtml(TRDN + WITH, GREEN)],
    ['range',            { known: true,  mode: 'range',  dir: 0, z: 0.1 },
        bannerHtml(RANGE, ACC),               bannerHtml(RANGE, ACC)]
];
TABLE.forEach(function (t) {
    eq(t[0] + '/long  byte-identical',  P.regimeBanner(JSON.parse(JSON.stringify(t[1])), true),  t[2]);
    eq(t[0] + '/short byte-identical',  P.regimeBanner(JSON.parse(JSON.stringify(t[1])), false), t[3]);
});
// Both stress texts are red: the state closes BOTH sides, and a colour that
// distinguished them would say otherwise.
eq('overheat is red, not green', TABLE[6][2].indexOf(GREEN), -1);
eq('overheat carries no amber', TABLE[6][2].indexOf('#e0a02a'), -1);
ok('the two stress texts differ', STRESS !== OVERHEAT);
eq('the pre-TZ-12 stress string is unchanged', TABLE[1][2], bannerHtml(STRESS, RED));

// D2b — the real route: btcStats -> marketRegime -> regimeBanner. The banner is
// driven by what production actually computes, not by a hand-built reg.
{
    const VH = P.VOL_HARD, H = P.H_NOISE;
    ok('VOL_HARD and H_NOISE are present', typeof VH === 'number' && typeof H === 'number');
    // r7 chosen so z lands exactly where the case needs it: z = r7/(v*sqrt(H)).
    function btcFor(v, z) { return { volatility: v, r7: z * v * Math.sqrt(H), r14: 0 }; }
    const CASES = [
        ['end-to-end +4 sigma',  btcFor(VH / 2, 4),      'stress', OVERHEAT],
        ['end-to-end -4 sigma',  btcFor(VH / 2, -4),     'stress', STRESS],
        ['end-to-end +Z exact',  btcFor(VH / 2, Z),      'stress', OVERHEAT],
        ['end-to-end -Z exact',  btcFor(VH / 2, -Z),     'stress', STRESS],
        ['end-to-end quiet',     btcFor(VH / 2, 0.2),    'range',  RANGE],
        ['end-to-end vol hard',  btcFor(VH, 0.2),        'stress', STRESS]
    ];
    CASES.forEach(function (c) {
        const reg = P.marketRegime(c[1]);
        eq(c[0] + ' mode', reg.mode, c[2]);
        if (c[2] === 'stress') eq(c[0] + ' dir stays 0', reg.dir, 0);
        [true, false].forEach(function (isLong) {
            const out = P.regimeBanner(reg, isLong);
            ok(c[0] + (isLong ? '/long' : '/short') + ' prints its text',
               out.indexOf(c[3]) !== -1, out);
        });
    });
}
console.log('  compared: ' + N.stress);

// ───────────────────────────────────────────────────────────────────────────
section = 'inert';
console.log('=== E. Inertness: the new measure reaches no consumer ===');
// Stage A's whole contract. When Stage C lands this section inverts for
// abnormal === true and keeps holding for abnormal === false.
STATES.forEach(function (s) {
    [true, false].forEach(function (isLong) {
        const key = s[0] + '/' + (isLong ? 'long' : 'short');
        [true, false].forEach(function (abnormal) {
            const reg = JSON.parse(JSON.stringify(s[1]));
            reg.day = { median: 2.43, n: 25, abnormal: abnormal };
            eq(key + ' unchanged by reg.day.abnormal=' + abnormal,
               P.regimeBanner(reg, isLong), seen[key]);
        });
        // A null day, the shape listExhaustion returns below quorum.
        const regNull = JSON.parse(JSON.stringify(s[1]));
        regNull.day = { median: null, n: 3, abnormal: false };
        eq(key + ' unchanged by a below-quorum reg.day',
           P.regimeBanner(regNull, isLong), seen[key]);
    });
});
console.log('  compared: ' + N.inert);

// ───────────────────────────────────────────────────────────────────────────
section = 'purity';
console.log('=== F. Purity: regimeBanner names, it does not compute ===');
STATES.forEach(function (s) {
    [true, false].forEach(function (isLong) {
        const key = s[0] + '/' + (isLong ? 'long' : 'short');
        const reg = Object.freeze(JSON.parse(JSON.stringify(s[1])));
        const before = JSON.stringify(reg);
        const a = P.regimeBanner(reg, isLong);
        const b = P.regimeBanner(reg, isLong);
        eq(key + ' is deterministic', a, b);
        eq(key + ' does not mutate reg', JSON.stringify(reg), before);
    });
});
// listExhaustion must not mutate the rows it reads either.
{
    const rows = [1, 2, 3, 4, 5, 6, 7, 8].map(rowFor);
    const before = JSON.stringify(rows);
    P.listExhaustion(rows);
    eq('listExhaustion does not mutate its rows', JSON.stringify(rows), before);
    eq('listExhaustion does not reorder its rows', rows.length, 8);
}
console.log('  compared: ' + N.purity);

// ───────────────────────────────────────────────────────────────────────────
section = 'control';
console.log('=== G. Negative control: this bench can actually fail ===');
// A check that never fires proves nothing (inv. 22). Prove the comparator
// reports a mismatch, without letting the probe count against this run and
// without printing a FAIL line a reader would take for a real one.
{
    const before = fails, beforeN = N.control, beforeC = checks;
    const realLog = console.log;
    console.log = function () {};
    eq('deliberate mismatch', P.dayRangeRatio(110, 100, 105, 0.01), null);
    console.log = realLog;
    const detected = (fails === before + 1);
    fails = before; N.control = beforeN; checks = beforeC;
    ok('comparator detects a wrong answer', detected);
    console.log('  comparator reported the planted mismatch: ' + detected);
}
console.log('  compared: ' + N.control);

// ───────────────────────────────────────────────────────────────────────────
section = 'wiring';
console.log('=== H. Wiring: every field the measure READS is a field update() WRITES ===');
// Invariant 48 — a bench that builds its own input proves the FUNCTION, not
// the WIRING. Sections B, C and D above all hand listExhaustion rows shaped by
// this file, so they stayed green through a revision in which the live row
// object carried none of hi24 / lo24 / cur and the measure returned
// {median: null, n: 0} on every render. This section reads the two sides of
// the contract out of the SOURCE and compares them, so the same divergence
// cannot pass again.
//
// The mechanism takes a list of readers; a second one is added by naming it
// here. Only listExhaustion is wired at this revision.
const READERS = ['listExhaustion'];
const PRODUCER = 'update';

// Cut a top-level function out of the script by brace matching. Not a regex
// over the whole file: a regex cannot tell a closing brace of the function
// from a closing brace of a string or a nested block, and the answer this
// section gives is only as good as its slice.
function cutFunction(source, name) {
    const sig = 'function ' + name + '(';
    const at = source.indexOf(sig);
    if (at < 0) return null;
    const open = source.indexOf('{', at);
    if (open < 0) return null;
    let depth = 0, i = open;
    let inS = null, inLine = false, inBlock = false, inRe = false, esc = false;
    // The last SIGNIFICANT character — whitespace and comments skipped. It is
    // the only thing that separates a regex literal from a division: after an
    // identifier, a number, ')' or ']' a slash divides; after an operator or an
    // opening bracket it opens a pattern. Guessing wrong swallows the rest of
    // the function and this section would then report a producer that has no
    // fields at all, which inv. 22 turns into a failure rather than a pass.
    let prev = '';
    for (; i < source.length; i++) {
        const c = source[i];
        if (inLine) { if (c === '\n') inLine = false; continue; }
        if (inBlock) { if (c === '*' && source[i + 1] === '/') { inBlock = false; i++; } continue; }
        if (inS) { if (esc) { esc = false; } else if (c === '\\') { esc = true; }
                   else if (c === inS) { inS = null; prev = c; } continue; }
        if (inRe) { if (esc) { esc = false; } else if (c === '\\') { esc = true; }
                    else if (c === '/') { inRe = false; prev = c; } continue; }
        if (c === '/' && source[i + 1] === '/') { inLine = true; i++; continue; }
        if (c === '/' && source[i + 1] === '*') { inBlock = true; i++; continue; }
        if (/\s/.test(c)) continue;
        if (c === '"' || c === "'" || c === '`') { inS = c; prev = c; continue; }
        if (c === '/') {
            if (/[\w$)\]'"`]/.test(prev)) { prev = c; continue; }   // division
            inRe = true; continue;
        }
        if (c === '{') depth++;
        else if (c === '}') { depth--; if (depth === 0) return source.slice(at, i + 1); }
        prev = c;
    }
    return null;
}

// Every field the reader takes off the row it was handed, one level deep plus
// the second level wherever the source reads one (row.t.fut). The reader binds
// its row argument to the local `row`, which is what makes this readable off
// the text: a rename there is a change to this contract and must be made here
// too, deliberately.
function fieldsRead(body) {
    const out = {};
    const re = /\brow\.([A-Za-z_$][\w$]*)(?:\.([A-Za-z_$][\w$]*))?/g;
    let m;
    while ((m = re.exec(body)) !== null) {
        out[m[1]] = true;
        if (m[2]) out[m[1] + '.' + m[2]] = true;
    }
    return Object.keys(out).sort();
}

// Every field the row object receives in the producer: the keys of the
// `var row = { … }` literal, plus every `row.<ident> =` assignment in the
// body. `orow.<ident> =` is deliberately NOT counted — that is the off-list
// filter writing to rows it took out of the array, downstream of the contract.
function fieldsWritten(body) {
    const out = {};
    const lit = /var\s+row\s*=\s*(?:rowRange\()?\{([\s\S]*?)\}/.exec(body);
    if (lit) {
        const re = /([A-Za-z_$][\w$]*)\s*:/g;
        let m;
        while ((m = re.exec(lit[1])) !== null) out[m[1]] = true;
    }
    const re2 = /\brow\.([A-Za-z_$][\w$]*)\s*=(?!=)/g;
    let m2;
    while ((m2 = re2.exec(body)) !== null) out[m2[1]] = true;
    return Object.keys(out).sort();
}

// The comparison itself, factored so the positive control below can run it
// over a MUTATED copy of the source and be told what that copy is missing.
function wiringGaps(source) {
    const prod = cutFunction(source, PRODUCER);
    if (prod === null) return { error: 'producer ' + PRODUCER + ' not found' };
    const writes = fieldsWritten(prod);
    const per = [];
    for (let r = 0; r < READERS.length; r++) {
        const body = cutFunction(source, READERS[r]);
        if (body === null) return { error: 'reader ' + READERS[r] + ' not found' };
        const reads = fieldsRead(body);
        const missing = reads.filter(function (f) {
            // A nested read is satisfied by its ROOT being written: update()
            // writes row.t and row.cd whole, and `fut` / `volatility` are
            // fields of the objects it assigns, not of the row.
            return writes.indexOf(f.split('.')[0]) < 0;
        });
        per.push({ reader: READERS[r], reads: reads, missing: missing });
    }
    return { writes: writes, per: per };
}

const W = wiringGaps(src);
ok('wiring extractor found both sides', !W.error);
if (W.error) {
    console.log('  FAIL ' + W.error);
} else {
    // Inv. 22: zero reads or zero writes is a FAILURE, not a pass. An
    // extractor that silently matched nothing would make this whole section
    // green by finding no gap in an empty set.
    ok('producer writes at least one row field', W.writes.length > 0);
    console.log('  ' + PRODUCER + '() writes: ' + W.writes.join(', '));
    for (let r = 0; r < W.per.length; r++) {
        const p = W.per[r];
        ok(p.reader + ' reads at least one row field', p.reads.length > 0);
        console.log('  ' + p.reader + ' reads: ' + p.reads.join(', '));
        // One check per field read, named, so a failure says WHICH field the
        // live row never carries.
        for (let f = 0; f < p.reads.length; f++) {
            const fld = p.reads[f];
            const root = fld.split('.')[0];
            ok(p.reader + ' reads row.' + fld + ' -> ' + PRODUCER + '() writes row.' + root,
               W.writes.indexOf(root) >= 0);
        }
        if (p.missing.length) {
            console.log('  FAIL ' + p.reader + ' reads fields the live row never carries: '
                      + p.missing.join(', '));
        }
    }
}

// Positive control (inv. 23). A checker that cannot fail is not a check: run
// the same extractor over a copy of the source with one producing assignment
// deleted, and over a copy with one extra read added, and require it to name
// exactly that field and nothing else.
{
    const realLog = console.log;

    const cutWrite = src.replace('row.cur  = parseFloat(coin.lastPrice);', '');
    ok('control copy differs from the source', cutWrite !== src);
    console.log = function () {};
    const A = wiringGaps(cutWrite);
    console.log = realLog;
    eq('deleting row.cur reports exactly [cur]',
       A.error ? 'ERR:' + A.error : A.per[0].missing.join(','), 'cur');

    const addRead = src.replace('            if (!row.cd) continue;',
                                '            if (!row.cd) continue;\n            if (row.zzzNotWritten) continue;');
    ok('control copy differs from the source', addRead !== src);
    console.log = function () {};
    const B = wiringGaps(addRead);
    console.log = realLog;
    eq('adding a read of row.zzzNotWritten reports exactly [zzzNotWritten]',
       B.error ? 'ERR:' + B.error : B.per[0].missing.join(','), 'zzzNotWritten');

    // And the unmutated source must report nothing at all, or the two controls
    // above would be indistinguishable from a checker that always fires.
    eq('the real source reports no missing field',
       W.error ? 'ERR:' + W.error : W.per[0].missing.join(','), '');
    console.log('  controls: deleted write named, added read named, clean source silent');
}
console.log('  compared: ' + N.wiring);

// ───────────────────────────────────────────────────────────────────────────
const sum = Object.keys(N).reduce(function (a, k) { return a + N[k]; }, 0);
console.log('\n--- per-section comparison counters ---');
Object.keys(N).forEach(function (k) { console.log('  ' + k + ': ' + N[k]); });
console.log('  SUM: ' + sum);
console.log('\n--- checks: ' + checks + '  fails: ' + fails + ' ---');
if (checks === 0) {
    console.log('FAIL bench verified nothing');
    process.exit(1);
}
if (sum !== checks) {
    console.log('FAIL counter sum ' + sum + ' does not equal the check total ' + checks);
    process.exit(1);
}
process.exit(fails === 0 ? 0 : 1);
