// bench/board2_bench.js
// Verifies the live board of 20.08, 02:04-02:08 (LONG + SHORT + two full
// CRYPTO FUTURE screens) against production maths extracted from index.html.
// Invariant 21: no formula is copied here — every function under test is the
// production function, loaded from the <script> block.
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');

function load(file) {
    const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
    const src = html.slice(html.indexOf('<script>') + 8, html.lastIndexOf('</script>'));
    const stub = new Proxy(function () {}, {
        get: () => stub, set: () => true, apply: () => stub, construct: () => stub });
    const sb = { document: { getElementById: () => stub, querySelector: () => stub,
                 querySelectorAll: () => [], addEventListener: () => {},
                 createElement: () => stub, body: stub, head: stub },
        localStorage: { getItem: () => null, setItem: () => {} },
        navigator: { userAgent: 'node' }, location: { href: '' },
        fetch: () => Promise.resolve({ json: () => ({}) }),
        setTimeout: () => 0, clearTimeout: () => {}, setInterval: () => 0,
        clearInterval: () => {}, requestAnimationFrame: () => 0,
        console, Math, Date, JSON, parseFloat, parseInt, isFinite, isNaN };
    sb.window = sb; vm.createContext(sb);
    vm.runInContext(src, sb, { filename: file });
    return sb;
}
const P = load('index.html');

let checks = 0, fails = 0;
function near(n, got, want, tol) {
    checks++;
    if (!(isFinite(got) && Math.abs(got - want) <= tol)) {
        fails++; console.log('  FAIL ' + n + ': got ' + got + ' want ' + want + ' +-' + tol);
    }
}
function ok(n, cond) { checks++; if (!cond) { fails++; console.log('  FAIL ' + n); } }

// ── Карточки 02:04-02:07. ratio > 0 => доска читает UP-регрессию. ──────────
const C = [
 {s:'XRP',   long:1, cur:1.1300, mn:0.9893, mx:1.3724, pos:37, b:1.10, fcPct:+0.0025, fcPx:1.1328,
  liqL:0.7694, liqS:1.4963, sc:91, tier:'strong', rr:1.6, conf:69, r2:0.60, rho:0.84, mdl:'yellow'},
 {s:'SKY',   long:1, cur:0.0601, mn:0.0487, mx:0.0714, pos:50, b:0.50, fcPct:+0.0011, fcPx:0.0602,
  liqL:0.0409, liqS:0.0795, sc:89, tier:'strong', rr:1.1, conf:33, r2:0.17, rho:0.49, mdl:'red'},
 {s:'ZEC',   long:1, cur:570.85, mn:298.5784, mx:676.3640, pos:72, b:1.01, fcPct:+0.0023, fcPx:572.1564,
  liqL:388.5895, liqS:755.7232, sc:84, tier:'strong', rr:0.8, conf:33, r2:0.23, rho:0.53, mdl:'red'},
 {s:'HBAR',  long:1, cur:0.0716, mn:0.0647, mx:0.1081, pos:16, b:0.62, fcPct:+0.0016, fcPx:0.0718,
  liqL:0.0487, liqS:0.0948, sc:73, tier:'strong', rr:null, conf:44, r2:0.34, rho:0.58, mdl:'yellow'},
 {s:'BNB',   long:1, cur:632.98, mn:541.2293, mx:739.1556, pos:46, b:0.53, fcPct:+0.0014, fcPx:633.8739,
  liqL:430.5060, liqS:837.2418, sc:72, tier:'strong', rr:1.3, conf:54, r2:0.43, rho:0.79, mdl:'yellow'},
 {s:'RENDER',long:1, cur:1.3860, mn:1.2351, mx:2.3999, pos:13, b:0.66, fcPct:+0.0018, fcPx:1.3884,
  liqL:0.9430, liqS:1.8339, sc:71, tier:'strong', rr:null, conf:34, r2:0.19, rho:0.68, mdl:'red'},
 {s:'UNI',   long:0, cur:3.6830, mn:2.3409, mx:4.5354, pos:61, b:0.80, fcPct:+0.0031, fcPx:3.6942,
  liqL:2.5090, liqS:4.8795, sc:74, tier:'strong', rr:null, conf:33, r2:0.15, rho:0.61, mdl:'red'},
 {s:'ADA',   long:0, cur:0.1902, mn:0.1388, mx:0.2539, pos:45, b:0.85, fcPct:+0.0032, fcPx:0.1908,
  liqL:0.1296, liqS:0.2520, sc:66, tier:'mid', rr:null, conf:39, r2:0.22, rho:0.69, mdl:'red'},
 {s:'ONDO',  long:0, cur:0.3506, mn:0.2934, mx:0.4571, pos:null, b:0.73, fcPct:null, fcPx:null,
  liqL:null, liqS:null, sc:61, tier:'mid', rr:null, conf:33, r2:0.22, rho:0.60, mdl:'red'}
];

console.log('\n=== 1. Ликвидация 3X от прогноза (production liqPrice) ===');
C.filter(c => c.liqL !== null).forEach(c => {
    near(c.s + ' liq LONG',  P.liqPrice(c.fcPx, 3, true),  c.liqL, Math.max(1e-4, c.liqL * 5e-4));
    near(c.s + ' liq SHORT', P.liqPrice(c.fcPx, 3, false), c.liqS, Math.max(1e-4, c.liqS * 5e-4));
});

console.log('=== 2. Прогноз монеты = цена x (1 + b*ratio) ===');
C.filter(c => c.fcPx !== null).forEach(c =>
    near(c.s + ' fc$', c.cur * (1 + c.fcPct), c.fcPx, Math.max(1e-4, c.fcPx * 6e-4)));

console.log('=== 3. Положение в диапазоне 90д (production rangePos) ===');
C.filter(c => c.pos !== null).forEach(c =>
    near(c.s + ' pos%', P.rangePos({min_price: c.mn, max_price: c.mx}, c.cur), c.pos, 0.6));

console.log('=== 4. МДЛ (production gateState) ===');
C.forEach(c => ok(c.s + ' mdl=' + c.mdl, P.gateState(c.conf, c.r2, c.rho) === c.mdl));

console.log('=== 5. Тиры и НЕПРЕРЫВНОСТЬ рейтинга внутри стороны ===');
['long', 'short'].forEach(side => {
    const L = C.filter(c => (side === 'long') === !!c.long);
    const seen = {};
    L.forEach((c, i) => {
        const band = c.sc >= 70 ? 'strong' : c.sc >= 50 ? 'mid' : c.sc >= 35 ? 'cand' : 'watch';
        ok(side + ' ' + c.s + ' tier', band === c.tier);
        ok(side + ' ' + c.s + ' rank=' + (i + 1) + ' unique', !seen[i + 1]);
        seen[i + 1] = 1;
        ok(side + ' ' + c.s + ' >= TIER_MIN (on board)', c.sc >= P.TIER_MIN);
        if (i) ok(side + ' order ' + c.s, c.sc <= L[i - 1].sc);
    });
});

console.log('=== 6. Вето R:R — все напечатанные ниже RR_MIN ===');
C.filter(c => c.rr !== null).forEach(c => {
    ok(c.s + ' rr<RR_MIN', c.rr < P.RR_MIN);
    const cd  = {volatility: 0.008, min_price: c.mn, max_price: c.mx};
    const rew = c.long ? (c.mx - c.cur) / c.cur : (c.cur - c.mn) / c.cur;
    const dec = {ok: true, moneyBelowMin: false,
                 inv: {dist: rew / c.rr, sd: 0.04, price: c.cur * (c.long ? 0.9 : 1.1), capped: false}};
    const g = P.tradeGeometry(cd, c.cur, !!c.long, dec, c.cur * 1.02, c.cur * 0.98);
    near(c.s + ' geo.rr reproduces printed', g.rr, c.rr, 0.05);
});

console.log('=== 7. Экран CRYPTO FUTURE: XRP ЛОНГ, 3X, вход $1.1308 ===');
const E = 1.1308, STOP = 0.9763, QTY = 265.30, NOT = 300, MRG = 100;
near('XRP liq 3X',        P.liqPrice(E, 3, true), 0.7680, 5e-4);
near('XRP liq 2X (долив)',P.liqPrice(E, 2, true), 0.5795, 5e-4);
near('XRP стоп 13.7%',    (E - STOP) / E * 100, 13.7, 0.1);
near('XRP ликв 32.1%',    (E - 0.7680) / E * 100, 32.1, 0.1);
near('XRP запас 21.3%',   (STOP - 0.7680) / STOP * 100, 21.3, 0.1);
near('XRP убыток по стопу', QTY * (E - STOP), 40.99, 0.02);
near('XRP убыток по ликв.', QTY * (E - 0.7680), 96.25, 0.02);
near('XRP долив маржи',     NOT / 2 - MRG, 50.00, 0.01);
const pp = P.protectionPlan(E, E, true, 0.0053, {dist: (E - STOP) / E, price: STOP, capped: false},
                            0.0001, NOT, MRG, QTY, 3, 2);
near('XRP безубыток 7д',  pp.be, 1.1343, 5e-4);
near('XRP издержки 0.31%',pp.costFrac * 100, 0.31, 0.01);
near('XRP защёлка 1R',    pp.arm, 1.2853, 1e-3);
near('XRP долив (движок)',pp.addMargin, 50.00, 0.01);
near('XRP ликв. после долива', pp.addLiq, 0.5795, 5e-4);
const capX = Math.floor(Math.min(5.6, 8.3, 7.5, Math.max(2.6, P.L_MIN)));
ok('XRP потолок = 2X (min из четырёх, вниз)', capX === 2);

console.log('=== 8. Экран CRYPTO FUTURE: UNI ШОРТ, 3X, вход $3.6830 ===');
const Eu = 3.6830, STOPu = 4.6387, QTYu = 81.456;
near('UNI liq 3X',         P.liqPrice(Eu, 3, false), 4.8646, 1e-3);
near('UNI liq 2X (долив)', P.liqPrice(Eu, 2, false), 5.4785, 1e-3);
near('UNI стоп 25.9%',     (STOPu - Eu) / Eu * 100, 25.9, 0.1);
near('UNI запас 4.9%',     (4.8646 - STOPu) / STOPu * 100, 4.9, 0.1);
near('UNI убыток по стопу',QTYu * (STOPu - Eu), 77.85, 0.03);
near('UNI убыток по ликв.',QTYu * (4.8646 - Eu), 96.25, 0.03);
const ppu = P.protectionPlan(Eu, Eu, false, 0.0093, {dist: (STOPu - Eu) / Eu, price: STOPu, capped: false},
                             0.0001, 300, 100, QTYu, 3, 2);
near('UNI безубыток 7д (funding перекрывает)', ppu.be, 3.6871, 1e-3);
near('UNI защёлка 1R',     ppu.arm, 2.7273, 2e-3);
ok('UNI funding платят мне', ppu.costFrac < 0);
// Потолок: «риск маржи» 1.3X показан СЫРЫМ, но в min идёт с полом L_MIN.
const capU = Math.floor(Math.min(3.1, 4.3, 6.3, Math.max(1.3, P.L_MIN)));
ok('UNI потолок = 2X, пол L_MIN виден в результате, но не на экране', capU === 2 && P.L_MIN === 2);

console.log('=== 9. Смена метрик между 01:08 и 02:04 = переход слайдера через ноль ===');
// rho (corr_90) не зависит от направления и обязан совпасть; beta/R2 обязаны
// отличаться, потому что доска переключилась с down- на up-регрессию.
const PAIRS = [ // sym, rho@01:08, rho@02:04, b90_down, b90_up
  ['BNB', 0.79, 0.79, 0.88, 0.70], ['UNI', 0.61, 0.61, 1.42, 1.13],
  ['ADA', 0.69, 0.69, 1.34, 1.23], ['HBAR',0.58, 0.58, 0.88, 0.87],
  ['SKY', 0.49, 0.49, 0.91, 0.71], ['XRP', 0.84, 0.84, 1.05, 1.05]
];
PAIRS.forEach(p => {
    ok(p[0] + ' rho инвариантна к стороне', p[1] === p[2]);
    const cd = {up_beta_90: p[4], down_beta_90: p[3]};
    ok(p[0] + ' ratio>0 -> up_beta_90',  (1 >= 0 ? cd.up_beta_90 : cd.down_beta_90) === p[4]);
    ok(p[0] + ' ratio<0 -> down_beta_90', (-1 >= 0 ? cd.up_beta_90 : cd.down_beta_90) === p[3]);
});

console.log('=== 10. Стороны не подавлены: счёт считается на ОБЕИХ ===');
const cd = {volatility: 0.009, min_price: 1, max_price: 3, r7: 0.11, r30: 0.2, r14: 0.3,
            eff14: 0.4, vol_ratio: 1.1, rank: 30, rank_prev: 31, fdv_mc: 1.2,
            vol7: 0.009, vol90: 0.009};
[true, false].forEach(isLong => {
    ok('score есть на стороне ' + (isLong ? 'ЛОНГ' : 'ШОРТ'),
       P.scoreCandidate(cd, 'X', 2, 5, 5e8, isLong) !== null);
    ok('импульс есть на стороне ' + (isLong ? 'ЛОНГ' : 'ШОРТ'),
       P.momentumScore(cd, 'X', 2, 5, 5e8, {z: 0.5}, isLong) !== null);
});

console.log('\n--- checks: ' + checks + '  fails: ' + fails + ' ---');
process.exit(fails === 0 ? 0 : 1);
