#!/usr/bin/env node
// journal/write.js — прибор ТЗ-05 §3.13: «вход → вердикт доски → факт».
//
// Вердикт НЕ считается здесь. Он ИСПОЛНЯЕТСЯ: <script> вырезается из
// index.html, запускается в vm и продакшн-функции вызываются по имени
// (инв. 21, инв. 38(1)). Второй реализации любого правила, порога или формулы
// в этом файле нет и быть не может — всякое число вердикта приходит из вызова.
//
// Запись физически неизменяема (инв. 38(2)): файлы записи создаются через
// link() и падают с EEXIST, если уже существуют. Ни один существующий файл
// записи не открывается на изменение и не удаляется. Дозаписывается ровно
// один файл — журнал прогонов runs.jsonl, он для того и заведён (§4.3).
//
// Режимы: --probe · --dry-run · --snapshot · --resolve · без флага (snapshot+resolve).
'use strict';

const fs     = require('fs');
const path   = require('path');
const vm     = require('vm');
const os     = require('os');
const crypto = require('crypto');
const https  = require('https');

const REPO = path.join(__dirname, '..');

// Зеркала Binance. Боевые хосты отвечают 451 из GitHub Actions (инв. 24),
// поэтому здесь именно зеркало, а не api.binance.com. Это НЕ копия
// продакшн-константы: продакшн ходит на другой хост и меняться не должен.
const MIRROR   = 'https://data-api.binance.vision';
const HORIZONS = [7, 14];
const OUT_CAP  = 4;      // §6: не больше четырёх файлов исхода за прогон
const KLIMIT   = 25;     // §5.3: 24 закрытых часа + текущий

// ── Мелочи ──────────────────────────────────────────────────────────────────

// Единственная нормализация чисел в файле. Нужна не для округления (его нет),
// а для §4: NaN и Infinity в записи запрещены, отсутствие пишется null.
function fin(v) { return (typeof v === 'number' && isFinite(v)) ? v : null; }
function or(v)  { return v === undefined ? null : v; }

function iso(ms)     { return new Date(ms).toISOString().replace(/\.\d{3}Z$/, 'Z'); }
function isoHour(ms) { return new Date(Math.floor(ms / 3600000) * 3600000).toISOString().replace(/\.\d{3}Z$/, 'Z'); }
function dayOf(ms)   { return new Date(ms).toISOString().slice(0, 10); }
function dayMs(d)    { return Date.parse(d + 'T00:00:00Z'); }
function addDays(d, n) { return dayOf(dayMs(d) + n * 86400000); }
function sha16(s)    { return crypto.createHash('sha256').update(s, 'utf8').digest('hex').slice(0, 16); }

// Даты строго между a и b, обе исключены.
function between(a, b) {
    const out = [];
    for (let t = dayMs(a) + 86400000; t < dayMs(b); t += 86400000) out.push(dayOf(t));
    return out;
}

function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); }

// Запись файла-записи. link() атомарен и падает EEXIST на существующем пути:
// неизменяемость сделана физической, а не обещанной (инв. 38(2)). Оборванная
// запись не может оставить половину строки — до link() файл ещё временный.
// Возвращает false, если файл уже есть; бросает на любой другой ошибке.
function writeOnce(file, text) {
    ensureDir(path.dirname(file));
    if (fs.existsSync(file)) return false;
    const tmp = file + '.tmp-' + process.pid + '-' + Date.now();
    fs.writeFileSync(tmp, text, { encoding: 'utf8', flag: 'wx' });
    try {
        fs.linkSync(tmp, file);
    } catch (e) {
        fs.unlinkSync(tmp);
        if (e.code === 'EEXIST') return false;
        throw e;
    }
    fs.unlinkSync(tmp);
    return true;
}

function appendLine(file, obj) {
    ensureDir(path.dirname(file));
    fs.appendFileSync(file, JSON.stringify(obj) + '\n', 'utf8');
}

function readLines(file) {
    if (!fs.existsSync(file)) return [];
    return fs.readFileSync(file, 'utf8').split('\n')
        .filter(function (s) { return s.trim() !== ''; })
        .map(function (s) { return JSON.parse(s); });
}

// ── Движок: исполнение продакшн-скрипта ─────────────────────────────────────

function extractScript(html) {
    const opens = (html.match(/<script\b/g) || []).length;
    if (opens !== 1) throw new Error('index.html: ожидался ровно один <script>, найдено ' + opens);
    const a = html.indexOf('<script>');
    const b = html.lastIndexOf('</script>');
    if (a < 0 || b <= a) throw new Error('index.html: блок <script> не найден');
    return html.slice(a + '<script>'.length, b);
}

// Исходный текст литерала `var NAME = {...}` / `[...]`. Нужен только для
// отпечатка: cat.hash обязан идентифицировать ВЕРСИЮ реестра, а не его
// значение после разбора.
function literalOf(src, name) {
    const m = new RegExp('var\\s+' + name + '\\s*=\\s*').exec(src);
    if (!m) throw new Error('index.html: `var ' + name + '` не найден');
    const i = m.index + m[0].length;
    const open = src[i];
    if (open !== '{' && open !== '[') throw new Error('index.html: `' + name + '` не литерал');
    const close = open === '{' ? '}' : ']';
    let depth = 0, q = null, esc = false;
    for (let j = i; j < src.length; j++) {
        const c = src[j];
        if (esc) { esc = false; continue; }
        if (q) { if (c === '\\') esc = true; else if (c === q) q = null; continue; }
        if (c === '"' || c === '\'') { q = c; continue; }
        if (c === open) depth++;
        else if (c === close) { depth--; if (depth === 0) return src.slice(i, j + 1); }
    }
    throw new Error('index.html: незакрытый литерал ' + name);
}

// Имена, которые журнал читает ИЗ КОНТЕКСТА и не перепечатывает (инв. 20).
// Список проверяется на старте: переименование в index.html обязано ронять
// журнал громко, а не тихо менять смысл записи.
const NEED = [
    'GIST_URL', 'STALE_CRIT_MIN', 'CAT_WINDOW_D', 'TIER_MIN', 'CATALYSTS', 'tokens',
    'has', 'marketRegime', 'rangePos', 'sideRelevant', 'residual7',
    'leverageDecision', 'directionVerdict', 'tierOf', 'verdictNote'
];

function loadEngine(htmlPath) {
    const file = htmlPath || path.join(REPO, 'index.html');
    const html = fs.readFileSync(file, 'utf8');
    const src  = extractScript(html);

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

    for (let i = 0; i < NEED.length; i++) {
        if (sandbox[NEED[i]] === undefined) {
            throw new Error('index.html: `' + NEED[i] + '` отсутствует — журнал не имеет права угадывать');
        }
    }
    return {
        P: sandbox,
        src: src,
        scriptHash: sha16(src),
        catHash: sha16(literalOf(src, 'CATALYSTS'))
    };
}

// ── Транспорт ───────────────────────────────────────────────────────────────
// Единственный шов, который писатель делает ради проверяемости (§9): стенду
// нужен весь конвейер без сети. Продакшн-путь — стандартная библиотека.

function httpGet(u, redirects) {
    return new Promise(function (resolve) {
        const req = https.get(u, { timeout: 30000 }, function (res) {
            const code = res.statusCode;
            if (code >= 300 && code < 400 && res.headers.location && (redirects || 0) < 4) {
                res.resume();
                return resolve(httpGet(new URL(res.headers.location, u).toString(), (redirects || 0) + 1));
            }
            let buf = '';
            res.setEncoding('utf8');
            res.on('data', function (c) { buf += c; });
            res.on('end', function () {
                const good = code >= 200 && code < 300;
                let body = null, err = null;
                // Разбирать тело неуспешного ответа незачем: «нечитаемый JSON»
                // поверх http 403 прячет настоящую причину за следствием.
                if (good) {
                    try { body = JSON.parse(buf); }
                    catch (e) { err = 'нечитаемый JSON: ' + e.message; }
                }
                resolve({ ok: good && err === null,
                          status: code, body: body, error: err,
                          bytes: Buffer.byteLength(buf) });
            });
        });
        req.on('timeout', function () { req.destroy(new Error('timeout')); });
        req.on('error', function (e) {
            resolve({ ok: false, status: 0, body: null, error: e.code || e.message, bytes: 0 });
        });
    });
}

const httpTransport = { get: function (u) { return httpGet(u, 0); } };

// ── Прибор ──────────────────────────────────────────────────────────────────

function createJournal(opts) {
    const engine    = opts.engine;
    const P         = engine.P;
    const root      = opts.root;
    const transport = opts.transport || httpTransport;
    const commit    = (opts.commit || '').slice(0, 12) || null;
    const gapMs     = opts.gapMs === undefined ? 0 : opts.gapMs;
    // tsMs берётся из записанного ts, а не из сырых часов: запись обязана
    // воспроизводиться из самой себя (§4.1, окно катализатора).
    const tsMs      = Date.parse(iso(opts.nowMs === undefined ? Date.now() : opts.nowMs));

    const DATA = path.join(root, 'data');
    const OUT  = path.join(root, 'out');
    const RUNS = path.join(root, 'runs.jsonl');

    function sleep(ms) { return ms > 0 ? new Promise(function (r) { setTimeout(r, ms); }) : Promise.resolve(); }

    // ── Цены ────────────────────────────────────────────────────────────────
    function tickerUrl(syms) {
        return MIRROR + '/api/v3/ticker/24hr?symbols=' + encodeURIComponent(JSON.stringify(syms));
    }
    function klineUrl(pair, limit) {
        return MIRROR + '/api/v3/klines?symbol=' + pair + '&interval=1h&limit=' + limit;
    }

    function spotPairs() {
        const syms = ['BTCUSDT'];
        P.tokens.forEach(function (t) { if (!t.fut && syms.indexOf(t.s) === -1) syms.push(t.s); });
        return syms;
    }

    // Свеча -> {t, o, h, l, c, qv, n}. Формат Binance фиксирован позициями.
    function kline(row) {
        return { t: Number(row[0]), o: parseFloat(row[1]), h: parseFloat(row[2]),
                 l: parseFloat(row[3]), c: parseFloat(row[4]),
                 qv: parseFloat(row[7]), n: Number(row[8]) };
    }

    // Фолбэк §5.3: документированное приближение суточного окна биржи.
    // Именно поэтому px.src пишется в каждой строке.
    function fromKlines(pair, rows) {
        if (!Array.isArray(rows) || rows.length < 2) return null;
        const ks = rows.map(kline);
        const w  = ks.slice(Math.max(0, ks.length - 24));
        const last = ks[ks.length - 1];
        let hi = -Infinity, lo = Infinity, qv = 0, cnt = 0;
        w.forEach(function (k) {
            if (k.h > hi) hi = k.h;
            if (k.l < lo) lo = k.l;
            qv += k.qv; cnt += k.n;
        });
        const base = w[0].o;
        return { symbol: pair, lastPrice: last.c,
                 priceChangePercent: (base > 0 ? (last.c / base - 1) * 100 : null),
                 quoteVolume: qv, highPrice: hi, lowPrice: lo, count: cnt,
                 bidPrice: null, askPrice: null };
    }

    function fromTicker(row) {
        return { symbol: row.symbol, lastPrice: parseFloat(row.lastPrice),
                 priceChangePercent: parseFloat(row.priceChangePercent),
                 quoteVolume: parseFloat(row.quoteVolume),
                 highPrice: parseFloat(row.highPrice), lowPrice: parseFloat(row.lowPrice),
                 count: Number(row.count),
                 bidPrice: parseFloat(row.bidPrice), askPrice: parseFloat(row.askPrice) };
    }

    // Один источник на прогон (§5.3): смешивать тикер и свечи внутри одного
    // файла запрещено, иначе строки одного дня несравнимы между собой.
    async function fetchPrices() {
        const px = {};
        const spot = spotPairs();
        const r = await transport.get(tickerUrl(spot));
        if (r.ok && Array.isArray(r.body)) {
            r.body.forEach(function (row) { if (row && row.symbol) px[row.symbol] = fromTicker(row); });
            // fut:true пробуются ВСЕГДА и только поштучно: неподтверждённый
            // символ внутри ?symbols= роняет весь тикер (инв. 5).
            for (const t of P.tokens) {
                if (!t.fut) continue;
                await sleep(gapMs);
                const one = await transport.get(tickerUrl([t.s]));
                if (one.ok && Array.isArray(one.body) && one.body[0] && one.body[0].symbol) {
                    px[t.s] = fromTicker(one.body[0]);
                }
            }
            return { src: 'ticker', px: px, note: null };
        }
        const why = 'тикер недоступен (' + (r.error || 'http ' + r.status) + ')';
        for (const t of P.tokens.concat([{ s: 'BTCUSDT' }])) {
            await sleep(gapMs);
            const k = await transport.get(klineUrl(t.s, KLIMIT));
            if (!k.ok) continue;
            const row = fromKlines(t.s, k.body);
            if (row) px[t.s] = row;
        }
        return { src: 'klines', px: px, note: why };
    }

    // ── Снимок ──────────────────────────────────────────────────────────────

    // Подмножество CATALYSTS[sym] внутри живого окна на момент tsMs. Это НЕ
    // повторение catalystCheck: его РЕШЕНИЕ уже записано в why/note, здесь
    // только членство в окне, и порог CAT_WINDOW_D читается из контекста.
    function acting(sym) {
        const list = P.CATALYSTS[sym];
        const out = [];
        if (!list || !list.length) return out;
        for (let i = 0; i < list.length; i++) {
            const c = list[i];
            const t = Date.parse(c.d + 'T00:00:00Z');
            if (!isFinite(t)) continue;
            const days = (t - tsMs) / 86400000;
            if (days < -1 || days > P.CAT_WINDOW_D) continue;
            out.push({ d: c.d, dir: c.dir, t: c.t });
        }
        return out;
    }

    // Все выходы блока — из вызовов. Ни одного числа, посчитанного здесь.
    function sideBlock(cd, token, coin, isLong, reg, btcStats, rc7) {
        const cur  = coin.lastPrice, p24 = coin.priceChangePercent;
        const qv   = coin.quoteVolume, hi = coin.highPrice, lo = coin.lowPrice;
        const dec  = P.leverageDecision(cd, cur, isLong, btcStats);
        const vd   = P.directionVerdict(cd, token.s, token.name, cur, p24, qv, isLong,
                                        reg, dec, hi, lo, rc7, tsMs);
        const rp   = P.rangePos(cd, cur);
        const tier = P.has(vd.score) ? P.tierOf(vd.score).n : null;
        const row  = { t: token, coin: coin, cd: cd, dec: dec, vd: vd,
                       sc: P.has(vd.score) ? { score: vd.score, reasons: vd.reasons } : null };
        const verdict = P.verdictNote(row);
        const g = vd.geo, iv = dec.inv;
        return {
            rel: P.sideRelevant(rp, isLong),
            score: fin(vd.score),
            tier: tier,
            ch: or(vd.ch),
            action: or(vd.action),
            why: or(vd.why),
            note: or(vd.note),
            verdict: or(verdict),
            wait: fin(vd.wait),
            // Цель — ЧИТАЕТСЯ у бота, не пересчитывается (§4.1).
            tgt: fin(isLong ? cd.max_price : cd.min_price),
            // Объекты продакшн-функций кладутся целиком (§4.1). Имена схемы
            // идут первыми и в порядке схемы; остальное, что вернула функция,
            // дописано следом: поле, не записанное сегодня, из годовалой
            // записи не восстанавливается.
            geo: g ? { rr: fin(g.rr), reward: fin(g.reward), risk: fin(g.risk),
                       tgtSig: fin(g.tgtSig), sd: fin(g.sd),
                       veto: Array.isArray(g.veto) ? g.veto.slice() : [], wait: fin(g.wait) } : null,
            dec: { ok: !!dec.ok, L: fin(dec.L), binding: or(dec.binding),
                   moneyBelowMin: !!dec.moneyBelowMin,
                   parts: dec.parts ? { struct: fin(dec.parts.struct), noise: fin(dec.parts.noise),
                                        btc: fin(dec.parts.btc), money: fin(dec.parts.money) } : null },
            inv: iv ? { dist: fin(iv.dist), price: fin(iv.price), dStruct: fin(iv.dStruct),
                        capped: !!iv.capped, floored: !!iv.floored, sd: fin(iv.sd),
                        ref: fin(iv.ref), src: or(iv.src) } : null,
            _rp: rp
        };
    }

    function skipLine(d, sym, why) { return { k: 'x', d: d, sym: sym, why: why }; }

    function buildDay(coeffs, prices, d) {
        const btcStats = coeffs.btc || null;
        // Слой 0 — ОДИН вызов на весь список (§4.1).
        const reg  = P.marketRegime(btcStats);
        const rows = coeffs.analysis_data || [];
        const gen  = coeffs.generated_at || null;
        const genMs = gen ? Date.parse(gen) : NaN;
        const age  = isFinite(genMs) ? Math.round((tsMs - genMs) / 60000) : null;
        const cat  = { hash: engine.catHash };
        const fp   = { script: engine.scriptHash, commit: commit };

        const lines = [];
        let cov = 0, skip = 0, hardSkip = 0;

        P.tokens.forEach(function (t) {
            const coin = prices.px[t.s] || null;

            // Деградация — ровно как у доски (инв. 11–12, §5.5). Порядок
            // проверок тот же, что в update(): пара, мёртвый рынок, строка
            // бота, флаг ошибки.
            if (!coin) {
                lines.push(skipLine(d, t.name,
                    t.fut ? 'futures-only: no spot mirror pair' : 'no price data'));
                skip++; if (!t.fut) hardSkip++; return;
            }
            if (coin.count === 0 || (coin.bidPrice === 0 && coin.askPrice === 0)) {
                lines.push(skipLine(d, t.name, 'dead market')); skip++; hardSkip++; return;
            }
            let cd = null;
            for (let i = 0; i < rows.length; i++) if (rows[i].symbol === t.name) { cd = rows[i]; break; }
            if (!cd)      { lines.push(skipLine(d, t.name, 'no bot row'));    skip++; hardSkip++; return; }
            if (cd.error) { lines.push(skipLine(d, t.name, 'bot error flag')); skip++; hardSkip++; return; }

            const rc7   = P.residual7(cd, btcStats);
            const long  = sideBlock(cd, t, coin, true,  reg, btcStats, rc7);
            const short = sideBlock(cd, t, coin, false, reg, btcStats, rc7);
            // Ни одной стороны со счётом — движок не произвёл вердикта, и
            // частичная запись запрещена (§5.5).
            if (long.score === null && short.score === null) {
                lines.push(skipLine(d, t.name, 'no metrics')); skip++; hardSkip++; return;
            }
            const rp = long._rp;
            delete long._rp; delete short._rp;

            lines.push({
                k: 's', d: d, ts: iso(tsMs), sym: t.name, pair: t.s,
                gen: gen, age: age,
                px: { src: prices.src, cur: fin(coin.lastPrice), p24: fin(coin.priceChangePercent),
                      qv: fin(coin.quoteVolume), hi: fin(coin.highPrice), lo: fin(coin.lowPrice),
                      cnt: fin(coin.count) },
                reg: { mode: or(reg.mode), dir: fin(reg.dir), eff: fin(reg.eff),
                       z: fin(reg.z), known: !!reg.known },
                cd: cd, btc: btcStats, rp: fin(rp),
                long: long, short: short,
                cat: { acting: acting(t.name), hash: cat.hash },
                fp: fp
            });
            cov++;
        });

        return { lines: lines, cov: cov, skip: skip, hardSkip: hardSkip,
                 gen: gen, age: age, src: prices.src };
    }

    // Пробелы §4.4: пропущенная дата — СТРОКА, а не отсутствие строки (инв. 37).
    // Дедупликация по уже записанным пробелам: провалившийся прогон не имеет
    // права выписать один и тот же пробел дважды и сломать тождество.
    function backfillGaps(today) {
        // Сегодняшняя дата исключается сознательно: к этому моменту файл дня
        // уже записан, и без исключения newest === today давал бы пустой
        // интервал, то есть тихо стирал бы все пробелы простоя.
        const have = fs.existsSync(DATA)
            ? fs.readdirSync(DATA).filter(function (f) { return /^\d{4}-\d{2}-\d{2}\.jsonl$/.test(f); })
                .map(function (f) { return f.slice(0, 10); })
                .filter(function (d) { return d < today; }).sort()
            : [];
        if (!have.length) return [];
        const newest = have[have.length - 1];
        const known = {};
        readLines(RUNS).forEach(function (l) { if (l.k === 'g') known[l.d] = true; });
        const gaps = between(newest, today).filter(function (d) {
            return !known[d] && !fs.existsSync(path.join(DATA, d + '.jsonl'));
        });
        gaps.forEach(function (d) {
            appendLine(RUNS, { k: 'g', d: d, why: 'no run', found: iso(tsMs) });
        });
        return gaps;
    }

    async function snapshot(o) {
        const dry = !!(o && o.dry);
        const d   = dayOf(tsMs);
        const target = path.join(DATA, d + '.jsonl');

        const run = { k: 'r', ts: iso(tsMs), d: d, status: 'fail', cov: 0, skip: 0,
                      px: null, gen: null, age: null, resolved: [], note: null };

        if (!dry && fs.existsSync(target)) {
            run.status = 'dup';
            run.note = 'файл даты уже существует';
            return { run: run, lines: [], gaps: backfillGaps(d), wrote: false };
        }

        const cr = await transport.get(P.GIST_URL + '?t=' + tsMs);
        if (!cr.ok || !cr.body || typeof cr.body !== 'object') {
            run.note = 'coeffs недоступен: ' + (cr.error || 'http ' + cr.status);
            return { run: run, lines: [], gaps: [], wrote: false, fatal: true };
        }
        const coeffs = cr.body;
        const prices = await fetchPrices();
        if (!Object.keys(prices.px).length) {
            run.note = 'цены недоступны: ' + (prices.note || 'пустой ответ');
            return { run: run, lines: [], gaps: [], wrote: false, fatal: true };
        }

        const day = buildDay(coeffs, prices, d);
        if (day.lines.length !== P.tokens.length) {
            // Тождество §4.2 — молчаливый пропуск монеты есть дефект.
            throw new Error('покрытие: строк ' + day.lines.length + ', монет ' + P.tokens.length);
        }
        const text = day.lines.map(function (l) { return JSON.stringify(l); }).join('\n') + '\n';

        run.cov = day.cov; run.skip = day.skip; run.px = day.src;
        run.gen = day.gen; run.age = day.age;
        run.status = day.hardSkip > 0 ? 'partial' : 'ok';
        const notes = [];
        if (prices.note) notes.push(prices.note + ' — фолбэк на свечи');
        if (day.age !== null && day.age > P.STALE_CRIT_MIN) {
            notes.push('возраст coeffs ' + day.age + ' мин > STALE_CRIT_MIN ' + P.STALE_CRIT_MIN);
        }
        run.note = notes.length ? notes.join('; ') : null;

        const wrote = writeOnce(target, text);
        if (!wrote) { run.status = 'dup'; run.note = 'файл даты уже существует'; }
        return { run: run, lines: day.lines, gaps: backfillGaps(d), wrote: wrote, text: text };
    }

    // ── Исход ───────────────────────────────────────────────────────────────

    // Час ПЕРВОГО касания уровня. Ничего не предсказывает и ничего не
    // пересчитывает: уровни приходят из записи снимка (§4.5).
    function firstTouch(ks, level, up) {
        if (level === null || !isFinite(level)) return null;
        for (let i = 0; i < ks.length; i++) {
            if (up ? ks[i].h >= level : ks[i].l <= level) return ks[i].t;
        }
        return null;
    }

    function sideOutcome(ks, side, isLong) {
        if (!side) return { tgt: null, stop: null, wait: null, first: null };
        const tgtT  = firstTouch(ks, side.tgt, isLong);
        const stopT = firstTouch(ks, side.inv ? side.inv.price : null, !isLong);
        const waitT = firstTouch(ks, side.wait, !isLong);
        let first = null;
        if (tgtT !== null && stopT !== null)      first = tgtT === stopT ? 'tie' : (tgtT < stopT ? 'tgt' : 'stop');
        else if (tgtT !== null)                   first = 'tgt';
        else if (stopT !== null)                  first = 'stop';
        return { tgt: tgtT === null ? null : iso(tgtT),
                 stop: stopT === null ? null : iso(stopT),
                 wait: waitT === null ? null : iso(waitT),
                 first: first };
    }

    function windowOf(rows, startMs, endMs) {
        if (!Array.isArray(rows)) return null;
        const ks = rows.map(kline).filter(function (k) { return k.t >= startMs && k.t <= endMs; });
        if (!ks.length) return null;
        // Последний час окна обязан присутствовать: неполный исход хуже
        // отсутствующего, потому что он неизменяем (§6).
        if (ks[ks.length - 1].t < endMs - 3600000) return null;
        return ks;
    }

    function pending(today) {
        const have = fs.existsSync(DATA)
            ? fs.readdirSync(DATA).filter(function (f) { return /^\d{4}-\d{2}-\d{2}\.jsonl$/.test(f); })
                .map(function (f) { return f.slice(0, 10); }).sort()
            : [];
        const due = [];
        have.forEach(function (d) {
            HORIZONS.forEach(function (h) {
                if (dayMs(addDays(d, h)) > dayMs(today)) return;
                if (fs.existsSync(path.join(OUT, d + '-h' + h + '.jsonl'))) return;
                due.push({ d: d, h: h });
            });
        });
        due.sort(function (a, b) { return a.d === b.d ? a.h - b.h : (a.d < b.d ? -1 : 1); });
        return due.slice(0, OUT_CAP);
    }

    async function resolveOne(job) {
        const snap = readLines(path.join(DATA, job.d + '.jsonl')).filter(function (l) { return l.k === 's'; });
        if (!snap.length) return null;
        const startMs = Date.parse(snap[0].ts);
        const endMs   = startMs + job.h * 86400000;
        // 336 часов максимум плюс запас на дыры в серии зеркала.
        const limit   = Math.min(1000, job.h * 24 + 48);

        const btcRes = await transport.get(klineUrl('BTCUSDT', limit) + '&startTime=' + startMs + '&endTime=' + endMs);
        if (!btcRes.ok) return null;
        const btcKs = windowOf(btcRes.body, startMs, endMs);
        if (!btcKs) return null;

        const out = [];
        let hi = -Infinity, lo = Infinity;
        btcKs.forEach(function (k) { if (k.h > hi) hi = k.h; if (k.l < lo) lo = k.l; });
        out.push({ k: 'oh', d: job.d, h: job.h, asof: isoHour(endMs), src: 'klines',
                   // BTC не входит в tokens[] и строки снимка не имеет, поэтому
                   // p0 — открытие первой свечи окна, а не перенесённая цена.
                   btc: { p0: fin(btcKs[0].o), p1: fin(btcKs[btcKs.length - 1].c),
                          hi: fin(hi), lo: fin(lo) } });

        for (const s of snap) {
            await sleep(gapMs);
            const r = await transport.get(klineUrl(s.pair, limit) + '&startTime=' + startMs + '&endTime=' + endMs);
            if (!r.ok) return null;
            const ks = windowOf(r.body, startMs, endMs);
            if (!ks) return null;
            let khi = -Infinity, klo = Infinity;
            ks.forEach(function (k) { if (k.h > khi) khi = k.h; if (k.l < klo) klo = k.l; });
            out.push({ k: 'o', d: job.d, h: job.h, sym: s.sym,
                       p0: fin(s.px ? s.px.cur : null), p1: fin(ks[ks.length - 1].c),
                       hi: fin(khi), lo: fin(klo),
                       long: sideOutcome(ks, s.long, true),
                       short: sideOutcome(ks, s.short, false) });
        }
        const text = out.map(function (l) { return JSON.stringify(l); }).join('\n') + '\n';
        const file = path.join(OUT, job.d + '-h' + job.h + '.jsonl');
        if (!writeOnce(file, text)) return null;
        return { d: job.d, h: job.h, n: out.length - 1, text: text };
    }

    async function resolve(today) {
        const done = [];
        for (const job of pending(today || dayOf(tsMs))) {
            const r = await resolveOne(job);
            if (r) done.push({ d: r.d, h: r.h, n: r.n });
        }
        return done;
    }

    return {
        root: root, tsMs: tsMs, paths: { DATA: DATA, OUT: OUT, RUNS: RUNS },
        snapshot: snapshot, resolve: resolve, resolveOne: resolveOne, pending: pending,
        appendRun: function (run) { appendLine(RUNS, run); },
        buildDay: buildDay, fetchPrices: fetchPrices, acting: acting, sideBlock: sideBlock
    };
}

// ── CLI ─────────────────────────────────────────────────────────────────────

// Инв. 37: один grep-пригодный вывод на прогон, с generated_at.
function runLineOut(run) {
    return 'JOURNAL ' + run.status.toUpperCase() + ' ' + run.d
         + ' generated_at=' + (run.gen || '-')
         + ' age=' + (run.age === null ? '-' : run.age)
         + ' px=' + (run.px || '-')
         + ' cov=' + run.cov + ' skip=' + run.skip
         + ' resolved=' + run.resolved.length
         + (run.note ? ' note=' + JSON.stringify(run.note) : '');
}

async function probe(engine) {
    const P = engine.P;
    console.log('скрипт index.html  fp.script=' + engine.scriptHash);
    console.log('реестр CATALYSTS   cat.hash =' + engine.catHash
                + '  монет с событиями: ' + Object.keys(P.CATALYSTS).length);
    console.log('константы движка   CAT_WINDOW_D=' + P.CAT_WINDOW_D
                + '  STALE_CRIT_MIN=' + P.STALE_CRIT_MIN + '  TIER_MIN=' + P.TIER_MIN);
    console.log('монет в tokens[]   ' + P.tokens.length
                + ' (fut:true — ' + P.tokens.filter(function (t) { return t.fut; }).map(function (t) { return t.name; }).join(', ') + ')');

    let bad = 0;
    const g = await httpTransport.get(P.GIST_URL + '?t=' + Date.now());
    if (g.ok && g.body) {
        console.log('GIST               OK  http ' + g.status + '  ' + g.bytes + ' Б'
                    + '  generated_at=' + (g.body.generated_at || '-')
                    + '  монет=' + ((g.body.analysis_data || []).length)
                    + '  btc=' + (g.body.btc ? 'есть' : 'НЕТ'));
    } else {
        console.log('GIST               ПРОВАЛ  http ' + g.status + '  ' + (g.error || ''));
        bad++;
    }

    const spot = [];
    P.tokens.forEach(function (t) { if (!t.fut) spot.push(t.s); });
    const tk = await httpTransport.get(MIRROR + '/api/v3/ticker/24hr?symbols='
                + encodeURIComponent(JSON.stringify(['BTCUSDT'].concat(spot))));
    const tickerOk = tk.ok && Array.isArray(tk.body);
    console.log('ТИКЕР зеркала      ' + (tickerOk ? 'OK  строк ' + tk.body.length : 'ПРОВАЛ  http ' + tk.status + '  ' + (tk.error || '')));

    const kl = await httpTransport.get(MIRROR + '/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=' + KLIMIT);
    const klOk = kl.ok && Array.isArray(kl.body);
    console.log('СВЕЧИ зеркала      ' + (klOk ? 'OK  свечей ' + kl.body.length : 'ПРОВАЛ  http ' + kl.status + '  ' + (kl.error || '')));
    if (!tickerOk && !klOk) { console.log('оба ценовых пути недоступны'); bad++; }
    console.log('живой ценовой путь ' + (tickerOk ? 'ticker' : (klOk ? 'klines (фолбэк)' : 'НЕТ')));
    console.log(bad ? 'ПРОБА ПРОВАЛЕНА: обязательные источники недоступны' : 'ПРОБА ПРОЙДЕНА');
    return bad === 0 ? 0 : 1;
}

async function main(argv) {
    const args = argv.slice(2);
    const mode = args.find(function (a) { return a.slice(0, 2) === '--'; }) || '--all';
    const engine = loadEngine(path.join(REPO, 'index.html'));

    if (mode === '--probe') return probe(engine);

    const dry  = mode === '--dry-run';
    const root = dry ? fs.mkdtempSync(path.join(os.tmpdir(), 'jdry-')) : path.join(REPO, 'journal');
    const j = createJournal({ engine: engine, root: root, commit: process.env.GITHUB_SHA || '' });

    if (mode === '--resolve') {
        const done = await j.resolve();
        console.log('JOURNAL RESOLVE ' + dayOf(j.tsMs) + ' files=' + done.length
                    + ' ' + JSON.stringify(done));
        return 0;
    }

    const snap = await j.snapshot({ dry: dry });
    if (mode === '--all' && !snap.fatal) snap.run.resolved = await j.resolve();

    if (dry) {
        const first = snap.lines.filter(function (l) { return l.k === 's'; })[0];
        const skipped = snap.lines.filter(function (l) { return l.k === 'x'; });
        console.log('--- ЧЕРНОВОЙ ПРОГОН, в journal/ ничего не записано ---');
        console.log('временный каталог: ' + root);
        console.log('--- строка снимка ---');
        console.log(first ? JSON.stringify(first) : '(ни одной покрытой монеты)');
        console.log('--- строки пропуска ---');
        skipped.forEach(function (l) { console.log(JSON.stringify(l)); });
        console.log('--- строка прогона ---');
        console.log(JSON.stringify(snap.run));
    } else {
        // Строка прогона пишется ВСЕГДА, включая провал: §4.3, инв. 37.
        j.appendRun(snap.run);
    }

    console.log(runLineOut(snap.run));
    // Прогон, не записавший данные, обязан вернуть НЕНУЛЕВОЙ код (инв. 37).
    return snap.run.status === 'fail' ? 1 : 0;
}

module.exports = {
    loadEngine, createJournal, httpTransport, writeOnce, readLines, appendLine,
    between, addDays, dayOf, dayMs, iso, isoHour, sha16, fin, main, MIRROR, HORIZONS, OUT_CAP
};

if (require.main === module) {
    main(process.argv).then(function (code) { process.exit(code); },
        function (e) { console.log('JOURNAL FAIL ' + (e && e.stack || e)); process.exit(1); });
}
