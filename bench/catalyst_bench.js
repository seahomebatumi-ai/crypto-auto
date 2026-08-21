// bench/catalyst_bench.js — TZ-06. The catalyst layer is the only layer that can
// CLOSE a trade direction, and until this change it did so on three hand-typed
// strings with no source. This bench holds the new rule in place.
//
// No rule is copied here (inv. 21): catalystCheck, directionVerdict, the loader,
// catalystsApply and catalystBanner are all pulled out of the <script> block of
// index.html at run time and executed as the production functions. The loader is
// driven through a stubbed XMLHttpRequest, which is why every rejection path can
// be exercised without a server.
//
// A bench that verified nothing must fail (inv. 22, 29): the check count is
// printed and zero is a failure. The quorum rule currently has ZERO live cases —
// nothing in catalysts.json is `confirmed` — so it is exercised against
// synthetic entries with known answers, in both directions.
'use strict';
const fs   = require('fs');
const path = require('path');
const vm   = require('vm');

const ROOT = path.join(__dirname, '..');
const HTML = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const SRC  = HTML.slice(HTML.indexOf('<script>') + 8, HTML.lastIndexOf('</script>'));
const RAW  = fs.readFileSync(path.join(ROOT, 'catalysts.json'), 'utf8');

// Primary sources: the project's own domains and the specification repositories
// where an upgrade or an unlock is actually decided. Aggregators are absent on
// purpose — the ENA check that motivated this TZ returned six mutually
// inconsistent answers from six trackers, so "many aggregators agree" is not
// evidence and two of them are not a quorum.
const PRIMARY = [
    'z.cash', 'zips.z.cash', 'electriccoin.co', 'forum.zcashcommunity.com',
    'github.com', 'raw.githubusercontent.com',
    'solana.com', 'solana.org', 'avax.network', 'avalabs.org',
    'ethereum.org', 'eips.ethereum.org', 'xrpl.org', 'ripple.com',
    'cardano.org', 'iohk.io', 'tron.network', 'near.org', 'chain.link',
    'aave.com', 'governance.aave.com', 'sui.io', 'hedera.com', 'stellar.org',
    'algorand.co', 'bnbchain.org', 'binance.com', 'ondo.finance', 'ethena.fi',
    'getmonero.org', 'bch.info', 'uniswap.org', 'gov.uniswap.org', 'yearn.fi',
    'renderfoundation.com', 'fetch.ai', 'bittensor.com', 'sky.money',
    'hyperliquid.xyz', 'ton.org'
];

const DAY = 86400000;

let checks = 0, fails = 0, quiet = false;
function eq(name, got, want) {
    checks++;
    if (!Object.is(got, want)) {
        fails++;
        if (!quiet) console.log('  FAIL ' + name + ': got ' + JSON.stringify(got) + ' want ' + JSON.stringify(want));
    }
}
function deq(name, got, want) {
    checks++;
    const a = JSON.stringify(got), b = JSON.stringify(want);
    if (a !== b) { fails++; if (!quiet) console.log('  FAIL ' + name + ':\n    got  ' + a + '\n    want ' + b); }
}
function ok(name, cond) { eq(name, !!cond, true); }

// ── Sandbox ─────────────────────────────────────────────────────────────────
// Same shims the other node benches use, plus the one thing this layer needs:
// an XMLHttpRequest the bench controls.
function mkSandbox(xhrCtor) {
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
        XMLHttpRequest: xhrCtor,
        setTimeout: () => 0, clearTimeout: () => {}, setInterval: () => 0,
        clearInterval: () => {}, requestAnimationFrame: () => 0,
        console, Math, Date, JSON, parseFloat, parseInt, isFinite, isNaN
    };
    sandbox.window = sandbox;
    vm.createContext(sandbox);
    vm.runInContext(SRC, sandbox, { filename: 'index.html:<script>' });
    return sandbox;
}

// An XHR whose whole behaviour is one callback the bench supplies.
function mkXhr(behave) {
    return function () {
        const self = this;
        self.readyState = 0; self.status = 0; self.responseText = '';
        self.onreadystatechange = null; self.onerror = null;
        self.open = function () {};
        self.send = function () { behave(self); };
    };
}
function respond(status, body) {
    return mkXhr(function (x) {
        x.readyState = 4; x.status = status; x.responseText = body;
        if (x.onreadystatechange) x.onreadystatechange();
    });
}
function netFail() {
    return mkXhr(function (x) { if (x.onerror) x.onerror(); });
}

// init() fires loadCatalysts() at the bottom of the script, so a sandbox is
// already in its post-load state the moment it is built. The pending state is
// reached with a transport that never answers — that is also the real state of
// the page for the first few milliseconds after it opens.
const PENDING = mkSandbox(mkXhr(function () {}));
const P = mkSandbox(respond(200, RAW));
const NEED = ['CATALYSTS', 'CAT_LOADED', 'CAT_ERR', 'catalystsApply', 'loadCatalysts',
              'catalystBanner', 'catalystCheck', 'directionVerdict', 'tokens', 'CAT_WINDOW_D'];

console.log('=== 0. Production surface ===');
NEED.forEach(function (n) { ok('index.html defines ' + n, P[n] !== undefined); });
eq('pending: registry empty', Object.keys(PENDING.CATALYSTS).length, 0);
eq('pending: CAT_LOADED false', PENDING.CAT_LOADED, false);
eq('pending: CAT_ERR still null', PENDING.CAT_ERR, null);
ok('pending: banner printed anyway', PENDING.catalystBanner().length > 0);
ok('pending: no coin can be vetoed', PENDING.catalystCheck('ZEC', false, Date.now()).veto === null);
eq('loaded: CAT_LOADED', P.CAT_LOADED, true);
eq('loaded: CAT_ERR', P.CAT_ERR, null);
eq('loaded: banner silent', P.catalystBanner(), '');
const CAT = JSON.parse(RAW);
deq('loaded: registry equals the file', P.CATALYSTS, CAT.items);
eq('schema version', CAT.v, 1);
const SYMS = P.tokens.map(function (t) { return t.name; });

// ── 1. Schema ───────────────────────────────────────────────────────────────
// TZ-06 §2.5.1 says "all eight fields"; the file the same TZ specifies carries
// seven (d · dir · kind · t · conf · src · added) and its field-rule paragraph
// names the same seven. The exact key set is asserted, and the symbol key is
// asserted separately — that is the eighth identifying element of an entry.
const KEYS = ['d', 'dir', 'kind', 't', 'conf', 'src', 'added'];
const DIRS = ['long', 'short'];
const KINDS = ['unlock', 'protocol', 'listing', 'macro'];
const CONFS = ['confirmed', 'disputed'];

console.log('=== 1. Schema of catalysts.json ===');
let entries = 0;
const seenTriple = {};
Object.keys(CAT.items).forEach(function (sym) {
    ok('items key "' + sym + '" is in tokens[]', SYMS.indexOf(sym) >= 0);
    const list = CAT.items[sym];
    ok(sym + ': entry list is an array', Array.isArray(list));
    list.forEach(function (e, i) {
        entries++;
        const tag = sym + '[' + i + '] ';
        deq(tag + 'exact key set', Object.keys(e).slice().sort(), KEYS.slice().sort());
        ok(tag + 'd is YYYY-MM-DD', /^\d{4}-\d{2}-\d{2}$/.test(e.d));
        ok(tag + 'd parses', isFinite(Date.parse(e.d + 'T00:00:00Z')));
        ok(tag + 'added is YYYY-MM-DD', /^\d{4}-\d{2}-\d{2}$/.test(e.added));
        ok(tag + 'dir in enum', DIRS.indexOf(e.dir) >= 0);
        ok(tag + 'kind in enum', KINDS.indexOf(e.kind) >= 0);
        ok(tag + 'conf in enum', CONFS.indexOf(e.conf) >= 0);
        ok(tag + 'src is an array', Array.isArray(e.src));
        ok(tag + 't is a non-empty string', typeof e.t === 'string' && e.t.length > 0);
        const key = sym + '|' + e.d + '|' + e.t;
        ok(tag + 'no duplicate (sym, d, t)', !seenTriple[key]);
        seenTriple[key] = true;
    });
});
console.log('  symbols: ' + Object.keys(CAT.items).length + ', entries: ' + entries);
ok('the registry is not empty', entries > 0);

// ── 2. Quorum (inv. 39) ─────────────────────────────────────────────────────
// `confirmed` costs either two independent sources or one primary one. Nothing
// in the file is confirmed today, so the rule is proved on synthetic entries
// with known answers — a rule with zero cases is not a control (inv. 22).
function hostOf(u) {
    const m = /^https?:\/\/([^/?#]+)/i.exec(String(u));
    if (!m) return null;
    return m[1].toLowerCase().replace(/:\d+$/, '').replace(/^www\./, '');
}
function quorumOk(e) {
    if (e.conf !== 'confirmed') return true;          // disputed carries no burden
    const hosts = (e.src || []).map(hostOf).filter(function (h) { return h !== null; });
    if (hosts.length >= 2) {
        const uniq = {}; hosts.forEach(function (h) { uniq[h] = true; });
        return Object.keys(uniq).length >= 2;         // two SOURCES, not one twice
    }
    return hosts.length === 1 && PRIMARY.indexOf(hosts[0]) >= 0;
}

console.log('=== 2. Quorum rule ===');
const QCASES = [
    { want: true,  why: 'one primary source',        e: { conf: 'confirmed', src: ['https://zips.z.cash/zip-0253'] } },
    { want: true,  why: 'two independent aggregators', e: { conf: 'confirmed', src: ['https://tokenomist.ai/x', 'https://cryptorank.io/y'] } },
    { want: false, why: 'one aggregator alone',      e: { conf: 'confirmed', src: ['https://tokenomist.ai/x'] } },
    { want: false, why: 'no source at all',          e: { conf: 'confirmed', src: [] } },
    { want: false, why: 'same host twice',           e: { conf: 'confirmed', src: ['https://tokenomist.ai/x', 'https://www.tokenomist.ai/y'] } },
    { want: false, why: 'not a URL',                 e: { conf: 'confirmed', src: ['со слов'] } },
    { want: true,  why: 'disputed needs nothing',    e: { conf: 'disputed',  src: [] } },
    { want: true,  why: 'primary plus aggregator',   e: { conf: 'confirmed', src: ['https://github.com/zcash/zips/pull/1', 'https://cryptorank.io/y'] } }
];
QCASES.forEach(function (c) { eq('quorum, ' + c.why, quorumOk(c.e), c.want); });
let confirmedLive = 0;
Object.keys(CAT.items).forEach(function (sym) {
    CAT.items[sym].forEach(function (e, i) {
        if (e.conf === 'confirmed') confirmedLive++;
        ok(sym + '[' + i + '] passes quorum', quorumOk(e));
    });
});
console.log('  synthetic cases: ' + QCASES.length + ', live confirmed entries: ' + confirmedLive);

// ── 3. Veto containment ─────────────────────────────────────────────────────
// 400 consecutive days x every symbol x both sides. Not one `disputed` entry may
// close a side at any offset. The notes have to keep appearing on exactly the
// days the old literal produced them: the supporting side sees the note over the
// 15 calendar days ending on the event date — the -1 back edge keeps the event
// day itself, CAT_WINDOW_D keeps the fourteen before it.
console.log('=== 3. Veto containment across 400 days x ' + SYMS.length + ' symbols x 2 sides ===');
const START = Date.parse('2026-06-01T11:00:00Z');
const noteDays = {};
let sweep = 0, vetoes = 0;
for (let d = 0; d < 400; d++) {
    const t0 = START + d * DAY;
    SYMS.forEach(function (sym) {
        [true, false].forEach(function (isLong) {
            const out = P.catalystCheck(sym, isLong, t0);
            sweep++;
            checks++;
            if (out.veto !== null) {
                fails++; vetoes++;
                if (!quiet) console.log('  FAIL disputed entry vetoed: ' + sym + ' day ' + d + ' long=' + isLong);
            }
            if (out.note !== null) {
                const k = sym + '|' + (isLong ? 'long' : 'short');
                (noteDays[k] = noteDays[k] || []).push(t0);
            }
        });
    });
}
console.log('  calls: ' + sweep + ', vetoes seen: ' + vetoes + ' (must be 0)');

Object.keys(CAT.items).forEach(function (sym) {
    CAT.items[sym].forEach(function (e) {
        const supporting = e.dir === 'long' ? 'long' : 'short';
        const opposing   = e.dir === 'long' ? 'short' : 'long';
        const got = noteDays[sym + '|' + supporting] || [];
        const eventMs = Date.parse(e.d + 'T00:00:00Z');
        // Stated as calendar days, not as a second copy of the window
        // arithmetic: the note stands on the 15 dates ending ON the event date
        // — the -1 back edge keeps the event day itself, CAT_WINDOW_D keeps the
        // fourteen before it. The millisecond edges are pinned in section 4.
        const gotDates = got.map(function (t) { return new Date(t).toISOString().slice(0, 10); });
        const wantDates = [];
        for (let k = 14; k >= 0; k--) wantDates.push(new Date(eventMs - k * DAY).toISOString().slice(0, 10));
        deq(sym + ': note dates on the supporting side', gotDates, wantDates);
        eq(sym + ': note span is 15 calendar days', gotDates.length, 15);
        eq(sym + ': the run ends on the event date', gotDates[gotDates.length - 1], e.d);
        deq(sym + ': no note on the opposing side', noteDays[sym + '|' + opposing] || [], []);
        ok(sym + ': the run is contiguous', got.every(function (t, i) { return i === 0 || t - got[i - 1] === DAY; }));
    });
});
const noSuch = SYMS.filter(function (s) { return !CAT.items[s]; });
noSuch.forEach(function (s) {
    deq(s + ': silent, no entry in the registry', P.catalystCheck(s, true, START), { veto: null, note: null });
});
console.log('  symbols with no entry stay silent: ' + noSuch.length);

// ── 4. Window identity on `confirmed` data ──────────────────────────────────
// The only edit to catalystCheck is the `conf` guard; everything the window is
// made of is byte-identical to the pre-change function (proved by the diff in
// the report). So the pre-change behaviour IS this function fed `confirmed`
// data, and the identity to hold is the edge table below — including the day
// after the event (-1, still inside) and the fifteenth day before it (outside).
console.log('=== 4. Window identity: the confirmed path is the old path ===');
const EV = '2026-09-10';
const evMs = Date.parse(EV + 'T00:00:00Z');
function withReg(items, fn) {
    const S = mkSandbox(respond(200, JSON.stringify({ v: 1, updated: '2026-08-21', items: items })));
    S.loadCatalysts();
    return fn(S);
}
const mkEntry = function (conf, dir) {
    return { d: EV, dir: dir, kind: 'protocol', t: 'X', conf: conf, src: [], added: '2026-08-21' };
};
const EDGES = [
    { off: -14 * DAY,     inside: true,  why: 'exactly CAT_WINDOW_D days before' },
    { off: -14 * DAY - 1, inside: false, why: 'one ms past CAT_WINDOW_D' },
    { off: -1,            inside: true,  why: 'one ms before the event' },
    { off: 0,             inside: true,  why: 'the event instant' },
    { off: DAY,           inside: true,  why: 'the -1 back edge, exactly' },
    { off: DAY + 1,       inside: false, why: 'one ms past the back edge' },
    { off: -400 * DAY,    inside: false, why: 'far in the future' },
    { off: 400 * DAY,     inside: false, why: 'far in the past' }
];
withReg({ ZEC: [mkEntry('confirmed', 'long')] }, function (S) {
    EDGES.forEach(function (c) {
        const t0 = evMs + c.off;
        eq('confirmed, SHORT vetoed — ' + c.why, S.catalystCheck('ZEC', false, t0).veto, c.inside ? 'X' : null);
        eq('confirmed, LONG noted — ' + c.why,  S.catalystCheck('ZEC', true,  t0).note, c.inside ? 'X' : null);
        eq('confirmed, LONG never vetoed — ' + c.why, S.catalystCheck('ZEC', true, t0).veto, null);
    });
});
withReg({ ZEC: [mkEntry('disputed', 'long')] }, function (S) {
    EDGES.forEach(function (c) {
        const t0 = evMs + c.off;
        eq('disputed, SHORT never vetoed — ' + c.why, S.catalystCheck('ZEC', false, t0).veto, null);
        eq('disputed, SHORT gets no note — ' + c.why, S.catalystCheck('ZEC', false, t0).note, null);
        eq('disputed, LONG still noted — ' + c.why, S.catalystCheck('ZEC', true, t0).note, c.inside ? 'X' : null);
    });
});
// A missing or unknown `conf` is treated as unverified, not as confirmed: the
// fail-safe direction of inv. 39 is "may not close a side".
withReg({ ZEC: [{ d: EV, dir: 'long', t: 'X' }] }, function (S) {
    eq('conf absent never vetoes', S.catalystCheck('ZEC', false, evMs).veto, null);
    eq('conf absent still notes', S.catalystCheck('ZEC', true, evMs).note, 'X');
});
withReg({ ZEC: [mkEntry('CONFIRMED', 'long')] }, function (S) {
    eq('conf is compared exactly, not case-insensitively', S.catalystCheck('ZEC', false, evMs).veto, null);
});
// First-note-wins and the early return on veto survive untouched.
withReg({ ZEC: [mkEntry('disputed', 'long'), { d: EV, dir: 'long', kind: 'protocol', t: 'Y', conf: 'disputed', src: [], added: '2026-08-21' }] },
    function (S) { eq('first note wins among disputed', S.catalystCheck('ZEC', true, evMs).note, 'X'); });
withReg({ ZEC: [mkEntry('confirmed', 'short'), { d: EV, dir: 'long', kind: 'protocol', t: 'Y', conf: 'confirmed', src: [], added: '2026-08-21' }] },
    function (S) { eq('veto returns early, later note not reached', S.catalystCheck('ZEC', true, evMs).note, null); });

// ── 5. Degraded load (inv. 40) ──────────────────────────────────────────────
console.log('=== 5. Degraded load: off and empty must not look the same ===');
const BAD = [
    { why: 'HTTP 500',        xhr: respond(500, RAW),                          err: 'HTTP 500' },
    { why: 'HTTP 404',        xhr: respond(404, ''),                           err: 'HTTP 404' },
    { why: 'file:// gives 0', xhr: respond(0, RAW),                            err: 'HTTP 0' },
    { why: 'truncated JSON',  xhr: respond(200, '{ "v": 1, "items": {'),       err: null },
    { why: 'version is not 1', xhr: respond(200, '{"v":2,"items":{}}'),        err: null },
    { why: 'no items object', xhr: respond(200, '{"v":1}'),                    err: null },
    { why: 'network error',   xhr: netFail(),                                  err: null }
];
BAD.forEach(function (c) {
    const S = mkSandbox(c.xhr);
    S.loadCatalysts();
    deq('down, ' + c.why + ': registry empty', S.CATALYSTS, {});
    eq('down, ' + c.why + ': CAT_LOADED false', S.CAT_LOADED, false);
    ok('down, ' + c.why + ': CAT_ERR non-empty', typeof S.CAT_ERR === 'string' && S.CAT_ERR.length > 0);
    if (c.err !== null) eq('down, ' + c.why + ': CAT_ERR text', S.CAT_ERR, c.err);
    const banner = S.catalystBanner();
    ok('down, ' + c.why + ': banner produced', banner.length > 0);
    ok('down, ' + c.why + ': banner carries CAT_ERR', banner.indexOf(S.CAT_ERR) >= 0);
    ok('down, ' + c.why + ': banner adds no class', banner.indexOf('class=') < 0);
    SYMS.forEach(function (sym) {
        deq('down, ' + c.why + ': ' + sym + ' silent', S.catalystCheck(sym, true, Date.now()), { veto: null, note: null });
        deq('down, ' + c.why + ': ' + sym + ' silent SHORT', S.catalystCheck(sym, false, Date.now()), { veto: null, note: null });
    });
});

// directionVerdict has to complete on a full row with the layer down.
const FIX = {
    symbol: 'ZEC', up_beta: 0.9, up_r2: 0.4, down_beta: 1.1, down_r2: 0.5,
    up_beta_90: 1.0, up_r2_90: 0.5, down_beta_90: 0.9, down_r2_90: 0.4,
    corr_90: 0.7, tail_beta: 1.2, tail_r2: 0.3,
    r7: 0.02, r14: -0.05, r30: 0.11, min30: 30.8, max30: 47.3,
    vol7: 0.02, eff14: -0.7, vol_ratio: 0.7, price_pos: 8, volatility: 0.018,
    min_price: 28.3, max_price: 48.4, error: false, rank: 161, fdv_mc: 1.8, rank_prev: 155
};
const BTC = { min_price: 41200, max_price: 88400, price_pos: 60, volatility: 0.008,
              r7: 0.014, r14: 0.026, r30: 0.05 };
[mkSandbox(respond(500, RAW)), mkSandbox(respond(200, RAW))].forEach(function (S, i) {
    S.loadCatalysts();
    const tag = i === 0 ? 'layer down' : 'layer up';
    const reg = S.marketRegime(BTC);
    [true, false].forEach(function (isLong) {
        let vd = null, threw = null;
        try {
            const dec = S.leverageDecision(FIX, 36.5, isLong, BTC);
            vd = S.directionVerdict(FIX, 'ZECUSDT', 'ZEC', 36.5, -1.07, 3.6e8, isLong,
                                    reg, dec, 38.1, 32.4, S.residual7(FIX, BTC),
                                    Date.parse('2026-08-21T13:00:00Z'));
        } catch (e) { threw = e; }
        eq(tag + ': directionVerdict did not throw (long=' + isLong + ')', threw, null);
        ok(tag + ': verdict produced (long=' + isLong + ')', vd !== null && typeof vd.action === 'string');
    });
});

// ── 6. Negative control ─────────────────────────────────────────────────────
console.log('=== 6. The bench must be able to fail ===');
{
    const before = fails;
    quiet = true;
    eq('planted mismatch', 1, 2);
    deq('planted object mismatch', { a: 1 }, { a: 2 });
    quiet = false;
    const detected = (fails === before + 2);
    fails = before; checks -= 2;
    ok('comparator catches a wrong answer', detected);
    console.log('  planted mismatches noticed: ' + detected);
}

console.log('\n--- checks: ' + checks + '  fails: ' + fails + ' ---');
if (checks === 0) { console.log('FAIL bench verified nothing'); process.exit(1); }
process.exit(fails === 0 ? 0 : 1);
