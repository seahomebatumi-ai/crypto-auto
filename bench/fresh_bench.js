// bench/fresh_bench.js
// TZ-04 scope C: the freshness badge must separate a scheduled pause from a
// missed refresh.
//
// The rule is NOT copied here (invariant 21): freshnessState is pulled out of
// the <script> block of index.html at runtime and executed as the production
// function. Because it takes `now` as an argument, the schedule window can be
// probed without overriding the global clock.
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

let checks = 0, fails = 0;
function eq(name, got, want) {
    checks++;
    if (got !== want) {
        fails++;
        console.log('  FAIL ' + name + ': got ' + JSON.stringify(got) + ' want ' + JSON.stringify(want));
    }
}
function ok(name, cond) { eq(name, !!cond, true); }

if (typeof P.freshnessState !== 'function') {
    console.log('FAIL freshnessState is not defined in index.html');
    process.exit(1);
}

// A local-time Date for a fixed, DST-quiet calendar day. getHours() returns the
// requested hour in any zone; the assertion below proves it for this runner.
function at(h, m) { return new Date(2026, 7, 21, h, m, 0, 0); }

console.log('=== 0. Production constants and clock construction ===');
eq('STALE_WARN_MIN', P.STALE_WARN_MIN, 75);
eq('STALE_CRIT_MIN', P.STALE_CRIT_MIN, 130);
eq('SCHED_FIRST_H', P.SCHED_FIRST_H, 9);
eq('SCHED_LAST_H', P.SCHED_LAST_H, 1);
eq('SCHED_LAST_M', P.SCHED_LAST_M, 50);
for (let h = 0; h < 24; h++) {
    eq('at(' + h + ':30).getHours()', at(h, 30).getHours(), h);
}

console.log('=== 1. The TZ-04 case table ===');
const TABLE = [
    { h: 14, m: 0,  age: 20,  want: 'ok'    },
    { h: 14, m: 0,  age: 90,  want: 'warn'  },
    { h: 14, m: 0,  age: 200, want: 'crit'  },
    { h: 1,  m: 0,  age: 200, want: 'crit'  },   // 01:00 is still inside the schedule
    { h: 2,  m: 0,  age: 10,  want: 'pause' },
    { h: 3,  m: 0,  age: 70,  want: 'pause' },
    { h: 3,  m: 0,  age: 190, want: 'crit'  },   // two missed runs
    { h: 8,  m: 55, age: 425, want: 'pause' },
    { h: 9,  m: 30, age: 200, want: 'crit'  },   // outside the window, nothing forgiven
    { h: 9,  m: 30, age: 40,  want: 'ok'    }
];
TABLE.forEach(function (c) {
    const pad = (c.h < 10 ? '0' : '') + c.h + ':' + (c.m < 10 ? '0' : '') + c.m;
    const st = P.freshnessState(c.age, at(c.h, c.m));
    eq(pad + ' age ' + c.age, st.kind, c.want);
    eq(pad + ' age ' + c.age + ' mins', st.mins, Math.max(0, Math.round(c.age)));
});

console.log('=== 2. Window boundaries: the pair must land on different sides ===');
const B = [];
function boundary(label, h, m, age) {
    const st = P.freshnessState(age, at(h, m));
    B.push(label + ' age ' + age + ' -> ' + st.kind);
    return st.kind;
}
// 01:59 is outside the night window, 02:00 is the first minute inside it.
const b0159 = boundary('01:59', 1, 59, 80);
const b0200 = boundary('02:00', 2,  0, 80);
ok('01:59 vs 02:00 differ at age 80', b0159 !== b0200);
eq('01:59 age 80 is the plain ladder', b0159, 'warn');
eq('02:00 age 80 is forgiven', b0200, 'pause');
// 08:59 is the last minute inside the window, 09:00 the first plan run again.
const b0859 = boundary('08:59', 8, 59, 200);
const b0900 = boundary('09:00', 9,  0, 200);
ok('08:59 vs 09:00 differ at age 200', b0859 !== b0900);
eq('08:59 age 200 is forgiven', b0859, 'pause');
eq('09:00 age 200 is the plain ladder', b0900, 'crit');
B.forEach(function (line) { console.log('  ' + line); });

console.log('=== 3. Outside the night window the old ladder is untouched ===');
// The oracle is the ladder as it stood before TZ-04, rebuilt from the
// PRODUCTION constants above - this is what "not one number changes" means.
function ladder(age) {
    if (age > P.STALE_CRIT_MIN) return 'crit';
    if (age > P.STALE_WARN_MIN) return 'warn';
    return 'ok';
}
const AGES = [0, 0.4, 1, 30, 74, 75, 76, 129, 130, 131, 200, 600, 5000];
let outside = 0;
for (let h = 0; h < 24; h++) {
    if (h >= 2 && h < P.SCHED_FIRST_H) continue;
    for (const m of [0, 17, 30, 59]) {
        for (const age of AGES) {
            eq('ladder ' + h + ':' + m + ' age ' + age,
               P.freshnessState(age, at(h, m)).kind, ladder(age));
            outside++;
        }
    }
}
console.log('  ladder points verified outside the window: ' + outside);

console.log('=== 4. Structural properties across the whole day ===');
let pauseSeen = 0;
for (let h = 0; h < 24; h++) {
    for (const m of [0, 25, 50, 59]) {
        const now = at(h, m);
        const inWindow = (h >= 2 && h < P.SCHED_FIRST_H);
        let sawNonPause = false;
        for (const age of [0, 5, 20, 60, 85, 140, 300, 420, 500, 900, 4000]) {
            const st = P.freshnessState(age, now);
            ok('kind is one of four @' + h + ':' + m + ' age ' + age,
               ['ok', 'warn', 'crit', 'pause'].indexOf(st.kind) >= 0);
            eq('mins rounds @' + h + ':' + m + ' age ' + age,
               st.mins, Math.max(0, Math.round(age)));
            if (st.kind === 'pause') {
                pauseSeen++;
                // Forgiveness is a prefix in age: once the badge has stopped
                // forgiving at this instant, a larger age never forgives again.
                ok('pause is a prefix in age @' + h + ':' + m + ' age ' + age, !sawNonPause);
                ok('pause only inside the night window @' + h + ':' + m, inWindow);
            } else {
                sawNonPause = true;
            }
        }
    }
}
console.log('  pause outcomes observed: ' + pauseSeen);

console.log('=== 5. Negative control: the bench can actually fail ===');
// A check that never fires proves nothing (invariant 22). Prove the comparator
// reports a mismatch, without letting the probe count against this run and
// without printing a FAIL line that a reader would take for a real one.
const before = fails;
const realLog = console.log;
console.log = function () {};
eq('deliberate mismatch', P.freshnessState(20, at(14, 0)).kind, 'crit');
console.log = realLog;
const detected = (fails === before + 1);
fails = before;
checks -= 1;
ok('comparator detects a wrong answer', detected);
console.log('  comparator reported the planted mismatch: ' + detected);

console.log('\n--- checks: ' + checks + '  fails: ' + fails + ' ---');
if (checks === 0) {
    console.log('FAIL bench verified nothing');
    process.exit(1);
}
process.exit(fails === 0 ? 0 : 1);
