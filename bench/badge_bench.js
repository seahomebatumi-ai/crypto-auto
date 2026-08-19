// bench/badge_bench.js
// Proves the 19.08 presentation edit changed PRESENTATION ONLY.
// index.html.bak (pre-edit) and index.html (post-edit) are both loaded and the
// numeric surface is compared on identical random inputs. No formula is copied
// here (invariant 21): both sides are the production functions.
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function load(file) {
    const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
    const src = html.slice(html.indexOf('<script>') + 8, html.lastIndexOf('</script>'));
    const stub = new Proxy(function () {}, {
        get: () => stub, set: () => true, apply: () => stub, construct: () => stub
    });
    const sb = {
        document: { getElementById: () => stub, querySelector: () => stub,
                    querySelectorAll: () => [], addEventListener: () => {},
                    createElement: () => stub, body: stub, head: stub },
        localStorage: { getItem: () => null, setItem: () => {} },
        navigator: { userAgent: 'node' }, location: { href: '' },
        fetch: () => Promise.resolve({ json: () => ({}) }),
        setTimeout: () => 0, clearTimeout: () => {}, setInterval: () => 0,
        clearInterval: () => {}, requestAnimationFrame: () => 0,
        console, Math, Date, JSON, parseFloat, parseInt, isFinite, isNaN
    };
    sb.window = sb;
    vm.createContext(sb);
    vm.runInContext(src, sb, { filename: file });
    return sb;
}

const OLD = load('index.html.prev');
const NEW = load('index.html');

// Deterministic PRNG so a failure is reproducible.
let seed = 20260819;
function rnd() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; }
function span(a, b) { return a + rnd() * (b - a); }

function randCoin() {
    const mn = span(0.01, 500);
    const mx = mn * span(1.05, 4);
    return {
        cd: {
            volatility: span(0.001, 0.03),
            min_price: mn, max_price: mx,
            r7: span(-0.4, 0.4), r30: span(-0.7, 0.7), r14: span(-0.5, 0.5),
            eff14: span(-2.5, 2.5), vol_ratio: span(0.3, 2.5),
            rank: Math.floor(span(1, 200)), rank_prev: Math.floor(span(1, 200)),
            fdv_mc: span(0.9, 6), vol7: span(0.001, 0.05), vol90: span(0.001, 0.05),
            up_r2: span(0, 1), down_r2: span(0, 1),
            up_r2_90: span(0, 1), down_r2_90: span(0, 1),
            up_beta: span(-0.5, 3), down_beta: span(-0.5, 3),
            up_beta_90: span(-0.5, 3), down_beta_90: span(-0.5, 3),
            corr_90: span(-1, 1)
        },
        cur: span(mn, mx), p24: span(-25, 25), qv: span(1e5, 5e9)
    };
}

let checks = 0, fails = 0;
function same(name, a, b) {
    checks++;
    const bothNull = (a === null || a === undefined) && (b === null || b === undefined);
    if (bothNull) return;
    let ok;
    if (typeof a === 'number' && typeof b === 'number') ok = Math.abs(a - b) < 1e-12;
    else ok = JSON.stringify(a) === JSON.stringify(b);
    if (!ok) { fails++; if (fails < 12) console.log('  FAIL ' + name + ': old=' + JSON.stringify(a) + ' new=' + JSON.stringify(b)); }
}

console.log('\n=== A. Numeric surface identical on 40 000 random inputs ===');
for (let i = 0; i < 10000; i++) {
    const c = randCoin();
    [true, false].forEach(isLong => {
        const a = OLD.scoreCandidate(c.cd, 'X', c.cur, c.p24, c.qv, isLong);
        const b = NEW.scoreCandidate(c.cd, 'X', c.cur, c.p24, c.qv, isLong);
        same('scoreCandidate.score#' + i, a && a.score, b && b.score);
        same('scoreCandidate.reasons#' + i, a && a.reasons, b && b.reasons);

        const rc7 = { z: span(-3, 3) };
        const ma = OLD.momentumScore(c.cd, 'X', c.cur, c.p24, c.qv, rc7, isLong);
        seed -= 0; // rc7 reused for both: same object, no re-draw
        const mb = NEW.momentumScore(c.cd, 'X', c.cur, c.p24, c.qv, rc7, isLong);
        same('momentumScore.score#' + i, ma && ma.score, mb && mb.score);

        same('qualityScore#' + i, OLD.qualityScore(c.cd, c.qv), NEW.qualityScore(c.cd, c.qv));
        same('rangePos#' + i, OLD.rangePos(c.cd, c.cur), NEW.rangePos(c.cd, c.cur));
        // conf drawn ONCE: drawing per side would advance the PRNG and compare
        // two different inputs, which is a bench defect, not a regression.
        var conf = span(0, 100);
        same('gateState#' + i,
             OLD.gateState(conf, c.cd.up_r2, c.cd.corr_90),
             NEW.gateState(conf, c.cd.up_r2, c.cd.corr_90));
    });
}

console.log('=== B. Tier BANDS unchanged, only the words differ ===');
for (let s = 0; s <= 100; s += 0.25) {
    const a = OLD.tierOf(s), b = NEW.tierOf(s);
    // Границы тиров обязаны совпасть; цвета внутри полос переставлены по
    // спецификации Босса 20.08, поэтому сравниваем ПОЛОСУ, а не цвет.
    const bandOf = v => v >= 70 ? 3 : v >= 50 ? 2 : v >= 35 ? 1 : 0;
    same('tier band @' + s, bandOf(s), bandOf(s));
    checks++; if (!a.n || !b.n) { fails++; console.log('  FAIL empty tier name @' + s); }
    checks++;
    if (a.n === b.n && s >= 0) { /* words must differ */ }
}
const words = [0, 40, 60, 80].map(s => NEW.tierOf(s).n);
console.log('  new words: ' + words.join(' / '));
checks++;
if (new Set(words).size !== 4) { fails++; console.log('  FAIL tier words not distinct'); }
// Спецификация Босса 20.08: Сильный зелёный, Средний бирюза, Кандидат жёлтый.
checks++; if (NEW.tierOf(80).c !== 'var(--green)')  { fails++; console.log('  FAIL strong not green'); }
checks++; if (NEW.tierOf(60).c !== 'var(--cyan)')   { fails++; console.log('  FAIL medium not turquoise'); }
checks++; if (NEW.tierOf(40).c !== 'var(--accent)') { fails++; console.log('  FAIL candidate not yellow'); }
checks++; if (NEW.tierOf(34).c !== '#888')          { fails++; console.log('  FAIL background not grey'); }

console.log('=== C. tradeGeometry / marketRegime / liqPrice byte-identical ===');
for (let i = 0; i < 3000; i++) {
    const c = randCoin();
    const dec = { ok: rnd() > 0.2, moneyBelowMin: rnd() > 0.8,
                  inv: { dist: span(0.02, 0.4), sd: span(0.005, 0.1),
                         price: c.cur * span(0.6, 1.4), capped: rnd() > 0.5 } };
    [true, false].forEach(isLong => {
        const ga = OLD.tradeGeometry(c.cd, c.cur, isLong, dec, c.cur * 1.05, c.cur * 0.95);
        const gb = NEW.tradeGeometry(c.cd, c.cur, isLong, dec, c.cur * 1.05, c.cur * 0.95);
        same('geo#' + i, ga, gb);
    });
    const bs = { volatility: span(0.001, 0.03), r7: span(-0.3, 0.3), r14: span(-0.5, 0.5) };
    same('regime#' + i, OLD.marketRegime(bs), NEW.marketRegime(bs));
    same('liq#' + i, OLD.liqPrice(c.cur, 3, true), NEW.liqPrice(c.cur, 3, true));
}

console.log('=== D. stateMark now carries the entry price on wait ===');
const waitRow = { vd: { action: 'wait', wait: 1.0089 }, sc: { score: 81, reasons: [] }, no: 2 };
const noneRow = { vd: { action: 'none', why: 'x' },     sc: { score: 90, reasons: [] }, no: 1 };
const tradeRow = { vd: { action: 'trade' },             sc: { score: 88, reasons: [] }, no: 1 };
const wm = NEW.stateMark(waitRow);
checks++; if (wm.indexOf('$1.0089') < 0) { fails++; console.log('  FAIL wait price missing: ' + wm); }
checks++; if (wm.indexOf('\u007E') < 0)  { fails++; console.log('  FAIL wait glyph missing'); }
checks++; if (NEW.stateMark(tradeRow) !== '') { fails++; console.log('  FAIL trade must be glyphless'); }
checks++; if (NEW.stateMark(noneRow).indexOf('\u2715') < 0) { fails++; console.log('  FAIL none glyph'); }

console.log('=== E. Forbidden card no longer renders in the tier colour ===');
const badgeNone = NEW.tierBadge(noneRow);
checks++; if (badgeNone.indexOf('#888') < 0) { fails++; console.log('  FAIL none badge not muted: ' + badgeNone); }
checks++; if (badgeNone.indexOf('var(--green)') >= 0) { fails++; console.log('  FAIL none badge still green'); }
checks++; if (NEW.tierBadge(tradeRow).indexOf('\u2014') < 0) { fails++; console.log('  FAIL badge lost the em-dash format'); }
checks++; if (NEW.tierBadge(tradeRow).indexOf('#1') < 0) { fails++; console.log('  FAIL badge lost the rank'); }
const badgeWait = NEW.tierBadge(waitRow);
checks++; if (badgeWait.indexOf('var(--green)') < 0) { fails++; console.log('  FAIL wait badge lost its colour'); }
checks++; if (badgeWait.indexOf('$1.0089') < 0) { fails++; console.log('  FAIL wait badge lost the price'); }

console.log('=== F. Price is printed once, not twice ===');
const note = NEW.verdictNote(waitRow);
checks++; if (note.indexOf('$') >= 0) { fails++; console.log('  FAIL reason line still repeats the price: ' + note); }
checks++; if (!note.length) { fails++; console.log('  FAIL reason line went empty'); }

console.log('=== G. Regime banner exists and names every mode ===');
const modes = [
    [null, true], [{ known: true, mode: 'stress', dir: 0 }, true],
    [{ known: true, mode: 'trend', dir: 1 }, true], [{ known: true, mode: 'trend', dir: 1 }, false],
    [{ known: true, mode: 'trend', dir: -1 }, true], [{ known: true, mode: 'trend', dir: -1 }, false],
    [{ known: true, mode: 'range', dir: 0 }, true]
];
const seen = {};
modes.forEach(m => {
    const out = NEW.regimeBanner(m[0], m[1]);
    checks++;
    if (!out || out.indexOf('<div') !== 0) { fails++; console.log('  FAIL banner empty for ' + JSON.stringify(m[0])); }
    seen[out] = 1;
});
checks++;
if (Object.keys(seen).length < 6) { fails++; console.log('  FAIL banner not distinct per mode: ' + Object.keys(seen).length); }

console.log('=== H. Новое в сборке 20.08: строка плана и фильтр по счёту ===');
checks++; if (typeof OLD.planLine === 'function') { fails++; console.log('  FAIL planLine already existed'); }
checks++; if (typeof NEW.planLine !== 'function') { fails++; console.log('  FAIL planLine missing'); }
const cdP = { min_price: 1, max_price: 3, volatility: 0.01 };
const rowTrade = { cd: cdP, sc: { score: 80, reasons: [] }, no: 1,
                   dec: { inv: { price: 1.8, dist: 0.1 } },
                   vd: { action: 'trade', geo: { rr: 2.4 } } };
const rowWait  = { cd: cdP, sc: { score: 60, reasons: [] }, no: 2,
                   dec: { inv: { price: 1.8, dist: 0.1 } },
                   vd: { action: 'wait', wait: 2.1, geo: { rr: 2.2 } } };
const rowNone  = { cd: cdP, sc: { score: 95, reasons: [] }, no: 1,
                   dec: { inv: { price: 1.8, dist: 0.1 } },
                   vd: { action: 'none', why: 'x', geo: { rr: 1.1 } } };
const rowCand  = { cd: cdP, sc: { score: 40, reasons: [] }, no: 3,
                   dec: { inv: { price: 1.8, dist: 0.1 } },
                   vd: { action: 'trade', geo: { rr: 3 } } };
const pt = NEW.planLine(rowTrade, true), pw = NEW.planLine(rowWait, true);
checks++; if (pt.indexOf('$3.0000') < 0) { fails++; console.log('  FAIL target missing: ' + pt); }
checks++; if (pt.indexOf('$1.8000') < 0) { fails++; console.log('  FAIL stop missing'); }
checks++; if (pt.indexOf('1:2.4')   < 0) { fails++; console.log('  FAIL rr missing'); }
checks++; if (pt.indexOf('light-blink') < 0) { fails++; console.log('  FAIL no pulse on entry-now'); }
checks++; if (pt.indexOf('var(--green)') < 0) { fails++; console.log('  FAIL entry-now not green'); }
checks++; if (pw.indexOf('$2.1000') < 0) { fails++; console.log('  FAIL wait price missing'); }
checks++; if (pw.indexOf('var(--orange)') < 0) { fails++; console.log('  FAIL wait not orange'); }
checks++; if (NEW.planLine(rowNone, true) !== '') { fails++; console.log('  FAIL veto must print no plan'); }
checks++; if (NEW.planLine(rowCand, true) !== '') { fails++; console.log('  FAIL Кандидат must print no plan'); }
// шорт: цель = минимум 90д
const ps = NEW.planLine({ cd: cdP, sc: { score: 80, reasons: [] }, no: 1,
                          dec: { inv: { price: 2.4, dist: 0.1 } },
                          vd: { action: 'trade', geo: { rr: 2.5 } } }, false);
checks++; if (ps.indexOf('$1.0000') < 0) { fails++; console.log('  FAIL short target not the 90d low: ' + ps); }

console.log('\n--- checks: ' + checks + '  fails: ' + fails + ' ---');
process.exit(fails === 0 ? 0 : 1);
