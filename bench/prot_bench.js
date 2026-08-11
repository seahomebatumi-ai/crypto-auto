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
    var row = {
        t: { name: 'UNI', s: 'UNIUSDT' }, idx: 0,
        coin: coinOf(opts.price === undefined ? 10 : opts.price),
        cd: cdOf(opts.cd || {}), state: 'ok', sc: null
    };
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

// ── 5. Nothing else moved: the rest of the board is byte-identical ──────────
function suiteNoRegression(nu, old) {
    var scenarios = [
        { entry: 10, price: 10.4, fr: 0.0001, side: 'long', lev: 4 },
        { entry: 10, price: 9.1, fr: -0.0003, side: 'short', lev: 3 },
        { entry: 12.6, price: 12.0, fr: 0.0009, side: 'long', lev: 7, sizeMode: 'coin', qty: 750 },
        { entry: 9.2, price: 9.2, fr: null, side: 'short', lev: 2, margin: 250 },
        { entry: 10, price: 10, fr: 0.0001, side: 'long', lev: 5, cd: { volatility: 0.025 } },
        { entry: 10, price: 10, fr: 0.0001, side: 'long', lev: 5, cd: { volatility: null } }
    ];
    var HDR = '\u0417\u0410\u0429\u0418\u0422\u0410 \u041F\u041E\u0417\u0418\u0426\u0418\u0418';
    for (var i = 0; i < scenarios.length; i++) {
        var rn = armCtx(nu, scenarios[i]);
        var ro = armCtx(old, scenarios[i]);
        var hn = nu.boardHtml(rn, 0);
        var ho = old.boardHtml(ro, 0);
        // strip the new section from the new output, then compare byte for byte
        var idx = hn.indexOf(HDR);
        var stripped = hn;
        if (idx > 0) {
            var s0 = hn.lastIndexOf('<div class="bd-sec', idx);
            var s1 = hn.indexOf('<div class="bd-sec', idx);
            // find the end of the protection section by matching its own div depth
            var depth = 0, p = s0, end = -1;
            while (p < hn.length) {
                var openTag = hn.indexOf('<div', p);
                var closeTag = hn.indexOf('</div>', p);
                if (closeTag < 0) break;
                if (openTag >= 0 && openTag < closeTag) { depth++; p = openTag + 4; }
                else { depth--; p = closeTag + 6; if (depth === 0) { end = p; break; } }
            }
            if (end > 0) stripped = hn.substring(0, s0) + hn.substring(end);
            void s1;
        }
        ok('rest of board unchanged #' + i, stripped === ho,
           'len ' + stripped.length + ' vs ' + ho.length);
        if (stripped !== ho) {
            for (var c = 0; c < Math.min(stripped.length, ho.length); c++) {
                if (stripped[c] !== ho[c]) {
                    notes.push('  first diff at ' + c + ': ...' + stripped.substr(Math.max(0, c - 60), 120)
                             + ' ||| ' + ho.substr(Math.max(0, c - 60), 120));
                    break;
                }
            }
        }
    }
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

suiteRender(nu, 'candidate');
if (old) {
    suiteRender(old, 'baseline');
    suiteTouchIdentity(nu, old);
}
suitePlan(nu);
suiteBoard(nu);
suiteFuzz(nu, 4000);
if (old) suiteNoRegression(nu, old);

console.log(notes.join('\n'));
console.log('PASS ' + pass + '   FAIL ' + fail);
process.exit(fail ? 1 : 0);
