// prot_bench.js — validation harness for the POSITION PROTECTION block.
// Invariant 21: zero copies of production math. Every formula under test is
// executed from the real index.html at run time; edits propagate automatically.
//
// Usage:  node bench/prot_bench.js [pathToIndexHtml] [pathToBaselineHtml]

var fs = require('fs');
var vm = require('vm');

function loadFront(file) {
    var html = fs.readFileSync(file, 'utf8');
    var m = html.match(/<script>([\s\S]*)<\/script>/);
    if (!m) throw new Error('no <script> in ' + file);
    var src = m[1];
    var a = src.indexOf('var REL_LOW');
    var b = src.indexOf("document.getElementById('slider').oninput");
    if (a < 0 || b < 0) throw new Error('anchors not found in ' + file);
    src = src.slice(a, b);
    var ctx = {
        console: console, Math: Math, Date: Date, JSON: JSON, Number: Number,
        String: String, Array: Array, Object: Object, isFinite: isFinite,
        parseFloat: parseFloat, parseInt: parseInt,
        setInterval: function () { return 0; }, clearInterval: function () {},
        setTimeout: function () { return 0; }, clearTimeout: function () {},
        document: {
            addEventListener: function () {},
            getElementById: function () { return null; },
            body: { style: {} }
        },
        localStorage: {
            getItem: function () { return null; },
            setItem: function () {}, removeItem: function () {}
        },
        fetch: function () { return { then: function () { return { catch: function () {} }; } }; },
        prompt: function () { return null; },
        alert: function () {}
    };
    ctx.globalThis = ctx;
    vm.createContext(ctx);
    vm.runInContext(src, ctx, { filename: file });
    // TZ-07 scope B. The board is executed against the REAL registry from the
    // checkout. There is no XMLHttpRequest in this sandbox, so production's own
    // loader cannot run and CATALYSTS would stay {} — this bench would then
    // validate a configuration that is not production (inv. 22, 40). Today that
    // is invisible because every live entry is `disputed` and therefore vetoes
    // nothing; the first `confirmed` entry would silently split the bench from
    // the live board it was built to reproduce.
    // The registry is read and validated by the one mechanism already written
    // for exactly this, journal/write.js:loadCatalysts, and injected the same
    // way it injects it: no second loader, no XHR stub. A missing or invalid
    // file exits non-zero — an empty registry is the defect, not the recovery.
    var cat;
    try {
        cat = require('../journal/write.js').loadCatalysts();
    } catch (e) {
        console.log('FAIL catalyst registry: ' + ((e && e.message) || e));
        process.exit(1);
    }
    ctx.CATALYSTS  = cat.items;
    ctx.CAT_LOADED = true;
    ctx.CAT_ERR    = null;
    ctx.catUpdated = cat.updated;
    return ctx;
}

// ── Test bookkeeping ────────────────────────────────────────────────────────
var pass = 0, fail = 0, notes = [];
function ok(name, cond, info) {
    if (cond) { pass++; }
    else { fail++; notes.push('FAIL: ' + name + (info ? '  [' + info + ']' : '')); }
}
function near(a, b, eps) { return Math.abs(a - b) <= (eps === undefined ? 1e-9 : eps); }

// ── Synthetic market fixtures ───────────────────────────────────────────────
function cdOf(o) {
    var base = {
        symbol: 'UNI', volatility: 0.01, min_price: 8, max_price: 14,
        min30: 9, max30: 13, corr_90: 0.7,
        up_beta: 1.1, down_beta: 1.2, up_r2: 0.4, down_r2: 0.45,
        up_beta_90: 1.05, down_beta_90: 1.15, up_r2_90: 0.42, down_r2_90: 0.44,
        r7: 0.02, r14: -0.03, r30: 0.05, vol7: 0.011, eff14: 0.3,
        rank: 30, fdv_mc: 1.2, error: false
    };
    for (var k in (o || {})) base[k] = o[k];
    return base;
}
function coinOf(price, o) {
    var base = {
        symbol: 'UNIUSDT', lastPrice: String(price), priceChangePercent: '1.5',
        quoteVolume: '90000000', count: '120000', bidPrice: String(price),
        askPrice: String(price)
    };
    for (var k in (o || {})) base[k] = o[k];
    return base;
}
// TZ-13 §2 Stage A. update() now parses lastPrice / highPrice / lowPrice ONCE,
// onto the row, and every consumer — boardHtml included — reads them from
// there. A fixture that builds a row must build the NEW row: the three values
// are taken from the SAME ticker object the fixture already carries, never
// from a new number, so no board here moves because of the contract change.
function rowRange(row) {
    row.cur  = parseFloat(row.coin.lastPrice);
    row.hi24 = parseFloat(row.coin.highPrice);
    row.lo24 = parseFloat(row.coin.lowPrice);
    return row;
}
function armCtx(ctx, opts) {
    opts = opts || {};
    ctx.boardSide = opts.side || 'long';
    ctx.currentSide = opts.side || 'long';
    ctx.currentLev = opts.lev || 4;
    ctx.sizeMode = opts.sizeMode || 'usdt';
    ctx.posMargin = opts.margin === undefined ? 1000 : opts.margin;
    ctx.posQty = opts.qty || 0;
    ctx.currentStress = 'normal';
    ctx.entryState = {};
    if (opts.entry) ctx.entryState.UNI = { price: opts.entry };
    ctx.cachedFunding = {};
    if (opts.fr !== undefined && opts.fr !== null) ctx.cachedFunding.UNIUSDT = opts.fr;
    ctx.botData = { analysis_data: [], btc: { volatility: 0.004, r7: 0.01, r14: 0.02, r30: 0.03,
                                              min_price: 90000, max_price: 130000 } };
    ctx.lastCtx = {
        isLong: (opts.side || 'long') === 'long',
        btcStats: ctx.botData.btc, ratio: 0.02, stressMult: 1.0,
        target: 102000, btc: 100000
    };
    ctx.lastShownSyms = ['UNI'];
    var row = rowRange({
        t: { name: 'UNI', s: 'UNIUSDT' }, idx: 0,
        coin: coinOf(opts.price === undefined ? 10 : opts.price),
        cd: cdOf(opts.cd || {}), state: 'ok', sc: null
    });
    ctx.lastRows = [row];
    return row;
}

// ── 1. Harness self-check: production board renders at all ──────────────────
function suiteRender(ctx, label) {
    var row = armCtx(ctx, { entry: 10, price: 10.4, fr: 0.0001 });
    var h = ctx.boardHtml(row, 0);
    ok(label + ': board renders', typeof h === 'string' && h.length > 3000, 'len=' + (h || '').length);
    return h;
}

// ── 2. touchProb refactor must be bit-identical to the old liqTouchProb ─────
function suiteTouchIdentity(nu, old) {
    if (!nu.touchProb) { notes.push('SKIP touch identity: no touchProb in candidate'); return; }
    var vols = [null, 0, 0.0001, 0.002, 0.005, 0.01, 0.02, 0.029, 0.05, 0.2, 1.5];
    var levs = [1, 1.01, 1.5, 2, 3, 4, 5, 7, 10, 25, 50, 80, 125];
    var hrs = [1, 12, 168, 336, 720, 4000];
    var n = 0, worst = 0;
    for (var i = 0; i < vols.length; i++)
        for (var j = 0; j < levs.length; j++)
            for (var k = 0; k < hrs.length; k++)
                for (var s = 0; s < 2; s++) {
                    var a = old.liqTouchProb(vols[i], levs[j], s === 0, hrs[k]);
                    var b = nu.liqTouchProb(vols[i], levs[j], s === 0, hrs[k]);
                    n++;
                    if (a === null || b === null) {
                        ok('touch identity null@' + i + j + k + s, a === b, a + ' vs ' + b);
                    } else {
                        var d = Math.abs(a - b);
                        if (d > worst) worst = d;
                        ok('touch identity val@' + i + j + k + s, d === 0, a + ' vs ' + b);
                    }
                }
    notes.push('touchProb identity: ' + n + ' cases, max |diff| = ' + worst);
}

// ── 3. protectionPlan — analytic checks ─────────────────────────────────────
function suitePlan(ctx) {
    var P = ctx.protectionPlan;
    if (!P) { notes.push('SKIP plan suite: no protectionPlan'); return; }
    var FEE = ctx.FEE_TAKER, PAY = ctx.FUND_PAY_7D, ARM = ctx.ARM_R;
    ok('constants exist', typeof FEE === 'number' && typeof PAY === 'number' && typeof ARM === 'number');

    var inv = { dist: 0.10, price: 9.0, capped: false, floored: false, src: 'мин30', sd: 0.049, ref: 9.0 };
    var vol = 0.01, E = 10, notional = 4000, mrg = 1000, qty = 400;

    // 3.1 Long, no funding data: break-even = entry + round-trip fee
    var p = P(E, 10, true, vol, inv, null, notional, mrg, qty, 4, 4);
    ok('long BE fee-only', near(p.be, E * (1 + 2 * FEE), 1e-12), 'be=' + p.be);
    ok('long costFrac fee-only', near(p.costFrac, 2 * FEE, 1e-15));
    ok('funding unknown flagged', p.fundKnown === false);

    // 3.2 Short mirrors long exactly
    var ps = P(E, 10, false, vol, inv, null, notional, mrg, qty, 4, 4);
    ok('short BE mirrored', near(ps.be, E * (1 - 2 * FEE), 1e-12), 'be=' + ps.be);

    // 3.3 Funding paid by me (long, positive rate) pushes BE further away
    var fr = 0.0001;
    var pf = P(E, 10, true, vol, inv, fr, notional, mrg, qty, 4, 4);
    ok('long pays funding -> BE higher', pf.be > p.be);
    ok('long funding frac', near(pf.costFrac, 2 * FEE + fr * PAY, 1e-15), 'cf=' + pf.costFrac);
    ok('cost in usd', near(pf.costUsd, pf.costFrac * notional, 1e-12));

    // 3.4 Funding received (long, negative rate) pulls BE below entry
    var pr = P(E, 10, true, vol, inv, -0.001, notional, mrg, qty, 4, 4);
    ok('long receives funding -> BE below entry', pr.be < E, 'be=' + pr.be);
    ok('receiving flagged by sign', pr.costFrac < 0, 'cf=' + pr.costFrac);

    // 3.5 Short with positive rate receives funding
    var prs = P(E, 10, false, vol, inv, 0.001, notional, mrg, qty, 4, 4);
    ok('short receives on positive rate', prs.costFrac < 0 && prs.be > E, 'be=' + prs.be);

    // 3.6 Arm price = entry ± ARM_R·dist, never closer than break-even
    ok('arm price long', near(pf.arm, E * (1 + ARM * inv.dist), 1e-12), 'arm=' + pf.arm);
    ok('arm price short', near(ps.arm, E * (1 - ARM * inv.dist), 1e-12), 'arm=' + ps.arm);
    ok('arm not pushed', pf.armAtBe === false);
    var pbig = P(E, 10, true, vol, { dist: 0.0005, price: 9.995, capped: false, floored: true, sd: 0.049 },
                 0.002, notional, mrg, qty, 4, 4);
    ok('arm floored at BE when costs exceed 1R', pbig.armAtBe === true && near(pbig.arm, pbig.be, 1e-12),
       'arm=' + pbig.arm + ' be=' + pbig.be);

    // 3.7 Touch probability of the break-even stop = reflection principle
    var b = Math.abs(Math.log(pf.arm / pf.be));
    var expect = 2 * (1 - ctx.normCdf(b / (vol * Math.sqrt(ctx.H_NOISE))));
    ok('scratch prob at arm', near(pf.pArm, expect, 1e-12), pf.pArm + ' vs ' + expect);
    ok('scratch prob in [0,1]', pf.pArm >= 0 && pf.pArm <= 1);

    // 3.8 Risk removed = money lost on the structural stop
    ok('risk removed usd', near(pf.riskUsd, qty * Math.abs(E - inv.price), 1e-9), 'r=' + pf.riskUsd);
    ok('risk removed pct', near(pf.riskPct, pf.riskUsd / mrg, 1e-12));

    // 3.9 At 1R the unrealised profit equals exactly the risk being removed
    ok('arm profit == removed risk', near(qty * Math.abs(pf.arm - E), pf.riskUsd, 1e-9),
       (qty * Math.abs(pf.arm - E)) + ' vs ' + pf.riskUsd);
    ok('risk pct == dist x L', near(pf.riskPct, inv.dist * (notional / mrg), 1e-12), 'rp=' + pf.riskPct);

    // 3.10 Stage machine: below BE / between / armed
    var s1 = P(E, 10.00, true, vol, inv, fr, notional, mrg, qty, 4, 4);
    var s2 = P(E, 10.60, true, vol, inv, fr, notional, mrg, qty, 4, 4);
    var s3 = P(E, 11.20, true, vol, inv, fr, notional, mrg, qty, 4, 4);
    ok('stage cost', s1.stage === 'cost', s1.stage);
    ok('stage wait', s2.stage === 'wait', s2.stage);
    ok('stage armed', s3.stage === 'armed', s3.stage);
    ok('pNow only when past BE', s1.pNow === null && s2.pNow !== null && s3.pNow !== null);
    ok('pNow shrinks as price runs', s3.pNow < s2.pNow, s2.pNow + ' -> ' + s3.pNow);
    var t1 = P(E, 10.00, false, vol, inv, null, notional, mrg, qty, 4, 4);
    var t3 = P(E, 8.80, false, vol, inv, null, notional, mrg, qty, 4, 4);
    ok('short stage cost', t1.stage === 'cost', t1.stage);
    ok('short stage armed', t3.stage === 'armed', t3.stage);

    // 3.11 Margin top-up: only above the ceiling, restores effective leverage
    // notional = mrg * L, as on the board (identity of invariant 16)
    var n6 = mrg * 6, q6 = n6 / E;
    var pm = P(E, 10, true, vol, inv, null, n6, mrg, q6, 6, 4);
    ok('top-up present above ceiling', pm.addMargin !== null && pm.addMargin > 0, 'add=' + pm.addMargin);
    ok('top-up restores ceiling leverage',
       near(n6 / (mrg + pm.addMargin), 4, 1e-9), 'Leff=' + (n6 / (mrg + pm.addMargin)));
    ok('top-up liq equals ceiling liq',
       near(pm.addLiq, ctx.liqPrice(E, 4, true), 1e-12), pm.addLiq + ' vs ' + ctx.liqPrice(E, 4, true));
    var pm2 = P(E, 10, true, vol, inv, null, notional, mrg, qty, 4, 4);
    ok('no top-up at/below ceiling', pm2.addMargin === null);
    var pm3 = P(E, 10, true, vol, inv, null, notional, mrg, qty, 5, null);
    ok('no top-up without ceiling', pm3.addMargin === null);

    // 3.12 Degenerate and missing inputs (invariant 9)
    ok('null on bad entry', P(0, 10, true, vol, inv, null, notional, mrg, qty, 4, 4) === null);
    ok('null on bad price', P(E, 0, true, vol, inv, null, notional, mrg, qty, 4, 4) === null);
    var nv = P(E, 10.5, true, null, inv, null, notional, mrg, qty, 4, 4);
    ok('no vol -> plan without probabilities', nv !== null && nv.pArm === null && nv.pNow === null);
    var nvz = P(E, 10.5, true, 0, inv, null, notional, mrg, qty, 4, 4);
    ok('zero vol -> no probabilities', nvz !== null && nvz.pArm === null);
    var ni = P(E, 10.5, true, vol, null, null, notional, mrg, qty, 4, 4);
    ok('no invalidation -> BE only', ni !== null && ni.arm === null && ni.riskUsd === null && ni.stage === 'wait');
    var nz = P(E, 10.5, true, vol, inv, null, 0, 0, 0, 4, 4);
    ok('zero size -> money fields null, prices alive',
       nz !== null && nz.costUsd === null && nz.riskUsd === null && nz.be > 0);
    var mad = P(E, 10.5, true, vol, inv, 0.06, notional, mrg, qty, 4, 4);
    ok('absurd funding clamped, BE stays positive', mad.be > 0 && mad.costFrac < 1, 'be=' + mad.be);
    var mads = P(E, 9.5, false, vol, inv, 0.06, notional, mrg, qty, 4, 4);
    ok('absurd funding short BE positive', mads.be > 0, 'be=' + mads.be);
    var cap = P(E, 10.5, true, vol, { dist: 0.294, price: 7.06, capped: true, floored: false, sd: 0.049 },
                null, notional, mrg, qty, 4, 4);
    ok('capped invalidation still yields arm', cap.arm > 0 && cap.capped === true);

    // 3.13 Identity: money side is consistent with position identity
    var q2 = 250, n2 = q2 * E, m2 = n2 / 5;
    var pid = P(E, 10, true, vol, inv, 0.0002, n2, m2, q2, 5, 5);
    ok('cost scales with notional', near(pid.costUsd, pid.costFrac * n2, 1e-12));
    ok('cost as share of margin == costFrac x L', near(pid.costUsd / m2, pid.costFrac * 5, 1e-12));
}

// ── 4. Board markup contract ────────────────────────────────────────────────
function suiteBoard(ctx) {
    var H = '\u0417\u0410\u0429\u0418\u0422\u0410 \u041F\u041E\u0417\u0418\u0426\u0418\u0418'; // ЗАЩИТА ПОЗИЦИИ
    var row = armCtx(ctx, { entry: 10, price: 10.4, fr: 0.0001 });
    var h = ctx.boardHtml(row, 0);
    ok('board has protection block', h.indexOf(H) > 0);
    ok('protection header unique (anchor invariant 18)',
       h.indexOf(H) === h.lastIndexOf(H));
    // metal ring switch: the section must not carry an inline style
    var idx = h.indexOf(H);
    var secStart = h.lastIndexOf('<div class="bd-sec', idx);
    ok('no inline style on protection section',
       h.substring(secStart, idx).indexOf('style=') < 0, h.substring(secStart, secStart + 90));
    // order: protection sits between «ЕСЛИ СРАБОТАЕТ» and «ОТКУДА ПЛЕЧО»
    var win = h.indexOf('\u0415\u0421\u041B\u0418 \u0421\u0420\u0410\u0411\u041E\u0422\u0410\u0415\u0422');
    var src = h.indexOf('\u041E\u0422\u041A\u0423\u0414\u0410 \u041F\u041B\u0415\u0427\u041E');
    ok('block order', win > 0 && src > 0 && win < idx && idx < src, win + '/' + idx + '/' + src);
    ok('no undefined leaked', h.indexOf('undefined') < 0);
    ok('no NaN leaked', h.indexOf('NaN') < 0);

    // survives every degraded input (invariant 9)
    var cases = [
        { n: 'no volatility', cd: { volatility: null } },
        { n: 'no min30/max30', cd: { min30: null, max30: null } },
        { n: 'no 90d range', cd: { min_price: null, max_price: null, min30: null, max30: null } },
        { n: 'no betas', cd: { up_beta: null, down_beta: null, up_beta_90: null, down_beta_90: null } },
        { n: 'no r7/r30', cd: { r7: null, r14: null, r30: null, eff14: null } },
        { n: 'vol 3.5%/h', cd: { volatility: 0.035 } },
        { n: 'vol 2.5%/h', cd: { volatility: 0.025 } },
        { n: 'vol7 spike', cd: { vol7: 0.05 } },
        { n: 'entry below min', entry: 7.5 },
        { n: 'entry above max', entry: 15.5 },
        { n: 'no funding', fr: null },
        { n: 'huge funding', fr: 0.01 },
        { n: 'negative funding', fr: -0.004 },
        { n: 'coin mode', sizeMode: 'coin', qty: 1000 },
        { n: 'coin mode zero qty', sizeMode: 'coin', qty: 0 },
        { n: 'margin zero', margin: 0 },
        { n: 'lev 2', lev: 2 },
        { n: 'lev 7', lev: 7 },
        { n: 'penny coin', price: 0.00031, entry: 0.0003,
          cd: { min_price: 0.00021, max_price: 0.00052, min30: 0.00026, max30: 0.00045 } }
    ];
    for (var s = 0; s < 2; s++) {
        for (var i = 0; i < cases.length; i++) {
            var o = {};
            for (var k in cases[i]) o[k] = cases[i][k];
            o.side = s === 0 ? 'long' : 'short';
            if (o.entry === undefined) o.entry = o.price !== undefined ? o.price : 10;
            if (o.price === undefined) o.price = 10.4;
            if (o.fr === undefined) o.fr = 0.0001;
            var r = armCtx(ctx, o);
            var out = null, err = null;
            try { out = ctx.boardHtml(r, 0); } catch (e) { err = e && e.message; }
            ok('render ' + o.side + ' / ' + cases[i].n, err === null && typeof out === 'string', err);
            if (out) {
                ok('no undefined ' + o.side + ' / ' + cases[i].n, out.indexOf('undefined') < 0);
                ok('no NaN ' + o.side + ' / ' + cases[i].n, out.indexOf('NaN') < 0);
            }
        }
    }
}

// ── 4b. «РИСК ВЫНОСА» — the squeeze block (TZ-12 stage C) ───────────────────
// Display order of every header the board can print, so «out of order» is a
// failure and not something a reader has to notice. Position SIXTH is NOT
// asserted from this list — «СТОРОНА ПРОТИВ СТРУКТУРЫ» and «ВНИМАНИЕ» are
// alarms rather than numbered blocks (§3.7) and come and go with the fixture.
// Sixth is asserted where the block order actually lives: the concatenation at
// the end of boardHtml (inv. 15), read out of index.html in 4b.0.
var ORDER = [
    '\u0421\u0422\u041e\u0420\u041e\u041d\u0410 \u041f\u0420\u041e\u0422\u0418\u0412 \u0421\u0422\u0420\u0423\u041a\u0422\u0423\u0420\u042b',    // СТОРОНА ПРОТИВ СТРУКТУРЫ
    '\u0412\u041d\u0418\u041c\u0410\u041d\u0418\u0415',    // ВНИМАНИЕ
    '\u041f\u041e\u0427\u0415\u041c\u0423 \u042d\u0422\u0410 \u041c\u041e\u041d\u0415\u0422\u0410',    // ПОЧЕМУ ЭТА МОНЕТА
    '\u0414\u0418\u0410\u041f\u0410\u0417\u041e\u041d 90 \u0414\u041d\u0415\u0419',    // ДИАПАЗОН 90 ДНЕЙ
    '\u0422\u041e\u0427\u041a\u0410 \u0412\u0425\u041e\u0414\u0410',    // ТОЧКА ВХОДА
    '\u0412\u042b\u0411\u041e\u0420 \u041f\u041b\u0415\u0427\u0410',    // ВЫБОР ПЛЕЧА
    '\u0420\u0418\u0421\u041a \u0412\u042b\u041d\u041e\u0421\u0410',    // РИСК ВЫНОСА
    '\u0420\u0410\u0417\u041c\u0415\u0420 \u041f\u041e\u0417\u0418\u0426\u0418\u0418',    // РАЗМЕР ПОЗИЦИИ
    '\u0413\u0420\u0410\u041d\u0418\u0426\u042b \u0421\u0414\u0415\u041b\u041a\u0418',    // ГРАНИЦЫ СДЕЛКИ
    '\u0426\u0415\u041d\u0410 \u0412\u0420\u0415\u041c\u0415\u041d\u0418',    // ЦЕНА ВРЕМЕНИ
    '\u0415\u0421\u041b\u0418 \u0418\u0414\u0415\u042f \u041d\u0415 \u0421\u0420\u0410\u0411\u041e\u0422\u0410\u0415\u0422',    // ЕСЛИ ИДЕЯ НЕ СРАБОТАЕТ
    '\u0415\u0421\u041b\u0418 \u0421\u0420\u0410\u0411\u041e\u0422\u0410\u0415\u0422',    // ЕСЛИ СРАБОТАЕТ
    '\u0417\u0410\u0429\u0418\u0422\u0410 \u041f\u041e\u0417\u0418\u0426\u0418\u0418',    // ЗАЩИТА ПОЗИЦИИ
    '\u041e\u0422\u041a\u0423\u0414\u0410 \u041f\u041b\u0415\u0427\u041e',    // ОТКУДА ПЛЕЧО
    '\u0414\u041e\u0412\u0415\u0420\u0418\u0415 \u041a \u041c\u041e\u0414\u0415\u041b\u0418'    // ДОВЕРИЕ К МОДЕЛИ
];
var SQZ      = '\u0420\u0418\u0421\u041a \u0412\u042b\u041d\u041e\u0421\u0410';   // РИСК ВЫНОСА
var LEVH     = '\u0412\u042b\u0411\u041e\u0420 \u041f\u041b\u0415\u0427\u0410';   // ВЫБОР ПЛЕЧА
var SIZEH    = '\u0420\u0410\u0417\u041c\u0415\u0420 \u041f\u041e\u0417\u0418\u0426\u0418\u0418';   // РАЗМЕР ПОЗИЦИИ
var OWNLAB   = '\u0421\u0435\u0433\u043e\u0434\u043d\u044f \u0443\u0436\u0435 \u0432\u044b\u043d\u0435\u0441\u0435\u043d\u043e';   // Сегодня уже вынесено
var MEDPRE   = '\u043c\u0435\u0434\u0438\u0430\u043d\u0430 \u0441\u043f\u0438\u0441\u043a\u0430 ';   // медиана списка 
var MEDMID   = ' \u043f\u043e ';   //  по 
var MEDNONE  = '\u0441\u043f\u0438\u0441\u043e\u043a \u043d\u0435 \u0438\u0437\u043c\u0435\u0440\u0435\u043d';   // список не измерен
var STOPLAB  = '\u0421\u0442\u043e\u043f \u043e\u0442\u043e\u0434\u0432\u0438\u043d\u0443\u0442 \u043e\u0442 \u0448\u0443\u043c\u0430';   // Стоп отодвинут от шума
var CAPTXT   = '\u043e\u043f\u043e\u0440\u044b \u0440\u044f\u0434\u043e\u043c \u043d\u0435\u0442, \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u043d\u0430\u0440\u0438\u0441\u043e\u0432\u0430\u043d';   // опоры рядом нет, уровень нарисован
var FLRTXT   = '\u0441\u0442\u043e\u043f \u043f\u0440\u0438\u0436\u0430\u0442 \u043a \u043f\u043e\u043b\u0443 2';   // стоп прижат к полу 2
var NOVOL    = '\u0431\u043e\u0442 \u043d\u0435 \u0434\u0430\u043b \u0432\u043e\u043b\u0430\u0442\u0438\u043b\u044c\u043d\u043e\u0441\u0442\u044c';   // бот не дал волатильность
var LIQLAB   = '\u0417\u0430\u043f\u0430\u0441 \u0434\u043e \u043b\u0438\u043a\u0432\u0438\u0434\u0430\u0446\u0438\u0438 \u043f\u0440\u0438 ';   // Запас до ликвидации при 
var TOUCH    = '\u0448\u0430\u043d\u0441 \u0437\u0430\u0434\u0435\u0442\u044c \u0437\u0430 \u0441\u0443\u0442\u043a\u0438 ';   // шанс задеть за сутки 
var ABNORM   = '\u0430\u043d\u043e\u043c\u0430\u043b\u044c\u043d';   // аномальн
var SIGMA    = '\u03c3';   // σ

function headersOf(h) {
    var out = [], re = /<div class="bd-h[^"]*">([^<]*)<\/div>/g, m;
    while ((m = re.exec(h)) !== null) out.push(m[1]);
    return out;
}
// A spot row exactly as the render loop builds one, plus the three range fields
// listExhaustion reads. `fut` is the DECLARED venue (§3.14, inv. 41).
function exRow(name, fut, hi, lo, cur, vol) {
    var t = { name: name, s: name + 'USDT' };
    if (fut) t.fut = true;
    return { t: t, hi24: hi, lo24: lo, cur: cur, cd: { volatility: vol }, state: 'ok' };
}
function spotList(n) {
    var out = [];
    for (var i = 0; i < n; i++) out.push(exRow('S' + i, false, 104 + i, 100, 102, 0.01));
    return out;
}
// The rendered «РИСК ВЫНОСА» section alone, so cleanliness can be asserted on
// THIS block without being masked or faked by the rest of the board.
function sqzSection(h) {
    var i = h.indexOf(SQZ);
    if (i < 0) return '';
    var a = h.lastIndexOf('<div class="bd-sec', i);
    var b = h.indexOf('<div class="bd-sec', i);
    return h.slice(a, b < 0 ? h.length : b);
}
function sqzBoard(ctx, o, rows) {
    var row = armCtx(ctx, o);
    row.coin.highPrice = o.hi === undefined ? '10.9' : o.hi;
    row.coin.lowPrice  = o.lo === undefined ? '9.95' : o.lo;
    rowRange(row);   // the ticker object changed, so the row re-reads it
    ctx.lastRows = [row].concat(rows === undefined ? spotList(25) : rows);
    return { row: row, h: ctx.boardHtml(row, 0) };
}

// 4b.0 — sixth in the concatenation, read from the source. inv. 15 puts the
// block order in exactly one place, so that is the place the position is
// asserted; the rendered checks below then prove the source order reaches the
// screen. Reading index.html here is not a second implementation of anything:
// it is the ONE list the invariant names.
function suiteSqueezeOrder(file) {
    var src = fs.readFileSync(file, 'utf8');
    var at = src.indexOf('h += sHero + sRel + sWarn');
    ok('concatenation found in ' + file, at > 0);
    if (at < 0) return;
    var tail = src.slice(at, src.indexOf(';', at));
    // Drop «h +=» before splitting: the compound operator carries a '+' of its own.
    tail = tail.replace(/\/\/[^\n]*/g, '').replace(/^\s*h\s*\+=/, '');
    var ops = tail.split('+').map(function (x) { return x.trim(); })
                  .filter(function (x) { return x.length > 0; });
    var want = ['sHero', 'sRel', 'sWarn', 'sWhy', 'sRange', 'sEntry', 'sLev',
                'sSqz', 'sSize', 'sBounds', 'sTime', 'sLoss', 'sWin', 'sProt',
                'sSrc', 'sTrust'];
    ok('concatenation operands unchanged apart from the insertion',
       ops.join(',') === want.join(','), ops.join(','));
    // Block 1 is sHero + sRel + sWarn — one numbered block, three strings.
    var numbered = ops.slice(2);   // drop sRel, sWarn: they fold into block 1
    ok('sSqz is the SIXTH numbered block', numbered.indexOf('sSqz') === 5,
       numbered.join(','));
    ok('sSqz sits between sLev and sSize',
       numbered[4] === 'sLev' && numbered[6] === 'sSize', numbered.join(','));
}

function suiteSqueeze(ctx) {
    // 4b.1 — present, correctly placed, no inline style, on every side x every
    // leverage button the board draws. The TZ says «the four leverage buttons»;
    // the board draws six (2..7), so all six are covered — a superset.
    var sides = ['long', 'short'], levs = [2, 3, 4, 5, 6, 7], si, li;
    for (si = 0; si < sides.length; si++) {
        for (li = 0; li < levs.length; li++) {
            var b = sqzBoard(ctx, { entry: 10, price: 10.4, fr: 0.0001,
                                    side: sides[si], lev: levs[li] });
            var h = b.h, tag = sides[si] + '/' + levs[li] + 'X';
            var i = h.indexOf(SQZ);
            ok('sqz present ' + tag, i > 0);
            ok('sqz header unique (inv. 18) ' + tag, i === h.lastIndexOf(SQZ));
            var hs = headersOf(h);
            var pos = hs.indexOf(SQZ);
            ok('sqz between lev and size ' + tag,
               pos > 0 && hs[pos - 1] === LEVH && hs[pos + 1] === SIZEH,
               hs.slice(Math.max(0, pos - 1), pos + 2).join(' | '));
            var last = -1, ordered = true;
            for (var q = 0; q < hs.length; q++) {
                var at = ORDER.indexOf(hs[q]);
                if (at < 0 || at <= last) { ordered = false; break; }
                last = at;
            }
            ok('header order is canonical ' + tag, ordered, hs.join(' | '));
            // §3.7: an inline style on the .bd-sec kills the metal ring.
            var secStart = h.lastIndexOf('<div class="bd-sec', i);
            ok('no inline style on the sqz section ' + tag,
               h.substring(secStart, i).indexOf('style=') < 0,
               h.substring(secStart, secStart + 90));
            // The PRESSED button, never the RESULT (inv. 14).
            ok('sqz reads the pressed leverage ' + tag,
               h.indexOf(LIQLAB + levs[li] + 'X') > 0);
            // The sigma distance must actually move with the pressed button.
            var expB = Math.abs(Math.log(ctx.liqPrice(10, levs[li], sides[si] === 'long') / 10));
            var expSd = (expB / ctx.sigmaDay(0.01)).toFixed(1).replace('.', ',');
            ok('sqz sigma distance matches liqPrice at the pressed lev ' + tag,
               h.indexOf('>' + expSd + SIGMA) > 0, 'want ' + expSd);
            // §3 non-goal: measurement only, no threshold and no verdict word.
            ok('sqz says nothing about an abnormal day ' + tag,
               h.toLowerCase().indexOf(ABNORM) < 0);
            ok('no undefined in sqz board ' + tag, h.indexOf('undefined') < 0);
            ok('no NaN in sqz board ' + tag, h.indexOf('NaN') < 0);
            var sc = sqzSection(h);
            ok('sqz section is non-empty ' + tag, sc.length > 200, 'len=' + sc.length);
            ok('sqz section carries no Infinity ' + tag, sc.indexOf('Infinity') < 0);
        }
    }

    // 4b.2 — row 3 reads dec.inv: capped, floored, neither. Each fixture is
    // asserted to BE the state it claims before its text is checked (inv. 23).
    var invCases = [
        ['capped',  { min30: 2.0, min_price: 1.8 },   CAPTXT],
        ['floored', { min30: 10.0, min_price: 9.99 }, FLRTXT],
        ['neither', { min30: 9.0, min_price: 8.0 },   null]
    ];
    for (var c = 0; c < invCases.length; c++) {
        var b2 = sqzBoard(ctx, { entry: 10, price: 10.4, fr: 0.0001, side: 'long',
                                 lev: 4, cd: invCases[c][1] });
        var h2 = b2.h;
        var dec2 = ctx.leverageDecision(b2.row.cd, 10, true, ctx.botData.btc);
        var want = invCases[c][0];
        var got = dec2.inv && dec2.inv.capped ? 'capped'
                : (dec2.inv && dec2.inv.floored ? 'floored' : 'neither');
        ok('fixture really is ' + want, got === want, 'got ' + got);
        ok('sqz block present under ' + want, h2.indexOf(SQZ) > 0);
        ok('stop row present under ' + want, h2.indexOf(STOPLAB) > 0);
        if (invCases[c][2]) {
            ok('stop row text under ' + want, h2.indexOf(invCases[c][2]) > 0);
        } else {
            ok('stop row prints sigmas under ' + want,
               h2.indexOf(CAPTXT) < 0 && h2.indexOf(FLRTXT) < 0);
            var wantSig = (dec2.inv.dist / dec2.inv.sd).toFixed(1).replace('.', ',');
            ok('stop sigmas equal dec.inv.dist / dec.inv.sd (inv. 20)',
               h2.indexOf('>' + wantSig + SIGMA) > 0, 'want ' + wantSig);
        }
        ok('no undefined under ' + want, h2.indexOf('undefined') < 0);
        ok('no NaN under ' + want, h2.indexOf('NaN') < 0);
    }

    // 4b.3 — missing volatility: the block survives and says what is missing.
    {
        var h3 = sqzBoard(ctx, { entry: 10, price: 10.4, fr: 0.0001, side: 'long',
                                 lev: 4, cd: { volatility: null } }).h;
        ok('block survives without volatility', h3.indexOf(SQZ) > 0);
        ok('sigma distance is reported unavailable', h3.indexOf(NOVOL) > 0);
        ok('no touch probability without volatility', h3.indexOf(TOUCH) < 0);
        ok('own ratio omitted without volatility', h3.indexOf(OWNLAB) < 0);
        ok('the list line still prints without volatility', h3.indexOf(MEDPRE) > 0);
        ok('the rest of the board lives (inv. 9)', h3.indexOf(SIZEH) > 0);
        ok('no undefined without volatility', h3.indexOf('undefined') < 0);
        ok('no NaN without volatility', h3.indexOf('NaN') < 0);
    }

    // 4b.4 — the list line: quorum met, quorum not met, and the venue exclusion
    // reaching the board rather than only the function.
    {
        var base = { entry: 10, price: 10.4, fr: 0.0001, side: 'long', lev: 4 };
        var bq = sqzBoard(ctx, base, spotList(25));
        var lq = ctx.listExhaustion(ctx.lastRows);
        ok('quorum met -> a median is printed', bq.h.indexOf(MEDPRE) > 0);
        ok('quorum met -> no not-measured line', bq.h.indexOf(MEDNONE) < 0);
        ok('printed median and n equal listExhaustion',
           bq.h.indexOf(MEDPRE + lq.median.toFixed(1).replace('.', ',') + MEDMID + lq.n) > 0,
           'n=' + lq.n + ' med=' + lq.median);

        var bn = sqzBoard(ctx, base, spotList(3));
        ok('below quorum -> the list says it could not be measured', bn.h.indexOf(MEDNONE) > 0);
        ok('below quorum -> no median printed', bn.h.indexOf(MEDPRE) < 0);
        ok('below quorum -> the coin line still prints', bn.h.indexOf(OWNLAB) > 0);
        ok('below quorum -> block still present', bn.h.indexOf(SQZ) > 0);

        // 25 spot + 3 fut must render byte-identically to 25 spot alone.
        var spot25 = spotList(25);
        var hSpot = sqzBoard(ctx, base, spot25).h;
        var hFut = sqzBoard(ctx, base, spot25.concat([
            exRow('XMR', true, 900, 100, 500, 0.01),
            exRow('LIT', true, 900, 100, 500, 0.01),
            exRow('HYPE', true, 900, 100, 500, 0.01)
        ])).h;
        ok('three fut:true rows change nothing on the board', hSpot === hFut,
           'len ' + hSpot.length + ' vs ' + hFut.length);
        // …and the same three rows counted as spot WOULD have changed it, or the
        // check above proves nothing (inv. 22, 23).
        var hNaive = sqzBoard(ctx, base, spot25.concat([
            exRow('XMR', false, 900, 100, 500, 0.01),
            exRow('LIT', false, 900, 100, 500, 0.01),
            exRow('HYPE', false, 900, 100, 500, 0.01)
        ])).h;
        ok('the same rows without the declaration DO change the board', hSpot !== hNaive);
    }

    // 4b.5 — E <= 0 and a non-finite liquidation: row 1 goes, the block stays.
    {
        var bz = sqzBoard(ctx, { entry: 10, price: 10.4, fr: 0.0001, side: 'long', lev: 4 });
        var realLiq = ctx.liqPrice;
        ctx.liqPrice = function () { return Infinity; };
        var hz = ctx.boardHtml(bz.row, 0);
        ctx.liqPrice = realLiq;
        ok('liqPrice restored', ctx.liqPrice === realLiq);
        ok('non-finite liq -> block survives', hz.indexOf(SQZ) > 0);
        ok('non-finite liq -> row 1 omitted', hz.indexOf(LIQLAB) < 0);
        ok('non-finite liq -> row 2 still prints', hz.indexOf(OWNLAB) > 0);
        ok('non-finite liq -> nothing leaked',
           hz.indexOf('undefined') < 0 && hz.indexOf('NaN') < 0);

        // E <= 0 comes from entryState, which is where the board reads it.
        var be = sqzBoard(ctx, { entry: 10, price: 10.4, fr: 0.0001, side: 'long', lev: 4 });
        ctx.entryState.UNI = { price: 0 };
        var he = ctx.boardHtml(be.row, 0);
        ok('fixture really has E <= 0', ctx.entryState.UNI.price <= 0);
        ok('E <= 0 -> block survives', he.indexOf(SQZ) > 0);
        ok('E <= 0 -> row 1 omitted', he.indexOf(LIQLAB) < 0);
        ok('E <= 0 -> the rest of the board lives (inv. 9)', he.indexOf(SIZEH) > 0);
        // Cleanliness is asserted on THIS block. The whole board is not clean at
        // E = 0 and was not before TZ-12: «ГРАНИЦЫ СДЕЛКИ» prints «NaN% от входа»
        // from Math.abs(liq / E - 1) with E = 0, on origin/main as well. That is a
        // pre-existing defect, reported and NOT fixed here (contract §12).
        var sec = sqzSection(he);
        ok('E <= 0 -> the sqz block itself is clean',
           sec.indexOf('undefined') < 0 && sec.indexOf('NaN') < 0
           && sec.indexOf('Infinity') < 0, sec.slice(0, 200));
        if (he.indexOf('NaN') >= 0) {
            notes.push('PRE-EXISTING (not TZ-12, present on origin/main): at E = 0 the board '
                     + 'prints NaN in «\u0413\u0420\u0410\u041d\u0418\u0426\u042b '
                     + '\u0421\u0414\u0415\u041b\u041a\u0418» — Math.abs(liq / E - 1).');
        }
    }

    // 4b.6 — purity (inv. 27). Perturbing ONLY what the block reads must leave
    // the verdict, the score and the leverage decision byte-identical.
    {
        var opts = { entry: 10, price: 10.4, fr: 0.0001, side: 'long', lev: 4 };
        function decisionOf(rows) {
            var bb = sqzBoard(ctx, opts, rows);
            var r = bb.row, Ez = 10, isLong = true;
            var dec = ctx.leverageDecision(r.cd, Ez, isLong, ctx.botData.btc);
            var reg = ctx.marketRegime(ctx.botData.btc);
            var vd = ctx.directionVerdict(r.cd, r.t.s, r.t.name, 10.4, 1.5, 90000000,
                                          isLong, reg, dec, 10.9, 9.95,
                                          ctx.residual7(r.cd, ctx.botData.btc),
                                          Date.UTC(2026, 7, 23));
            return JSON.stringify({ vd: vd, dec: dec,
                sc: ctx.scoreCandidate(r.cd, r.t.s, 10.4, 1.5, 90000000, isLong) });
        }
        var a = decisionOf(spotList(25));
        var b = decisionOf(spotList(3));
        var c2 = decisionOf([]);
        ok('verdict unchanged by the list the block reads (below quorum)', a === b);
        ok('verdict unchanged by the list the block reads (empty)', a === c2);
        // …and the board itself DOES move with the list, or the two checks
        // above are vacuous (inv. 22).
        var withList = sqzBoard(ctx, opts, spotList(25)).h;
        var withoutList = sqzBoard(ctx, opts, spotList(3)).h;
        ok('the block itself does move with the list', withList !== withoutList);
    }
}

// ── 5. Nothing else moved: the whole board is byte-identical ─────────────
// TZ-11 Stage A. This suite used to strip the «POSITION PROTECTION» section
// from the CANDIDATE only and compare the remainder. That was correct exactly
// once — while the baseline predated the section and the candidate carried it.
// Both revisions have carried it since TZ-07, so the asymmetry no longer
// compensated for anything: it DELETED a section from one side of an otherwise
// byte-identical pair and reported six differences of its own making. The
// transformation is now symmetric in the only form worth having — neither side
// is touched — and the assertion itself is unchanged and stricter: the WHOLE
// board must match, section included. A differ that cannot pass on identity is
// not evidence of anything (inv. 45), which is why cmpIdentity below runs it
// against the candidate's own source inside the default suite.
var boardCmp = 0;   // comparisons actually performed (inv. 22, inv. 43)
function suiteNoRegression(nu, old, label) {
    var tag = label ? ' [' + label + ']' : '';
    var scenarios = [
        { entry: 10, price: 10.4, fr: 0.0001, side: 'long', lev: 4 },
        { entry: 10, price: 9.1, fr: -0.0003, side: 'short', lev: 3 },
        { entry: 12.6, price: 12.0, fr: 0.0009, side: 'long', lev: 7, sizeMode: 'coin', qty: 750 },
        { entry: 9.2, price: 9.2, fr: null, side: 'short', lev: 2, margin: 250 },
        { entry: 10, price: 10, fr: 0.0001, side: 'long', lev: 5, cd: { volatility: 0.025 } },
        { entry: 10, price: 10, fr: 0.0001, side: 'long', lev: 5, cd: { volatility: null } }
    ];
    for (var i = 0; i < scenarios.length; i++) {
        var rn = armCtx(nu, scenarios[i]);
        var ro = armCtx(old, scenarios[i]);
        var hn = nu.boardHtml(rn, 0);
        var ho = old.boardHtml(ro, 0);
        boardCmp++;                                   // counted at the comparison site
        ok('rest of board unchanged' + tag + ' #' + i, hn === ho,
           'len ' + hn.length + ' vs ' + ho.length);
        if (hn !== ho) {
            for (var c = 0; c < Math.min(hn.length, ho.length); c++) {
                if (hn[c] !== ho[c]) {
                    notes.push('  first diff at ' + c + ': ...' + hn.substr(Math.max(0, c - 60), 120)
                             + ' ||| ' + ho.substr(Math.max(0, c - 60), 120));
                    break;
                }
            }
        }
    }
}

// ── 5b. Identity: the differ compared with ITSELF must find nothing ──────
// Runs in the DEFAULT suite, with or without a baseline argument. index.html is
// loaded a SECOND time into its own context, so the two sides are independent
// evaluations of the same bytes and the comparison exercises the real differ
// rather than an object identity. Zero differences is the pass condition; zero
// comparisons is a failure, not a pass (inv. 22).
function suiteIdentity(candidate) {
    var self = loadFront(candidate);
    var before = boardCmp;
    suiteNoRegression(self, loadFront(candidate), 'identity');
    ok('identity run compared boards', boardCmp > before,
       (boardCmp - before) + ' comparisons');
    notes.push('identity: ' + (boardCmp - before) + ' boards compared against '
             + candidate + ' itself');
}

// ── 6. Fuzz: no exception, no NaN, no undefined on any board ────────────────
function suiteFuzz(ctx, n) {
    var seed = 12345;
    function rnd() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; }
    function pick(a) { return a[Math.floor(rnd() * a.length)]; }
    var bad = 0, thrown = 0, checked = 0;
    for (var i = 0; i < n; i++) {
        var price = pick([0.00021, 0.031, 0.42, 1.0, 9.8, 63, 480, 3900, 91000]);
        var vol = pick([null, 0, 0.0004, 0.003, 0.009, 0.015, 0.021, 0.028, 0.034, 0.06]);
        var mn = price * (0.35 + rnd() * 0.6), mx = price * (1.02 + rnd() * 1.4);
        var cd = {
            volatility: vol,
            min_price: pick([mn, null]), max_price: pick([mx, null]),
            min30: pick([mn * (1 + rnd() * 0.3), null, price * 1.4]),
            max30: pick([mx * (1 - rnd() * 0.3), null, price * 0.7]),
            corr_90: pick([null, -0.8, 0.2, 0.9]),
            up_beta: pick([null, 0.4, 1.3]), down_beta: pick([null, 0.6, 2.4]),
            up_r2: pick([null, 0.05, 0.5]), down_r2: pick([null, 0.1, 0.7]),
            up_beta_90: pick([null, 0.9, 2.9]), down_beta_90: pick([null, 1.1, 3.3]),
            up_r2_90: pick([null, 0.2, 0.6]), down_r2_90: pick([null, 0.3, 0.5]),
            tail_beta: pick([null, 3.5]), tail_r2: pick([null, 0.02, 0.4]),
            r7: pick([null, -0.4, 0.02, 0.9]), r14: pick([null, -0.2, 0.3]),
            r30: pick([null, -0.5, 0.6]), vol7: pick([null, 0.002, 0.05]),
            eff14: pick([null, -0.9, 0.2, 0.95]), rank: pick([null, 5, 140]),
            fdv_mc: pick([null, 1.1, 6]), error: false
        };
        var o = {
            side: pick(['long', 'short']), lev: pick([2, 3, 4, 5, 6, 7]),
            price: price, entry: price * (0.5 + rnd() * 1.2),
            fr: pick([null, 0, 0.00001, -0.0002, 0.0009, -0.004, 0.02, -0.05]),
            margin: pick([0, 1, 55, 600, 25000]),
            sizeMode: pick(['usdt', 'coin']), qty: pick([0, 0.004, 17, 125000])
        };
        var row = armCtx(ctx, o);
        row.cd = cd;
        var h = null;
        try { h = ctx.boardHtml(row, 0); } catch (e) { thrown++; notes.push('THROW: ' + e.message); continue; }
        checked++;
        if (h.indexOf('undefined') >= 0 || h.indexOf('NaN') >= 0 || h.indexOf('Infinity') >= 0) {
            bad++;
            if (bad < 4) notes.push('DIRTY OUTPUT: ' + JSON.stringify(o).substring(0, 180));
        }
    }
    ok('fuzz: no exceptions', thrown === 0, thrown + ' throws');
    ok('fuzz: clean output', bad === 0, bad + ' dirty of ' + checked);
    notes.push('fuzz: ' + checked + ' boards rendered clean');
}

// ── main ────────────────────────────────────────────────────────────────────
var candidate = process.argv[2] || 'index.html';
var baseline = process.argv[3] || null;
var nu = loadFront(candidate);
var old = baseline ? loadFront(baseline) : null;

// A parity fix that silently degrades to {} reproduces the original defect one
// layer down, so the loaded registry is asserted, not assumed.
ok('catalyst registry non-empty', Object.keys(nu.CATALYSTS).length > 0,
   Object.keys(nu.CATALYSTS).length + ' coins');
notes.push('registry: ' + Object.keys(nu.CATALYSTS).length + ' coins, updated '
         + (nu.catUpdated || '-'));

suiteRender(nu, 'candidate');
if (old) {
    suiteRender(old, 'baseline');
    suiteTouchIdentity(nu, old);
}
suitePlan(nu);
suiteBoard(nu);
suiteSqueezeOrder(candidate);
suiteSqueeze(nu);
suiteFuzz(nu, 4000);
// The identity run is unconditional: it is what makes every OTHER comparison in
// this file admissible as evidence, so it may not depend on an optional argument.
suiteIdentity(candidate);
if (old) suiteNoRegression(nu, old, 'baseline');

console.log(notes.join('\n'));
console.log('PASS ' + pass + '   FAIL ' + fail);
// Invariant 22: a bench that compared nothing is a FAILED bench, never a green
// one. The guard is on the TOTAL of both counters, so an absent
// index.html.prev — which legitimately skips the baseline suites — stays legal:
// it is zero COMPARISONS that is illegal, not a skipped optional suite.
if (pass + fail === 0) { console.log('FAIL bench verified nothing'); process.exit(1); }
// The board differ is the instrument Stage C's no-regression proof rests on. A
// run in which it compared zero boards is a run that proved nothing about it,
// however many other checks passed (inv. 22).
if (boardCmp === 0) { console.log('FAIL board differ compared nothing'); process.exit(1); }
process.exit(fail ? 1 : 0);
