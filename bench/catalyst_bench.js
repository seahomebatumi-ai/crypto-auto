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
// printed and zero is a failure. The quorum rule is exercised against synthetic
// entries with known answers in both directions, and — since TZ-09 — against a
// live `confirmed` entry as well.
//
// ── Rules the next registry edit follows (TZ-09 §3.4) ───────────────────────
// JSON carries no comments, so the rules for editing catalysts.json live here,
// next to the quorum rule that enforces them, where the next editor meets them:
//
//   * `d` is the date the event RESOLVES, announced by a primary source. A
//     month, a quarter, a "target" or a window is not a date and does not
//     become an entry. SOL's "Alpenglow in October" was invented precision and
//     was deleted rather than re-dated.
//   * `dir` is mechanical, never a forecast. Supply that certainly reaches the
//     market -> `short`. Determinate one-way mechanics -> that side. A
//     scheduled resolution with an unknowable outcome -> `both`. Anything
//     requiring an opinion about the OUTCOME does not belong in the registry at
//     all: that is how the ZEC entry acquired a direction it could not support.
//   * `src` must support the date in `d`, not merely the existence of the event.
//   * The registry carries COIN-SCOPED events only (TZ-21 §2 rule 1). A
//     market-wide event — a macro release, a central-bank decision, an index
//     rebalance — never enters the file. Market-wide risk is already measured,
//     by marketRegime in §3.12 Layer 0, and a per-coin veto is the wrong
//     instrument for it: a `dir:'both'` macro entry would close both sides on
//     all 28 coins for fifteen days out of roughly forty-five. A `"*"` key is
//     therefore not a missing feature but permanently out of scope, and the
//     `items key "<sym>" is in tokens[]` assertion that refuses it is correct
//     rather than a limitation to work around.
//   * The registry carries RESOLVING events only (TZ-21 §2 rule 2). An event
//     qualifies when something the market prices becomes KNOWN or IRREVERSIBLE
//     on `d`: an unlock releases supply, a governance vote concludes, a listing
//     goes live, a court or an agency issues a decision. An administrative
//     milestone on the path to such an event does NOT qualify — a
//     comment-period deadline, a filing date, a hearing being scheduled.
//     Nothing resolves on that date, so a veto would spend fifteen days of both
//     sides on a non-event.
//   * A `disputed` entry must carry its own argument, in `basis` (TZ-21 §2
//     rule 3). Map §3.15 deletes rather than demotes an entry NO host confirms,
//     because such an entry keeps printing an argument built on a date nobody
//     confirms; that stays true. It does not cover a second case: the primary
//     publishes the MECHANISM and not the CALENDAR. There a derived date is
//     supported by the rule it is derived from ONLY WHEN THE DERIVATION IS
//     WRITTEN INTO `basis` — an underived date and an undocumented derivation
//     are indistinguishable to the next reader. So the classes split: no
//     primary publishes the event at all -> delete the entry; the primary
//     publishes the mechanism but not the date -> `conf:'disputed'` is
//     permitted and `basis` is MANDATORY; the primary publishes the date ->
//     `conf:'confirmed'` per inv. 39. `basis` is inside cat.hash (§3.13), so
//     the argument sits next to every journaled verdict.
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
// purpose — the ENA check that motivated TZ-06 returned six mutually
// inconsistent answers from six trackers, so "many aggregators agree" is not
// evidence and two of them are not a quorum.
//
// This list is the registry's TRUST ROOT: an entry is `confirmed` if and only if
// one of these hosts (or a subdomain of one — see isPrimary) stands behind its
// date. **It changes only through a TZ**, never as a side effect of wanting a
// particular entry to pass. Adding a host here promotes every future entry that
// cites it, which is exactly the decision an implementer may not take alone.
// Suffix matching means subdomains need not be listed one by one:
// `docs.ethena.fi` and `support.binance.com` already resolve through `ethena.fi`
// and `binance.com`.
const PRIMARY = [
    'z.cash', 'zips.z.cash', 'electriccoin.co', 'forum.zcashcommunity.com',
    'zfnd.org',
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
// TZ-09 §4.4. `both` is an ADDITIVE enum value and the schema version stays 1:
// production's loader and catalystCheck already handle it (`c.dir !== mine` is
// true on both sides, `c.dir === mine` false on both), so an older build fed the
// same file behaves identically (inv. 1, 9). It is the only honest `dir` for a
// scheduled event whose date is known and whose outcome is not.
const KEYS = ['d', 'dir', 'kind', 't', 'conf', 'src', 'added'];
const DIRS = ['long', 'short', 'both'];
const KINDS = ['unlock', 'protocol', 'listing', 'macro'];
const CONFS = ['confirmed', 'disputed'];
// TZ-21 §3.A. `basis` records the derivation an entry stands on when the primary
// publishes the MECHANISM and not the CALENDAR (§2 rule 3). It is deliberately
// NOT in KEYS: a key listed there is demanded of every entry, and a `confirmed`
// entry whose primary published the date argues nothing beyond `src`. So the key
// set below admits it and the five assertions after it carry the whole rule —
// mandatory at `conf:'disputed'`, constrained wherever it appears.
//
// ASCII because the file is ASCII (§3.15) and `basis` is prose the next EDITOR
// reads, not a string the board prints: `t` is the escaped one. A `\uXXXX`
// escape parses to a non-ASCII character, so the test is on the PARSED value and
// not on the file's bytes, which the byte scan covers separately.
const BASIS_MAX = 300;
function isAscii(s) {
    for (let i = 0; i < s.length; i++) if (s.charCodeAt(i) > 127) return false;
    return true;
}

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
        deq(tag + 'exact key set besides the optional basis',
            Object.keys(e).filter(function (k) { return k !== 'basis'; }).sort(),
            KEYS.slice().sort());
        ok(tag + 'd is YYYY-MM-DD', /^\d{4}-\d{2}-\d{2}$/.test(e.d));
        ok(tag + 'd parses', isFinite(Date.parse(e.d + 'T00:00:00Z')));
        ok(tag + 'added is YYYY-MM-DD', /^\d{4}-\d{2}-\d{2}$/.test(e.added));
        ok(tag + 'dir in enum', DIRS.indexOf(e.dir) >= 0);
        ok(tag + 'kind in enum', KINDS.indexOf(e.kind) >= 0);
        ok(tag + 'conf in enum', CONFS.indexOf(e.conf) >= 0);
        ok(tag + 'src is an array', Array.isArray(e.src));
        ok(tag + 't is a non-empty string', typeof e.t === 'string' && e.t.length > 0);
        // Five unconditional checks, so the count is the same whether or not the
        // entry carries the field: a guard that skips its assertions on absent
        // data verifies nothing on exactly the entry that omitted it (inv. 22).
        const hasBasis = Object.prototype.hasOwnProperty.call(e, 'basis');
        const basisStr = hasBasis && typeof e.basis === 'string';
        ok(tag + 'basis is present at conf disputed', e.conf !== 'disputed' || hasBasis);
        ok(tag + 'basis is a string when present', !hasBasis || basisStr);
        ok(tag + 'basis is non-empty after trim when present',
           !hasBasis || (basisStr && e.basis.trim().length > 0));
        ok(tag + 'basis is ASCII-only when present', !hasBasis || (basisStr && isAscii(e.basis)));
        ok(tag + 'basis is at most ' + BASIS_MAX + ' chars when present',
           !hasBasis || (basisStr && e.basis.length <= BASIS_MAX));
        const key = sym + '|' + e.d + '|' + e.t;
        ok(tag + 'no duplicate (sym, d, t)', !seenTriple[key]);
        seenTriple[key] = true;
    });
});
console.log('  symbols: ' + Object.keys(CAT.items).length + ', entries: ' + entries);
ok('the registry is not empty', entries > 0);

// TZ-09 §4.7. `updated` is what the board and the journal print as the age of
// the registry, and nothing forced it to move: an edit that adds an entry and
// forgets the field currently passes every other check while advertising a
// staleness that is a lie. No wall clock is involved — the file is compared
// against itself, so this assertion cannot expire (§4.8).
let newestAdded = '';
Object.keys(CAT.items).forEach(function (sym) {
    CAT.items[sym].forEach(function (e) { if (e.added > newestAdded) newestAdded = e.added; });
});
ok('updated (' + CAT.updated + ') is not older than the newest added (' + newestAdded + ')',
   typeof CAT.updated === 'string' && CAT.updated >= newestAdded);

// ── 2. Quorum (§3.15 / инв. 39, изменён ТЗ-09) ──────────────────────────────
// `confirmed` costs ONE PRIMARY SOURCE. The two-host branch is gone.
//
// The old rule accepted "two distinct hosts of any kind", which contradicted the
// paragraph above PRIMARY that motivated it: the ENA probe returned six mutually
// inconsistent answers from six trackers, and a rule that lets any two of those
// six confer authority buys precisely what TZ-09 found. The same probe on AVAX
// returned three different next-unlock dates in one week (10 August; 21 August
// with 3 584 842 tokens; 12 May), none of them the 18 September the registry
// claimed, with no Avalanche primary publishing an unlock calendar at all; on
// HYPE it returned four different dates across four trackers plus a ~30x gap
// between the projected unlock and the amount the team itself claims. Two of
// them agreeing is not corroboration, it is the same guess copied twice.
//
// Since `confirmed` CLOSES a trading side, the bar is the source's AUTHORITY,
// not the number of sites repeating it. Aggregators may still appear in `src` as
// corroboration; they can no longer confer authority, however many of them agree.
function hostOf(u) {
    const m = /^https?:\/\/([^/?#]+)/i.exec(String(u));
    if (!m) return null;
    return m[1].toLowerCase().replace(/:\d+$/, '').replace(/^www\./, '');
}
// Suffix match on a DOT boundary, so `docs.ethena.fi` resolves through
// `ethena.fi` while `notethena.fi` does not, and `ethena.fi.attacker.com` — where
// the primary is a left label of somebody else's domain — does not either.
function isPrimary(h) {
    for (let i = 0; i < PRIMARY.length; i++) {
        const p = PRIMARY[i];
        if (h === p || h.slice(-(p.length + 1)) === '.' + p) return true;
    }
    return false;
}
function quorumOk(e) {
    if (e.conf !== 'confirmed') return true;      // disputed carries no burden
    const hosts = (e.src || []).map(hostOf).filter(function (h) { return h !== null; });
    for (let i = 0; i < hosts.length; i++) if (isPrimary(hosts[i])) return true;
    return false;
}

console.log('=== 2. Quorum rule ===');
const QCASES = [
    { want: true,  why: 'one primary source',        e: { conf: 'confirmed', src: ['https://zips.z.cash/zip-0253'] } },
    { want: false, why: 'two independent aggregators — was `pass` before TZ-09',
                                                     e: { conf: 'confirmed', src: ['https://tokenomist.ai/x', 'https://cryptorank.io/y'] } },
    { want: false, why: 'one aggregator alone',      e: { conf: 'confirmed', src: ['https://tokenomist.ai/x'] } },
    { want: false, why: 'no source at all',          e: { conf: 'confirmed', src: [] } },
    { want: false, why: 'same aggregator twice',     e: { conf: 'confirmed', src: ['https://tokenomist.ai/x', 'https://www.tokenomist.ai/y'] } },
    { want: false, why: 'not a URL',                 e: { conf: 'confirmed', src: ['со слов'] } },
    { want: true,  why: 'disputed needs nothing',    e: { conf: 'disputed',  src: [] } },
    { want: true,  why: 'primary plus aggregator',   e: { conf: 'confirmed', src: ['https://github.com/zcash/zips/pull/1', 'https://cryptorank.io/y'] } },
    { want: true,  why: 'subdomain of a primary',    e: { conf: 'confirmed', src: ['https://docs.ethena.fi/ena/tokenomics'] } },
    { want: true,  why: '`www.` and port stripped',  e: { conf: 'confirmed', src: ['https://WWW.Binance.com:443/en/support/announcement/detail/x'] } },
    { want: false, why: 'suffix lookalike',          e: { conf: 'confirmed', src: ['https://notethena.fi/x'] } },
    { want: false, why: 'primary as a left label',   e: { conf: 'confirmed', src: ['https://ethena.fi.attacker.com/x'] } },
    { want: true,  why: 'the live ZEC entry',        e: { conf: 'confirmed', src: ['https://forum.zcashcommunity.com/t/nu7-coinholder-vote/56912'] } }
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

// ── 3. Authority table across the sweep (TZ-09 §4.5) ────────────────────────
// 400 consecutive days x every symbol in tokens[] x both sides, from the same
// fixed START as before TZ-09.
//
// What this section asserted until TZ-09 was "no live entry may veto" and "the
// supporting side sees notes on 15 dates" — statements about the CONTENTS of one
// edition of catalysts.json, true only while every entry was `disputed`. That
// expectation goes red the moment the registry does its job, and it did: the
// first `confirmed` entry turned a passing bench red without a single defect in
// the product. A control whose expectation is a snapshot of the data it controls
// is not a control (inv. 22).
//
// So the expectation is DERIVED from each entry instead, by its own authority:
//
//   conf          dir     veto LONG  veto SHORT  note LONG  note SHORT
//   not confirmed  long       no         no         yes        no
//   not confirmed  short      no         no         no         yes
//   not confirmed  both       no         no         no         no
//   confirmed      long       no         YES        yes        no
//   confirmed      short     YES         no         no         yes
//   confirmed      both      YES        YES         no         no
//
// Read as two independent questions. `conf` decides whether the entry may CLOSE
// a side at all; `dir` decides which side it SUPPORTS. An entry annotates the
// side it supports, and a `confirmed` entry closes every side it does not — so
// `both`, which supports neither, closes both and annotates nothing.
//
// Every veto and every note carries the entry's own `t`; a wrong entry's text on
// the right day is a failure, because the board prints that string as the reason
// it refused the trade.
function iso(ms) { return new Date(ms).toISOString().slice(0, 10); }
// The 15 calendar dates on which an entry acts: the event date and the
// CAT_WINDOW_D before it. CAT_WINDOW_D is read from production (inv. 20, 21) —
// this is the calendar-date form of the assertion, deliberately NOT a second
// copy of the millisecond arithmetic in catalystCheck. The millisecond edges are
// pinned separately in section 4.
function windowDates(d) {
    const ms = Date.parse(d + 'T00:00:00Z');
    const out = [];
    for (let k = P.CAT_WINDOW_D; k >= 0; k--) out.push(iso(ms - k * DAY));
    return out;
}

console.log('=== 3. Authority table across 400 days x ' + SYMS.length + ' symbols x 2 sides ===');

// ── 3a. Overlap guard (TZ-09 §4.6) ──────────────────────────────────────────
// The table above is stated PER ENTRY, and it is only the right expectation
// while at most one entry owns any given swept date. If a coin ever has two
// entries whose windows overlap, the answer on the overlapping days is decided
// by the precedence rule inside catalystCheck — first veto returns, first note
// wins — and NOT by this table. Comparing against the table anyway would test
// the wrong thing quietly, which is the failure mode this whole file exists to
// prevent. Detect it, print it, fail. Today: zero overlaps.
const overlaps = [];
Object.keys(CAT.items).forEach(function (sym) {
    const list = CAT.items[sym];
    for (let i = 0; i < list.length; i++) {
        for (let j = i + 1; j < list.length; j++) {
            const a = windowDates(list[i].d), b = windowDates(list[j].d);
            const shared = a.filter(function (x) { return b.indexOf(x) >= 0; });
            if (shared.length) {
                overlaps.push(sym + '[' + i + '] ' + list[i].d + ' and ' + sym + '[' + j + '] ' +
                              list[j].d + ' share ' + shared.length + ' day(s): ' + shared.join(', '));
            }
        }
    }
});
overlaps.forEach(function (o) { console.log('  OVERLAP ' + o); });
eq('no coin has two entries whose windows overlap', overlaps.length, 0);

// The entry acting on one symbol/date, or null. At most one, guaranteed above.
function actingOn(sym, dayISO) {
    const list = CAT.items[sym] || [];
    for (let i = 0; i < list.length; i++) {
        if (windowDates(list[i].d).indexOf(dayISO) >= 0) return list[i];
    }
    return null;
}
function expected(sym, isLong, dayISO) {
    const e = actingOn(sym, dayISO);
    if (!e) return { veto: null, note: null };
    const supports = e.dir === (isLong ? 'long' : 'short');
    return {
        veto: (e.conf === 'confirmed' && !supports) ? e.t : null,
        note: supports ? e.t : null
    };
}

const START = Date.parse('2026-06-01T11:00:00Z');
let sweep = 0, vetoed = 0, noted = 0;
for (let d = 0; d < 400; d++) {
    const t0 = START + d * DAY;
    const dayISO = iso(t0);
    SYMS.forEach(function (sym) {
        [true, false].forEach(function (isLong) {
            const want = expected(sym, isLong, dayISO);
            const got = P.catalystCheck(sym, isLong, t0);
            sweep++;
            if (want.veto !== null) vetoed++;
            if (want.note !== null) noted++;
            deq(dayISO + ' ' + sym + (isLong ? ' LONG' : ' SHORT'), got, want);
        });
    });
}
console.log('  calls: ' + sweep + ', days a side was closed: ' + vetoed + ', days a side was annotated: ' + noted);
// §4.5 requires the table to hold "on all fifteen calendar dates ending on `d`",
// which the sweep above proves only for dates the sweep actually reaches. An
// entry whose window fell outside START..START+399 would satisfy every deq above
// by comparing null against null — passing while verifying nothing (inv. 22).
// This asserts the premise instead of assuming it.
const firstDay = iso(START), lastDay = iso(START + 399 * DAY);
ok('every entry window falls inside the swept range ' + firstDay + '..' + lastDay,
   Object.keys(CAT.items).every(function (sym) {
       return CAT.items[sym].every(function (e) {
           return windowDates(e.d).every(function (x) { return x >= firstDay && x <= lastDay; });
       });
   }));

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
// TZ-09 §4.4. `dir: 'both'` is the claim that a scheduled binary event —
// a governance vote, a court date, an exchange decision — supports NEITHER side,
// and the claim this TZ makes is that expressing it costs ZERO production
// changes. That claim is proved here, by running the same production
// catalystCheck: `c.dir !== mine` holds on both sides, so a confirmed `both`
// closes both and reaches its early return before any note is set; `c.dir ===
// mine` is false on both sides, so a disputed `both` is completely silent. The
// window edges are the same eight — a new enum value must not move them.
withReg({ ZEC: [mkEntry('confirmed', 'both')] }, function (S) {
    EDGES.forEach(function (c) {
        const t0 = evMs + c.off;
        eq('confirmed both, LONG vetoed — ' + c.why,  S.catalystCheck('ZEC', true,  t0).veto, c.inside ? 'X' : null);
        eq('confirmed both, SHORT vetoed — ' + c.why, S.catalystCheck('ZEC', false, t0).veto, c.inside ? 'X' : null);
        eq('confirmed both, LONG never noted — ' + c.why,  S.catalystCheck('ZEC', true,  t0).note, null);
        eq('confirmed both, SHORT never noted — ' + c.why, S.catalystCheck('ZEC', false, t0).note, null);
    });
});
withReg({ ZEC: [mkEntry('disputed', 'both')] }, function (S) {
    EDGES.forEach(function (c) {
        const t0 = evMs + c.off;
        eq('disputed both, LONG never vetoed — ' + c.why,  S.catalystCheck('ZEC', true,  t0).veto, null);
        eq('disputed both, SHORT never vetoed — ' + c.why, S.catalystCheck('ZEC', false, t0).veto, null);
        eq('disputed both, LONG never noted — ' + c.why,   S.catalystCheck('ZEC', true,  t0).note, null);
        eq('disputed both, SHORT never noted — ' + c.why,  S.catalystCheck('ZEC', false, t0).note, null);
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
