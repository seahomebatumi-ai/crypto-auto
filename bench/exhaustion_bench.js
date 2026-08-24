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
// SCOPE AT THIS REVISION (TZ-14). The constant now exists. DAY_RANGE_ABNORMAL
// = 1.39 is declared in index.html, pinned to bench/exhaustion-calibration.txt,
// and listExhaustion compares the list median against it. The two cases TZ-10
// could not write — the threshold edge and the banner at abnormal === true —
// are written here, and the sections whose comments predicted their own
// inversion (C's «permanently false», E's «inertness») are inverted rather
// than deleted: what was «the measure reaches no consumer» is now «the measure
// reaches EXACTLY ONE consumer, in EXACTLY ONE shape, and nothing else moved».
//
// Sections added by TZ-14:
//   I  record     the source constant and the calibration record agree (inv. 46)
//   J  threshold  the truth table of `abnormal`, plus a negative control that
//                 proves the comparison reads the CONSTANT and not a literal
//   K  live       the real update() over two lists straddling 1.39, rendered
//                 through the real DOM path (inv. 48)
//   L  surfaces   the same sentence on the card list and on the board (inv. 33)
//
// Section added by TZ-15:
//   M  caption    the block's caption denies no mechanism the block has, with
//                 the reverted-caption control that proves the scan can fire
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const HTML_PATH = path.join(__dirname, '..', 'index.html');
const RECORD_PATH = path.join(__dirname, 'exhaustion-calibration.txt');
const HTML = fs.readFileSync(HTML_PATH, 'utf8');
const src = HTML.slice(HTML.indexOf('<script>') + 8, HTML.lastIndexOf('</script>'));

// Minimal DOM/browser shims: the module body only needs these to evaluate.
// Factored into a loader because section J re-evaluates a MUTATED copy of the
// same source in its own context — a negative control that has to run the real
// module body, not a patched copy of one function.
function loadProduction(source) {
    const stub = new Proxy(function () {}, {
        get: () => stub, set: () => true, apply: () => stub, construct: () => stub
    });
    const sb = {
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
    sb.window = sb;
    vm.createContext(sb);
    vm.runInContext(source, sb, { filename: 'index.html:<script>' });
    return sb;
}

const P = loadProduction(src);   // production namespace

['dayRangeRatio', 'sigmaDay', 'listExhaustion', 'regimeBanner', 'marketRegime',
 'dayStateNote', 'numRu', 'boardHtml'].forEach(function (f) {
    if (typeof P[f] !== 'function') {
        console.log('FAIL ' + f + ' is not defined in index.html');
        process.exit(1);
    }
});

// Per-section counters. The gate total is a SUM of these, never an estimate
// (inv. 43), and each one counts comparisons actually made at its own site.
const N = { identity: 0, nulls: 0, quorum: 0, venue: 0, banner: 0, stress: 0, inert: 0,
            purity: 0, control: 0, wiring: 0,
            record: 0, threshold: 0, live: 0, surfaces: 0, caption: 0 };
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
// TZ-14 contract, replacing TZ-10's «abnormal is permanently false». The
// measure now carries the verdict of the calibrated rule at every magnitude,
// and the expectation is derived from the production constant rather than
// restated: a bench that hard-coded 1.39 here would go green on a source whose
// constant had drifted, which is what section I exists to prevent.
[0.01, 1, 2.43, 5, 100, 1e6].forEach(function (r) {
    const rows = [];
    for (let i = 0; i < 25; i++) rows.push(rowFor(r));
    const got = P.listExhaustion(rows);
    eq('abnormal at median ' + r, got.abnormal, got.median >= P.DAY_RANGE_ABNORMAL);
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
// output. Every reg here carries NO `day` field at all — the shape a caller
// that never wired the measure would hand in — so these ten outputs are the
// abnormal === false half, and section E proves the day field cannot move
// them either. The matching abnormal === true half is section E's second half.
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
// A reg with no day field prints ONE div and nothing amber after it. The
// literal below is production's own accent border, so a day line appearing
// where no day was supplied fails here rather than downstream.
const ACCENT_DIV = 'border-left:3px solid var(--accent);font-size:0.82em;letter-spacing:0.04em;color:var(--accent);';
Object.keys(seen).forEach(function (k) {
    eq(k + ' prints exactly one div without a day', seen[k].split('<div ').length - 1, 1);
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
console.log('=== E. The measure reaches ONE consumer, in ONE shape (TZ-14 D3) ===');
// TZ-10 wrote this section as «the new measure reaches no consumer» and said in
// its own comment that it would invert for abnormal === true and keep holding
// for abnormal === false. That is exactly what it does now. The quiet half is
// the stronger half: a day the rule did not call abnormal, and a day the list
// was too short to measure, must leave all ten (state x side) outputs
// byte-identical to the released banner.
//
// MED / THR / WORD are the three things the appended tail has to carry. They
// are written as escapes like every Russian string in this file, and they are
// NOT the whole sentence: asserting the sentence twice would only prove this
// file agrees with itself, while these three prove the tail says WHICH median,
// against WHICH threshold, in the state word the Boss reads first.
const WORD = '\u0414\u0415\u041d\u042c \u0423\u0416\u0415 \u0412\u042b\u041d\u0415\u0421\u0415\u041d';   // ДЕНЬ УЖЕ ВЫНЕСЕН
const MED  = '\u043c\u0435\u0434\u0438\u0430\u043d\u0430 \u0441\u043f\u0438\u0441\u043a\u0430 ';   // медиана списка
const THR  = '\u043f\u043e\u0440\u043e\u0433 ';   // порог
const NOTBAN = '\u041c\u0435\u0440\u0430 \u0434\u043d\u044f, \u043d\u0435 \u0437\u0430\u043f\u0440\u0435\u0442.';   // Мера дня, не запрет.
const DAY_MED = 2.43;
let tailSeen = null;
STATES.forEach(function (s) {
    [true, false].forEach(function (isLong) {
        const key = s[0] + '/' + (isLong ? 'long' : 'short');

        // ── the quiet half: byte-identical to the released banner ──────────
        const regQuiet = JSON.parse(JSON.stringify(s[1]));
        regQuiet.day = { median: DAY_MED, n: 25, abnormal: false };
        eq(key + ' unchanged at abnormal === false',
           P.regimeBanner(regQuiet, isLong), seen[key]);
        // A null median, the shape listExhaustion returns below quorum. An
        // unmeasured list is not a quiet one and must print nothing either.
        const regNull = JSON.parse(JSON.stringify(s[1]));
        regNull.day = { median: null, n: 3, abnormal: false };
        eq(key + ' unchanged by a below-quorum reg.day',
           P.regimeBanner(regNull, isLong), seen[key]);

        // ── the loud half: a strict PREFIX plus exactly one appended line ──
        const regLoud = JSON.parse(JSON.stringify(s[1]));
        regLoud.day = { median: DAY_MED, n: 25, abnormal: true };
        const out = P.regimeBanner(regLoud, isLong);
        eq(key + ' at abnormal === true: the quiet output is a strict prefix',
           out.slice(0, seen[key].length), seen[key]);
        ok(key + ' at abnormal === true: something was appended',
           out.length > seen[key].length);
        const tail = out.slice(seen[key].length);
        eq(key + ' tail is exactly one div',
           tail.split('<div ').length - 1 + '/' + (tail.slice(-6) === '</div>' ? 'closed' : 'open'),
           '1/closed');
        ok(key + ' tail is amber', tail.indexOf(ACCENT_DIV) > 0);
        ok(key + ' tail carries the state word', tail.indexOf(WORD) > 0);
        ok(key + ' tail carries the median text',
           tail.indexOf(MED + P.numRu(DAY_MED, 1)) > 0);
        ok(key + ' tail carries the threshold text',
           tail.indexOf(THR + P.numRu(P.DAY_RANGE_ABNORMAL, 2)) > 0);
        ok(key + ' tail says it is a measure and not a prohibition',
           tail.indexOf(NOTBAN) > 0);
        // The regime line's OWN colour is not touched by the day state: the
        // prefix assertion above already proves it byte for byte, and this
        // names the failure if it ever stops holding.
        eq(key + ' the regime line keeps its own colour',
           out.indexOf(seen[key].slice(0, seen[key].indexOf('>') + 1)), 0);
        // Every state appends the SAME line: the day is a property of the
        // session, not of the regime it happens to sit in.
        if (tailSeen === null) tailSeen = tail;
        else eq(key + ' appends the same tail as every other state', tail, tailSeen);
    });
});
ok('a tail was captured for the report', tailSeen !== null && tailSeen.length > 0);
console.log('  appended tail (verbatim): ' + tailSeen);
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
// dayStateNote, held to the same standard as regimeBanner before it (TZ-14 D3):
// deterministic, non-mutating, and empty on every shape that has nothing to
// state. The empty cases are asserted as EXACTLY '' — a note that returned a
// space or a stray div would still be falsy at the call sites and would print
// an empty amber line on both surfaces.
{
    const SILENT = [
        ['absent day',      undefined],
        ['null day',        null],
        ['below quorum',    { median: null, n: 3, abnormal: false }],
        ['quiet day',       { median: 1.0, n: 25, abnormal: false }],
        ['loud but unmeasured', { median: null, n: 3, abnormal: true }]
    ];
    SILENT.forEach(function (c) {
        eq('dayStateNote is empty on a ' + c[0], P.dayStateNote(c[1]), '');
    });
    const day = Object.freeze({ median: 2.43, n: 25, abnormal: true });
    const before = JSON.stringify(day);
    const a = P.dayStateNote(day), b = P.dayStateNote(day);
    ok('dayStateNote speaks on a loud day', a.length > 0);
    eq('dayStateNote is deterministic', a, b);
    eq('dayStateNote does not mutate its day', JSON.stringify(day), before);
    // numRu is the ONE formatter (inv. 20): swap it and the sentence must move.
    // Proven by behaviour rather than by reading the source, the same way A1
    // proves dayRangeRatio routes through sigmaDay.
    const realNum = P.numRu;
    P.numRu = function (x, d) { return 'Z' + realNum(x, d); };
    const swapped = P.dayStateNote(day);
    P.numRu = realNum;
    ok('dayStateNote routes both numbers through numRu',
       swapped !== a && swapped.split('Z').length - 1 === 2, swapped);
    eq('numRu restored', P.dayStateNote(day), a);
    // numRu itself: two decimals for the threshold, one for the median, comma
    // in both. Two rounding helpers would eventually disagree; there is one.
    eq('numRu(1.39, 2)', P.numRu(1.39, 2), '1,39');
    eq('numRu(2.43, 1)', P.numRu(2.43, 1), '2,4');
    eq('numRu(2, 1)', P.numRu(2, 1), '2,0');
    eq('numRu(-0.25, 1)', P.numRu(-0.25, 1), '-0,3');
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

// ── H2. The SECOND contract: reg.day (TZ-14 D4, inv. 48) ───────────────────
// The same mechanism, one object over. listExhaustion reads fields off the ROW
// update() builds; regimeBanner reads fields off the REG update() hands it, and
// TZ-14 adds one to that object. The failure mode is identical to the one H
// exists to catch: every fixture in this file builds its own reg, so a revision
// in which update() forgot to write reg.day would leave the whole file green
// and the live banner permanently silent. Read both sides off the source and
// compare them, with one check per field read and the same mutation controls.
//
// The reg object is produced in TWO places and that is the contract: the object
// literal marketRegime returns, plus every `reg.<f> =` update() performs on it.
// Both are counted, or the field TZ-14 adds would look like a gap.
const REG_READERS = ['regimeBanner'];
function regFieldsRead(body) {
    const out = {};
    const re = /\breg\.([A-Za-z_$][\w$]*)(?:\.([A-Za-z_$][\w$]*))?/g;
    let m;
    while ((m = re.exec(body)) !== null) {
        out[m[1]] = true;
        if (m[2]) out[m[1] + '.' + m[2]] = true;
    }
    return Object.keys(out).sort();
}
function regFieldsWritten(source) {
    const out = {};
    const mr = cutFunction(source, 'marketRegime');
    if (mr === null) return null;
    const lit = /var\s+out\s*=\s*\{([\s\S]*?)\}/.exec(mr);
    if (lit) {
        const re = /([A-Za-z_$][\w$]*)\s*:/g;
        let m;
        while ((m = re.exec(lit[1])) !== null) out[m[1]] = true;
    }
    const re2 = /\bout\.([A-Za-z_$][\w$]*)\s*=(?!=)/g;
    let m2;
    while ((m2 = re2.exec(mr)) !== null) out[m2[1]] = true;
    const prod = cutFunction(source, PRODUCER);
    if (prod === null) return null;
    const re3 = /\breg\.([A-Za-z_$][\w$]*)\s*=(?!=)/g;
    let m3;
    while ((m3 = re3.exec(prod)) !== null) out[m3[1]] = true;
    return Object.keys(out).sort();
}
function regGaps(source) {
    const writes = regFieldsWritten(source);
    if (writes === null) return { error: 'the reg producers were not found' };
    const per = [];
    for (let r = 0; r < REG_READERS.length; r++) {
        const body = cutFunction(source, REG_READERS[r]);
        if (body === null) return { error: 'reader ' + REG_READERS[r] + ' not found' };
        const reads = regFieldsRead(body);
        const missing = reads.filter(function (f) {
            return writes.indexOf(f.split('.')[0]) < 0;
        });
        per.push({ reader: REG_READERS[r], reads: reads, missing: missing });
    }
    return { writes: writes, per: per };
}

const RW = regGaps(src);
ok('reg wiring extractor found both sides', !RW.error);
if (RW.error) {
    console.log('  FAIL ' + RW.error);
} else {
    ok('the reg producers write at least one field', RW.writes.length > 0);
    console.log('  marketRegime + ' + PRODUCER + '() write reg: ' + RW.writes.join(', '));
    for (let r = 0; r < RW.per.length; r++) {
        const p = RW.per[r];
        ok(p.reader + ' reads at least one reg field', p.reads.length > 0);
        console.log('  ' + p.reader + ' reads reg: ' + p.reads.join(', '));
        for (let f = 0; f < p.reads.length; f++) {
            const fld = p.reads[f];
            const root = fld.split('.')[0];
            ok(p.reader + ' reads reg.' + fld + ' -> reg.' + root + ' is written',
               RW.writes.indexOf(root) >= 0);
        }
        if (p.missing.length) {
            console.log('  FAIL ' + p.reader + ' reads reg fields nothing writes: '
                      + p.missing.join(', '));
        }
    }
    // The field this TZ adds, named. A generic gap check would pass on a source
    // that had dropped reg.day from BOTH sides at once.
    ok('regimeBanner reads reg.day', RW.per[0].reads.indexOf('day') >= 0,
       RW.per[0].reads.join(','));
    ok(PRODUCER + '() writes reg.day', RW.writes.indexOf('day') >= 0, RW.writes.join(','));
    // …and it is written from listExhaustion, not from a literal.
    ok(PRODUCER + '() writes reg.day from listExhaustion',
       /\breg\.day\s*=\s*listExhaustion\s*\(/.test(cutFunction(src, PRODUCER) || ''));
}

// Positive controls, the same three as section H: a deleted write, an added
// read, and a clean source that must stay silent.
{
    const realLog = console.log;

    const cutDay = src.replace('reg.day = listExhaustion(rows);', '');
    ok('the reg control copy differs from the source', cutDay !== src);
    console.log = function () {};
    const A2 = regGaps(cutDay);
    console.log = realLog;
    eq('deleting reg.day reports exactly [day]',
       A2.error ? 'ERR:' + A2.error : A2.per[0].missing.join(','), 'day');

    const addRead = src.replace('function regimeBanner(reg, isLong) {\n    var txt, col;',
                                'function regimeBanner(reg, isLong) {\n    var txt, col;\n    if (reg && reg.zzzNotWritten) { txt = 1; }');
    ok('the reg read-control copy differs from the source', addRead !== src);
    console.log = function () {};
    const B2 = regGaps(addRead);
    console.log = realLog;
    eq('adding a read of reg.zzzNotWritten reports exactly [zzzNotWritten]',
       B2.error ? 'ERR:' + B2.error : B2.per[0].missing.join(','), 'zzzNotWritten');

    eq('the real source reports no missing reg field',
       RW.error ? 'ERR:' + RW.error : RW.per[0].missing.join(','), '');
    console.log('  reg controls: deleted write named, added read named, clean source silent');
}
console.log('  compared: ' + N.wiring);

// ───────────────────────────────────────────────────────────────────────────
section = 'record';
console.log('=== I. The constant and the record it is pinned to (TZ-14 D1, inv. 46) ===');
// A production constant copied out of a calibration record is only as good as
// the record still saying what it said when it was audited. Both sides are read
// from disk HERE, at gate time, and compared as numbers. A missing, unreadable
// or line-less record is a FAILURE and never a skip: a gate that quietly passed
// when it could not find its evidence would be the exact defect inv. 22 and 42
// name.
const DECL_RE = /\bvar\s+DAY_RANGE_ABNORMAL\s*=\s*([0-9]+\.[0-9]+)\s*;/g;
{
    // 1. Exactly one declaration in the source, and it is a two-decimal literal.
    const decls = [];
    let m;
    DECL_RE.lastIndex = 0;
    while ((m = DECL_RE.exec(src)) !== null) decls.push(m[1]);
    eq('exactly one DAY_RANGE_ABNORMAL declaration in index.html', decls.length, 1);
    const literal = decls.length === 1 ? decls[0] : '';
    eq('the source literal carries two decimals',
       /^[0-9]+\.[0-9]{2}$/.test(literal), true);
    eq('the declared value reaches the runtime',
       P.DAY_RANGE_ABNORMAL, parseFloat(literal));
    eq('DAY_RANGE_ABNORMAL is a finite number at runtime',
       typeof P.DAY_RANGE_ABNORMAL === 'number' && isFinite(P.DAY_RANGE_ABNORMAL), true);

    // 2. The record. Read it, or fail naming the file.
    let record = null, readErr = null;
    try { record = fs.readFileSync(RECORD_PATH, 'utf8'); }
    catch (e) { readErr = (e && e.message) || String(e); }
    ok('the calibration record is readable: ' + RECORD_PATH,
       record !== null, readErr === null ? '' : readErr);
    if (record === null) {
        console.log('  FAIL calibration record missing or unreadable: '
                  + RECORD_PATH + (readErr ? ' — ' + readErr : ''));
    } else {
        const lines = record.split('\n').filter(function (l) {
            return /^\s*DAY_RANGE_ABNORMAL\s*=\s*[0-9.]+\s*$/.test(l);
        });
        eq('exactly one DAY_RANGE_ABNORMAL line in the record', lines.length, 1);
        if (lines.length !== 1) {
            console.log('  FAIL the record carries ' + lines.length
                      + ' DAY_RANGE_ABNORMAL lines, expected 1');
        } else {
            const recVal = parseFloat(lines[0].split('=')[1]);
            ok('the record value parses as a number', isFinite(recVal), lines[0]);
            eq('source constant equals the record value', P.DAY_RANGE_ABNORMAL, recVal);
            console.log('  index.html: ' + literal + '   '
                      + path.basename(RECORD_PATH) + ': ' + recVal.toFixed(2)
                      + '   equal: ' + (P.DAY_RANGE_ABNORMAL === recVal));
        }
    }
}
console.log('  compared: ' + N.record);

// ───────────────────────────────────────────────────────────────────────────
section = 'threshold';
console.log('=== J. The truth table of `abnormal` (TZ-14 D2) ===');
// The rule adopted is «at or above the calibrated p90», so the tie must land on
// TRUE. To state that as an assertion rather than a hope, the fixture has to
// produce a median EXACTLY equal to the constant — and rowFor cannot: the
// ratio grid steps over 1.39 and lands one ULP away on either side.
//
// The construction below removes the rounding instead of tolerating it. The
// production denominator is cur * sigmaDay(vol) * sqrt(8/pi); scan cur over
// ULPs until that product is exactly 1, then a row with lo = 0 has ratio
// hi - 0 = hi, exactly. Every ratio in the double grid becomes reachable, and
// the epsilons below are ONE ULP — the smallest ε that exists, so no operator
// with any slack at all can pass this table.
const F64 = new Float64Array(1);
const U32 = new Uint32Array(F64.buffer);
function ulp(x, dir) {
    F64[0] = x;
    let lo = U32[0], hi = U32[1];
    if (dir > 0) { lo = (lo + 1) >>> 0; if (lo === 0) hi = (hi + 1) >>> 0; }
    else { if (lo === 0) { hi = (hi - 1) >>> 0; lo = 0xFFFFFFFF; } else lo = (lo - 1) >>> 0; }
    U32[0] = lo; U32[1] = hi;
    return F64[0];
}
const TH = P.DAY_RANGE_ABNORMAL;
const T_VOL = 0.01;
const T_CUR = (function () {
    const K2 = Math.sqrt(8 / Math.PI);
    const start = 1 / (P.sigmaDay(T_VOL) * K2);
    for (let i = 0; i <= 4096; i++) {
        for (const dir of [1, -1]) {
            let c = start;
            for (let k = 0; k < i; k++) c = ulp(c, dir);
            if (c * P.sigmaDay(T_VOL) * K2 === 1) return c;
            if (i === 0) break;
        }
    }
    return null;
})();
ok('a fixture family with an exact denominator was found', T_CUR !== null);
// Inv. 22/23: the fixture is asserted to BE what it claims before anything is
// concluded from it. Without this, a family whose denominator drifted off 1
// would silently turn the whole table into a test of rowFor's rounding.
if (T_CUR !== null) {
    eq('the fixture denominator is exactly 1',
       T_CUR * P.sigmaDay(T_VOL) * Math.sqrt(8 / Math.PI), 1);
    eq('the fixture reproduces a requested ratio exactly',
       P.dayRangeRatio(TH, 0, T_CUR, T_VOL), TH);
}
function thRows(ratio, n) {
    const out = [];
    for (let i = 0; i < n; i++) {
        out.push({ t: { name: 'S' + i, s: 'S' + i + 'USDT' },
                   hi24: ratio, lo24: 0, cur: T_CUR, cd: { volatility: T_VOL } });
    }
    return out;
}
const TRUTH = [
    ['median at 1 ULP below the threshold', ulp(TH, -1), 9,  false, 'lt'],
    ['median exactly at the threshold',     TH,          9,  true,  'eq'],
    ['median at 1 ULP above the threshold', ulp(TH, +1), 9,  true,  'gt'],
    ['median null (below quorum, n = 7)',   2.0,         7,  false, 'null'],
    ['median null (empty list)',            2.0,         0,  false, 'null']
];
const TRUTH_ROWS = [];
TRUTH.forEach(function (c) {
    const rows = thRows(c[1], c[2]);
    const got = P.listExhaustion(rows);
    // First: the fixture really is the case it claims (inv. 23).
    if (c[4] === 'null') eq(c[0] + ': fixture median is null', got.median, null);
    else if (c[4] === 'lt') ok(c[0] + ': fixture median is strictly below', got.median < TH);
    else if (c[4] === 'eq') eq(c[0] + ': fixture median is exactly the constant', got.median, TH);
    else ok(c[0] + ': fixture median is strictly above', got.median > TH);
    // Then: the verdict.
    eq(c[0] + ' -> abnormal ' + c[3], got.abnormal, c[3]);
    eq(c[0] + ': n is the contributing count', got.n, c[2]);
    TRUTH_ROWS.push([c[0], got.median === null ? 'null' : String(got.median),
                     got.n, got.abnormal, c[3]]);
});
console.log('  --- truth table ---');
TRUTH_ROWS.forEach(function (r) {
    console.log('    ' + r[0] + '  median=' + r[1] + '  n=' + r[2]
              + '  abnormal=' + r[3] + '  (want ' + r[4] + ')');
});

// Negative control (inv. 22, 23). The comparison must read the CONSTANT, not a
// literal 1.39 that happens to equal it. Re-evaluate the WHOLE module body from
// a copy of the source with the declaration rewritten to 9.99, and require the
// same list — which is above 1.39 and below 9.99 — to flip to false. A
// hard-coded comparison would keep saying true and this control would fail.
{
    const mutated = src.replace(/\bvar\s+DAY_RANGE_ABNORMAL\s*=\s*[0-9.]+\s*;/,
                                'var DAY_RANGE_ABNORMAL = 9.99;');
    ok('the 9.99 control copy differs from the source', mutated !== src);
    const Q = loadProduction(mutated);
    eq('the control copy really carries 9.99', Q.DAY_RANGE_ABNORMAL, 9.99);
    // One list, two constants. Built for Q's own arithmetic so the fixture is
    // not smuggled across contexts.
    const ratio = 2.43;
    function qRows(n) {
        const out = [];
        for (let i = 0; i < n; i++) {
            const hi = 100 + ratio * (100 * Q.sigmaDay(0.01) * Math.sqrt(8 / Math.PI));
            out.push({ hi24: hi, lo24: 100, cur: 100, cd: { volatility: 0.01 } });
        }
        return out;
    }
    const rows = qRows(25);
    const under99 = Q.listExhaustion(rows);
    ok('the control list sits between the two constants',
       under99.median > TH && under99.median < 9.99, String(under99.median));
    eq('with the constant at 9.99 the same list is NOT abnormal', under99.abnormal, false);
    // …and the real source calls the same list abnormal, or the control above
    // would pass on a comparison that never fires at all.
    const rowsP = [];
    for (let i = 0; i < 25; i++) rowsP.push(rowFor(ratio));
    eq('with the real constant the same list IS abnormal',
       P.listExhaustion(rowsP).abnormal, true);
    // The sentence follows the constant too: dayStateNote prints 9,99 there.
    eq('dayStateNote in the control prints the control threshold',
       Q.dayStateNote({ median: 2.43, n: 25, abnormal: true })
        .indexOf(Q.numRu(9.99, 2)) > 0, true);
    console.log('  negative control: constant 9.99 -> median '
              + under99.median.toFixed(4) + ' abnormal=' + under99.abnormal
              + ' (real constant ' + TH + ' -> abnormal=true)');
}
console.log('  compared: ' + N.threshold);

// ───────────────────────────────────────────────────────────────────────────
section = 'live';
console.log('=== K. The live path: real update(), real render (TZ-14 D4, inv. 48) ===');
// Section H proves the CONTRACT off the source text. This proves the REACH:
// production's own update() is run over two fixture books whose list medians
// straddle the constant, the output is taken from the element the browser would
// paint, and the two renders are differenced. A bench that builds its own rows
// proves the function; only this proves that the field the banner reads is the
// field the render loop wrote.
//
// The two books differ by ONE ULP-scale nudge of highPrice — about 1.4e-11
// relative — chosen so that nothing a human or a toFixed can see has moved.
// Any byte of difference beyond the day line is therefore a real reach into
// something this TZ was not allowed to touch, not a rounding artefact.
function loadLive(source) {
    const CAPTURED = {};
    const CACHE = {};
    function recEl(id) {
        const e = { _id: id, style: {}, innerText: '', value: '', className: '',
            classList: { add: function () {}, remove: function () {} },
            addEventListener: function () {}, appendChild: function () {},
            setAttribute: function () {}, getAttribute: function () { return null; },
            oninput: null, onclick: null, onchange: null, checked: false,
            scrollIntoView: function () {}, focus: function () {}, blur: function () {},
            remove: function () {}, querySelector: function () { return recEl('q'); },
            querySelectorAll: function () { return []; },
            getElementsByClassName: function () { return []; },
            getBoundingClientRect: function () {
                return { top: 0, left: 0, width: 0, height: 0, bottom: 0, right: 0 }; },
            scrollTop: 0, scrollHeight: 0, offsetTop: 0, offsetHeight: 0,
            parentNode: null, children: [] };
        Object.defineProperty(e, 'innerHTML', {
            get: function () { return CAPTURED[id] || ''; },
            set: function (v) { CAPTURED[id] = String(v); }
        });
        return e;
    }
    const sb = {
        document: {
            getElementById: function (id) {
                if (!CACHE[id]) CACHE[id] = recEl(id);
                return CACHE[id];
            },
            addEventListener: function () {},
            querySelector: function () { return recEl('q'); },
            querySelectorAll: function () { return []; },
            createElement: function () { return recEl('new'); },
            body: recEl('body'), head: recEl('head')
        },
        localStorage: { getItem: function () { return null; },
                        setItem: function () {}, removeItem: function () {} },
        navigator: { userAgent: 'node' }, location: { href: '' },
        fetch: function () { const d = {}; d.then = function () { return d; };
                             d.catch = function () { return d; };
                             d.finally = function () { return d; }; return d; },
        setTimeout: function () { return 0; }, clearTimeout: function () {},
        setInterval: function () { return 0; }, clearInterval: function () {},
        requestAnimationFrame: function () { return 0; }, alert: function () {},
        console, Math, Date, JSON, parseFloat, parseInt, isFinite, isNaN
    };
    sb.window = sb;
    vm.createContext(sb);
    vm.runInContext(source, sb, { filename: 'index.html:<script> (live)' });
    // The real registry, loaded by the one mechanism already written for it —
    // no second loader and no XHR stub (the same injection prot_bench.js and
    // board2_bench.js perform). An empty registry would make this a render of a
    // configuration that is not production (inv. 22, 40).
    let cat;
    try { cat = require('../journal/write.js').loadCatalysts(); }
    catch (e) {
        console.log('FAIL catalyst registry: ' + ((e && e.message) || e));
        process.exit(1);
    }
    sb.CATALYSTS = cat.items; sb.CAT_LOADED = true; sb.CAT_ERR = null;
    sb.catUpdated = cat.updated;
    sb.__captured = CAPTURED;
    return sb;
}

// One book, built from the REAL token registry so the venue split is the live
// one: every spot token gets a ticker whose day range is exactly `ratio`
// typical days wide, and the three fut:true tokens are given a wild range that
// must not reach the measure at all.
function liveBook(L, ratio) {
    const VOL = 0.01, CUR = 100, LO = 100;
    const denom = CUR * L.sigmaDay(VOL) * Math.sqrt(8 / Math.PI);
    const HI = LO + ratio * denom;
    const market = [], fut = {}, analysis = [], funding = {};
    market.push({ symbol: 'BTCUSDT', lastPrice: '68000', priceChangePercent: '0.4',
                  quoteVolume: '900000000', highPrice: '68500', lowPrice: '67500',
                  count: '900000', bidPrice: '67999', askPrice: '68001' });
    for (let i = 0; i < L.tokens.length; i++) {
        const t = L.tokens[i];
        const wild = !!t.fut;
        const tick = {
            symbol: t.s, lastPrice: String(CUR), priceChangePercent: '1.5',
            quoteVolume: '90000000',
            highPrice: wild ? String(LO + 40 * denom) : String(HI),
            lowPrice: String(LO),
            count: '120000', bidPrice: '99.99', askPrice: '100.01'
        };
        if (wild) fut[t.s] = tick; else market.push(tick);
        funding[t.s] = 0.0001;
        analysis.push({
            symbol: t.name, error: false, volatility: VOL,
            min_price: 70, max_price: 140, min30: 80, max30: 130,
            corr_90: 0.7, up_beta: 1.1, down_beta: 1.2, up_r2: 0.4, down_r2: 0.45,
            up_beta_90: 1.05, down_beta_90: 1.15, up_r2_90: 0.42, down_r2_90: 0.44,
            r7: 0.02, r14: -0.03, r30: 0.05, vol7: 0.011, eff14: 0.3,
            vol_ratio: 1.0, rank: 30 + i, rank_prev: 30 + i, fdv_mc: 1.2,
            price_pos: 50
        });
    }
    return {
        botData: { generated_at: '2026-08-24T09:00:00Z',
                   btc: { min_price: 58244, max_price: 77847, volatility: 0.0102,
                          r7: 0.01, r14: 0.02, r30: 0.03 },
                   analysis_data: analysis },
        market: market, fut: fut, funding: funding
    };
}

function liveRender(L, book, side) {
    L.botData = book.botData;
    L.cachedMarketData = book.market;
    L.cachedFutTickers = book.fut;
    L.cachedFunding = book.funding;
    L.currentSide = side;
    L.currentStress = 'normal';
    L.currentLev = 3;
    L.showOff = false;
    L.boardSym = null;
    L.entryState = {};
    L.document.getElementById('slider').value = '69000';
    L.__captured['results'] = '';
    L.update();
    return { html: L.__captured['results'] || '',
             day: L.lastRegime ? L.lastRegime.day : undefined,
             rows: L.lastRows.length };
}

{
    const L = loadLive(src);
    ok('the live context evaluated production', typeof L.update === 'function');
    ok('the live context sees the real token registry',
       Array.isArray(L.tokens) && L.tokens.length > 20, String(L.tokens && L.tokens.length));

    // The straddle is relative 1e-9, not one ULP: the book travels through
    // String() and parseFloat() the way a ticker does, and a ratio rebuilt from
    // hi - lo over a recomputed denominator round-trips only to about one ULP.
    // 1e-9 is seven orders of magnitude above that noise and eleven below
    // anything a toFixed on this book can print, so the two renders differ in
    // the measure and in nothing a reader could see.
    const QUIET = TH * (1 - 1e-9), LOUD = TH * (1 + 1e-9);
    const rendered = {};
    [['long', true], ['short', false]].forEach(function (sideCase) {
        const side = sideCase[0];
        const a = liveRender(L, liveBook(L, QUIET), side);
        const b = liveRender(L, liveBook(L, LOUD), side);
        rendered[side] = { a: a, b: b };

        // 1. update() wrote reg.day, and it is the shape listExhaustion returns.
        ok(side + ': update() wrote reg.day', a.day !== undefined && a.day !== null);
        eq(side + ': reg.day has the measure shape',
           a.day ? Object.keys(a.day).sort().join(',') : '', 'abnormal,median,n');
        // 2. The two books really straddle the constant (inv. 23): without this
        //    the whole comparison below could be two identical quiet renders.
        ok(side + ': the quiet book is measured', a.day.median !== null);
        ok(side + ': the loud book is measured', b.day.median !== null);
        ok(side + ': the quiet median is strictly below the constant',
           a.day.median < TH, String(a.day.median));
        ok(side + ': the loud median is strictly above the constant',
           b.day.median > TH, String(b.day.median));
        eq(side + ': the quiet book is not abnormal', a.day.abnormal, false);
        eq(side + ': the loud book IS abnormal', b.day.abnormal, true);
        // 3. The venue rule survived the live path: the three fut tokens carry a
        //    40-sigma range and would have dragged the median if counted.
        eq(side + ': the measure counted the spot tokens only', a.day.n, b.day.n);
        eq(side + ': n equals the declared spot count', a.day.n,
           L.tokens.filter(function (t) { return !t.fut; }).length);
        // 4. The render reached the screen at all.
        ok(side + ': the quiet render produced a list', a.html.length > 1000);
        ok(side + ': the loud render produced a list', b.html.length > 1000);

        // 5. THE claim. The loud render is the quiet render plus exactly one
        //    day line, and nothing else moved.
        const line = P.regimeBanner({ known: true, mode: 'range', dir: 0, z: 0.1,
                                      day: b.day }, side === 'long')
                      .slice(P.regimeBanner({ known: true, mode: 'range', dir: 0, z: 0.1 },
                                            side === 'long').length);
        ok(side + ': a day line was derived for the differ', line.length > 0);
        eq(side + ': the quiet render carries no day line', a.html.indexOf(WORD), -1);
        eq(side + ': the loud render carries exactly one day line',
           b.html.split(line).length - 1, 1);
        eq(side + ': removing the day line reproduces the quiet render byte for byte',
           b.html.split(line).join(''), a.html);
        console.log('  ' + side + ': quiet median ' + a.day.median.toFixed(12)
                  + ' n=' + a.day.n + ' dayLine=' + (a.html.indexOf(WORD) >= 0)
                  + '  |  loud median ' + b.day.median.toFixed(12)
                  + ' n=' + b.day.n + ' dayLine=' + (b.html.indexOf(WORD) >= 0)
                  + '  |  rest identical: '
                  + (b.html.split(line).join('') === a.html));
    });

    // 6. The day state does not depend on the side the Boss selected: the same
    //    book must produce the same reg.day in LONG and in SHORT.
    eq('the day state is the same in LONG and SHORT',
       JSON.stringify(rendered.long.b.day), JSON.stringify(rendered.short.b.day));

    // 7. Side «none»: the banner is not rendered at all, so no day line either,
    //    and reg.day is still computed — it is unconditional by construction.
    {
        const c = liveRender(L, liveBook(L, LOUD), 'none');
        ok('side none still computes reg.day', c.day !== undefined && c.day !== null);
        eq('side none: reg.day is abnormal all the same', c.day.abnormal, true);
        eq('side none prints no day line', c.html.indexOf(WORD), -1);
    }
}
console.log('  compared: ' + N.live);

// ───────────────────────────────────────────────────────────────────────────
section = 'surfaces';
console.log('=== L. One sentence, both surfaces (TZ-14 D5, inv. 33) ===');
// Inv. 33 names the defect: the card list and the board are two surfaces of the
// same verdict, and a board silent about what the list said is the same bug as
// a list silent about what the board said. The sentence is compared as a
// STRING between the two renders, not as a pair of substrings that merely look
// alike.
{
    const L = loadLive(src);
    const book = liveBook(L, TH * (1 + 1e-9));
    const listRes = liveRender(L, book, 'long');
    ok('the list render is abnormal', listRes.day && listRes.day.abnormal === true);
    const sentence = L.dayStateNote(listRes.day);
    ok('a sentence exists to compare', sentence.length > 0);

    // Surface 1 — the card list, through the banner.
    ok('the card list carries the sentence', listRes.html.indexOf(sentence) > 0);
    eq('the card list carries it exactly once',
       listRes.html.split(sentence).length - 1, 1);

    // Surface 2 — the board, through «РИСК ВЫНОСА», rendered by production's
    // own renderBoard over the same lastRows the list just produced.
    L.boardSide = 'long';
    L.boardSym = L.lastShownSyms[0];
    L.__captured['board'] = '';
    L.renderBoard();
    const boardHtml = L.__captured['board'] || '';
    ok('the board rendered', boardHtml.length > 500, String(boardHtml.length));
    ok('the board carries the sentence', boardHtml.indexOf(sentence) > 0);
    eq('the board carries it exactly once', boardHtml.split(sentence).length - 1, 1);
    eq('the two surfaces print the IDENTICAL sentence',
       boardHtml.slice(boardHtml.indexOf(sentence), boardHtml.indexOf(sentence) + sentence.length),
       listRes.html.slice(listRes.html.indexOf(sentence), listRes.html.indexOf(sentence) + sentence.length));
    // §3.7 / inv. 19: the sentence rides in a bd-kv, and the section keeps its
    // metal ring — an inline style on the .bd-sec would kill it.
    const SQZ_H = '\u0420\u0418\u0421\u041a \u0412\u042b\u041d\u041e\u0421\u0410';   // РИСК ВЫНОСА
    const at = boardHtml.indexOf(SQZ_H);
    ok('the board carries the squeeze-risk block', at > 0);
    const secStart = boardHtml.lastIndexOf('<div class="bd-sec', at);
    eq('no inline style on the squeeze-risk .bd-sec',
       boardHtml.substring(secStart, at).indexOf('style='), -1);
    ok('the sentence sits inside the squeeze-risk block',
       boardHtml.indexOf(sentence) > at);
    // The caption is unchanged and still follows the sentence.
    const CAPT = '1,0 \u2014 \u043e\u0431\u044b\u0447\u043d\u044b\u0439 \u0434\u0435\u043d\u044c';   // 1,0 - obychnyy den
    ok('the caption survives and follows the sentence',
       boardHtml.indexOf(CAPT) > boardHtml.indexOf(sentence));
    // A quiet day must silence BOTH surfaces, or «both print it» is vacuous.
    {
        const quiet = liveRender(L, liveBook(L, TH * (1 - 1e-9)), 'long');
        eq('a quiet day silences the card list', quiet.html.indexOf(WORD), -1);
        L.boardSym = L.lastShownSyms[0];
        L.__captured['board'] = '';
        L.renderBoard();
        eq('a quiet day silences the board', (L.__captured['board'] || '').indexOf(WORD), -1);
    }
    console.log('  sentence: ' + sentence);
}

// D5's second claim: the identifier occurs in exactly three enclosing sites in
// index.html — the declaration, listExhaustion, dayStateNote — using the brace
// matcher section H already carries. A fourth site would be a second place
// where the threshold is spent, which is what inv. 20 exists to prevent.
//
// Counted over CODE, not over prose: the same state machine cutFunction uses to
// tell a string from a comment strips the comments first, so a doc comment that
// explains the constant is not mistaken for a place that reads it.
function stripComments(source) {
    let out = '';
    let inS = null, inLine = false, inBlock = false, inRe = false, esc = false, prev = '';
    for (let i = 0; i < source.length; i++) {
        const c = source[i];
        if (inLine) { if (c === '\n') { inLine = false; out += c; } continue; }
        if (inBlock) { if (c === '*' && source[i + 1] === '/') { inBlock = false; i++; } continue; }
        if (inS) { out += c;
                   if (esc) { esc = false; } else if (c === '\\') { esc = true; }
                   else if (c === inS) { inS = null; prev = c; } continue; }
        if (inRe) { out += c;
                    if (esc) { esc = false; } else if (c === '\\') { esc = true; }
                    else if (c === '/') { inRe = false; prev = c; } continue; }
        if (c === '/' && source[i + 1] === '/') { inLine = true; i++; continue; }
        if (c === '/' && source[i + 1] === '*') { inBlock = true; i++; continue; }
        if (c === '"' || c === "'" || c === '`') { inS = c; prev = c; out += c; continue; }
        if (c === '/') {
            out += c;
            if (/[\w$)\]'"`]/.test(prev)) { prev = c; continue; }   // division
            inRe = true; continue;
        }
        out += c;
        if (!/\s/.test(c)) prev = c;
    }
    return out;
}
{
    const code = stripComments(src);
    ok('the comment stripper kept the code', code.indexOf('function listExhaustion(') > 0);
    ok('the comment stripper removed the prose',
       code.indexOf('The ONE site that compares against') < 0);
    const total = (code.match(/\bDAY_RANGE_ABNORMAL\b/g) || []).length;
    const decls = (code.match(/\bvar\s+DAY_RANGE_ABNORMAL\s*=/g) || []).length;
    eq('exactly one declaration', decls, 1);

    const SITES = ['listExhaustion', 'dayStateNote'];
    let inFunctions = 0;
    const per = [];
    SITES.forEach(function (fn) {
        const body = cutFunction(code, fn);
        ok(fn + ' is cut from the stripped source', body !== null);
        const c = body === null ? 0 : (body.match(/\bDAY_RANGE_ABNORMAL\b/g) || []).length;
        eq(fn + ' names DAY_RANGE_ABNORMAL exactly once', c, 1);
        inFunctions += c;
        per.push(fn + '=' + c);
    });
    eq('three enclosing sites in total, and no fourth', decls + inFunctions, total);
    eq('the total is three', total, 3);
    // The comparison itself lives in listExhaustion and nowhere else.
    const cmp = (cutFunction(code, 'listExhaustion') || '')
                 .match(/>=\s*DAY_RANGE_ABNORMAL/g) || [];
    eq('listExhaustion carries the one >= comparison', cmp.length, 1);
    eq('and it is >=, never >',
       /[^>=]>\s*DAY_RANGE_ABNORMAL/.test(cutFunction(code, 'listExhaustion') || ''), false);
    const noteBody = cutFunction(code, 'dayStateNote') || '';
    eq('dayStateNote compares nothing against the constant',
       /[<>]=?\s*DAY_RANGE_ABNORMAL|DAY_RANGE_ABNORMAL\s*[<>]=?/.test(noteBody), false);
    // Nobody else may compare against it either: every other top-level function
    // is cut and required to be silent about the constant.
    const OTHERS = ['regimeBanner', 'boardHtml', 'update', 'scoreCandidate',
                    'tradeGeometry', 'leverageDecision', 'directionVerdict',
                    'liqPrice', 'tierBadge', 'byScore', 'assignRanks', 'planLine',
                    'marketRegime', 'numRu'];
    OTHERS.forEach(function (fn) {
        const body = cutFunction(code, fn);
        ok(fn + ' is cut from the stripped source', body !== null);
        eq(fn + ' never names DAY_RANGE_ABNORMAL',
           body === null ? -1 : (body.match(/\bDAY_RANGE_ABNORMAL\b/g) || []).length, 0);
    });
    console.log('  DAY_RANGE_ABNORMAL code sites: declaration=' + decls
              + ', ' + per.join(', ') + '  total=' + total
              + '  (comments included: '
              + ((src.match(/\bDAY_RANGE_ABNORMAL\b/g) || []).length) + ')');
}
console.log('  compared: ' + N.surfaces);

// ───────────────────────────────────────────────────────────────────────────
section = 'caption';
console.log('=== M. The caption denies nothing the block does (TZ-15, inv. 50) ===');
// Invariant 50 — a stated absence is a dependency of the thing it denies.
// TZ-14 gave the squeeze-risk block a threshold and an amber day line, and the
// block's own caption went on saying «poroga net, sravneniya net» two lines
// under it. Nothing in the gate could see the contradiction: a bench compares
// BEHAVIOUR against a specification, and that was a claim ABOUT one.
//
// This section is the missing instrument, and it is deliberately narrow
// (TZ-15 §3, non-goal 9). It reads ONE block, located exactly as section L
// locates it, and scans only for denials of a mechanism THIS block has. A
// phrase blacklist over the whole file is a different and much worse
// instrument: it fires on the many absences that are still true — §3.11's
// scratch probability legitimately has no threshold — and a control that
// cries wolf is removed within two TZs.
//
// No second render path is written: loadLive / liveBook / liveRender /
// renderBoard are section L's, reused by name (inv. 48).

const SQZ_HEAD  = '\u0420\u0418\u0421\u041a \u0412\u042b\u041d\u041e\u0421\u0410';   // RISK VYNOSA
const NOTE_OPEN = '<div class="bd-note">';
const CAPT_HEAD = '1,0 \u2014 \u043e\u0431\u044b\u0447\u043d\u044b\u0439 \u0434\u0435\u043d\u044c';   // 1,0 - obychnyy den

// The three clauses M2 requires the caption to keep: the derived unit, the
// words that place the measure under inv. 27, and the coverage of the list.
const UNIT  = '\u221a(8/\u03c0)';   // sqrt(8/pi)
const INV27 = '\u043d\u0430 \u0441\u0447\u0451\u0442, \u043f\u043b\u0435\u0447\u043e \u0438 \u0432\u0435\u0440\u0434\u0438\u043a\u0442';   // na schyot, plecho i verdikt
const COVER = '25 \u0441\u043f\u043e\u0442\u043e\u0432\u044b\u043c \u043c\u043e\u043d\u0435\u0442\u0430\u043c';   // 25 spotovym monetam

// The sentence TZ-15 §2 A1 specifies, character for character. This is the
// EXPECTATION, written here from the TZ — never lifted out of index.html, or
// the comparison would be the production string against itself.
const CAPTION =
      '1,0 \u2014 \u043e\u0431\u044b\u0447\u043d\u044b\u0439 \u0434\u0435\u043d\u044c: \u0443 \u0431\u0440\u043e\u0443\u043d\u043e\u0432\u0441\u043a\u043e\u0433\u043e \u0431\u043b\u0443\u0436\u0434\u0430\u043d\u0438\u044f E[\u0445\u043e\u0434\u0430] = \u03c3\u00b7\u221a(8/\u03c0), \u043f\u043e\u044d\u0442\u043e\u043c\u0443 \u0435\u0434\u0438\u043d\u0438\u0446\u0430 \u0437\u0434\u0435\u0441\u044c \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d\u0430, \u0430 \u0432\u044b\u0432\u0435\u0434\u0435\u043d\u0430. '
    + '\u041f\u043e\u0440\u043e\u0433, \u0432\u044b\u0448\u0435 \u043a\u043e\u0442\u043e\u0440\u043e\u0433\u043e \u0434\u0435\u043d\u044c \u043d\u0430\u0437\u0432\u0430\u043d \u0432\u044b\u043d\u0435\u0441\u0435\u043d\u043d\u044b\u043c, \u2014 90-\u0439 \u043f\u0440\u043e\u0446\u0435\u043d\u0442\u0438\u043b\u044c \u043c\u0435\u0434\u0438\u0430\u043d\u044b \u0441\u043f\u0438\u0441\u043a\u0430 \u043f\u043e \u0442\u0440\u0451\u0445\u043b\u0435\u0442\u043d\u0435\u043c\u0443 \u0430\u0440\u0445\u0438\u0432\u0443; \u044d\u0442\u043e \u043c\u0435\u0440\u0430 \u0434\u043d\u044f, \u0430 \u043d\u0435 \u0437\u0430\u043f\u0440\u0435\u0442: \u043d\u0430 \u0441\u0447\u0451\u0442, \u043f\u043b\u0435\u0447\u043e \u0438 \u0432\u0435\u0440\u0434\u0438\u043a\u0442 \u043e\u043d\u0430 \u043d\u0435 \u0432\u043b\u0438\u044f\u0435\u0442. '
    + '\u0421\u043f\u0438\u0441\u043e\u043a \u0441\u0447\u0438\u0442\u0430\u0435\u0442\u0441\u044f \u043f\u043e 25 \u0441\u043f\u043e\u0442\u043e\u0432\u044b\u043c \u043c\u043e\u043d\u0435\u0442\u0430\u043c: \u0442\u0440\u0438 \u0444\u044c\u044e\u0447\u0435\u0440\u0441\u043d\u044b\u0435 \u0432 \u043c\u0435\u0440\u0443 \u043d\u0435 \u0432\u0445\u043e\u0434\u044f\u0442.';

// origin/main's caption, carried so M4 can put it back. It is the defect this
// section exists to catch: two denials of a threshold the block now has.
const CAPTION_MAIN =
      '1,0 \u2014 \u043e\u0431\u044b\u0447\u043d\u044b\u0439 \u0434\u0435\u043d\u044c: \u0443 \u0431\u0440\u043e\u0443\u043d\u043e\u0432\u0441\u043a\u043e\u0433\u043e \u0431\u043b\u0443\u0436\u0434\u0430\u043d\u0438\u044f E[\u0445\u043e\u0434\u0430] = \u03c3\u00b7\u221a(8/\u03c0), \u043f\u043e\u044d\u0442\u043e\u043c\u0443 \u0435\u0434\u0438\u043d\u0438\u0446\u0430 \u0437\u0434\u0435\u0441\u044c \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d\u0430, \u0430 \u0432\u044b\u0432\u0435\u0434\u0435\u043d\u0430. '
    + '\u0427\u0438\u0441\u043b\u043e \u043f\u0435\u0447\u0430\u0442\u0430\u0435\u0442\u0441\u044f \u043a\u0430\u043a \u0435\u0441\u0442\u044c \u2014 \u043f\u043e\u0440\u043e\u0433\u0430 \u043d\u0435\u0442, \u0441\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u044f \u043d\u0435\u0442, \u043d\u0430 \u0441\u0447\u0451\u0442, \u043f\u043b\u0435\u0447\u043e \u0438 \u0432\u0435\u0440\u0434\u0438\u043a\u0442 \u043e\u043d\u043e \u043d\u0435 \u0432\u043b\u0438\u044f\u0435\u0442. '
    + '\u0421\u043f\u0438\u0441\u043e\u043a \u0441\u0447\u0438\u0442\u0430\u0435\u0442\u0441\u044f \u043f\u043e 25 \u0441\u043f\u043e\u0442\u043e\u0432\u044b\u043c \u043c\u043e\u043d\u0435\u0442\u0430\u043c: \u0442\u0440\u0438 \u0444\u044c\u044e\u0447\u0435\u0440\u0441\u043d\u044b\u0435 \u0432 \u043c\u0435\u0440\u0443 \u043d\u0435 \u0432\u0445\u043e\u0434\u044f\u0442.';

// The six ways this block could deny its own threshold. Compared lower-cased,
// each one separately, so a failure names WHICH denial came back.
const DENIALS = [
    '\u043f\u043e\u0440\u043e\u0433\u0430 \u043d\u0435\u0442',   // poroga net
    '\u0441\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u044f \u043d\u0435\u0442',   // sravneniya net
    '\u043d\u0435\u0442 \u043f\u043e\u0440\u043e\u0433\u0430',   // net poroga
    '\u043d\u0435\u0442 \u0441\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u044f',   // net sravneniya
    '\u0431\u0435\u0437 \u043f\u043e\u0440\u043e\u0433\u0430',   // bez poroga
    '\u043d\u0435 \u0441\u0440\u0430\u0432\u043d\u0438\u0432\u0430\u0435\u0442',   // ne sravnivaet
];
const GLOSS = ['poroga net', 'sravneniya net', 'net poroga',
               'net sravneniya', 'bez poroga', 'ne sravnivaet'];

// index.html escapes every character above U+007F, so a runtime string must be
// re-encoded before it can be found in — or substituted into — the SOURCE.
// The round-trip is asserted in M4 rather than assumed: if this encoder and the
// file's convention ever disagreed, the control would substitute nothing, the
// scan would stay silent, and a broken control would report success.
function toSourceEscapes(s) {
    let out = '';
    for (let i = 0; i < s.length; i++) {
        const c = s.charCodeAt(i);
        out += c > 0x7f ? '\\u' + ('0000' + c.toString(16)).slice(-4) : s.charAt(i);
    }
    return out;
}

// The block, located exactly as section L locates it: forward to the header,
// back to the .bd-sec that opens it, then forward to the NEXT .bd-sec — the
// sections are flat siblings — or to the end of the board.
function sqzBlock(board) {
    const at = board.indexOf(SQZ_HEAD);
    if (at < 0) return null;
    const start = board.lastIndexOf('<div class="bd-sec', at);
    if (start < 0) return null;
    let end = board.indexOf('<div class="bd-sec', at);
    if (end < 0) end = board.length;
    return board.slice(start, end);
}

// The caption is the bd-note that opens with the unit line. The block carries a
// second bd-note above it (the liquidation-touch note), so «the last note» and
// «the first note» are both wrong answers.
function captionOf(block) {
    const a = block.indexOf(NOTE_OPEN + CAPT_HEAD);
    if (a < 0) return null;
    const b = block.indexOf('</div>', a);
    if (b < 0) return null;
    return block.slice(a + NOTE_OPEN.length, b);
}

// PURE — no counter is touched here. M1 and M4 point this same instrument at
// two different sources and assert OPPOSITE outcomes; a scan that counted its
// own hits would turn the control's success into a recorded failure. The
// counting happens at the assertion sites below, where the comparison is
// (inv. 43).
function scanDenials(block) {
    const low = String(block).toLowerCase();
    const hit = [];
    for (let i = 0; i < DENIALS.length; i++) {
        if (low.indexOf(DENIALS[i]) >= 0) hit.push(GLOSS[i]);
    }
    return hit;
}

// One render, one board, one block, through production's own update() and
// renderBoard() — the same sequence section L performs.
function boardBlock(L, ratio) {
    const res = liveRender(L, liveBook(L, ratio), 'long');
    L.boardSide = 'long';
    L.boardSym = L.lastShownSyms[0];
    L.__captured['board'] = '';
    L.renderBoard();
    const board = L.__captured['board'] || '';
    return { board: board, block: sqzBlock(board), day: res.day };
}

{
    const L = loadLive(src);
    const QUIET_R = TH * (1 - 1e-9), LOUD_R = TH * (1 + 1e-9);
    const quiet = boardBlock(L, QUIET_R);
    const loud  = boardBlock(L, LOUD_R);
    const RENDERS = [['quiet', quiet], ['loud', loud]];
    eq('the quiet render is NOT abnormal', quiet.day && quiet.day.abnormal, false);
    eq('the loud render IS abnormal', loud.day && loud.day.abnormal, true);

    // ── M5 first. Everything below is a statement ABOUT a block, so the block
    // is established before it is scanned (inv. 22). A scan that had silently
    // widened to the whole board would fire on absences that are still true,
    // and would look exactly like a pass until it did.
    RENDERS.forEach(function (r) {
        const tag = r[0], b = r[1], blk = b.block;
        ok('M5 ' + tag + ': the board rendered', b.board.length > 500);
        ok('M5 ' + tag + ': the block was located', blk !== null);
        ok('M5 ' + tag + ': the block is non-empty', blk !== null && blk.length > 0);
        ok('M5 ' + tag + ': the block is PART of the board, not the board',
           blk !== null && blk.length < b.board.length);
        eq('M5 ' + tag + ': the block opens exactly one .bd-sec',
           blk === null ? -1 : blk.split('<div class="bd-sec').length - 1, 1);
        eq('M5 ' + tag + ': the block carries exactly one header',
           blk === null ? -1 : blk.split('<div class="bd-h').length - 1, 1);
        eq('M5 ' + tag + ': and that one header is the squeeze-risk header',
           blk === null ? -1 : blk.indexOf('<div class="bd-h">' + SQZ_HEAD),
           blk === null ? -2 : blk.indexOf('<div class="bd-h'));
        ok('M5 ' + tag + ': the board carries sections this scan did NOT read',
           b.board.split('<div class="bd-sec').length - 1 > 1);
    });

    // ── M1. The block carries no denial. Six phrases, each compared and counted
    // separately, on each of the two renders. The number of comparisons is
    // itself asserted, so an emptied list cannot pass as a clean scan.
    let compared = 0;
    RENDERS.forEach(function (r) {
        const tag = r[0], low = String(r[1].block).toLowerCase();
        DENIALS.forEach(function (p, i) {
            eq('M1 ' + tag + ': the block does not say "' + GLOSS[i] + '"',
               low.indexOf(p) >= 0, false);
            compared++;
        });
    });
    eq('M1 compared all six phrases on both renders', compared, DENIALS.length * 2);
    eq('M1 the denial set is the six the TZ names', DENIALS.length, 6);

    // ── M2. What the caption DOES say. The three clauses first, then the whole
    // sentence as ONE string comparison against the §2 A1 expectation.
    RENDERS.forEach(function (r) {
        const tag = r[0], cap = captionOf(String(r[1].block));
        ok('M2 ' + tag + ': the caption was located', cap !== null);
        ok('M2 ' + tag + ': it carries the derived unit',
           cap !== null && cap.indexOf(UNIT) > 0);
        ok('M2 ' + tag + ': it carries the inv. 27 words',
           cap !== null && cap.indexOf(INV27) > 0);
        ok('M2 ' + tag + ': it carries the coverage clause',
           cap !== null && cap.indexOf(COVER) > 0);
        eq('M2 ' + tag + ': the caption IS the sentence TZ-15 s2 A1 specifies',
           cap, CAPTION);
        eq('M2 ' + tag + ': the board prints the caption exactly once',
           r[1].board.split(NOTE_OPEN + CAPT_HEAD).length - 1, 1);
        eq('M2 ' + tag + ': and the block prints it exactly once',
           String(r[1].block).split(NOTE_OPEN + CAPT_HEAD).length - 1, 1);
    });
    console.log('  caption: ' + captionOf(String(loud.block)));

    // ── M3. Inv. 20: the constant keeps three code sites, and a literal in a
    // static caption would be a fourth in a form no re-calibration could reach.
    // The value is read THROUGH the live context; nothing here is a literal.
    const NUM = L.numRu(L.DAY_RANGE_ABNORMAL, 2);
    ok('M3 the threshold string came from the live context',
       typeof L.DAY_RANGE_ABNORMAL === 'number' && NUM.length > 0);
    const loudSentence = L.dayStateNote(loud.day);
    ok('M3 the loud day has a day line at all', loudSentence.length > 0);
    ok('M3 the day line prints the threshold', loudSentence.indexOf(NUM) > 0);
    ok('M3 the loud block carries that day line', String(loud.block).indexOf(loudSentence) > 0);
    eq('M3 the loud caption does NOT repeat the number',
       captionOf(String(loud.block)).indexOf(NUM), -1);
    eq('M3 the quiet block does not carry the number at all',
       String(quiet.block).indexOf(NUM), -1);
    eq('M3 the quiet caption does not carry it either',
       captionOf(String(quiet.block)).indexOf(NUM), -1);

    // ── M4. The control, and the point of the section: a section that has
    // never failed on purpose is not yet a control. Same shape as G's planted
    // mismatch and J's 9.99 constant — the caption is rewritten back to its
    // origin/main text in a COPY of the source, the copy is evaluated in its
    // own context, and the SAME scan is required to fire and to name what it
    // found while the clean source stays silent.
    const capSrc  = toSourceEscapes(CAPTION);
    const mainSrc = toSourceEscapes(CAPTION_MAIN);
    ok('M4 the encoder round-trips against the file convention',
       src.indexOf(capSrc) > 0);
    eq('M4 the specified caption occurs once in the source',
       src.split(capSrc).length - 1, 1);
    eq('M4 origin/main\'s caption is gone from the source',
       src.indexOf(mainSrc), -1);
    const reverted = src.split(capSrc).join(mainSrc);
    ok('M4 the control copy differs from the source', reverted !== src);
    const Q = loadLive(reverted);
    const ctl = boardBlock(Q, LOUD_R);
    ok('M4 the control copy rendered the block',
       ctl.block !== null && ctl.block.length > 0);
    eq('M4 the control copy really carries the reverted caption',
       captionOf(String(ctl.block)), CAPTION_MAIN);
    const fired = scanDenials(ctl.block);
    ok('M4 the scan FIRES on the reverted caption', fired.length > 0);
    eq('M4 and it names both denials origin/main carried', fired.length, 2);
    eq('M4 the first is the threshold denial', fired[0], GLOSS[0]);
    eq('M4 the second is the comparison denial', fired[1], GLOSS[1]);
    const silent = scanDenials(loud.block).concat(scanDenials(quiet.block));
    eq('M4 and the clean source is silent on both renders', silent.length, 0);
    console.log('  negative control: reverted caption -> scan fired, naming '
              + fired.length + ': ' + fired.join(' + ')
              + '   |   clean source -> ' + silent.length + ' phrases found');
}
console.log('  compared: ' + N.caption);

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
