#!/usr/bin/env python3
"""Стенд движка направления (SYSTEM_MAP §3.12).

Инвариант 21 соблюдён буквально: НИ ОДНОЙ копии продакшн-математики.
JS вырезается из index.html по именам с сопоставлением скобок и исполняется
настоящим node; метрики монеты считаются функциями, вырезанными из main.py
через AST. Правка любого из двух файлов меняет стенд автоматически.

Режимы:
    --identity   тождество старого и нового scoreCandidate (200k входов)
    --props      структурные свойства вердикта (связность, монотонность)
    --fixtures   воспроизведение доски Босса 18-19.08 (данные ранга 1)
    --sim        синтетические миры: что вето делает с R-кратными
    --all        всё подряд; код возврата 1 при любом провале
"""
import argparse
import ast
import json
import os
import random
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NEW_HTML = os.path.join(ROOT, "index.html")
OLD_HTML = os.path.join(ROOT, "orig.html")
BOT_PY = os.path.join(ROOT, "main.py")

CONSTS = [
    "FEE_TAKER", "LIQ_MMR", "RISK_Z", "H_NOISE", "H_REACT", "H_BTC", "L_CAP", "L_MIN",
    "INV_FLOOR_SD", "INV_CAP_SD", "MAX_MARGIN_LOSS", "EFF_TREND", "PACE_Z",
    "VOL_ABNORMAL", "VOL_HARD", "VOL_STOP", "RES_Z", "RES_R2_CAP",
    "RR_MIN", "TGT_SIGMA_MIN", "ENTRY_CHASE_SD", "REG_STRESS_Z",
    "CAT_WINDOW_D", "STRESS_MULT", "TIER_STRONG", "TIER_MID", "TIER_MIN",
]
FUNCS = [
    "has", "firstNum", "clamp01", "sigmaDay", "normCdf", "touchProb",
    "liqPrice", "liqTouchProb", "lStruct", "lNoise", "advBeta", "lBtcCheck",
    "volRegime", "residual7", "lMoney", "invalidationInfo", "fixHint",
    "leverageDecision", "scoreCandidate", "qualityScore", "scoreFinish",
    "tierOf", "marketRegime", "tradeGeometry", "momentumScore",
    "catalystCheck", "directionVerdict", "rangePos", "sideRelevant",
    "byScore", "assignRanks",
    "fmtP", "pctTxt", "numAttr",
]


# ---------------------------------------------------------------- extraction
def script_of(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"<script>(.*)</script>", src, re.S)
    if not m:
        raise SystemExit("no <script> in %s" % path)
    return m.group(1)


def cut_function(js, name):
    """Вырезать `function NAME(...) {...}` сопоставлением скобок."""
    m = re.search(r"^function %s\s*\(" % re.escape(name), js, re.M)
    if not m:
        raise SystemExit("function %s not found" % name)
    i = js.index("{", m.end() - 1)
    depth, j, in_s, in_c, esc = 0, i, None, None, False
    while j < len(js):
        c = js[j]
        if in_c == "//":
            if c == "\n":
                in_c = None
        elif in_s:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == in_s:
                in_s = None
        elif c == "/" and js[j + 1:j + 2] == "/":
            in_c = "//"
        elif c in "'\"":
            in_s = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return js[m.start():j + 1]
        j += 1
    raise SystemExit("unbalanced braces in %s" % name)


def cut_var(js, name):
    m = re.search(r"^var %s\s*=" % re.escape(name), js, re.M)
    if not m:
        raise SystemExit("var %s not found" % name)
    j, depth, in_s, esc = m.end(), 0, None, False
    while j < len(js):
        c = js[j]
        if in_s:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == in_s:
                in_s = None
        elif c in "'\"":
            in_s = c
        elif c in "{[(":
            depth += 1
        elif c in "}])":
            depth -= 1
        elif c == ";" and depth == 0:
            return js[m.start():j + 1]
        j += 1
    raise SystemExit("unterminated var %s" % name)


def harness(names_new, extra=""):
    """Собрать JS-окружение из ПРОДАКШН-кода без единой копии."""
    js = script_of(NEW_HTML)
    parts = ["'use strict';", "var cachedFunding = {};"]
    for c in CONSTS:
        parts.append(cut_var(js, c))
    parts.append(cut_var(js, "CATALYSTS"))
    for f in names_new:
        parts.append(cut_function(js, f))
    parts.append(extra)
    return "\n".join(parts)


def run_node(code):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(code)
        path = fh.name
    try:
        p = subprocess.run(["node", path], capture_output=True, text=True)
        if p.returncode != 0:
            print(p.stdout[-4000:])
            print(p.stderr[-4000:], file=sys.stderr)
            raise SystemExit("node failed")
        return json.loads(p.stdout)
    finally:
        os.unlink(path)


def bot_funcs():
    """window_stats / window_vol из main.py через AST — без копий."""
    tree = ast.parse(open(BOT_PY, encoding="utf-8").read())
    want = {"window_stats", "window_vol"}
    ns = {}
    src = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in want:
            src.append(ast.get_source_segment(
                open(BOT_PY, encoding="utf-8").read(), node))
    exec("import numpy as np\n" + "\n\n".join(src), ns)
    return ns


# ---------------------------------------------------------------- checks
def check_identity(n=200000):
    """Старый и новый scoreCandidate обязаны совпадать БИТ В БИТ."""
    old_js = script_of(OLD_HTML)
    new_js = script_of(NEW_HTML)
    old_fn = cut_function(old_js, "scoreCandidate").replace(
        "function scoreCandidate(", "function scoreOld(", 1)
    code = "\n".join(
        ["'use strict';", "var cachedFunding = {};"]
        + [cut_var(new_js, c) for c in
           ["EFF_TREND", "PACE_Z", "VOL_ABNORMAL"]]
        + [cut_function(new_js, f) for f in
           ["has", "clamp01", "sigmaDay", "volRegime",
            "scoreCandidate", "qualityScore", "scoreFinish"]]
        + [old_fn]
        + [r"""
function rnd(s){ s.x = (s.x * 1103515245 + 12345) & 0x7fffffff; return s.x / 0x7fffffff; }
function maybe(s, v){ return rnd(s) < 0.15 ? null : v; }
var st = { x: 12345 }, bad = 0, cmp = 0;
for (var i = 0; i < %d; i++) {
  var vol = rnd(st) * 0.04;
  var mn  = 1 + rnd(st) * 50;
  var mx  = mn * (1 + rnd(st) * 3);
  var cur = mn * (1 + rnd(st) * 3);
  var cd = {
    volatility: rnd(st) < 0.05 ? null : vol,
    min_price: maybe(st, mn), max_price: maybe(st, mx),
    r7: maybe(st, (rnd(st) - 0.5) * 0.6), r30: maybe(st, (rnd(st) - 0.5) * 1.2),
    vol7: maybe(st, vol * (0.3 + rnd(st) * 3)),
    eff14: maybe(st, (rnd(st) - 0.5) * 6),
    vol_ratio: maybe(st, rnd(st) * 2),
    rank: maybe(st, Math.floor(rnd(st) * 300) + 1),
    rank_prev: maybe(st, Math.floor(rnd(st) * 300) + 1),
    fdv_mc: maybe(st, rnd(st) * 6)
  };
  var sym = 'S' + (i %% 7);
  cachedFunding[sym] = rnd(st) < 0.3 ? null : (rnd(st) - 0.4) * 0.003;
  var p24 = maybe(st, (rnd(st) - 0.5) * 40);
  var qv  = maybe(st, Math.pow(10, 3 + rnd(st) * 7));
  var isLong = rnd(st) < 0.5;
  var a = scoreOld(cd, sym, cur, p24, qv, isLong);
  var b = scoreCandidate(cd, sym, cur, p24, qv, isLong);
  cmp++;
  if (JSON.stringify(a) !== JSON.stringify(b)) bad++;
}
console.log(JSON.stringify({ compared: cmp, mismatch: bad }));
""" % n])
    r = run_node(code)
    ok = r["mismatch"] == 0 and r["compared"] == n
    return ok, "scoreCandidate тождество: сверено %d, расхождений %d" % (
        r["compared"], r["mismatch"]), r["compared"]


def check_props(n=60000):
    """Структурные свойства вердикта."""
    code = harness(FUNCS, r"""
function rnd(s){ s.x = (s.x * 1103515245 + 12345) & 0x7fffffff; return s.x / 0x7fffffff; }
var st = { x: 987654321 };
var both = 0, tradeNoGeo = 0, waitBadGeo = 0, stressTrade = 0, trendBoth = 0;
var checks = 0, trades = 0, waits = 0, nones = 0, rrFail = 0;
// Инв. 43: `cmp` растёт В ТОЧКЕ СРАВНЕНИЯ и НИГДЕ больше. `checks` остаётся
// числом СЦЕНАРИЕВ и живёт только в сообщении: сценарий — не сверка.
var cmp = 0;
for (var i = 0; i < %d; i++) {
  var vol = 0.002 + rnd(st) * 0.02;
  var mn  = 1 + rnd(st) * 100;
  var mx  = mn * (1 + 0.05 + rnd(st) * 2.5);
  var cur = mn * (1 + rnd(st) * (mx / mn - 1));
  var cd = {
    volatility: vol, min_price: mn, max_price: mx,
    min30: mn * (1 + rnd(st) * 0.3), max30: mx * (1 - rnd(st) * 0.3),
    r7: (rnd(st) - 0.5) * 0.5, r14: (rnd(st) - 0.5) * 0.8,
    r30: (rnd(st) - 0.5) * 1.0,
    vol7: vol * (0.4 + rnd(st) * 2.5), eff14: (rnd(st) - 0.5) * 5,
    vol_ratio: rnd(st) * 2, rank: Math.floor(rnd(st) * 200) + 1,
    rank_prev: Math.floor(rnd(st) * 200) + 1, fdv_mc: rnd(st) * 5,
    up_beta_90: 0.5 + rnd(st) * 2, down_beta_90: 0.5 + rnd(st) * 2,
    up_r2_90: rnd(st) * 0.7, down_r2_90: rnd(st) * 0.7
  };
  var btc = { volatility: 0.003 + rnd(st) * 0.012,
              r7: (rnd(st) - 0.5) * 0.3, r14: (rnd(st) - 0.5) * 0.5,
              min_price: 50000, max_price: 90000 };
  var reg = marketRegime(btc);
  var hi = cur * (1 + rnd(st) * 0.12), lo = cur * (1 - rnd(st) * 0.12);
  var qv = Math.pow(10, 5 + rnd(st) * 4);
  var p24 = (rnd(st) - 0.5) * 25;
  var pair = 'P', name = 'NOCAT';
  var out = {};
  for (var k = 0; k < 2; k++) {
    var isLong = (k === 0);
    var dec = leverageDecision(cd, cur, isLong, btc);
    var rc7 = residual7(cd, btc);
    out[k] = directionVerdict(cd, pair, name, cur, p24, qv, isLong,
                              reg, dec, hi, lo, rc7, Date.UTC(2026, 7, 19));
  }
  checks++;
  cmp++; if (out[0].action === 'trade' && out[1].action === 'trade') both++;
  cmp++; if (reg.mode === 'stress' &&
      (out[0].action !== 'none' || out[1].action !== 'none')) stressTrade++;
  cmp++; if (reg.mode === 'trend' && out[0].action !== 'none'
      && out[1].action !== 'none') trendBoth++;
  for (var k2 = 0; k2 < 2; k2++) {
    var v = out[k2];
    if (v.action === 'trade') {
      trades++;
      // Три сверки стоят ПОД условием сознательно: у неторгуемой стороны
      // геометрии нет, и сверять там нечего. Считается то, что исполнилось.
      cmp++; if (!v.geo || v.geo.veto.length) tradeNoGeo++;
      cmp++; if (v.geo && v.geo.rr !== null && v.geo.rr < RR_MIN) rrFail++;
      cmp++; if (v.geo && v.geo.wait !== null) waitBadGeo++;
    } else if (v.action === 'wait') { waits++; }
    else { nones++; }
  }
}
console.log(JSON.stringify({ checks: checks, cmp: cmp, both: both,
  stressTrade: stressTrade, trendBoth: trendBoth, tradeNoGeo: tradeNoGeo,
  rrFail: rrFail, waitBadGeo: waitBadGeo,
  trades: trades, waits: waits, nones: nones }));
""" % n)
    r = run_node(code)
    fails = []
    if r["both"]:        fails.append("обе стороны торгуемы: %d" % r["both"])
    if r["stressTrade"]: fails.append("сделка в стрессе: %d" % r["stressTrade"])
    if r["trendBoth"]:   fails.append("две стороны в тренде: %d" % r["trendBoth"])
    if r["tradeNoGeo"]:  fails.append("сделка при вето: %d" % r["tradeNoGeo"])
    if r["rrFail"]:      fails.append("сделка с R:R<порога: %d" % r["rrFail"])
    if r["waitBadGeo"]:  fails.append("сделка при погоне: %d" % r["waitBadGeo"])
    msg = ("свойства: %d сценариев -> сделок %d, ожиданий %d, отказов %d"
           % (r["checks"], r["trades"], r["waits"], r["nones"]))
    if fails:
        msg += " | ПРОВАЛ: " + "; ".join(fails)
    # Инв. 43: возвращается СЧЁТЧИК из точки сравнения, а не `сценарии * 8`.
    # Множитель 8 был допущением о числе утверждений на сценарий, и ничто его
    # не удерживало: сверок на сценарий три плюс три на КАЖДУЮ торгуемую
    # сторону, а торгуемых сторон на сценарии от нуля до двух.
    return not fails, msg, r["cmp"]


def check_regime():
    """Слой 0: стресс СИММЕТРИЧЕН по знаку z (ТЗ-12, стадия A).

    Решётка по z на [-4, +4] и по volatility поперёк границы VOL_HARD.
    Утверждается ровно то, что задано спецификацией:
      mode === 'stress'  тогда и только тогда, когда  v >= VOL_HARD или |z| >= REG_STRESS_Z
      dir  === 0         в КАЖДОЙ стрессовой ячейке
    Плюс зеркальное свойство, которое НЕ ссылается ни на один порог: при том же
    v и том же eff режим у +z и у -z обязан совпадать. Односторонняя редакция
    сравнения проваливает его без единого упоминания REG_STRESS_Z.
    """
    code = harness(FUNCS, r"""
var Z = REG_STRESS_Z, VH = VOL_HARD, RH = Math.sqrt(H_NOISE), RE = Math.sqrt(2 * H_NOISE);
// Сетка волатильности ПОПЕРЁК границы: под ней, ровно на ней, над ней.
var VS = [0.0005, 0.002, 0.005, 0.01, 0.015, VH - 1e-9, VH - 1e-12, VH,
          VH + 1e-12, VH + 1e-9, 0.025, 0.03, 0.05];
// Сетка z на [-4, +4] шагом 0.1 плюс точные границы и их окрестности плюс
// два журнальных дня 21.08 (+4.06) и 22.08 (+4.01).
var ZS = [];
for (var q = -40; q <= 40; q++) ZS.push(q / 10);
[Z, Z - 1e-9, Z - 1e-12, Z + 1e-12, Z + 1e-9, 4.06, 4.01, 0].forEach(function (t) {
  ZS.push(t); if (t !== 0) ZS.push(-t);
});
// eff подобран так, чтобы задеть обе стороны порога EFF_TREND и клип +-3.
var ES = [0, 0.3, -0.3, EFF_TREND, -EFF_TREND, 0.9, -0.9, 3.5, -3.5];

var cmp = 0, cells = 0, badMode = 0, badDir = 0, badMirror = 0, badZ = 0,
    badKnown = 0, badEff = 0, exact = 0, stressCells = 0, trendCells = 0, rangeCells = 0;
var firstBad = '';

function want(v, z) { return (v >= VH || (z !== null && Math.abs(z) >= Z)) ? 'stress' : null; }

for (var i = 0; i < VS.length; i++) {
  var v = VS[i];
  for (var j = 0; j < ZS.length; j++) {
    for (var k = 0; k < ES.length; k++) {
      var z = ZS[j], e = ES[k];
      var btc = { volatility: v, r7: z * v * RH, r14: e * v * RE };
      var out = marketRegime(btc);
      cells++;
      // Целостность фикстуры: продакшн обязан сообщить ровно тот z, который
      // ему задан, иначе решётка проверяет не то, что думает.
      cmp++; if (out.z === null || Math.abs(out.z - z) > 1e-9 * (Math.abs(z) + 1)) {
        badZ++; if (!firstBad) firstBad = 'z ' + z + ' -> ' + out.z;
      }
      cmp++; if (out.known !== true) badKnown++;
      if (out.z !== null && Math.abs(out.z) === Z) exact++;

      // Спецификация, дословно.
      var expected = want(v, out.z);
      if (expected === null) {
        var effClipped = Math.max(-3, Math.min(3, e));
        expected = Math.abs(effClipped) >= EFF_TREND ? 'trend' : 'range';
      }
      cmp++; if (out.mode !== expected) {
        badMode++;
        if (!firstBad) firstBad = 'v=' + v + ' z=' + z + ' eff=' + e
                                + ' -> ' + out.mode + ', ждали ' + expected;
      }
      if (out.mode === 'stress') {
        stressCells++;
        cmp++; if (out.dir !== 0) {
          badDir++;
          if (!firstBad) firstBad = 'dir=' + out.dir + ' в стрессе v=' + v + ' z=' + z;
        }
      } else if (out.mode === 'trend') {
        trendCells++;
        cmp++; if (out.dir !== (out.eff > 0 ? 1 : -1)) badEff++;
      } else {
        rangeCells++;
        cmp++; if (out.dir !== 0) badEff++;
      }

      // Зеркало: тот же v, тот же eff, противоположный знак z. Ни одного
      // порога в утверждении нет — только симметрия.
      var mirror = marketRegime({ volatility: v, r7: -z * v * RH, r14: e * v * RE });
      cmp++; if (mirror.mode !== out.mode) {
        badMirror++;
        if (!firstBad) firstBad = 'зеркало v=' + v + ' z=' + z + ': '
                                + out.mode + ' vs ' + mirror.mode;
      }
      cmp++; if (mirror.dir !== out.dir) badMirror++;
    }
  }
}
// z отсутствует: стресс обязан остаться доступным по одной волатильности.
[0.0005, VH - 1e-9, VH, 0.05].forEach(function (v) {
  var out = marketRegime({ volatility: v, r14: 0 });
  cells++;
  cmp++; if (out.z !== null) badZ++;
  var expected = v >= VH ? 'stress' : 'range';
  cmp++; if (out.mode !== expected) { badMode++; if (!firstBad) firstBad = 'z=null v=' + v; }
  cmp++; if (out.mode === 'stress' && out.dir !== 0) badDir++;
});
console.log(JSON.stringify({ cmp: cmp, cells: cells, badMode: badMode, badDir: badDir,
  badMirror: badMirror, badZ: badZ, badKnown: badKnown, badEff: badEff, exact: exact,
  stressCells: stressCells, trendCells: trendCells, rangeCells: rangeCells,
  firstBad: firstBad }));
""")
    r = run_node(code)
    fails = []
    if r["badMode"]:   fails.append("режим не по спецификации: %d" % r["badMode"])
    if r["badDir"]:    fails.append("dir != 0 в стрессе: %d" % r["badDir"])
    if r["badMirror"]: fails.append("асимметрия по знаку z: %d" % r["badMirror"])
    if r["badZ"]:      fails.append("фикстура не воспроизводит z: %d" % r["badZ"])
    if r["badKnown"]:  fails.append("known != true: %d" % r["badKnown"])
    if r["badEff"]:    fails.append("dir не по знаку eff: %d" % r["badEff"])
    # Инв. 23: точная граница z = +-REG_STRESS_Z обязана БЫТЬ в прогоне, а не
    # предполагаться. Ноль таких ячеек — провал решётки, а не успех.
    if not r["exact"]:
        fails.append("ни одна ячейка не встала ровно на |z| = REG_STRESS_Z")
    if not r["stressCells"] or not r["trendCells"] or not r["rangeCells"]:
        fails.append("решётка не покрыла все три режима: stress %d / trend %d / range %d"
                     % (r["stressCells"], r["trendCells"], r["rangeCells"]))
    msg = ("режим: %d ячеек -> стресс %d, тренд %d, диапазон %d; "
           "точных границ |z| = %.1f: %d"
           % (r["cells"], r["stressCells"], r["trendCells"], r["rangeCells"],
              2.0, r["exact"]))
    if fails:
        msg += " | ПРОВАЛ: " + "; ".join(fails)
        if r["firstBad"]:
            msg += "\n  первая ячейка: " + r["firstBad"]
    return not fails, msg, r["cmp"]


def check_fixtures():
    """Данные ранга 1 с доски Босса 18-19.08.2026."""
    code = harness(FUNCS, r"""
function mk(o){ return o; }
var out = [];
// --- GRAM, доска 19.08 11:47-11:48 ---
var gram = { volatility: 0.0094, min_price: 1.3027, max_price: 2.2473,
             min30: 1.3027, max30: 2.2473,
             r7: -0.025, r14: -0.02, r30: -0.05, vol7: 0.0094,
             eff14: -0.1, rank: 25, rank_prev: 25, fdv_mc: 1.9,
             up_beta_90: 1.00, down_beta_90: 1.00,
             up_r2_90: 0.13, down_r2_90: 0.13, vol_ratio: 1.0 };
var btc = { volatility: 0.0065, r7: 0.01, r14: 0.004,
            min_price: 59300, max_price: 90000 };
var reg = marketRegime(btc);
for (var s = 0; s < 2; s++) {
  var isLong = (s === 0);
  var dec = leverageDecision(gram, 1.3190, isLong, btc);
  var geo = tradeGeometry(gram, 1.3190, isLong, dec, 1.3260, 1.3150);
  var v = directionVerdict(gram, 'GRAMUSDT', 'GRAM', 1.3190, 0.30, 3e7,
            isLong, reg, dec, 1.3260, 1.3150, residual7(gram, btc),
            Date.UTC(2026, 7, 19));
  out.push({ coin: 'GRAM', side: isLong ? 'long' : 'short',
             rr: geo ? geo.rr : null, tgtSig: geo ? geo.tgtSig : null,
             veto: geo ? geo.veto : null, action: v.action, why: v.why });
}
// --- ZEC, доска 19.08 11:48-11:49 ---
var zec = { volatility: 0.0134, min_price: 298.5784, max_price: 682.7536,
            // max30 обратно вычислен из НАПЕЧАТАННОГО доской стопа
            // 574.4101 = max30*(1+0.5*sigmaDay): данные ранга 1, не оценка.
            // min30 доской не показан -> помечен как допущение и в проверках
            // не участвует (проверяется только сам факт отказа от лонга).
            min30: 400.0, max30: 556.156,
            r7: 0.056, r14: 0.02, r30: -0.011, vol7: 0.0134,
            eff14: -0.12, rank: 14, rank_prev: 13, fdv_mc: 1.0,
            up_beta_90: 1.66, down_beta_90: 1.66,
            up_r2_90: 0.17, down_r2_90: 0.17, vol_ratio: 1.0 };
for (var s2 = 0; s2 < 2; s2++) {
  var isL = (s2 === 0);
  var dec2 = leverageDecision(zec, 502.98, isL, btc);
  var geo2 = tradeGeometry(zec, 502.98, isL, dec2, 518.0, 484.0);
  var v2 = directionVerdict(zec, 'ZECUSDT', 'ZEC', 502.98, -0.98, 3.4e8,
            isL, reg, dec2, 518.0, 484.0, residual7(zec, btc),
            Date.UTC(2026, 7, 19));
  out.push({ coin: 'ZEC', side: isL ? 'long' : 'short',
             rr: geo2 ? geo2.rr : null, tgtSig: geo2 ? geo2.tgtSig : null,
             veto: geo2 ? geo2.veto : null, action: v2.action, why: v2.why,
             wait: v2.wait });
}
console.log(JSON.stringify({ regime: reg.mode, rows: out }));
""")
    r = run_node(code)
    rows = {(x["coin"], x["side"]): x for x in r["rows"]}
    fails, lines = [], []
    # Пре-регистрация: что стенд ОБЯЗАН показать (§3.12, инв. 23). Инв. 43:
    # `cmp` растёт перед КАЖДЫМ утверждением. Строк четыре, но утверждений
    # тоже четыре, а не четыре на строку: ZEC min30 помечен допущением и в
    # сверках не участвует, у GRAM лонга сверяется только R:R.
    cmp = 0
    gs = rows[("GRAM", "short")]
    cmp += 1
    if gs["action"] != "none" or not gs["veto"]:
        fails.append("GRAM шорт не отклонён")
    gl = rows[("GRAM", "long")]
    cmp += 1
    if gl["rr"] is None or abs(gl["rr"] - 7.7) > 0.25:
        fails.append("GRAM лонг R:R %.2f != 7.7 доски" % (gl["rr"] or -1))
    zs = rows[("ZEC", "short")]
    cmp += 1
    if zs["rr"] is None or abs(zs["rr"] - 2.9) > 0.15:
        fails.append("ZEC шорт R:R %.2f != 2.9 доски" % (zs["rr"] or -1))
    zl = rows[("ZEC", "long")]
    cmp += 1
    if zl["action"] == "trade":
        fails.append("ZEC лонг выдан сделкой без отката")
    for k, x in sorted(rows.items()):
        lines.append("  %-5s %-5s rr=%s  %sсигм  -> %s %s"
                     % (x["coin"], x["side"],
                        "н/д" if x["rr"] is None else "%.2f" % x["rr"],
                        "н/д" if x["tgtSig"] is None else "%.2f" % x["tgtSig"],
                        x["action"], x["why"] or ""))
    msg = "фикстуры (режим %s):\n%s" % (r["regime"], "\n".join(lines))
    if fails:
        msg += "\n  ПРОВАЛ: " + "; ".join(fails)
    return not fails, msg, cmp


def _path(rnd, n, vol, world, start=100.0, mu=0.0):
    p = [start]
    for _ in range(n):
        shock = rnd.gauss(0, vol)
        if world == "mean":
            pull = -0.004 * (p[-1] / start - 1.0)
            p.append(max(1e-9, p[-1] * (1 + pull + shock)))
        else:
            p.append(max(1e-9, p[-1] * (1 + mu + shock)))
    return p


def _cd(bot, p):
    """Метрики монеты — ТОЛЬКО функциями, вырезанными из main.py (инв. 21)."""
    t0 = 1_700_000_000_000
    pl = [[t0 + i * 3600_000, v] for i, v in enumerate(p)]
    r7, _, _ = bot["window_stats"](pl, 7)
    r14, _, _ = bot["window_stats"](pl, 14)
    r30, mn30, mx30 = bot["window_stats"](pl, 30)
    v7 = bot["window_vol"](pl, 7)
    rv = (sum((p[i + 1] / p[i] - 1) ** 2 for i in range(len(p) - 1))
          / (len(p) - 1)) ** 0.5
    eff = None
    if r14 is not None and rv > 0:
        eff = max(-3.0, min(3.0, r14 / (rv * (336 ** 0.5))))
    return {"volatility": rv, "min_price": min(p), "max_price": max(p),
            "min30": mn30, "max30": mx30, "r7": r7, "r14": r14, "r30": r30,
            "vol7": v7, "eff14": eff, "vol_ratio": 1.0}


def check_sim(seeds=14, coins=90):
    """Синтетические миры. ПРАВИЛО зафиксировано до прогона (инв. 23) и с тех
    пор НЕ менялось:

      1) средняя R-кратная отобранной ТРОЙКИ у движка не ниже, чем у прежней
         системы (топ-3 по счёту), в каждом из трёх миров;
      2) доля сделок с целью внутри недельного шума падает до нуля;
      3) число выданных сделок падает — это цена, и она называется вслух.

    Сравнение — «топ-3 против топ-3»: именно так рейтинг и используется.
    Предсказания здесь нет ни у одной стороны; измеряется ГЕОМЕТРИЯ отбора.

    Первый прогон 19.08 провалился из-за ДВУХ дефектов генератора, а не
    правила: (а) статистика BTC была прибита к плоской, поэтому в трендовом
    мире движок судил каналом возврата — переключатель режима не проверялся
    вовсе; (б) снос ±0.35 сигмы в час давал рост в ~1900 раз за 90 дней.
    Исправлен генератор; правило осталось прежним.
    """
    bot = bot_funcs()
    rnd = random.Random(20260819)
    batches = []
    for world in ("mean", "trend", "walk"):
        for seed in range(seeds):
            bvol = 0.004 + rnd.random() * 0.004
            bmu = (rnd.choice([-1, 1]) * bvol * 0.03) if world == "trend" else 0.0
            bp = _path(rnd, 90 * 24, bvol, world, 60000.0, bmu)
            bcd = _cd(bot, bp)
            btc = {"volatility": bcd["volatility"], "r7": bcd["r7"],
                   "r14": bcd["r14"], "min_price": bcd["min_price"],
                   "max_price": bcd["max_price"]}
            rows = []
            for c in range(coins):
                vol = 0.003 + rnd.random() * 0.018
                mu = (rnd.choice([-1, 1]) * vol * 0.03) if world == "trend" else 0.0
                p = _path(rnd, 90 * 24, vol, world, 100.0, mu)
                fwd = _path(rnd, 30 * 24, vol, world, p[-1], mu)
                cd = _cd(bot, p)
                cd.update({"rank": 1 + (c % 120), "rank_prev": 1 + (c % 120),
                           "fdv_mc": 1.2, "up_beta_90": 1.0,
                           "down_beta_90": 1.0, "up_r2_90": 0.3,
                           "down_r2_90": 0.3})
                rows.append({"cur": p[-1], "hi24": max(p[-24:]),
                             "lo24": min(p[-24:]), "fwd": fwd, "cd": cd})
            batches.append({"world": world, "btc": btc, "rows": rows})

    code = harness(FUNCS, """
var B = %s;
var out = [];
for (var b = 0; b < B.length; b++) {
  var bat = B[b], reg = marketRegime(bat.btc);
  for (var i = 0; i < bat.rows.length; i++) {
    var d = bat.rows[i];
    for (var s = 0; s < 2; s++) {
      var isLong = (s === 0);
      var dec = leverageDecision(d.cd, d.cur, isLong, bat.btc);
      if (!dec.inv) continue;
      var geo = tradeGeometry(d.cd, d.cur, isLong, dec, d.hi24, d.lo24);
      if (!geo) continue;
      var sc = scoreCandidate(d.cd, 'P', d.cur, 0, 1e7, isLong);
      if (!sc) continue;
      var v = directionVerdict(d.cd, 'P', 'NOCAT', d.cur, 0, 1e7, isLong,
                reg, dec, d.hi24, d.lo24, null, Date.UTC(2026, 7, 19));
      // ГОНКА БАРЬЕРОВ до первого касания. Цель — структурный ориентир 90д,
      // поэтому горизонт замера 30 суток: мерить его 7 днями значит
      // гарантировать отрицательную R обеим системам и ничего не различить.
      // Издержки берутся продакшн-константой: 2 тейкерских ноги в единицах R
      // равны 2*FEE_TAKER/risk (плечо сокращается).
      var tgt = isLong ? d.cd.max_price : d.cd.min_price;
      var stop = dec.inv.price;
      var cost = geo.risk > 0 ? (2 * FEE_TAKER) / geo.risk : 0;
      var R = -cost;
      for (var f = 0; f < d.fwd.length; f++) {
        var px = d.fwd[f];
        var tHit = isLong ? (px >= tgt) : (px <= tgt);
        var sHit = isLong ? (px <= stop) : (px >= stop);
        if (sHit) { R = -1 - cost; break; }
        if (tHit && geo.rr !== null) { R = geo.rr - cost; break; }
      }
      out.push({ b: b, w: bat.world, reg: reg.mode, sc: sc.score,
                 vsc: v.score, act: v.action, R: R, sig: geo.tgtSig });
    }
  }
}
console.log(JSON.stringify(out));
""" % json.dumps(batches))
    res = run_node(code)
    per = {}
    for x in res:
        per.setdefault(x["b"], []).append(x)
    agg = {}
    regs = {}
    for b, rows in per.items():
        w = rows[0]["w"]
        regs.setdefault(w, {}).setdefault(rows[0]["reg"], 0)
        regs[w][rows[0]["reg"]] += 1
        base = sorted(rows, key=lambda x: -x["sc"])[:3]
        act = [x for x in rows if x["act"] == "trade"]
        new = sorted(act, key=lambda x: -(x["vsc"] or 0))[:3]
        a = agg.setdefault(w, {"nb": 0, "nn": 0, "rb": [], "rn": [],
                               "sb": 0, "sn": 0, "skip": 0})
        a["nb"] += len(base)
        a["nn"] += len(new)
        a["rb"] += [x["R"] for x in base]
        a["rn"] += [x["R"] for x in new]
        a["sb"] += sum(1 for x in base if x["sig"] is not None and x["sig"] < 1.0)
        a["sn"] += sum(1 for x in new if x["sig"] is not None and x["sig"] < 1.0)
        if not new:
            a["skip"] += 1
    fails, lines = [], []
    # Инв. 43, §4.2 ТЗ-08: блок статистический, поэтому чисел два и они разные.
    # СВЕРКИ — два пре-зарегистрированных утверждения на каждый из трёх миров;
    # правило 3 («число сделок падает») названо вслух и утверждением не
    # является. ОБЪЁМ ВЫБОРКИ — len(res) траекторий — печатается в сообщении.
    # Прежний `len(res)` возвращал выборку вместо сверок.
    cmp = 0
    for w in ("mean", "trend", "walk"):
        a = agg[w]
        rb = sum(a["rb"]) / len(a["rb"]) if a["rb"] else 0.0
        rn = sum(a["rn"]) / len(a["rn"]) if a["rn"] else 0.0
        cmp += 1
        if a["rn"] and rn < rb - 1e-9:
            fails.append("%s: средняя R упала %+.3f -> %+.3f" % (w, rb, rn))
        cmp += 1
        if a["sn"]:
            fails.append("%s: остались цели внутри шума (%d)" % (w, a["sn"]))
        lines.append(
            "  %-5s режим %-22s | сделок %4d -> %4d | средняя R %+.3f -> %+.3f"
            " | цель в шуме %d -> %d | пустых дат %d"
            % (w, str(regs[w]), a["nb"], a["nn"], rb, rn, a["sb"], a["sn"],
               a["skip"]))
    msg = ("синтетика (%d дат x %d монет, наблюдений: %d):\n%s"
           % (len(per), coins, len(res), "\n".join(lines)))
    if fails:
        msg += "\n  ПРОВАЛ: " + "; ".join(fails)
    return not fails, msg, cmp


def check_display(n=4000, coins=28):
    """Отображение и порядок (правка Босса 19.08).

    Пре-регистрация — что стенд обязан подтвердить:
      1) tierOf режет строго по TIER_STRONG/TIER_MID/TIER_MIN, четыре имени,
         четыре цвета, границы включительно;
      2) список отсортирован СТРОГО по счёту, состояние на порядок не влияет;
      3) нумерация СПЛОШНАЯ 1..N без дыр, и номер есть у КАЖДОЙ показанной
         строки СО СЧЁТОМ; его нет ровно у двух: строк без счёта и строк,
         свёрнутых как нерелевантные стороне (row.off). Прежнее ожидание
         «номер только у торгуемых и ожидающих» — редакция 19.08 (3),
         развёрнутая инв. 34 в тот же день: номер снова МЕСТО В РЕЙТИНГЕ,
         а не утверждение о сделке;
      4) нумерация ведётся ПО СТОРОНЕ НЕЗАВИСИМО, поэтому одна монета имеет
         право на номер в ОБОИХ списках — это следствие п. 3, а не дефект.
         Инв. 30 при этом не ослаблен и не тронут: гарантию «одна сторона»
         несёт action, и её проверяет --props (счётчик `both`), а не номер.
    """
    code = harness(FUNCS, r"""
// Инв. 43: `cmp` растёт В ТОЧКЕ СРАВНЕНИЯ и возвращается в JSON — ровно
// так же, как ordFail и badNo. `lists`, `trades`, `waits`, `greys`, `bothNo`
// остаются ИЗМЕРЕНИЯМИ: они печатаются, но ничего не утверждают.
var out = { tier: [], cmp: 0, ordFail: 0, gapFail: 0, badNo: 0, bothNo: 0,
            lists: 0, trades: 0, waits: 0, greys: 0 };
// 1. Границы тиров
var probe = [100, 70.0, 69.99, 50.0, 49.99, 35.0, 34.99, 0, -5];
for (var i = 0; i < probe.length; i++) {
  var t = tierOf(probe[i]);
  out.tier.push([probe[i], t.n, t.c]);
}
function rnd(s){ s.x = (s.x * 1103515245 + 12345) & 0x7fffffff; return s.x / 0x7fffffff; }
var st = { x: 20260819 };
for (var L = 0; L < %d; L++) {
  var vol = 0.003 + rnd(st) * 0.02;
  var btc = { volatility: 0.003 + rnd(st) * 0.012,
              r7: (rnd(st) - 0.5) * 0.3, r14: (rnd(st) - 0.5) * 0.5,
              min_price: 50000, max_price: 90000 };
  var reg = marketRegime(btc);
  // Данные монет генерируются ОДИН раз и судятся обеими сторонами: иначе
  // C5 в лонг-списке и C5 в шорт-списке — разные монеты, и проверка
  // инварианта 30 ничего не проверяет.
  var pool = [];
  for (var c = 0; c < %d; c++) {
    var v2 = 0.003 + rnd(st) * 0.02;
    var mn = 1 + rnd(st) * 100;
    var mx = mn * (1 + 0.05 + rnd(st) * 2.5);
    var cur = mn * (1 + rnd(st) * (mx / mn - 1));
    pool.push({ name: 'C' + c, cur: cur,
      p24: (rnd(st) - 0.5) * 25, qv: Math.pow(10, 5 + rnd(st) * 4),
      hi: cur * (1 + rnd(st) * 0.12), lo: cur * (1 - rnd(st) * 0.12),
      cd: { volatility: v2, min_price: mn, max_price: mx,
        min30: mn * (1 + rnd(st) * 0.3), max30: mx * (1 - rnd(st) * 0.3),
        r7: (rnd(st) - 0.5) * 0.5, r14: (rnd(st) - 0.5) * 0.8,
        r30: (rnd(st) - 0.5) * 1.0, vol7: v2 * (0.4 + rnd(st) * 2.5),
        eff14: (rnd(st) - 0.5) * 5, vol_ratio: rnd(st) * 2,
        rank: Math.floor(rnd(st) * 200) + 1,
        rank_prev: Math.floor(rnd(st) * 200) + 1, fdv_mc: rnd(st) * 5,
        up_beta_90: 0.5 + rnd(st) * 2, down_beta_90: 0.5 + rnd(st) * 2,
        up_r2_90: rnd(st) * 0.7, down_r2_90: rnd(st) * 0.7 } });
  }
  var sides = {};
  for (var sIdx = 0; sIdx < 2; sIdx++) {
    var isLong = (sIdx === 0);
    var rows = [];
    for (var pi = 0; pi < pool.length; pi++) {
      var pc = pool[pi];
      var dec = leverageDecision(pc.cd, pc.cur, isLong, btc);
      var vd = directionVerdict(pc.cd, 'P', pc.name, pc.cur, pc.p24, pc.qv,
                 isLong, reg, dec, pc.hi, pc.lo,
                 residual7(pc.cd, btc), Date.UTC(2026, 7, 19));
      rows.push({ t: { name: pc.name }, cd: pc.cd, vd: vd,
                  sc: (vd.score !== null) ? { score: vd.score } : null });
    }
    rows.sort(byScore);
    assignRanks(rows);
    out.lists++;
    for (var i2 = 1; i2 < rows.length; i2++) {
      var a = rows[i2 - 1].sc ? rows[i2 - 1].sc.score : -1;
      var b = rows[i2].sc ? rows[i2].sc.score : -1;
      out.cmp++;
      if (b - a > 0.05) out.ordFail++;
    }
    var seen = 0;
    for (var i3 = 0; i3 < rows.length; i3++) {
      var r = rows[i3], act = r.vd.action;
      var sc = r.sc ? r.sc.score : null;
      // Инв. 34: номер есть у КАЖДОЙ показанной строки со счётом; отнимают
      // его только отсутствие счёта и свёртка стороны (row.off).
      var wants = sc !== null && !r.off;
      // Одна сверка номера на строку: либо номер обязан быть следующим по
      // порядку, либо его обязано не быть вовсе. Ветки взаимоисключающие.
      out.cmp++;
      if (wants) { seen++; if (r.no !== seen) out.gapFail++; }
      else if (r.no !== 0) out.badNo++;
      if (act === 'trade') out.trades++;
      else if (act === 'wait') out.waits++;
      else out.greys++;
    }
    sides[sIdx] = rows;
  }
  // 4. Монеты с номером С ОБЕИХ сторон. Считаются, но провалом больше не
  // являются: нумерация ведётся ПО СТОРОНЕ независимо, и номер вернулся к
  // смыслу «место в рейтинге этой стороны». Число печатается, чтобы разворот
  // ожидания был ИЗМЕРЕН, а не подразумевался (инв. 37).
  // bothNo НЕ инкрементирует cmp: число печатается, но провалом не является
  // (инв. 34), а счёт проверок считает СВЕРКИ, а не измерения.
  for (var c2 = 0; c2 < %d; c2++) {
    var nA = 0, nB = 0;
    for (var q = 0; q < sides[0].length; q++)
      if (sides[0][q].t.name === 'C' + c2) nA = sides[0][q].no;
    for (var q2 = 0; q2 < sides[1].length; q2++)
      if (sides[1][q2].t.name === 'C' + c2) nB = sides[1][q2].no;
    if (nA > 0 && nB > 0) out.bothNo++;
  }
}
console.log(JSON.stringify(out));
""" % (n // coins, coins, coins))
    r = run_node(code)
    # Нижний тир — «Фон», не «Наблюдать»: слово называет ОЧЕРЕДЬ ВНИМАНИЯ,
    # а не рекомендацию, и «Наблюдать» читалось как указание (инв. 33).
    want = {100: "Сильный", 70.0: "Сильный", 69.99: "Средний", 50.0: "Средний",
            49.99: "Кандидат", 35.0: "Кандидат", 34.99: "Фон",
            0: "Фон", -5: "Фон"}
    fails = []
    # Сверки границ тиров идут здесь, поэтому и счётчик здесь. Инв. 43.
    cmp = r["cmp"]
    for score, name, col in r["tier"]:
        cmp += 1
        if want[score] != name:
            fails.append("tierOf(%s) = %s, ждали %s" % (score, name, want[score]))
    if r["ordFail"]: fails.append("порядок не по счёту: %d" % r["ordFail"])
    if r["gapFail"]: fails.append("дыра в нумерации: %d" % r["gapFail"])
    if r["badNo"]:   fails.append("номер там, где не положен: %d" % r["badNo"])
    msg = ("отображение: %d списков -> торгуемых %d, ожиданий %d, серых %d; "
           "границы тиров 70/50/35 включительно, нумерация сплошная; "
           "монет с номером с обеих сторон %d (разрешено, инв. 34)"
           % (r["lists"], r["trades"], r["waits"], r["greys"], r["bothNo"]))
    if fails:
        msg += "\n  ПРОВАЛ: " + "; ".join(fails)
    # Инв. 43: прежнее выражение `списков * торгуемых + len(tier)` было
    # ПРОИЗВЕДЕНИЕМ двух не связанных величин — числа списков и числа
    # торгуемых карточек во всех списках сразу. Оно не раскладывалось ни на
    # одну сверку. Теперь это сумма счётчиков: порядок (пара соседей),
    # нумерация (строка) и границы тиров (проба).
    return not fails, msg, cmp


def check_control(seeds=16, coins=70, days=360):
    """Контроль с ИЗВЕСТНЫМ ответом (инв. 23) — проверяется сам стенд.

    Чистое блуждание, гонка барьеров БЕЗ обрезания горизонта. Теория:
    при нулевом сносе P(цель раньше стопа) = risk/(risk+reward), значит
    E[R] = rr*risk/(risk+reward) - 1*reward/(risk+reward) = 0 у ЛЮБОГО
    отбора. Если стенд честен, обе руки обязаны дать около нуля минус
    издержки. Отсюда же следует главное ограничение: на блуждании
    геометрия не может поднять среднюю R — и не обязана. Она работает
    против ИЗДЕРЖЕК и против сноса, а не против математики.
    """
    bot = bot_funcs()
    rnd = random.Random(4242)
    batches = []
    for seed in range(seeds):
        bvol = 0.004 + rnd.random() * 0.004
        bp = _path(rnd, 90 * 24, bvol, "walk", 60000.0, 0.0)
        bcd = _cd(bot, bp)
        btc = {"volatility": bcd["volatility"], "r7": bcd["r7"],
               "r14": bcd["r14"], "min_price": bcd["min_price"],
               "max_price": bcd["max_price"]}
        rows = []
        for c in range(coins):
            vol = 0.004 + rnd.random() * 0.012
            p = _path(rnd, 90 * 24, vol, "walk", 100.0, 0.0)
            fwd = _path(rnd, days * 24, vol, "walk", p[-1], 0.0)
            cd = _cd(bot, p)
            cd.update({"rank": 1 + (c % 120), "rank_prev": 1 + (c % 120),
                       "fdv_mc": 1.2, "up_beta_90": 1.0, "down_beta_90": 1.0,
                       "up_r2_90": 0.3, "down_r2_90": 0.3})
            rows.append({"cur": p[-1], "hi24": max(p[-24:]),
                         "lo24": min(p[-24:]), "fwd": fwd, "cd": cd})
        batches.append({"world": "walk", "btc": btc, "rows": rows})

    code = harness(FUNCS, """
var B = %s;
var out = [];
for (var b = 0; b < B.length; b++) {
  var bat = B[b], reg = marketRegime(bat.btc);
  for (var i = 0; i < bat.rows.length; i++) {
    var d = bat.rows[i];
    for (var s = 0; s < 2; s++) {
      var isLong = (s === 0);
      var dec = leverageDecision(d.cd, d.cur, isLong, bat.btc);
      if (!dec.inv) continue;
      var geo = tradeGeometry(d.cd, d.cur, isLong, dec, d.hi24, d.lo24);
      if (!geo || geo.rr === null) continue;
      var sc = scoreCandidate(d.cd, 'P', d.cur, 0, 1e7, isLong);
      if (!sc) continue;
      var v = directionVerdict(d.cd, 'P', 'NOCAT', d.cur, 0, 1e7, isLong,
                reg, dec, d.hi24, d.lo24, null, Date.UTC(2026, 7, 19));
      var tgt = isLong ? d.cd.max_price : d.cd.min_price;
      var stop = dec.inv.price, done = false, R = 0;
      for (var f = 0; f < d.fwd.length; f++) {
        var px = d.fwd[f];
        if (isLong ? (px <= stop) : (px >= stop)) { R = -1; done = true; break; }
        if (isLong ? (px >= tgt) : (px <= tgt)) { R = geo.rr; done = true; break; }
      }
      if (!done) continue;
      out.push({ sc: sc.score, act: v.action, vsc: v.score, R: R });
    }
  }
}
console.log(JSON.stringify(out));
""" % json.dumps(batches))
    res = run_node(code)
    base = sorted(res, key=lambda x: -x["sc"])
    new = [x for x in res if x["act"] == "trade"]
    def stat(a):
        if not a:
            return 0.0, 0.0
        mu = sum(x["R"] for x in a) / len(a)
        if len(a) < 2:
            return mu, 0.0
        var = sum((x["R"] - mu) ** 2 for x in a) / (len(a) - 1)
        return mu, (var / len(a)) ** 0.5
    rb, sb = stat(base)
    rn, sn = stat(new)
    # Допуск ВЫВОДИТСЯ из выборки, а не назначается: R-кратные тяжелохвостые
    # (-1 против +rr), и фиксированный порог здесь был бы произволом.
    fails = []
    # Инв. 43, §4.2 ТЗ-08: блок статистический, чисел два. СВЕРКИ — два
    # утверждения о том, что обе руки лежат на нуле в пределах 2SE. ОБЪЁМ
    # ВЫБОРКИ — len(res) исходов гонки барьеров — печатается в сообщении.
    # Сотни тысяч траекторий, сведённые в две статистики, дают две сверки.
    cmp = 0
    cmp += 1
    if abs(rb) > 2 * sb + 1e-9: fails.append("прежняя %+.3f вне 2SE" % rb)
    cmp += 1
    if new and abs(rn) > 2 * sn + 1e-9: fails.append("движок %+.3f вне 2SE" % rn)
    msg = ("контроль блуждания без обрезания (наблюдений: %d): прежняя %+.3f "
           "(2SE %.3f), движок %+.3f (2SE %.3f, n=%d) — обе обязаны лежать "
           "на нуле, и это ГРАНИЦА полезности геометрии"
           % (len(res), rb, 2 * sb, rn, 2 * sn, len(new)))
    if fails:
        msg += " | ПРОВАЛ: " + "; ".join(fails)
    return not fails, msg, cmp


def main():
    ap = argparse.ArgumentParser()
    for f in ("identity", "props", "fixtures", "display", "sim", "control", "all"):
        ap.add_argument("--" + f, action="store_true")
    a = ap.parse_args()
    todo = []
    if a.all or a.identity:  todo.append(("ТОЖДЕСТВО", check_identity))
    if a.all or a.props:     todo.append(("СВОЙСТВА", check_props))
    # ТЗ-12 §2 D. Симметрия режима идёт под тем же флагом сознательно:
    # отдельный флаг потребовал бы 13-го шага в bench.yml, а ТЗ держит 12.
    if a.all or a.props:     todo.append(("РЕЖИМ", check_regime))
    if a.all or a.fixtures:  todo.append(("ФИКСТУРЫ", check_fixtures))
    if a.all or a.display:   todo.append(("ОТОБРАЖЕНИЕ", check_display))
    if a.all or a.control:   todo.append(("КОНТРОЛЬ", check_control))
    if a.all or a.sim:       todo.append(("СИНТЕТИКА", check_sim))
    if not todo:
        ap.print_help()
        return 2
    bad, total = 0, 0
    for name, fn in todo:
        ok, msg, cnt = fn()
        total += cnt
        # Инв. 22: блок, не сверивший НИЧЕГО, — провал, а не успех. Требуется
        # до того, как блок встанет в ворота (п. 7.12 контракта): зелёный,
        # не сверивший ничего, — ровно то состояние, ради которого это ТЗ.
        if cnt == 0:
            ok = False
            msg += "\n  ПРОВАЛ: блок не сверил ничего"
        print("[%s] %s\n%s\n" % ("OK " if ok else "FAIL", name, msg))
        if not ok:
            bad += 1
    print("ИТОГО проверок: %d | провалов блоков: %d" % (total, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
