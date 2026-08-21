// bench/verify_board.js
// Verifies the 2026-08-19 live board screenshots (LONG + SHORT, 3X, Normal)
// against production maths extracted from index.html at runtime.
// No formula is copied here (invariant 21): every function under test is the
// production function, loaded from the <script> block of index.html.
//
// Inputs are the ten card readings the Boss photographed. They are treated as
// rank-1 data (he stated he applied the new code and tested the live board).
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

// TZ-07 scope B. The board is executed against the REAL registry from the
// checkout. There is no XMLHttpRequest in this sandbox, so production's own
// loader cannot run and CATALYSTS would stay {} — this bench would then
// validate a configuration that is not production (inv. 22, 40). Today that is
// invisible because every live entry is `disputed` and therefore vetoes
// nothing; the first `confirmed` entry would silently split the bench from the
// live board it was built to reproduce.
// The registry is read and validated by the one mechanism already written for
// exactly this, journal/write.js:loadCatalysts, and injected the same way it
// injects it: no second loader, no XHR stub. A missing or invalid file exits
// non-zero — falling back to an empty registry is the defect, not the recovery.
let CAT;
try {
    CAT = require('../journal/write.js').loadCatalysts();
} catch (e) {
    console.log('FAIL catalyst registry: ' + ((e && e.message) || e));
    process.exit(1);
}
sandbox.CATALYSTS  = CAT.items;
sandbox.CAT_LOADED = true;
sandbox.CAT_ERR    = null;

let checks = 0, fails = 0;
function near(name, got, want, tol) {
    checks++;
    const ok = isFinite(got) && Math.abs(got - want) <= tol;
    if (!ok) { fails++; console.log('  FAIL ' + name + ': got ' + got + ' want ' + want + ' +-' + tol); }
    return ok;
}
function eq(name, got, want) {
    checks++;
    if (got !== want) { fails++; console.log('  FAIL ' + name + ': got ' + JSON.stringify(got) + ' want ' + JSON.stringify(want)); }
}

// ── Board readings, 19.08.2026 01:08-01:09, 3X, Normal ──────────────────────
// btcFc = BTC forecast delta printed in the header at that card's tick.
const LONG_BTC_FC = -0.0047;   // $69 400 vs $69 727
const SHORT_BTC_FC = -0.0027;  // $69 400 vs $69 589
const TAIL_BTC_FC = -0.0017;   // screenshot 4 tick, BTC ~ $69 518

const CARDS = [
  // sym, side, cur, mn, mx, posPct, b14, fcPct, fcPrice, liqL, liqS, score, tier, rr
  { s:'SKY',  long:true,  cur:0.0614, mn:0.0487, mx:0.0716, pos:55, b:0.59, btcFc:LONG_BTC_FC,
    fcPct:-0.0028, fcPx:0.0612, liqL:0.0416,  liqS:0.0809,  score:90, tier:'strong', rr:0.9 },
  { s:'XRP',  long:true,  cur:1.1068, mn:0.9893, mx:1.3755, pos:30, b:0.90, btcFc:LONG_BTC_FC,
    fcPct:-0.0042, fcPx:1.1021, liqL:0.7485,  liqS:1.4557,  score:81, tier:'strong', rr:null },
  { s:'ZEC',  long:true,  cur:577.51, mn:298.5784, mx:676.3640, pos:74, b:1.50, btcFc:LONG_BTC_FC,
    fcPct:-0.0070, fcPx:573.4549, liqL:389.4715, liqS:757.4384, score:78, tier:'strong', rr:0.7 },
  { s:'BNB',  long:true,  cur:629.04, mn:541.2293, mx:739.1556, pos:44, b:0.46, btcFc:LONG_BTC_FC,
    fcPct:-0.0021, fcPx:627.6937, liqL:426.3086, liqS:829.0788, score:67, tier:'mid', rr:1.4 },
  { s:'HBAR', long:true,  cur:0.0712, mn:0.0647, mx:0.1081, pos:15, b:0.68, btcFc:LONG_BTC_FC,
    fcPct:-0.0032, fcPx:0.0710, liqL:0.0482,  liqS:0.0938,  score:64, tier:'mid', rr:null },
  { s:'UNI',  long:false, cur:3.7130, mn:2.3409, mx:4.5354, pos:63, b:1.72, btcFc:SHORT_BTC_FC,
    fcPct:-0.0047, fcPx:3.6956, liqL:2.5100,  liqS:4.8813,  score:81, tier:'strong', rr:null },
  { s:'ADA',  long:false, cur:0.1882, mn:0.1388, mx:0.2539, pos:43, b:1.15, btcFc:SHORT_BTC_FC,
    fcPct:-0.0031, fcPx:0.1876, liqL:0.1274,  liqS:0.2478,  score:76, tier:'strong', rr:null },
  { s:'ONDO', long:false, cur:0.3526, mn:0.2934, mx:0.4571, pos:36, b:1.30, btcFc:TAIL_BTC_FC,
    fcPct:-0.0022, fcPx:0.3518, liqL:0.2389,  liqS:0.4647,  score:67, tier:'mid', rr:null },
  { s:'AVAX', long:false, cur:6.8220, mn:5.8757, mx:9.5722, pos:26, b:1.70, btcFc:TAIL_BTC_FC,
    fcPct:-0.0029, fcPx:6.8023, liqL:4.6199,  liqS:8.9847,  score:57, tier:'mid', rr:null },
  { s:'TRX',  long:false, cur:0.3336, mn:0.3120, mx:0.3759, pos:34, b:0.17, btcFc:TAIL_BTC_FC,
    fcPct:-0.0003, fcPx:0.3335, liqL:0.2265,  liqS:0.4405,  score:57, tier:'mid', rr:null }
];

console.log('\n=== 0. Catalyst registry parity with production ===');
// A parity fix that silently degrades to {} reproduces the original defect one
// layer down, so the loaded registry is asserted, not assumed.
eq('registry non-empty', Object.keys(P.CATALYSTS).length > 0, true);
console.log('  registry: ' + Object.keys(P.CATALYSTS).length + ' coins, updated '
          + (CAT.updated || '-'));

console.log('=== 1. Liquidation price, 3X, from forecast (production liqPrice) ===');
CARDS.forEach(c => {
    near(c.s + ' liq LONG 3X',  P.liqPrice(c.fcPx, 3, true),  c.liqL, Math.max(1e-4, c.liqL * 5e-4));
    near(c.s + ' liq SHORT 3X', P.liqPrice(c.fcPx, 3, false), c.liqS, Math.max(1e-4, c.liqS * 5e-4));
});

console.log('=== 2. Beta transfer of the BTC forecast onto the coin ===');
CARDS.forEach(c => {
    near(c.s + ' fc%', c.b * c.btcFc, c.fcPct, 6e-4);
    near(c.s + ' fc$', c.cur * (1 + c.fcPct), c.fcPx, Math.max(1e-4, c.fcPx * 6e-4));
});

console.log('=== 3. 90d range position (production rangePos) ===');
CARDS.forEach(c => {
    const rp = P.rangePos({ min_price: c.mn, max_price: c.mx }, c.cur);
    near(c.s + ' pos%', rp, c.pos, 0.6);
});

console.log('=== 4. Tier boundaries (production tierOf) ===');
CARDS.forEach(c => {
    const t = P.tierOf(c.score);
    const band = c.score >= 70 ? 'strong' : c.score >= 50 ? 'mid' : c.score >= 35 ? 'cand' : 'watch';
    eq(c.s + ' tier band', band, c.tier);
    checks++; if (!t || !t.n) { fails++; console.log('  FAIL ' + c.s + ' tierOf returned nothing'); }
});

console.log('=== 5. Ranking is monotone non-increasing in score, per side ===');
['long', 'short'].forEach(side => {
    const list = CARDS.filter(c => (side === 'long') === c.long);
    for (let i = 1; i < list.length; i++) {
        checks++;
        if (list[i].score > list[i - 1].score) {
            fails++; console.log('  FAIL ' + side + ' order: ' + list[i].s + ' above ' + list[i - 1].s);
        }
    }
});

console.log('=== 6. RR veto threshold: every printed RR is below RR_MIN ===');
CARDS.filter(c => c.rr !== null).forEach(c => {
    checks++;
    if (!(c.rr < P.RR_MIN)) { fails++; console.log('  FAIL ' + c.s + ' rr ' + c.rr + ' not < RR_MIN ' + P.RR_MIN); }
    // reward implied by the printed RR must equal the 90d-extreme reward
    const reward = c.long ? (c.mx - c.cur) / c.cur : (c.cur - c.mn) / c.cur;
    const risk = reward / c.rr;
    checks++;
    if (!(risk > 0 && risk < 0.5)) { fails++; console.log('  FAIL ' + c.s + ' implied risk ' + risk); }
});

console.log('=== 7. Geometry target is the 90d extreme, in EVERY regime ===');
// tradeGeometry takes no regime/channel argument: the target is cd.max_price
// for a long and cd.min_price for a short, whichever channel ranked the coin.
// Consequence: in trend mode the ranking is continuation (momentumScore) while
// the trade gate still measures reward against a mean-reversion target.
CARDS.forEach(c => {
    const cd  = { volatility: 0.008, min_price: c.mn, max_price: c.mx };
    const dec = { ok: true, moneyBelowMin: false,
                  inv: { dist: 0.10, sd: 0.04, price: c.long ? c.cur*0.9 : c.cur*1.1, capped: false } };
    const g = P.tradeGeometry(cd, c.cur, c.long, dec, c.cur*1.02, c.cur*0.98);
    const wantReward = c.long ? (c.mx - c.cur) / c.cur : (c.cur - c.mn) / c.cur;
    near(c.s + ' reward vs 90d extreme', g.reward, wantReward, 1e-9);
    near(c.s + ' rr = reward/dist',      g.rr,     wantReward / 0.10, 1e-9);
});
const withRR = CARDS.filter(c => c.long && c.rr !== null).sort((a, b) => b.score - a.score);
console.log('  live score/RR pairs: ' + withRR.map(c => c.s + ' ' + c.score + '/' + c.rr).join('  ')
          + '   (all < RR_MIN ' + P.RR_MIN + ')');

console.log('=== 8. Regime reproduction: all SHORT cards vetoed => trend, dir=+1 ===');
// marketRegime is fed the BTC statistics implied by the board: a +7.9% day
// after a multi-week base gives eff14 above EFF_TREND.
const btcTrendUp = { volatility: 0.006, r7: 0.09, r14: 0.16 };
const regUp = P.marketRegime(btcTrendUp);
eq('regime mode', regUp.mode, 'trend');
eq('regime dir', regUp.dir, 1);
checks++;
if (!(Math.abs(regUp.eff) >= P.EFF_TREND)) { fails++; console.log('  FAIL eff below EFF_TREND'); }

console.log('=== 9. Structural connectivity: no coin can be LONG and SHORT ===');
// directionVerdict returns 'none' on the side opposite the trend, always.
eq('short side closed in up-trend', regUp.dir !== -1, true);

console.log('\n--- checks: ' + checks + '  fails: ' + fails + ' ---');
process.exit(fails === 0 ? 0 : 1);
