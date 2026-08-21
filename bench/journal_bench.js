// bench/journal_bench.js — офлайновый стенд журнала ТЗ-05 §9. Сеть не нужна.
//
// Контроль номер один: журнал не имеет права считать вердикт сам (инв. 21,
// 38(1)). Поэтому раздел 1 сверяет КАЖДОЕ поле КАЖДОЙ записи со СВЕЖИМ
// вызовом продакшн-функции на тех же входах — не с сохранённым ожиданием.
// Сохранённое ожидание проверяло бы вчерашнюю копию формулы, то есть ровно то,
// что запрещено.
//
// Фикстуры подаются через шов транспорта в journal/write.js: это единственная
// уступка проверяемости, которую писатель делает, и она не касается математики.
//
// Стенд, ничего не сверивший, обязан упасть и напечатать число сверок
// (инв. 22, 29, 37).
'use strict';
const fs     = require('fs');
const path   = require('path');
const os     = require('os');
const crypto = require('crypto');

const W   = require(path.join(__dirname, '..', 'journal', 'write.js'));
const eng = W.loadEngine(path.join(__dirname, '..', 'index.html'));
const P   = eng.P;

let checks = 0, fails = 0, quiet = false;
function fail(msg) { fails++; if (!quiet) console.log('  FAIL ' + msg); }
function eq(name, got, want) {
    checks++;
    if (!Object.is(got, want)) fail(name + ': got ' + JSON.stringify(got) + ' want ' + JSON.stringify(want));
}
function deq(name, got, want) {
    checks++;
    const a = JSON.stringify(got), b = JSON.stringify(want);
    if (a !== b) fail(name + ':\n    got  ' + a + '\n    want ' + b);
}
function ok(name, cond) { eq(name, !!cond, true); }

function tmp(tag) { return fs.mkdtempSync(path.join(os.tmpdir(), 'jb-' + tag + '-')); }
function hashFile(f) { return crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex'); }
function lines(f) { return W.readLines(f); }

// Детерминированный ГПСЧ: фикстуры обязаны быть воспроизводимы, иначе красный
// прогон нельзя повторить.
function rng(seed) {
    let a = seed >>> 0;
    return function () {
        a |= 0; a = (a + 0x6D2B79F5) | 0;
        let t = Math.imul(a ^ (a >>> 15), 1 | a);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
}

const DAY = 86400000, HOUR = 3600000;

// ── Фикстуры ────────────────────────────────────────────────────────────────

function coinRow(r, sym, i) {
    const base = 0.4 + r() * 300;
    const vol  = 0.004 + r() * 0.028;
    const mn   = base * (0.5 + r() * 0.35);
    const mx   = base * (1.15 + r() * 0.9);
    return {
        symbol: sym,
        up_beta: 0.5 + r(), up_r2: r(), down_beta: 0.5 + r(), down_r2: r(),
        up_beta_90: 0.5 + r(), up_r2_90: r(), down_beta_90: 0.5 + r(), down_r2_90: r(),
        corr_90: r(), tail_beta: 0.5 + r() * 2, tail_r2: r(),
        r7: (r() - 0.5) * 0.4, r14: (r() - 0.5) * 0.6, r30: (r() - 0.5) * 0.9,
        min30: mn * (1 + r() * 0.2), max30: mx * (1 - r() * 0.2),
        vol7: vol * (0.6 + r()), eff14: (r() - 0.5) * 4, vol_ratio: 0.5 + r() * 2,
        price_pos: r() * 100, volatility: vol,
        min_price: mn, max_price: mx, error: false,
        rank: 1 + Math.floor(r() * 200), fdv_mc: r() * 3,
        rank_prev: 1 + Math.floor(r() * 200)
    };
}

// Три режима BTC по построению: marketRegime обязан увидеть каждый.
function btcFor(mode, r) {
    const v = mode === 'stress' ? 0.05 : 0.006 + r() * 0.004;
    const base = { min_price: 40000, max_price: 90000, price_pos: 50,
                   volatility: v, r7: 0, r14: 0, r30: 0.05 };
    if (mode === 'trend-up')   { base.r14 = 0.9; base.r7 = 0.2; }
    if (mode === 'trend-down') { base.r14 = -0.9; base.r7 = -0.2; }
    if (mode === 'range')      { base.r14 = 0.002; base.r7 = 0.001; }
    if (mode === 'stress')     { base.r14 = -0.4; base.r7 = -0.9; }
    return base;
}

function tickerRowFor(row, r, chase) {
    const cur = row.min_price + (row.max_price - row.min_price) * (0.1 + r() * 0.8);
    const spanLo = chase ? cur * (0.80 + r() * 0.06) : cur * (0.95 + r() * 0.04);
    const spanHi = chase ? cur * (1.14 + r() * 0.06) : cur * (1.01 + r() * 0.04);
    return { symbol: null, lastPrice: String(cur),
             priceChangePercent: String((r() - 0.5) * 14),
             quoteVolume: String(1e6 + r() * 4e8),
             highPrice: String(spanHi), lowPrice: String(spanLo),
             count: String(1000 + Math.floor(r() * 500000)),
             bidPrice: String(cur * 0.9995), askPrice: String(cur * 1.0005) };
}

// Полная фикстура одного дня: coeffs + строки тикера по всем парам.
function makeDay(seed, opts) {
    const o = opts || {};
    const r = rng(seed);
    const rows = [];
    P.tokens.forEach(function (t, i) {
        const row = coinRow(r, t.name, i);
        if (o.degrade && i % 2 === 1) row.error = true;
        // Волатильности нет, но флага ошибки бот не поставил: счёт не считается
        // ни на одной стороне, вердикта нет — это «no metrics», а не «error».
        if (o.zeroVol === t.name) row.volatility = 0;
        rows.push(row);
    });
    const coeffs = {
        generated_at: o.gen === undefined ? '2026-08-21T12:41:03Z' : o.gen,
        btc: o.noBtc ? undefined : btcFor(o.mode || 'range', r),
        analysis_data: o.noRows ? [] : rows
    };
    if (o.noBtc) delete coeffs.btc;
    const tick = {};
    const chaseEvery = o.chase === undefined ? 3 : o.chase;
    P.tokens.forEach(function (t, i) {
        const row = rows[i] || coinRow(r, t.name, i);
        const tr = tickerRowFor(row, r, chaseEvery > 0 && i % chaseEvery === 0);
        tr.symbol = t.s;
        if (o.dead === t.s) { tr.count = '0'; }
        if (o.book === t.s) { tr.bidPrice = '0'; tr.askPrice = '0'; }
        if (o.futOk !== true && t.fut) return;      // зеркала спота у fut-пар нет
        if (o.drop === t.s) return;                 // спотовой пары нет в ответе
        tick[t.s] = tr;
    });
    tick.BTCUSDT = { symbol: 'BTCUSDT', lastPrice: '69727', priceChangePercent: '1.2',
                     quoteVolume: '5000000000', highPrice: '70500', lowPrice: '68900',
                     count: '900000', bidPrice: '69726', askPrice: '69728' };
    return { coeffs: coeffs, tick: tick, rows: rows };
}

function symsOf(u) {
    const m = /symbols=([^&]+)/.exec(u);
    return m ? JSON.parse(decodeURIComponent(m[1])) : null;
}
function qs(u, k) {
    const m = new RegExp('[?&]' + k + '=([^&]*)').exec(u);
    return m ? decodeURIComponent(m[1]) : null;
}

// Транспорт: fixtures — функция даты -> makeDay(...); klines — функция
// (pair, startMs, endMs) -> сырые строки Binance или null.
function mkTransport(cfg) {
    return { get: function (u) {
        if (u.indexOf(P.GIST_URL) === 0) {
            if (cfg.gistFail) return Promise.resolve({ ok: false, status: cfg.gistFail, body: null, error: 'planted', bytes: 0 });
            if (cfg.gistGarbage) return Promise.resolve({ ok: false, status: 200, body: null, error: 'нечитаемый JSON: truncated', bytes: 9 });
            return Promise.resolve({ ok: true, status: 200, body: cfg.day().coeffs, error: null, bytes: 1000 });
        }
        if (u.indexOf('/api/v3/ticker/24hr') >= 0) {
            if (cfg.tickerHttp) return Promise.resolve({ ok: false, status: cfg.tickerHttp, body: null, error: null, bytes: 0 });
            const syms = symsOf(u), tick = cfg.day().tick;
            const out = [];
            syms.forEach(function (s) { if (tick[s]) out.push(tick[s]); });
            if (!out.length) return Promise.resolve({ ok: false, status: 400, body: null, error: 'bad symbol', bytes: 0 });
            return Promise.resolve({ ok: true, status: 200, body: out, error: null, bytes: 5000 });
        }
        if (u.indexOf('/api/v3/klines') >= 0) {
            const pair = qs(u, 'symbol');
            const st = qs(u, 'startTime'), en = qs(u, 'endTime');
            const rows = cfg.klines ? cfg.klines(pair, st === null ? null : Number(st), en === null ? null : Number(en)) : null;
            if (!rows) return Promise.resolve({ ok: false, status: 404, body: null, error: 'no series', bytes: 0 });
            return Promise.resolve({ ok: true, status: 200, body: rows, error: null, bytes: rows.length * 100 });
        }
        return Promise.resolve({ ok: false, status: 404, body: null, error: 'unrouted', bytes: 0 });
    } };
}

function candle(t, o, h, l, c) { return [t, String(o), String(h), String(l), String(c), '1', t + HOUR - 1, '1000', 10, '0', '0', '0']; }

function journal(root, day, nowMs, cfg) {
    const c = Object.assign({ day: function () { return day; } }, cfg || {});
    return W.createJournal({ engine: eng, root: root, transport: mkTransport(c),
                             nowMs: nowMs, commit: 'abcdef0123456789' });
}

// Копилка всех записанных корней — раздел 7 проходит по ним целиком.
const ROOTS = [];
function track(r) { ROOTS.push(r); return r; }

// ── 1. Тождество вердикта: запись против свежего вызова продакшна ───────────

async function section1() {
    console.log('=== 1. Тождество вердикта: каждое поле против свежего вызова ===');
    const root = track(tmp('identity'));
    const MODES = ['range', 'trend-up', 'trend-down', 'stress'];
    const DAYS = 220;
    const seen = { mode: {}, action: {}, decOk: {}, geo: {}, rel: {} };
    let records = 0, cmps = 0;

    for (let i = 0; i < DAYS; i++) {
        const mode = MODES[i % MODES.length];
        const day  = makeDay(1000 + i, { mode: mode });
        const nowMs = Date.parse('2026-01-01T13:00:07Z') + i * DAY;
        const j = journal(root, day, nowMs);
        const res = await j.snapshot({});
        if (res.run.status !== 'ok' && res.run.status !== 'partial') {
            fail('день ' + i + ': статус ' + res.run.status + ' ' + res.run.note);
            continue;
        }
        j.appendRun(res.run);

        const tsMs = Date.parse(res.run.ts);
        const btc  = day.coeffs.btc || null;
        const reg  = P.marketRegime(btc);
        seen.mode[reg.mode + (reg.mode === 'trend' ? reg.dir : '')] = true;

        res.lines.forEach(function (L) {
            if (L.k !== 's') return;
            records++;
            const t  = P.tokens.filter(function (x) { return x.name === L.sym; })[0];
            const cd = day.rows.filter(function (x) { return x.symbol === L.sym; })[0];
            const tr = day.tick[t.s];
            const coin = { symbol: t.s, lastPrice: parseFloat(tr.lastPrice),
                           priceChangePercent: parseFloat(tr.priceChangePercent),
                           quoteVolume: parseFloat(tr.quoteVolume),
                           highPrice: parseFloat(tr.highPrice), lowPrice: parseFloat(tr.lowPrice),
                           count: Number(tr.count),
                           bidPrice: parseFloat(tr.bidPrice), askPrice: parseFloat(tr.askPrice) };
            const rc7 = P.residual7(cd, btc);
            const rp  = P.rangePos(cd, coin.lastPrice);

            deq(L.sym + ' cd вербатим', L.cd, cd);
            deq(L.sym + ' btc вербатим', L.btc, btc);
            deq(L.sym + ' reg', L.reg, { mode: reg.mode, dir: reg.dir, eff: reg.eff, z: reg.z, known: reg.known });
            eq(L.sym + ' rp', L.rp, rp === undefined ? null : rp);
            eq(L.sym + ' fp.script', L.fp.script, eng.scriptHash);
            eq(L.sym + ' fp.commit', L.fp.commit, 'abcdef012345');
            eq(L.sym + ' cat.hash', L.cat.hash, eng.catHash);
            cmps += 7;

            [true, false].forEach(function (isLong) {
                const S = isLong ? L.long : L.short;
                const dec = P.leverageDecision(cd, coin.lastPrice, isLong, btc);
                const vd  = P.directionVerdict(cd, t.s, t.name, coin.lastPrice,
                                               coin.priceChangePercent, coin.quoteVolume,
                                               isLong, reg, dec, coin.highPrice, coin.lowPrice,
                                               rc7, tsMs);
                const row = { t: t, coin: coin, cd: cd, dec: dec, vd: vd,
                              sc: P.has(vd.score) ? { score: vd.score, reasons: vd.reasons } : null };
                const tag = L.sym + (isLong ? ' L' : ' S') + ' ';
                seen.action[vd.action] = true;
                seen.decOk[String(dec.ok)] = true;
                seen.geo[String(vd.geo === null)] = true;

                eq(tag + 'rel', S.rel, P.sideRelevant(rp, isLong));
                eq(tag + 'score', S.score, P.has(vd.score) ? vd.score : null);
                eq(tag + 'tier', S.tier, P.has(vd.score) ? P.tierOf(vd.score).n : null);
                eq(tag + 'ch', S.ch, vd.ch);
                eq(tag + 'action', S.action, vd.action);
                eq(tag + 'why', S.why, vd.why);
                eq(tag + 'note', S.note, vd.note === undefined ? null : vd.note);
                eq(tag + 'verdict', S.verdict, P.verdictNote(row));
                eq(tag + 'wait', S.wait, vd.wait === null ? null : vd.wait);
                eq(tag + 'tgt', S.tgt, isLong ? cd.max_price : cd.min_price);
                cmps += 10;
                seen.rel[String(S.rel)] = true;

                if (vd.geo === null) { eq(tag + 'geo null', S.geo, null); cmps++; }
                else {
                    deq(tag + 'geo', S.geo, { rr: vd.geo.rr, reward: vd.geo.reward,
                                              risk: vd.geo.risk, tgtSig: vd.geo.tgtSig,
                                              sd: vd.geo.sd, veto: vd.geo.veto, wait: vd.geo.wait });
                    cmps++;
                }
                deq(tag + 'dec', S.dec, { ok: dec.ok, L: dec.L, binding: dec.binding,
                                          moneyBelowMin: dec.moneyBelowMin,
                                          parts: dec.parts ? { struct: dec.parts.struct, noise: dec.parts.noise,
                                                               btc: dec.parts.btc, money: dec.parts.money } : null });
                deq(tag + 'inv', S.inv, dec.inv ? { dist: dec.inv.dist, price: dec.inv.price,
                                                    dStruct: dec.inv.dStruct, capped: dec.inv.capped,
                                                    floored: dec.inv.floored, sd: dec.inv.sd,
                                                    ref: dec.inv.ref, src: dec.inv.src } : null);
                cmps += 2;

                // Действовавший набор катализаторов — сверка с РЕШЕНИЕМ
                // продакшн-функции, а не с повтором её фильтра.
                const cc = P.catalystCheck(t.name, isLong, tsMs);
                const texts = L.cat.acting.map(function (a) { return a.t; });
                if (cc.veto) { ok(tag + 'вето катализатора внутри acting', texts.indexOf(cc.veto) >= 0); cmps++; }
                if (cc.note) { ok(tag + 'заметка катализатора внутри acting', texts.indexOf(cc.note) >= 0); cmps++; }
                if (!L.cat.acting.length) {
                    eq(tag + 'пустой acting => молчит и catalystCheck', (cc.veto === null && cc.note === null), true);
                    cmps++;
                }
            });
            L.cat.acting.forEach(function (a) {
                const days = (Date.parse(a.d + 'T00:00:00Z') - tsMs) / DAY;
                ok(L.sym + ' acting в окне', days >= -1 && days <= P.CAT_WINDOW_D);
                cmps++;
            });
        });
    }

    console.log('  записей сверено: ' + records + ', сравнений: ' + cmps);
    ok('записей >= 5000', records >= 5000);
    ok('режим range встретился', !!seen.mode.range);
    ok('режим trend вверх встретился', !!seen.mode.trend1);
    ok('режим trend вниз встретился', !!seen.mode['trend-1']);
    ok('режим stress встретился', !!seen.mode.stress);
    ok('action none встретился', !!seen.action.none);
    ok('action trade или wait встретился', !!(seen.action.trade || seen.action.wait));
    ok('dec.ok true встретился', !!seen.decOk.true);
    ok('dec.ok false встретился', !!seen.decOk.false);
    ok('geo null встретился', !!seen.geo.true);
    ok('geo не-null встретился', !!seen.geo.false);
    ok('rel true и false встретились', !!(seen.rel.true && seen.rel.false));
    console.log('  режимы: ' + Object.keys(seen.mode).join(', ')
                + ' | действия: ' + Object.keys(seen.action).join(', '));
    return root;
}

// ── 2. Детерминизм ──────────────────────────────────────────────────────────

async function section2() {
    console.log('=== 2. Детерминизм: два прогона — байт в байт ===');
    const day = makeDay(7, { mode: 'range' });
    const now = Date.parse('2026-05-05T13:00:07Z');
    const a = track(tmp('det-a')), b = track(tmp('det-b'));
    const ra = await journal(a, day, now).snapshot({});
    const rb = await journal(b, day, now).snapshot({});
    const fa = path.join(a, 'data', '2026-05-05.jsonl');
    const fb = path.join(b, 'data', '2026-05-05.jsonl');
    eq('оба файла записаны', ra.wrote && rb.wrote, true);
    eq('байт в байт', fs.readFileSync(fa, 'utf8'), fs.readFileSync(fb, 'utf8'));
    eq('sha256 совпадает', hashFile(fa), hashFile(fb));
    // Порядок ключей — часть тождества: JSON.stringify сохраняет порядок
    // вставки, и запись обязана не зависеть от порядка обхода фикстуры.
    const ka = Object.keys(JSON.parse(fs.readFileSync(fa, 'utf8').split('\n')[0]));
    const kb = Object.keys(JSON.parse(fs.readFileSync(fb, 'utf8').split('\n')[0]));
    deq('порядок ключей', ka, kb);
    deq('порядок ключей — схема §4.1', ka,
        ['k','d','ts','sym','pair','gen','age','px','reg','cd','btc','rp','long','short','cat','fp']);
    const first = JSON.parse(fs.readFileSync(fa, 'utf8').split('\n')[0]);
    deq('порядок ключей px', Object.keys(first.px), ['src','cur','p24','qv','hi','lo','cnt']);
    deq('порядок ключей стороны', Object.keys(first.long),
        ['rel','score','tier','ch','action','why','note','verdict','wait','tgt','geo','dec','inv']);
    deq('порядок ключей inv', Object.keys(first.long.inv),
        ['dist','price','dStruct','capped','floored','sd','ref','src']);
    deq('порядок ключей dec', Object.keys(first.long.dec), ['ok','L','binding','moneyBelowMin','parts']);
    deq('порядок ключей dec.parts', Object.keys(first.long.dec.parts), ['struct','noise','btc','money']);
    deq('порядок ключей reg', Object.keys(first.reg), ['mode','dir','eff','z','known']);
}

// ── 3. Неизменяемость ───────────────────────────────────────────────────────

async function section3() {
    console.log('=== 3. Неизменяемость: второй прогон той же даты ===');
    const day = makeDay(11, { mode: 'trend-up' });
    const now = Date.parse('2026-05-06T13:00:07Z');
    const root = track(tmp('dup'));
    const j1 = journal(root, day, now);
    const r1 = await j1.snapshot({}); j1.appendRun(r1.run);
    const f = path.join(root, 'data', '2026-05-06.jsonl');
    const st0 = fs.statSync(f), h0 = hashFile(f);
    const runs0 = lines(path.join(root, 'runs.jsonl')).length;

    await new Promise(function (r) { setTimeout(r, 15); });
    const j2 = journal(root, day, now + 60000);
    const r2 = await j2.snapshot({}); j2.appendRun(r2.run);
    const st1 = fs.statSync(f), h1 = hashFile(f);

    eq('первый прогон записал', r1.wrote, true);
    eq('второй прогон статус', r2.run.status, 'dup');
    eq('второй прогон не писал', r2.wrote, false);
    eq('содержимое не изменилось', h1, h0);
    eq('mtime не изменился', st1.mtimeMs, st0.mtimeMs);
    eq('размер не изменился', st1.size, st0.size);
    // «Логирует dup» — строка прогона дозаписывается, файлы записи нет.
    const runs = lines(path.join(root, 'runs.jsonl'));
    eq('runs.jsonl вырос ровно на одну строку', runs.length, runs0 + 1);
    eq('последняя строка — dup', runs[runs.length - 1].status, 'dup');
    // Физическая гарантия: writeOnce на существующем пути обязан вернуть false.
    eq('writeOnce на существующем пути', W.writeOnce(f, 'ЧУЖОЙ ТЕКСТ'), false);
    eq('файл после попытки перезаписи', hashFile(f), h0);
}

// ── 4. Арифметика пробелов ──────────────────────────────────────────────────

async function section4() {
    console.log('=== 4. Пробелы: дыра обязана быть подписана ===');
    // 4a. Трёхдневный простой.
    const rootA = track(tmp('gap-a'));
    const d0 = Date.parse('2026-03-01T13:00:07Z');
    let j = journal(rootA, makeDay(21, {}), d0); let r = await j.snapshot({}); j.appendRun(r.run);
    j = journal(rootA, makeDay(22, {}), d0 + 4 * DAY); r = await j.snapshot({}); j.appendRun(r.run);
    const gaps = lines(path.join(rootA, 'runs.jsonl')).filter(function (l) { return l.k === 'g'; });
    eq('ровно три пробела', gaps.length, 3);
    deq('даты пробелов', gaps.map(function (g) { return g.d; }), ['2026-03-02', '2026-03-03', '2026-03-04']);
    deq('причина пробела', gaps.map(function (g) { return g.why; }), ['no run', 'no run', 'no run']);
    eq('найдено — момент заметившего прогона', gaps[0].found, W.iso(d0 + 4 * DAY));

    // 4b. Тридцать дат, среди них провалившийся прогон.
    const rootB = track(tmp('gap-b'));
    const start = Date.parse('2026-04-01T13:00:07Z');
    const FAILED = [6, 7, 17];   // прогоны, у которых недоступен Gist
    const SKIPPED = [11, 12];    // прогонов не было вовсе
    for (let i = 0; i < 30; i++) {
        if (SKIPPED.indexOf(i) >= 0) continue;
        const jj = journal(rootB, makeDay(300 + i, {}), start + i * DAY,
                           FAILED.indexOf(i) >= 0 ? { gistFail: 503 } : null);
        const rr = await jj.snapshot({});
        jj.appendRun(rr.run);
        if (FAILED.indexOf(i) >= 0) eq('день ' + i + ' — провал', rr.run.status, 'fail');
    }
    const snapDates = fs.readdirSync(path.join(rootB, 'data'))
        .filter(function (f) { return /\.jsonl$/.test(f); }).map(function (f) { return f.slice(0, 10); });
    const gapDates = {};
    lines(path.join(rootB, 'runs.jsonl')).forEach(function (l) { if (l.k === 'g') gapDates[l.d] = (gapDates[l.d] || 0) + 1; });
    const uniqGaps = Object.keys(gapDates);
    const first = snapDates.slice().sort()[0], today = W.dayOf(start + 29 * DAY);
    const span = Math.round((W.dayMs(today) - W.dayMs(first)) / DAY) + 1;
    console.log('  снимков ' + snapDates.length + ', пробелов ' + uniqGaps.length + ', календарных дат ' + span);
    eq('тождество §4.4', snapDates.length + uniqGaps.length, span);
    eq('каждый пробел выписан ровно один раз',
        uniqGaps.filter(function (d) { return gapDates[d] !== 1; }).length, 0);
    eq('провалившиеся и пропущенные даты подписаны',
        FAILED.concat(SKIPPED).filter(function (i) { return !gapDates[W.dayOf(start + i * DAY)]; }).length, 0);
    ok('ни один пробел не совпал с записанной датой',
        uniqGaps.every(function (d) { return snapDates.indexOf(d) < 0; }));
}

// ── 5. Тождество покрытия ───────────────────────────────────────────────────

async function section5() {
    console.log('=== 5. Покрытие: строк снимка + пропусков = длине tokens[] ===');
    const cases = [
        { tag: 'обычный', opts: {} },
        { tag: 'половина монет деградирована', opts: { degrade: true } },
        { tag: 'fut-пары доступны', opts: { futOk: true } },
        { tag: 'нет строк бота', opts: { noRows: true } },
        { tag: 'нет блока btc', opts: { noBtc: true } }
    ];
    for (let i = 0; i < cases.length; i++) {
        const root = track(tmp('cov' + i));
        const day = makeDay(500 + i, cases[i].opts);
        const j = journal(root, day, Date.parse('2026-06-0' + (i + 1) + 'T13:00:07Z'));
        const r = await j.snapshot({}); j.appendRun(r.run);
        const s = r.lines.filter(function (l) { return l.k === 's'; }).length;
        const x = r.lines.filter(function (l) { return l.k === 'x'; }).length;
        eq(cases[i].tag + ': s+x = tokens', s + x, P.tokens.length);
        eq(cases[i].tag + ': cov', r.run.cov, s);
        eq(cases[i].tag + ': skip', r.run.skip, x);
        console.log('  ' + cases[i].tag + ': cov ' + s + ' skip ' + x + ' статус ' + r.run.status);
    }
}

// ── 6. Деградации, по одному случаю на каждую ───────────────────────────────

function whyCount(res, why) {
    return res.lines.filter(function (l) { return l.k === 'x' && l.why === why; }).length;
}

async function section6() {
    console.log('=== 6. Деградации: по одному случаю ===');
    const now = Date.parse('2026-07-01T13:00:07Z');

    // 6.1 пустой analysis_data
    let root = track(tmp('deg1'));
    let day = makeDay(601, { noRows: true });
    let r = await journal(root, day, now).snapshot({});
    eq('пустой analysis_data: no bot row у всех спотовых', whyCount(r, 'no bot row'), P.tokens.filter(function (t) { return !t.fut; }).length);
    eq('пустой analysis_data: покрытие 0', r.run.cov, 0);
    eq('пустой analysis_data: статус partial', r.run.status, 'partial');

    // 6.2 нет блока btc — фронт это переживает (инв. 9), обязан и журнал
    root = track(tmp('deg2'));
    day = makeDay(602, { noBtc: true });
    r = await journal(root, day, now).snapshot({});
    ok('нет btc: монеты записаны', r.run.cov > 0);
    const l2 = r.lines.filter(function (l) { return l.k === 's'; })[0];
    deq('нет btc: reg как у продакшна', l2.reg, { mode: 'range', dir: 0, eff: null, z: null, known: false });
    eq('нет btc: btc записан как null', l2.btc, null);

    // 6.3 error:true
    root = track(tmp('deg3'));
    day = makeDay(603, {});
    day.rows[0].error = true;
    r = await journal(root, day, now).snapshot({});
    eq('error:true -> bot error flag', whyCount(r, 'bot error flag'), 1);

    // 6.4 count:0
    root = track(tmp('deg4'));
    day = makeDay(604, { dead: P.tokens[1].s });
    r = await journal(root, day, now).snapshot({});
    eq('count:0 -> dead market', whyCount(r, 'dead market'), 1);

    // 6.5 пустой стакан
    root = track(tmp('deg5'));
    day = makeDay(605, { book: P.tokens[2].s });
    r = await journal(root, day, now).snapshot({});
    eq('пустой стакан -> dead market', whyCount(r, 'dead market'), 1);

    // 6.6 coeffs старше STALE_CRIT_MIN
    root = track(tmp('deg6'));
    const oldGen = W.iso(now - (P.STALE_CRIT_MIN + 60) * 60000);
    day = makeDay(606, { gen: oldGen });
    r = await journal(root, day, now).snapshot({});
    eq('старый coeffs: запись состоялась', r.wrote, true);
    eq('старый coeffs: возраст записан сырым', r.lines.filter(function (l) { return l.k === 's'; })[0].age,
       P.STALE_CRIT_MIN + 60);
    ok('старый coeffs: отмечен в строке прогона', /STALE_CRIT_MIN/.test(r.run.note || ''));

    // 6.7 coeffs без полей, добавленных после 08.08 (инв. 9)
    root = track(tmp('deg7'));
    day = makeDay(607, {});
    const OLD = ['symbol', 'up_beta', 'up_r2', 'down_beta', 'down_r2',
                 'price_pos', 'volatility', 'min_price', 'max_price', 'error'];
    day.rows.forEach(function (row) {
        Object.keys(row).forEach(function (k) { if (OLD.indexOf(k) < 0) delete row[k]; });
    });
    day.coeffs.btc = { min_price: 40000, max_price: 90000, price_pos: 50, volatility: 0.008 };
    r = await journal(root, day, now).snapshot({});
    ok('старый бот: монеты записаны', r.run.cov > 0);
    const l7 = r.lines.filter(function (l) { return l.k === 's'; })[0];
    eq('старый бот: reg.known', l7.reg.known, true);
    eq('старый бот: reg.mode', l7.reg.mode, 'range');
    eq('старый бот: eff отсутствует -> null', l7.reg.eff, null);
    deq('старый бот: cd вербатим, без выдуманных полей', Object.keys(l7.cd).sort(), OLD.slice().sort());

    // 6.10 нет метрик: строка бота есть, ошибки нет, счёта нет ни на одной стороне
    root = track(tmp('deg10'));
    day = makeDay(610, { zeroVol: P.tokens[3].name });
    r = await journal(root, day, now).snapshot({});
    eq('нулевая волатильность -> no metrics', whyCount(r, 'no metrics'), 1);
    eq('нулевая волатильность: монета не потеряна', r.run.cov + r.run.skip, P.tokens.length);

    // 6.11 спотовой пары нет в ответе тикера
    root = track(tmp('deg11'));
    day = makeDay(611, { drop: P.tokens[4].s });
    r = await journal(root, day, now).snapshot({});
    eq('нет строки цены -> no price data', whyCount(r, 'no price data'), 1);
    eq('fut-пары по-прежнему помечены отдельно', whyCount(r, 'futures-only: no spot mirror pair'),
       P.tokens.filter(function (t) { return t.fut; }).length);

    // 6.8 обрезанный JSON у Gist
    root = track(tmp('deg8'));
    r = await journal(root, makeDay(608, {}), now, { gistGarbage: true }).snapshot({});
    eq('обрезанный JSON: статус fail', r.run.status, 'fail');
    eq('обрезанный JSON: ничего не записано', fs.existsSync(path.join(root, 'data')), false);
    ok('обрезанный JSON: причина в note', /coeffs/.test(r.run.note || ''));

    // 6.9 HTTP 400 у тикера -> фолбэк на свечи
    root = track(tmp('deg9'));
    day = makeDay(609, {});
    const kl = {};
    P.tokens.concat([{ s: 'BTCUSDT' }]).forEach(function (t) {
        const tr = day.tick[t.s] || day.tick.BTCUSDT;
        const base = parseFloat(tr.lastPrice);
        const rows = [];
        for (let h = 0; h < 25; h++) {
            const px = base * (0.98 + 0.0016 * h);
            rows.push(candle(now - (25 - h) * HOUR, px, px * 1.005, px * 0.995, px));
        }
        kl[t.s] = rows;
    });
    r = await journal(root, day, now, { tickerHttp: 400, klines: function (p) { return kl[p] || null; } }).snapshot({});
    eq('HTTP 400: источник цен', r.run.px, 'klines');
    ok('HTTP 400: монеты записаны', r.run.cov > 0);
    ok('HTTP 400: фолбэк отмечен в note', /фолбэк/.test(r.run.note || ''));
    const srcs = {};
    r.lines.forEach(function (l) { if (l.k === 's') srcs[l.px.src] = true; });
    deq('источник один на файл', Object.keys(srcs), ['klines']);
    const l9 = r.lines.filter(function (l) { return l.k === 's'; })[0];
    const kw = kl[l9.pair].slice(1);
    eq('свечи: cur = последнее закрытие', l9.px.cur, parseFloat(kl[l9.pair][24][4]));
    eq('свечи: hi = максимум 24 свечей', l9.px.hi, Math.max.apply(null, kw.map(function (c) { return parseFloat(c[2]); })));
    eq('свечи: lo = минимум 24 свечей', l9.px.lo, Math.min.apply(null, kw.map(function (c) { return parseFloat(c[3]); })));
    eq('свечи: cnt = сумма сделок 24 свечей', l9.px.cnt, kw.reduce(function (a, c) { return a + Number(c[8]); }, 0));
}

// ── 6a. Объявленная площадка: три формы одного и того же пропуска ───────────
// ТЗ-07 §3. `fut:true` — объявление Босса (карта §3.14), а не наблюдение,
// поэтому пропуск по такому активу есть ОБЪЯВЛЕННОЕ покрытие и жёстким
// пропуском не считается НИ В ОДНОЙ из трёх форм. Причина при этом
// измеряется: три разные строки, а не одна общая (инв. 37).

const FUT = P.tokens.filter(function (t) { return t.fut; });
const NO_PAIR  = 'futures-only: no spot mirror pair';
const DELISTED = 'futures-only: delisted spot mirror row';
const ALIVE    = 'futures-only: spot mirror row unexpectedly alive';

async function section6a() {
    console.log('=== 6a. fut:true — объявленное покрытие, а не сбой ===');
    const now = Date.parse('2026-07-02T13:00:07Z');
    ok('fut:true активов ровно три', FUT.length === 3);

    // 6a.1 Здоровый день: спот-зеркала у fut-пар нет вовсе.
    let root = track(tmp('fut1'));
    let r = await journal(root, makeDay(621, {}), now).snapshot({});
    eq('нет пары: строка', whyCount(r, NO_PAIR), FUT.length);
    eq('нет пары: делистнутых нет', whyCount(r, DELISTED), 0);
    eq('нет пары: живых нет', whyCount(r, ALIVE), 0);
    eq('нет пары: статус ok', r.run.status, 'ok');
    eq('нет пары: cov', r.run.cov, P.tokens.length - FUT.length);
    eq('нет пары: skip', r.run.skip, FUT.length);
    eq('нет пары: note пуст', r.run.note, null);

    // 6a.2 Зеркало отдаёт ДЕЛИСТНУТУЮ строку: count = 0.
    // Ровно этот случай делал status `partial` каждый день: строка уходила
    // в ветку «dead market», а та поднимает hardSkip.
    root = track(tmp('fut2'));
    r = await journal(root, makeDay(622, { futOk: true, dead: FUT[0].s }), now).snapshot({});
    eq('делистнутая строка: строка', whyCount(r, DELISTED), 1);
    eq('делистнутая строка: НЕ dead market', whyCount(r, 'dead market'), 0);
    eq('делистнутая строка: статус ok', r.run.status, 'ok');
    eq('делистнутая строка: cov', r.run.cov, P.tokens.length - FUT.length);

    // 6a.3 Пустой стакан у fut-пары — та же ветка, что count = 0.
    root = track(tmp('fut3'));
    r = await journal(root, makeDay(623, { futOk: true, book: FUT[1].s }), now).snapshot({});
    eq('пустой стакан у fut: делистнутая строка', whyCount(r, DELISTED), 1);
    eq('пустой стакан у fut: НЕ dead market', whyCount(r, 'dead market'), 0);
    eq('пустой стакан у fut: статус ok', r.run.status, 'ok');

    // 6a.4 Спот-пара fut:true актива ЖИВА. Тихо «нормально» пройти не имеет
    // права: пропуск записывается, hardSkip не растёт, аномалия уходит в
    // runs.jsonl отдельной строкой на каждый символ.
    root = track(tmp('fut4'));
    r = await journal(root, makeDay(624, { futOk: true }), now).snapshot({});
    eq('живая пара: строка', whyCount(r, ALIVE), FUT.length);
    eq('живая пара: статус ok', r.run.status, 'ok');
    eq('живая пара: cov', r.run.cov, P.tokens.length - FUT.length);
    eq('живая пара: skip', r.run.skip, FUT.length);
    FUT.forEach(function (t) {
        ok('живая пара: note называет ' + t.name,
           (r.run.note || '').indexOf('fut:true asset trading on spot: ' + t.name) >= 0);
    });

    // 6a.5 Все три формы в ОДНОМ прогоне: пары нет, строка мертва, строка жива.
    root = track(tmp('fut5'));
    r = await journal(root, makeDay(625, { futOk: true, dead: FUT[0].s, drop: FUT[1].s }), now).snapshot({});
    eq('три формы: нет пары', whyCount(r, NO_PAIR), 1);
    eq('три формы: делистнута', whyCount(r, DELISTED), 1);
    eq('три формы: жива', whyCount(r, ALIVE), 1);
    eq('три формы: статус ok', r.run.status, 'ok');
    eq('три формы: skip', r.run.skip, FUT.length);
    eq('три формы: note ровно про живую',
       r.run.note, 'fut:true asset trading on spot: ' + FUT[2].name);

    // 6a.6 Контроль §3.3: спотовый путь не тронут. Мёртвая СПОТОВАЯ пара
    // по-прежнему жёсткий пропуск, и статус обязан упасть в partial —
    // иначе правка съела бы ту самую деградацию, ради которой поле живёт.
    const spot0 = P.tokens.filter(function (t) { return !t.fut; })[0];
    root = track(tmp('fut6'));
    r = await journal(root, makeDay(626, { futOk: true, dead: spot0.s }), now).snapshot({});
    eq('спот мёртв: dead market', whyCount(r, 'dead market'), 1);
    eq('спот мёртв: статус partial', r.run.status, 'partial');
    eq('спот мёртв: живые fut на статус не влияют', whyCount(r, ALIVE), FUT.length);
}

// ── 7. Соответствие схеме ───────────────────────────────────────────────────

const REQ = {
    s: ['k','d','ts','sym','pair','gen','age','px','reg','cd','btc','rp','long','short','cat','fp'],
    x: ['k','d','sym','why'],
    r: ['k','ts','d','status','cov','skip','px','gen','age','resolved','note'],
    g: ['k','d','why','found'],
    oh: ['k','d','h','asof','src','btc'],
    o: ['k','d','h','sym','p0','p1','hi','lo','long','short']
};
const WHYS = ['futures-only: no spot mirror pair',
              'futures-only: delisted spot mirror row',
              'futures-only: spot mirror row unexpectedly alive',
              'no price data', 'bot error flag',
              'no bot row', 'dead market', 'no metrics'];
const STATUSES = ['ok', 'partial', 'dup', 'fail'];
const seenWhy = {}, seenK = {};

function walk(v, tag) {
    if (v === null) return;
    if (typeof v === 'number') { checks++; if (!isFinite(v)) fail(tag + ': не конечное число'); return; }
    if (typeof v === 'undefined') { checks++; fail(tag + ': undefined'); return; }
    if (Array.isArray(v)) { v.forEach(function (x, i) { walk(x, tag + '[' + i + ']'); }); return; }
    if (typeof v === 'object') { Object.keys(v).forEach(function (k) { walk(v[k], tag + '.' + k); }); }
}

function section7() {
    console.log('=== 7. Схема: каждая строка каждого записанного файла ===');
    let files = 0, rows = 0;
    ROOTS.forEach(function (root) {
        ['data', 'out'].forEach(function (sub) {
            const dir = path.join(root, sub);
            if (!fs.existsSync(dir)) return;
            fs.readdirSync(dir).forEach(function (f) { checkFile(path.join(dir, f)); files++; });
        });
        const runs = path.join(root, 'runs.jsonl');
        if (fs.existsSync(runs)) { checkFile(runs); files++; }
    });
    function checkFile(f) {
        const text = fs.readFileSync(f, 'utf8');
        checks++; if (text.length && text[text.length - 1] !== '\n') fail(f + ': файл не оканчивается \\n');
        checks++; if (/\r/.test(text)) fail(f + ': CR в файле');
        checks++; if (/[:,\[]\s*NaN/.test(text)) fail(f + ': NaN в тексте');
        checks++; if (/[:,\[]\s*undefined/.test(text)) fail(f + ': undefined в тексте');
        text.split('\n').filter(function (s) { return s !== ''; }).forEach(function (s, i) {
            rows++;
            let L;
            checks++;
            try { L = JSON.parse(s); } catch (e) { fail(f + ':' + (i + 1) + ' не JSON'); return; }
            checks++; if (!REQ[L.k]) { fail(f + ':' + (i + 1) + ' неизвестный k=' + L.k); return; }
            seenK[L.k] = true;
            if (L.k === 'x') seenWhy[L.why] = true;
            deq(f + ':' + (i + 1) + ' ключи', Object.keys(L), REQ[L.k]);
            checks++; if (!/^\d{4}-\d{2}-\d{2}$/.test(L.d) || !isFinite(W.dayMs(L.d))) fail(f + ':' + (i + 1) + ' d не дата');
            if (L.k === 'x') { checks++; if (WHYS.indexOf(L.why) < 0) fail(f + ':' + (i + 1) + ' причина вне словаря: ' + L.why); }
            if (L.k === 'r') { checks++; if (STATUSES.indexOf(L.status) < 0) fail(f + ':' + (i + 1) + ' статус вне словаря'); }
            if (L.k === 'o') {
                [L.long, L.short].forEach(function (S, si) {
                    checks++;
                    if ([null, 'tgt', 'stop', 'tie'].indexOf(S.first) < 0) fail(f + ':' + (i + 1) + ' first вне словаря');
                    deq(f + ':' + (i + 1) + ' ключи стороны ' + si, Object.keys(S), ['tgt', 'stop', 'wait', 'first']);
                });
            }
            walk(L, path.basename(f) + ':' + (i + 1));
        });
    }
    console.log('  файлов ' + files + ', строк ' + rows);
    ok('файлы проверялись', files > 0);
    ok('строки проверялись', rows > 0);
    // Причина пропуска, ни разу не встретившаяся, — это ветка писателя,
    // которую стенд не исполнил, то есть контролем не является (инв. 22, 37).
    WHYS.forEach(function (w) { ok('причина исполнена стендом: ' + w, !!seenWhy[w]); });
    deq('словарь k исчерпан', Object.keys(seenK).sort(), Object.keys(REQ).sort());
    console.log('  причины пропуска: ' + Object.keys(seenWhy).length + '/' + WHYS.length
                + ', виды строк: ' + Object.keys(seenK).sort().join(', '));
}

// ── 8. Исход: первое касание ────────────────────────────────────────────────

// Снимок собирается вручную РОВНО для резолвера: он не вызывает ни одной
// продакшн-функции, а читает уровни из записи. Так проверяются все ветки
// (tie / ни одного касания / обе стороны), которых случайная фикстура не даёт.
function handSnapshot(root, d, tsMs, sides) {
    const line = { k: 's', d: d, ts: W.iso(tsMs), sym: 'TST', pair: 'TSTUSDT',
                   gen: W.iso(tsMs - 600000), age: 10,
                   px: { src: 'ticker', cur: 100, p24: 0, qv: 1e6, hi: 101, lo: 99, cnt: 10 },
                   reg: { mode: 'range', dir: 0, eff: 0, z: 0, known: true },
                   cd: { symbol: 'TST' }, btc: null, rp: 50,
                   long: sides.long, short: sides.short,
                   cat: { acting: [], hash: eng.catHash },
                   fp: { script: eng.scriptHash, commit: 'abcdef012345' } };
    W.writeOnce(path.join(root, 'data', d + '.jsonl'), JSON.stringify(line) + '\n');
    return line;
}
function side(tgt, stop, wait) {
    return { rel: true, score: 50, tier: 'Средний', ch: 'возврат', action: 'trade',
             why: '', note: null, verdict: '', wait: wait, tgt: tgt,
             geo: { rr: 2, reward: 0.1, risk: 0.05, tgtSig: 2, sd: 0.02, veto: [], wait: wait },
             dec: { ok: true, L: 3, binding: 'структура', moneyBelowMin: false,
                    parts: { struct: 3, noise: 4, btc: 5, money: 6 } },
             inv: { dist: 0.05, price: stop, dStruct: 0.05, capped: false, floored: false,
                    sd: 0.02, ref: 95, src: 'мин30' } };
}

// path(h) -> {o,h,l,c} для каждого часа окна.
function pathSeries(startMs, hours, fn) {
    const rows = [];
    for (let h = 0; h <= hours; h++) {
        const c = fn(h);
        rows.push(candle(startMs + h * HOUR, c.o, c.h, c.l, c.c));
    }
    return rows;
}

async function section8() {
    console.log('=== 8. Исход: час первого касания, tie и пустой путь ===');
    const tsMs = Date.parse('2026-02-01T13:00:07Z');
    const H = 7, hours = H * 24;

    // 8a. Лонг: цель на 12-м часу, стоп не тронут. Шорт: стоп на 5-м часу.
    {
        const root = track(tmp('out-a'));
        handSnapshot(root, '2026-02-01', tsMs,
            { long: side(120, 90, 95), short: side(80, 110, 105) });
        const series = pathSeries(tsMs, hours, function (h) {
            if (h === 5)  return { o: 100, h: 111, l: 100, c: 101 };   // шорт-стоп 110 и лонг-ожидание 95? нет
            if (h === 12) return { o: 101, h: 121, l: 101, c: 110 };   // цель лонга 120
            return { o: 100, h: 100.5, l: 99.5, c: 100 };
        });
        const j = journal(root, null, tsMs + H * DAY, { klines: function () { return series; } });
        const done = await j.resolve(W.dayOf(tsMs + H * DAY));
        eq('8a: файл записан', done.length, 1);
        const L = lines(path.join(root, 'out', '2026-02-01-h7.jsonl'));
        eq('8a: заголовок BTC', L[0].k, 'oh');
        eq('8a: asof — конец окна по часу', L[0].asof, W.isoHour(tsMs + H * DAY));
        eq('8a: p0 перенесён из снимка', L[1].p0, 100);
        eq('8a: лонг цель — 12-й час', L[1].long.tgt, W.iso(tsMs + 12 * HOUR));
        eq('8a: лонг стоп не тронут', L[1].long.stop, null);
        eq('8a: лонг первым — цель', L[1].long.first, 'tgt');
        eq('8a: шорт стоп — 5-й час', L[1].short.stop, W.iso(tsMs + 5 * HOUR));
        eq('8a: шорт цель не тронута', L[1].short.tgt, null);
        eq('8a: шорт первым — стоп', L[1].short.first, 'stop');
        eq('8a: шорт ожидание 105 — 5-й час', L[1].short.wait, W.iso(tsMs + 5 * HOUR));
        eq('8a: лонг ожидание 95 не тронуто', L[1].long.wait, null);
        eq('8a: p1 — закрытие последней свечи', L[1].p1, 100);
    }

    // 8b. Обе цены внутри ОДНОЙ свечи -> tie, и это записывается, а не гадается.
    {
        const root = track(tmp('out-b'));
        handSnapshot(root, '2026-02-01', tsMs, { long: side(120, 90, null), short: side(80, 110, null) });
        const series = pathSeries(tsMs, hours, function (h) {
            if (h === 9) return { o: 100, h: 125, l: 75, c: 100 };   // накрывает все четыре уровня
            return { o: 100, h: 100.5, l: 99.5, c: 100 };
        });
        const j = journal(root, null, tsMs + H * DAY, { klines: function () { return series; } });
        await j.resolve(W.dayOf(tsMs + H * DAY));
        const L = lines(path.join(root, 'out', '2026-02-01-h7.jsonl'));
        eq('8b: лонг tie', L[1].long.first, 'tie');
        eq('8b: шорт tie', L[1].short.first, 'tie');
        eq('8b: лонг цель — 9-й час', L[1].long.tgt, W.iso(tsMs + 9 * HOUR));
        eq('8b: лонг стоп — 9-й час', L[1].long.stop, W.iso(tsMs + 9 * HOUR));
    }

    // 8c. Путь, не тронувший ничего.
    {
        const root = track(tmp('out-c'));
        handSnapshot(root, '2026-02-01', tsMs, { long: side(120, 90, 95), short: side(80, 110, 105) });
        const series = pathSeries(tsMs, hours, function () { return { o: 100, h: 100.5, l: 99.5, c: 100 }; });
        const j = journal(root, null, tsMs + H * DAY, { klines: function () { return series; } });
        await j.resolve(W.dayOf(tsMs + H * DAY));
        const L = lines(path.join(root, 'out', '2026-02-01-h7.jsonl'));
        deq('8c: лонг всё null', L[1].long, { tgt: null, stop: null, wait: null, first: null });
        deq('8c: шорт всё null', L[1].short, { tgt: null, stop: null, wait: null, first: null });
    }

    // 8d. Резолвер на настоящем снимке конвейера: уровни берутся из записи и
    //     НЕ пересчитываются — цель, пересчитанная по сегодняшнему cd, была бы
    //     другой целью.
    {
        const root = track(tmp('out-d'));
        const day = makeDay(880, { mode: 'range' });
        const now = Date.parse('2026-02-10T13:00:07Z');
        const j1 = journal(root, day, now);
        const r1 = await j1.snapshot({}); j1.appendRun(r1.run);
        const snap = r1.lines.filter(function (l) { return l.k === 's'; })[0];
        const tgt = snap.long.tgt;
        const series = pathSeries(now, hours, function (h) {
            if (h === 30) return { o: snap.px.cur, h: tgt * 1.001, l: snap.px.cur, c: snap.px.cur };
            return { o: snap.px.cur, h: snap.px.cur, l: snap.px.cur, c: snap.px.cur };
        });
        const j2 = journal(root, day, now + H * DAY, { klines: function () { return series; } });
        const done = await j2.resolve(W.dayOf(now + H * DAY));
        eq('8d: один файл исхода', done.length, 1);
        eq('8d: число строк монет', done[0].n, r1.run.cov);
        const L = lines(path.join(root, 'out', '2026-02-10-h7.jsonl'));
        const rec = L.filter(function (l) { return l.k === 'o' && l.sym === snap.sym; })[0];
        eq('8d: p0 равен px.cur снимка', rec.p0, snap.px.cur);
        eq('8d: цель тронута на 30-м часу', rec.long.tgt, W.iso(now + 30 * HOUR));
    }

    // 8e. Потолок в четыре файла за прогон (§6).
    {
        const root = track(tmp('out-cap'));
        const base = Date.parse('2026-02-01T13:00:07Z');
        for (let i = 0; i < 5; i++) {
            handSnapshot(root, W.dayOf(base + i * DAY), base + i * DAY,
                         { long: side(120, 90, null), short: side(80, 110, null) });
        }
        const later = base + 40 * DAY;
        const j = journal(root, null, later, { klines: function (p, st, en) {
            return pathSeries(st, Math.round((en - st) / HOUR), function () { return { o: 100, h: 100, l: 100, c: 100 }; });
        } });
        const done = await j.resolve(W.dayOf(later));
        eq('8e: не больше четырёх файлов за прогон', done.length, W.OUT_CAP);
        deq('8e: старые первыми', done.map(function (x) { return x.d + '-h' + x.h; }),
            [W.dayOf(base) + '-h7', W.dayOf(base) + '-h14',
             W.dayOf(base + DAY) + '-h7', W.dayOf(base + DAY) + '-h14']);
    }

    // 8f. Провал загрузки не оставляет частичного файла.
    {
        const root = track(tmp('out-fail'));
        handSnapshot(root, '2026-02-01', tsMs, { long: side(120, 90, null), short: side(80, 110, null) });
        const j = journal(root, null, tsMs + H * DAY, { klines: function () { return null; } });
        const done = await j.resolve(W.dayOf(tsMs + H * DAY));
        eq('8f: ничего не разрешено', done.length, 0);
        eq('8f: файла нет — следующий прогон повторит',
            fs.existsSync(path.join(root, 'out', '2026-02-01-h7.jsonl')), false);
    }
}

// ── 9. Отсутствие заглядывания вперёд ───────────────────────────────────────

async function section9() {
    console.log('=== 9. Заглядывание вперёд: обрезанная серия = полной ===');
    const tsMs = Date.parse('2026-02-01T13:00:07Z');
    const H = 7, hours = H * 24;
    const sides = { long: side(120, 90, 95), short: side(80, 110, 105) };
    function mkSeries(extraHours) {
        return pathSeries(tsMs, hours + extraHours, function (h) {
            if (h === 20) return { o: 100, h: 121, l: 100, c: 105 };
            if (h > hours) return { o: 100, h: 300, l: 10, c: 100 };   // будущее, видеть его нельзя
            return { o: 100, h: 100.5, l: 99.5, c: 100 };
        });
    }
    const rootT = track(tmp('look-t')), rootF = track(tmp('look-f'));
    handSnapshot(rootT, '2026-02-01', tsMs, sides);
    handSnapshot(rootF, '2026-02-01', tsMs, sides);
    const jt = journal(rootT, null, tsMs + H * DAY, { klines: function () { return mkSeries(0); } });
    const jf = journal(rootF, null, tsMs + H * DAY, { klines: function () { return mkSeries(72); } });
    await jt.resolve(W.dayOf(tsMs + H * DAY));
    await jf.resolve(W.dayOf(tsMs + H * DAY));
    const a = fs.readFileSync(path.join(rootT, 'out', '2026-02-01-h7.jsonl'), 'utf8');
    const b = fs.readFileSync(path.join(rootF, 'out', '2026-02-01-h7.jsonl'), 'utf8');
    eq('обрезанная и полная серии дают один файл', a, b);
    const L = JSON.parse(b.split('\n')[1]);
    eq('высшая точка окна не заражена будущим', L.hi, 121);
    eq('низшая точка окна не заражена будущим', L.lo, 99.5);
    eq('первое касание внутри окна', L.long.tgt, W.iso(tsMs + 20 * HOUR));
}

// ── 10. Закрытая на отказ проверка ──────────────────────────────────────────

function section10() {
    console.log('=== 10. Стенд обязан уметь падать ===');
    const before = fails;
    quiet = true;
    eq('подсаженное расхождение', 1, 2);
    deq('подсаженное расхождение объекта', { a: 1 }, { a: 2 });
    quiet = false;
    const detected = (fails === before + 2);
    fails = before; checks -= 2;
    ok('сравнитель ловит неверный ответ', detected);
    console.log('  подсаженные расхождения замечены: ' + detected);
}

// ── Прогон ──────────────────────────────────────────────────────────────────

(async function () {
    console.log('journal_bench: движок ' + eng.scriptHash + ', реестр ' + eng.catHash
                + ', монет ' + P.tokens.length + '\n');
    await section1();
    await section2();
    await section3();
    await section4();
    await section5();
    await section6();
    await section6a();
    await section8();
    await section9();
    section7();
    section10();

    console.log('\n--- проверок: ' + checks + '  провалов: ' + fails + ' ---');
    if (checks === 0) { console.log('FAIL стенд не сверил ничего'); process.exit(1); }
    process.exit(fails === 0 ? 0 : 1);
})().catch(function (e) {
    console.log('FAIL стенд упал: ' + (e && e.stack || e));
    process.exit(1);
});
