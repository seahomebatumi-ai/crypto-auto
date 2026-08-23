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

['dayRangeRatio', 'sigmaDay', 'listExhaustion', 'regimeBanner'].forEach(function (f) {
    if (typeof P[f] !== 'function') {
        console.log('FAIL ' + f + ' is not defined in index.html');
        process.exit(1);
    }
});

// Per-section counters. The gate total is a SUM of these, never an estimate
// (inv. 43), and each one counts comparisons actually made at its own site.
const N = { identity: 0, nulls: 0, quorum: 0, banner: 0, inert: 0, purity: 0, control: 0 };
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
