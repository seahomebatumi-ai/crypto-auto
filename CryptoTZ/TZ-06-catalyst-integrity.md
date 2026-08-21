# TZ-06 — Catalyst layer: sourced, quorum-gated, validated

**Canonical filename: `TZ-06-catalyst-integrity.md`.** Commit the file under this
name regardless of the name it arrived with. Destination: `CryptoTZ/`.

**Model: Opus.** Reason: this edit changes the load path of a veto layer inside
`index.html`, changes the journal's extraction contract, and adds a CI gate. Every
failure mode here is silent — a catalyst layer that quietly loads nothing looks
identical to a catalyst layer with nothing to say.

---

## 0. Fingerprint gate — verify BEFORE any work

Run `git fetch --all --prune` first. A file absent from an unfetched clone is not
absent from the repository.

Required state of `SYSTEM-MAP-CRYPTOCALCUL.md` at repository root:

| Anchor | Expected |
|---|---|
| `<!-- EDIT-MARKER 2026-08-14c-NEXT-GATE -->` | present |
| `### 3.13 Verdict journal` | present |
| `## 9. Журнал миграций` — newest entry | `- 2026-08-21 (2):` |
| `## 4. Инварианты — НЕ ЛОМАТЬ` — highest numbered invariant | 38 |

Required state of production files on `main` before the change:

| File | Lines | md5 (first 8) |
|---|---|---|
| `index.html` | 3449 | `ffec1dd1` |
| `main.py` | 506 | `1a5a5d98` |

Any mismatch → stop, report **ЗАБЛОКИРОВАНО**, change nothing.

---

## 1. Why this change exists

`index.html` line 789 holds `var CATALYSTS` — three entries covering three of the
twenty-eight traded coins. None carries a source. `catalystCheck` (line 1837) turns
any entry inside `CAT_WINDOW_D = 14` days that points the other way into a hard veto
that closes a side on that coin.

Measured consequence today: the `ZEC` entry dated `2026-08-25` sits four days inside
the window and is vetoing every SHORT on ZEC. Independent checking does not confirm
that date — Zcash's most recent settled upgrade is NU6.3 (Ironwood, 28.07.2026), the
NU7 deployment ZIP is still a draft with no agreed feature set, and published
timelines put NU7 activation no earlier than October. A trade side is being closed by
an unverified string.

The same check across public unlock trackers for a single ENA event returned six
mutually inconsistent answers spanning 1–29 September and 8.4M–333M tokens. The
conclusion is architectural, not editorial: **catalyst data from public aggregators
cannot be treated as confirmed by default.** A veto is the strongest action in the
direction engine and must not rest on the weakest data in the system.

This TZ does not add catalysts. It makes the layer incapable of vetoing on
unverified data, and makes the data machine-checkable. Coverage of the veto drops to
zero until sourced entries are added — that is the intended outcome, not a
regression.

---

## 2. Changes — exactly six, minimal diff

### 2.1 New file `catalysts.json` at repository root

Schema, version 1. `items` is keyed by the symbol as it appears in `tokens[]`
without the `USDT` suffix.

```json
{
  "v": 1,
  "updated": "2026-08-21",
  "items": {
    "ZEC":  [{ "d": "2026-08-25", "dir": "long",  "kind": "protocol",
               "t": "\u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043d\u0438\u0435 NU7 25.08",
               "conf": "disputed", "src": [], "added": "2026-08-21" }],
    "AVAX": [{ "d": "2026-09-18", "dir": "short", "kind": "unlock",
               "t": "\u0440\u0430\u0437\u043b\u043e\u043a 10.69M AVAX",
               "conf": "disputed", "src": [], "added": "2026-08-21" }],
    "SOL":  [{ "d": "2026-10-01", "dir": "long",  "kind": "protocol",
               "t": "Alpenglow \u0432 \u043e\u043a\u0442\u044f\u0431\u0440\u0435",
               "conf": "disputed", "src": [], "added": "2026-08-21" }]
  }
}
```

Field rules: `d` is `YYYY-MM-DD`; `dir` is `long` or `short`; `kind` is one of
`unlock` · `protocol` · `listing` · `macro`; `conf` is `confirmed` or `disputed`;
`src` is an array of absolute URLs; `t` is the Russian label already used on the
card, kept as `\uXXXX` escapes exactly as in the current literal so the on-screen
string does not change by one byte.

The three entries carry the current text and dates verbatim and are marked
`disputed` because none has a source. No content decision is made in this TZ.

### 2.2 `catalystCheck` — one guard, zero arithmetic change

Inside the existing loop, after the `days` window test and before the direction
test, an entry whose `conf` is not exactly `'confirmed'` may set `out.note` and must
never set `out.veto`. Everything else in the function — the `-1` back-window, the
`CAT_WINDOW_D` forward window, the first-note-wins rule, the early return on veto —
stays as written. Do not touch `CAT_WINDOW_D`.

### 2.3 `index.html` — load the file instead of holding the literal

`var CATALYSTS = { … }` at line 789 becomes `var CATALYSTS = {};` plus
`var CAT_LOADED = false;` and `var CAT_ERR = null;`.

Load once at startup with `XMLHttpRequest` against the same-origin relative path
`catalysts.json` (ES5 only: `var`, string concatenation, no arrow functions, no
template literals, no `fetch`). Rules:

- The board **never blocks** on the load. `update()` runs whether or not the file
  has arrived.
- On success: `CATALYSTS` is set to the parsed `items`, `CAT_LOADED = true`.
- On any failure — network, HTTP status other than 200, unparseable JSON, `v` not
  equal to `1` — `CATALYSTS` stays `{}`, `CAT_LOADED` stays `false`, `CAT_ERR`
  holds a short reason.
- While `CAT_LOADED` is false, the board prints one visible line above the list
  naming the layer as unavailable and giving `CAT_ERR`. Reuse the existing
  `regimeBanner` styling; add no new CSS and no new keyframes (inv. 19). A layer
  that is off must say so — a silent empty object is the exact failure inv. 37
  forbids.

### 2.4 `journal/write.js` — follow the data, not the literal

`'CATALYSTS'` is removed from the `NEED` list. The journal runs inside the
repository checkout, so it reads `catalysts.json` from disk — no network call is
added, and no CoinGecko or Binance budget changes. The `cat` field and its hash
continue to be recorded exactly as §3.13 specifies; the hash is taken over the
serialized `items` object so a re-ordering of keys cannot change it.

A missing, unparseable, or wrong-version `catalysts.json` makes the journal exit
non-zero and fail the workflow. The journal must never record a day whose catalyst
set it could not read (inv. 38).

### 2.5 New bench `bench/catalyst_bench.js`

Loads production functions out of `index.html` through the Node VM sandbox. No
formula is copied (inv. 21). It must cover:

1. **Schema** — every entry has all eight fields; `d` parses; `dir`, `kind`, `conf`
   are inside their enums; `src` is an array; no duplicate `(sym, d, t)`; every key
   of `items` exists in `tokens[]`.
2. **Quorum** — `conf: "confirmed"` requires either two or more entries in `src`, or
   exactly one whose host is on a primary-source allowlist declared at the top of
   the bench (project domains and specification repositories, not aggregators). A
   `confirmed` entry failing this is a bench failure.
3. **Veto containment** — sweep `nowMs` across 400 consecutive days × all 28 symbols
   × both sides; assert `out.veto` is null for every `disputed` entry at every
   offset, and that notes still appear on the days the old literal produced them.
4. **Window identity** — for a synthetic `confirmed` fixture, the days on which the
   veto fires must match the pre-change function exactly, including the `-1` back
   edge and the `CAT_WINDOW_D` forward edge.
5. **Degraded load** — with the loader forced to fail, `CATALYSTS` is `{}`,
   `CAT_LOADED` is false, `CAT_ERR` is non-empty, the banner string is produced,
   `catalystCheck` returns `{veto:null, note:null}` for every symbol, and
   `directionVerdict` completes without throwing on a full fixture row.

Print a total check count and return non-zero on any failure.

### 2.6 `.github/workflows/bench.yml`

Add one step running `node bench/catalyst_bench.js`, placed after the journal step.
Change nothing else in the file.

---

## 3. Non-goals — out of scope, do not touch

`scoreCandidate` · `momentumScore` · `qualityScore` · `scoreFinish` ·
`tradeGeometry` · `marketRegime` · `directionVerdict` beyond its unchanged call into
`catalystCheck` · `leverageDecision` · `invalidationInfo` · `protectionPlan` ·
`liqPrice` · `byScore` · `assignRanks` · `tierOf` · `CAT_WINDOW_D` · the
`coeffs.json` schema · `main.py` · CSS · keyframes · the 28-coin universe · the
Shortcuts schedule · any new runtime dependency for the hourly bot.

No new catalyst entries are added by this TZ. Do not research dates, do not fill
`src`, do not promote anything to `confirmed`. Sourcing is TZ-07.

---

## 4. Validation — run exactly this, report the numbers

| Step | Command | Pass condition |
|---|---|---|
| Syntax, front | `node --check` on the extracted `<script>` | exit 0 |
| Syntax, bot | `python3 -m py_compile main.py` | exit 0, file untouched |
| JSON | `node -e "JSON.parse(require('fs').readFileSync('catalysts.json','utf8'))"` | exit 0 |
| New bench | `node bench/catalyst_bench.js` | 0 failures, check count reported |
| Journal | `node bench/journal_bench.js` | 0 failures |
| Journal, degraded | run with `catalysts.json` renamed away | non-zero exit, message names the file |
| Freshness | `node bench/fresh_bench.js` | 0 failures |
| Board 19.08 | `node bench/verify_board.js` | 108 checks, 0 failures |
| Board 20.08 | `node bench/board2_bench.js` | 129 checks, 0 failures |
| Protection | `node bench/prot_bench.js index.html` | 0 failures |
| Offline verify | `python3 bench/verify_bench.py` | 0 failures |
| Direction | `python3 bench/direction_bench.py --props --fixtures --control --sim` | 0 failures |

**No-regression statement, required in the report.** A usage diff for
`TIER_STRONG` · `TIER_MID` · `TIER_MIN` · `RR_MIN` · `EFF_TREND` · `ENTRY_CHASE_SD`
· `LIQ_MMR` · `MAX_MARGIN_LOSS` · `RES_Z` · `PACE_Z` · `TGT_SIGMA_MIN` ·
`CAT_WINDOW_D` must come back **empty**. `scoreCandidate`, `tradeGeometry`,
`marketRegime` and `leverageDecision` must be byte-identical before and after.
State this explicitly; an absent statement is a rejected report.

**Report must also carry:** line counts and md5 for `index.html`, `main.py` and
`SYSTEM-MAP-CRYPTOCALCUL.md` after the change · the pull-request number and its CI
status · the exact path of the report itself, stated in Russian in the closing
message.

---

## 5. Invariants this change is bound by

Existing: 1 · 9 · 13 · 15 · 18 · 19 · 20 · 21 · 24 · 25 · 37 · 38.

Two new rules the Architect will enter into the System Map — honour them here:

- **39.** A catalyst may veto a side only when it is `confirmed`, and `confirmed`
  requires a quorum of independent sources or one primary source. Unverified data
  may annotate and may never close a trade direction.
- **40.** A layer that failed to load must say so on screen. An empty data structure
  and an unavailable data structure are different states and must never render the
  same.

---

## Что сделать
1. Загрузить `TZ-06-catalyst-integrity.md` в `CryptoTZ/`
2. В Claude Code отправить `EXECUTE TZ-06` — модель **Opus**
3. Прислать `CryptoReports/TZ-06-catalyst-integrity-report.md`
4. Слить pull request после моего вердикта
