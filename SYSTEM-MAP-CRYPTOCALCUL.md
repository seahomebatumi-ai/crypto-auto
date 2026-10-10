# SYSTEM MAP — Pro Crypto Tool

Technical contract of the live system: architecture, data flow, modules,
dependencies, invariants. Consult before any code change and when interpreting a
metric. Nothing here is history — the record of how the system got here is git
history plus `CryptoReports/**`. Workflow, roles and acceptance live in the
Architect's canon and in `EXECUTOR-INSTRUCTIONS.md` (the contract); this map
states only what the system is.

**Language.** English, except on-screen strings and board block names, which are
quoted verbatim in Russian because that is what the code prints.

---

## 0. Fingerprint

**Revision 2026-10-10-a.** No file of the table below moves. **The audit of the run of 10.10.2026 — the first
press under methodology `2026-10-09-b` to deliver an answer, both subagents in the foreground — found the three
roles inside their rules and the rules at fault, and `ANALYST-INSTRUCTIONS.md` `2026-10-10-a` repairs three of
them.** The answer publishes the funded book alone and names the rest of the list's trend coins, without a price,
in one line «Без размера:» — the answer of 10.10 printed fifteen trade objects around the three its budget and
its sheriff funded, four of the twelve others longs under a bearish verdict, and the owner read it as
contradictory; the ranking key is read in units of the owner's risk, ties to the larger turnover, because once
every object is sized from its own stop a key in per cent ranks the coins by their volatility; and a verdict may
only take away, the standing every unscored input has here (row «The verdict record is unscored»). §6, §6a and
§16 do not move: `sec6_md5` stays `d924d29faa3a2c7c0b5519d8e1f5fc45` and the hunter's brief is byte-identical.
**The owner asked on 10.10.2026 when the strategies can be trusted, and the answer is a reading:** row «The
engine's published book had never been scored» is re-measured — 40 trades of the runs of 26.09–08.10 closed at
−4.53 R and the sized book from 03.10 closed 9 at −7.0 R, beside +7.85 R on 62 through 26.09 that three trades
carry — so the gate of row «The engine places no order on the exchange» is read and not passed. **The grade the
owner sizes at 1 % rests on `residual7`, display-only since its archive reading** (inv. 27, §3.10a): new row
«`СИЛЬНАЯ` rests on a display-only signal».

**Revision 2026-10-09-f.** No file of the table below moves. **TZ-63 executed on 09.10.2026 on the VPS and is
accepted:** its branch `tz-63-vps-run-answer-only` at `cc6c498` — `vps` tree
`96d72e8df795c79ad7d77c9ee73d4bbc284534e7`, pull request #51 — takes effect when the deployer installs the merge,
and until then the run unit delivers any non-empty final message as before. The Architect's session reproduced
the branch's three files to the MD5, its selftest at 21 sections and 314 checks, and the record at 48 answers of
48 with the status of 09.10 refused. **The installed CLI carries the variable's name:** the program the run unit
starts is `/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`, 238 767 288 bytes, with
`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` four times and `run_in_background` forty — a name, not yet an effect
(row «A headless run delivered a status as its answer»). No analysis run has started since `ef89542`.

**Revision 2026-10-09-e.** No file of the table below moves. **The first press under `2026-10-09-a` delivered no
analysis:** the writer committed at 2026-10-09T13:01:27Z, the trader sent the hunter to the background — the
Claude Code the VPS runs, 2.1.282, starts a subagent in the background by default — and ended its turn with a
status in English, which the unit delivered to the owner as the answer; no analyst commit followed. **The
defect is the Architect's:** methodology §15 never said that the hunter's call returns its report, and it said
the trader «writes nothing while the hunter runs». **Repaired at three levels:** `ANALYST-INSTRUCTIONS.md`
`2026-10-09-b` runs both subagents in the foreground and makes the run one turn whose last message is the
answer; contract v28 states it as the floor; **TZ-63, issued against this revision,** sets
`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` in the run unit and makes `vps/run.py` deliver a final message only
where a line of it opens with «Время анализа:», and the notice «Анализ не завершён.» otherwise (row «A headless
run delivered a status as its answer»).

**Revision 2026-10-09-d.** No file of the table below moves. **The role split decided at `-09-c` is
written:** `ANALYST-INSTRUCTIONS.md` `2026-10-09-a` and contract v27 make the analysis run one session — the
trader, the one decision-maker — that launches a hunter after the freeze and a sheriff after the book is
composed. The hunter reads 118 972 bytes of the methodology's 385 311 and the sheriff 4 402; the trader
reads every section but those two briefs, 369 240 bytes against the 344 556 one agent read before, and no
page the hunt reads enters its context (row «One agent executes the whole methodology in one run», closed).
**The owner's message of 09.10.2026** — the method must be the one a professional trader enters by, and
where the large players enter, and in which coins, must be computed — **is answered by the hunter's
positioning read:** Binance's own statistics of its top traders, its crowd, its open interest and its
funding, each coin classed against its own month, which may refuse a trade, take `СИЛЬНАЯ` away, halve a
size and order the outside-list slots, and never produce a side, a level, a grade or a size until the
exchange's archive of the same series measures it (row «The positioning classes are unmeasured», new). **The
state gains the fields the watcher waits on** — a horizon entry's class and minute, and the four `# BTC`
levels (row «The watcher has no calendar and no regime input»). §6 and §6a did not move: `sec6_md5` stays
`d924d29faa3a2c7c0b5519d8e1f5fc45`, and every lane read under `2026-10-08-a` stays fresh.

**Revision 2026-10-09-c.** No file of the table below moves. **TZ-62 merged at `d446a6b` on 09.10.2026**
(`vps` tree `d65dfbd5d1830b477a084e2f288a851e377d6947`), and the first alert under the rule reached the owner
at 2026-10-09T07:00Z — a perpetual's monitoring tag, which the old rule recorded only (row «The owner's alert
channel carries promotions and misses contract notices»). **The owner asked again on 09.10.2026 whether the
hunter, the trader and the risk officer run independently. They do not, and the split is decided:** the reading
it waited on since `2026-10-05-a` — TZ-60's usage at `high` — was taken on 05.10, so the split is the next
Architect edit (row «One agent executes the whole methodology in one run»).

**Revision 2026-10-09-b.** No file of the table below moves. **TZ-62 executed on 09.10.2026 on the VPS and is
accepted:** its branch `tz-62-vps-alert-rule` at `42ecda3` — `vps` tree `d65dfbd5d1830b477a084e2f288a851e377d6947`,
pull request #50 — takes effect when the deployer installs the merge, and the old rule runs until then. Replayed
on the stream's whole record, nineteen publications since 05.10, the rule alerts none; the old rule's two alerts
over the same record were both the BNB promotions; and the exchange watcher's snapshot classes all 216 TradFi
contracts `TRADIFI_PERPETUAL`, a type A2 never alerts (row «The owner's alert channel carries promotions and
misses contract notices»).

**Revision 2026-10-09-a.** No file of the table below moves. **The owner's request of 09.10.2026 is decided,
and TZ-62 is issued against this revision:** his chat carries what can change a trade on Binance Futures or
bring a candidate to his spot portfolio, and no promotion at all. Both alerts known to have reached him from
the announcement stream were promotions naming BNB, the exchange's reward currency — 07.10 at 09:00:08Z,
which TZ-61 read, and 08.10 at 09:00Z, on his screenshot as «⚡ Binance · 13:00 Тбилиси · Latest Activities:
MET Trading Tournament: Trade to Share Up to 400 BNB Token Vouchers» — because `announce.act` alerted on any
title naming a list coin, whatever its catalogue. **Decided: the catalogue and the kind of notice decide
before the ticker does,** and a Futures notice that names a list contract only in its body now reaches him
with those contracts named (row «The owner's alert channel carries promotions and misses contract notices»).
The rest of his message — a funding level, order-book depth, unlocks — is answered in the same row, and none
of it is an alert.

**Revision 2026-10-08-b.** No file of the table below moves. **`ANALYST-INSTRUCTIONS.md` `2026-10-08-a`
carries the three changes revision `-08-a` of this map named, and the audit of the run of 07.10.2026
adds two.** The announcement stream's record and `fapi/v1/exchangeInfo` replace the path `robots.txt`
disallows (row «The engine's exchange-announcement read is a path its own §6 forbids», closed);
DefiLlama's `emissionsIndex`, measured from the Architect's session on 08.10.2026, replaces the refused
coin pages (rows «Unlock dates have no primary lane» and «DefiLlama's unlock datasets…»); the owner's
verdicts print on every catalyst item ahead and close the answer as «# BTC — МОЙ ВЕРДИКТ», each per cent
measured and each word logged to be scored (row «An expert verdict per catalyst and for BTC», closed, and
row «The verdict record is unscored», new); the structural file belongs to the freeze's UTC date or the
date before it, and a spot coin with no usable row is cut on its own day (row «The journal lands four to
seven hours after its schedule», new); and an object without a structural row is refused where its stop
lies at or beyond `liqPrice` at `L_MIN`. **The three longs of 07.10 are judged:** NMR, ORCA and MOVR were
published on a day screen at 0.5 % of capital each — one bet on a falling tape, within the side budget, the
size a professional gives a speculation the engine cannot measure — under a file that did not say whether a
refused unlock read counts as a read; it now says it does not, and the index now serving the lane carries no
cliff for ORCA and does not carry the other two. **§6 and §6a moved**, so the first run under the revision
re-reads every lane and re-measures every coin's coverage.

**Revision 2026-10-08-a.** No file of the table below moves. **TZ-61 executed on 07.10.2026 on the VPS
and is accepted: the announcement stream delivers.** Its verdict is `W1` — all seven of Binance's
channel posts of 05–07.10 joined a record by exact title, each inside a subscribed interval, and the
control post of 02.10 joined none — and the record holds twelve publications since the stream was
listed, received within 2.5 s of publication but once, with 24 s unsubscribed in four days (row «The
engine's exchange-announcement read is a path its own §6 forbids»). **The owner's chat stayed quiet
because of the alert rule, not the stream:** eleven titles named no list coin and were recorded only,
and the one alert was a promotion naming BNB. The STOP stands installed since 2026-10-05T12:26:39Z (row
«The assistant's build sequence», item (19)). **The unlock lane is refused:** the run of 07.10 read
`tokenomist.ai` at 19:11:44Z and every page and `robots.txt` answered 403 with the host's refusal of
automated access, so that row re-opens whole by its own trigger — and that run published three
outside-list longs with no cliff read (row «Unlock dates have no primary lane»). **The owner's request
of 07.10.2026** — a verdict per significant catalyst and one for BTC, each with an approximate expected
BTC move — is recorded (row «An expert verdict per catalyst and for BTC — the owner's request of
07.10.2026»). **The next revision of `ANALYST-INSTRUCTIONS.md` carries all three:** it admits the
stream's record in place of the disallowed path, replaces the unlock lane and prints the owner's
verdicts, and it is written after the audit of the run of 07.10, which judges the three longs.

**Revision 2026-10-07-a.** No file of the table below moves. **TZ-60 executed on 05.10.2026 on the VPS,
is accepted, and merged at `6e58aea` the same day** (`vps` tree
`81c33f881d4728eda33444e7840ecf9110d616d3`): the owner's STOP was proven on a transient unit and stops
the run unit from the deployer's install of that merge on; the size is `open` on two of the six runs —
one completed, one refused by the account; a completed press at `high` cost 9.2 % more than the run of
03.10 at the default effort, against no bar (row «The assistant's build sequence», item (19)). **Its
stream verdict `D0`, «silent», is withdrawn, and the defect is the Architect's, in TZ-57, TZ-58 and
TZ-60, not the stream's:** the list's `new=` counts entries of a sitemap, not publications, and both of
TZ-60's windows lay inside two and a half days in which Binance published no English announcement at all
— the run of 04.10 read the exchange's own list at 16:48:25Z and its newest record was dated 02.10, and
Binance's own channel carries nothing between 2026-10-02T09:02:01Z and 2026-10-05T02:04:14Z — while the
list counted 19 and 14 `new`. That reference was never compared with a dated source before a verdict
rested on it, which the canon's rule on registered expectations forbids, and its entries carry no key a
stream message carries, so its counts could never be joined to the stream at all. **Decided:** the
stream's reference is Binance's official English announcement channel on Telegram, read as a lower bound
— a post missing from a subscribed stream is a miss, and the channel's silence proves nothing — and the
owner's question, why the stream is silent while its subscription is confirmed, is answered by TZ-61,
read-only on the VPS, from the stream's own record, its own connection log and each record's alert
outcome, because a record reaches the owner's chat only when its title names a list coin, or a perpetual
inside a listing catalogue (row «The engine's exchange-announcement read is a path its own §6 forbids»).
TZ-61 is issued against this revision.

**Revision 2026-10-05-a.** No file of the table below moves. **Three owner messages of 05.10.2026 are
answered, and TZ-60 is issued against this revision.** **The owner's STOP:** on 04.10 he pressed the
button by accident while reading an answer and had no way to stop the run it started — the writer
committed at 17:15:12Z, 32 minutes after the run before it, and no analysis followed it to `main`.
**Decided:** «СТОП», «STOP» or `/stop` in his chat stops an analysis completely — a pending request
removed, the run unit stopped with its session and every process it started, no answer and no «Анализ
не завершён.», one confirmation — through a root path unit that holds no credential and starts no
model, so the bot gains no privilege; the messages that confirm a start name the word, and no
confirmation step is added before a run (row «The assistant's build sequence», item (18)). **The
reading TZ-58 and TZ-59 deferred** — the size on the runs the button started after TZ-57's merge, their
usage at `high`, and the stream against the exchange's own list — is TZ-60's Stage A: `main` shows two
writer commits since that merge and one analysis, and only the run unit's journal, which the VPS alone
holds, says what the second run did (rows «The assistant's build sequence» and «The engine's
exchange-announcement read is a path its own §6 forbids»). **A catalyst's age:**
`ANALYST-INSTRUCTIONS.md` `2026-10-05-a` prints, on every published object whose side or entry rests on a
dated event, when that date became public and the coin's move since, because the XRP item of 04.10 gave
the date its amendment activates and not the date, nine days earlier, on which that became public (row
«A catalyst's age never reached the answer»); §11 names the method's second market read. **The roles:**
the owner asked whether the hunter, the trader and the risk officer run independently; they do not — one
session runs the whole methodology on each press — and the split waits on TZ-60's usage at `high`,
because every role is a session drawn from the one account a press draws on (row «One agent executes the
whole methodology in one run»).

**Revision 2026-10-03-e.** No file of the table below moves. **TZ-58 executed on 03.10.2026 on the
VPS** — a first session in a cloud container stopped at its host check before any other work — and
its branch `tz-58-vps-fit-model-stream-list` at `a172529` is accepted, in effect once merged: **the
product's runs fit** — the completed run of 11:37Z held 332 668 928 bytes, resident and swap, inside a
budget of 704 643 072, and the run of 10:56Z was refused by the account's limit — so `fits=yes` and the
host stays at 1 vCPU and 1 GB; the stream answered the documented `SUBSCRIBE` on the server's own
connection and is listed; the exchange watcher reads the list. **Its model scope stopped on a known
answer the Architect registered on the layout of a tool's text** — `high` on the `--effort` line, which
the binary wraps onto the next line, where it is offered — so the pin passes to TZ-59, written on that
reading with no stage on the VPS (§10, row «The assistant's build sequence»). TZ-59 is issued against
this revision.

**Revision 2026-10-03-d.** No file of the table below moves. **TZ-57 executed on 03.10.2026 in a
cloud container, not on the VPS,** because its header named no host, so every stage that reads the
host stopped BLOCKED: its branch `claude/vibrant-albattani-ddmwh1` at `895d1dc` is accepted — the
watchers alert and request no run, `crypto-run.timer` is deleted, the stream's program sends the
documented `SUBSCRIBE`, and `common.record_limits` holds the record's budget rule — and is in effect
once merged; the fit, the model's pin, the stream's handshake and the list reader pass unchanged to
TZ-58. **Decided here: a TZ with a stage on the VPS names its host in its header, and its first stage
stops BLOCKED on any other machine before any work** (§10, row «The assistant's build sequence»).
TZ-58 is issued against this revision.

**Revision 2026-10-03-c.** No file of the table below moves. Revision `-b` was never uploaded, and
this one carries it whole. TZ-56 merged at `4c67ebe` on 03.10.2026: a run sets its own resident
ceiling at each start and pays for the rest of its budget with its own swap, the deployer verifies
every signed commit since the one it last accepted, Claude Code's auto memory is off, and the bot's
button and the watchers' run requests went into effect; the timers and the announcement stream stayed
off. **The product ran the same day** — the writer committed for two runs, at 10:56Z and 11:38Z, and
the second pushed the day's analysis at 11:58Z — and that is the measurement `-a` named: TZ-57 reads
the run unit's own journal, classes every run since TZ-56's install and writes the fit from those
lines, never from a session watching a run. **On that answer the owner decided that an analysis runs
only when he presses the button:** no timer and no watcher starts one, the watchers alert him and he
decides, so `crypto-run.timer` leaves the repository and the hunter keeps no schedule of its own;
**he proposed the run's model, and it is kept** — `claude-opus-5-5`, pinned, at `--effort high`,
because the method's measured failure is a run that stops short and effort governs how far a run goes
before it stops (§10, row «The assistant's build sequence»). **TZ-56 left the stream unproven:** the
exchange answers `REGISTER` to every connection, whether or not it sent a command, so that answer
acknowledges no subscription, and three hours on a program that sent no command received nothing. The
program returns to the documented `SUBSCRIBE`, and its delivery is checked against the exchange's own
list — the English announcement sitemap, a path its `robots.txt` permits, rebuilt daily — by the
watcher in code, never by a session holding a stream (§10, row «The engine's exchange-announcement
read is a path its own §6 forbids»). `ANALYST-INSTRUCTIONS.md` `2026-10-03-a` puts the strong trades
first, each with its reason, and moves no §6 text. TZ-57 is issued against this revision.

**Revision 2026-10-03-a.** No file of the table below moves. TZ-55 merged at `2aaa74f` on
03.10.2026: the run unit runs as its own user `cryptorun`, the deployer installs only a `vps`
tree GitHub signed, and the bot sets an undeliverable file aside as `.dead`; the run lane and the
announcement stream stay off. **The floor moves first, in the order inv. 59 fixes:** contract v26
makes the deployer verify every commit that changed `vps/` since the one it last accepted — v25
verified the newest alone, and a signed merge carries whatever reached `main` before it, which
TZ-55's audit found — classes `.claude/settings.json`, which turns Claude Code's auto memory off
for every session in this repository, and gives the Executor's closing message the signal `DONE
TZ-NN`, because the Architect reads reports from the repository (owner's message of 03.10.2026).
**TZ-55 decided nothing about size:** three full runs of three ended on the owner's account limit
and none on memory, and the session measuring the run held the memory and the account the run
needed. **The owner decided on 03.10.2026 that a run starts on swap and that he stops no service
for one**, so the resident ceiling is set at each start from what the host frees at that instant
and the rest of the budget is the run's own swap; the measurement becomes the product's own first
run, started with no Claude session open, and every run logs its own peaks and token usage (§10,
row «The assistant's build sequence»). TZ-56 is issued against both.

**Revision 2026-10-01-f.** No file of the table below moves. `vps/` went into effect on the VPS
when TZ-54 merged at `966b3f2` on 02.10.2026 — the deployer, the cleanup timer, the exchange
watcher and the Telegram bot enabled, the run lane and the announcement stream off. **The floor
moves first, in the order inv. 59 fixes:** contract v25 puts a model session under its own
unprivileged user, because TZ-54's report found the run unit — specified by contract v24 and
TZ-54 as root behind `InaccessiblePaths=` — able to read every credential it was meant to hide;
it names the deploy key v24's count of two left out, admits the run's own Claude login, and
lets the deployer install only a tree GitHub signed. Inv. 7 follows it here, and TZ-55 is
issued against both. **The host's size:** TZ-54's run did not fit, and the owner chose on
02.10.2026 to test on the 1 GB host before paying for more — so the rule of `-e` gains a test
mode instead of an answer: the run's budget stays one and a half times its measured footprint,
its resident part is capped at what the host frees and the rest goes to the run's own swap, and
it fits when it completes under those limits; a host that cannot carry it is answered by 1 vCPU
and 2 GB, since the measured run used a sixth of one CPU (§10, row «The assistant's build
sequence»). The book in code and the scorecard, named TZ-55 and TZ-56 in §10 until now, become
TZ-56 and TZ-57: the next number goes to the run lane.

**Revision 2026-10-01-e** moved no production file.
**The floor TZ-54 waited on moves, in the order inv. 59 fixes:** contract v24 admits exactly two
credentials on the VPS — the Telegram bot token and the Binance key that can only read — gives the
VPS payload writer a workflow step's standing, classes `vps/**` and makes merge the VPS's deployment
as it is Pages'; inv. 7 and inv. 44 follow it here, and TZ-54 is issued against both (§10, row «The
assistant's build sequence»). **The host's size is decided by a rule written before the
measurement:** TZ-54 measures a full analysis run in its own unit, and the scheduled runs are
enabled only where the unit's memory ceiling — one and a half times the run's measured footprint —
fits what the host frees when no other session runs; where it does not, the answer is 2 vCPU and
4 GB, because the other answer the owner named — the analysis on a GitHub runner — cannot execute
the method: item 90 reads `fapi.binance.com`, which a runner is refused (inv. 24). The hunter's own
schedule and the watcher's calendar and regime conditions wait on the methodology edit that splits
the hunter, because the state names neither a regime boundary nor a print's class and minute
(inv. 58).

**Revision 2026-10-01-d** moved no production file. Two owner messages of 01.10.2026 are answered. **He permitted bypassing Binance's restriction so that
the first signal of a spot listing is not lost; the permission is not used,** because Binance
publishes that primary source through an official, documented channel — its announcement WebSocket,
pushed on publication with title and body — which the watcher reads with a key that carries reading
only, while evading a challenge from the VPS would put at risk the one address every live price
comes from (§10, row «The engine's exchange-announcement read is a path its own §6 forbids»). **He
asked that runs clean up after themselves**, and it lands as a retention rule and a per-run ceiling
(§10, row «The assistant's build sequence»). Revisions `2026-10-01-b` and `-c` were never uploaded;
this one carries them whole.

**Revision 2026-10-01-c** moved no production file.
The owner chose on 01.10.2026 to build the delivery layer on the VPS as it is and to decide the host's
size on TZ-54's own measurement of a full analysis run, not in advance (§10, row «The assistant's build
sequence»); the watcher's exchange source follows the decision of `2026-10-01-b` (§10). **The revision
before this one was never uploaded**, so this one carries it whole.

**Revision 2026-10-01-b** moved no production file.
**TZ-53 is accepted.** The Executor's machine was read on 01.10.2026 from 08:02 to 08:08Z, and every
claim of the report this session could check reproduced: the files it fingerprinted, byte for byte
against `main` at `5f18ba3`; the remote's refs; and every host this session's own environment reaches —
Telegram's two answers, FRED's and the Federal Reserve's pages, Binance's `robots.txt` decisions, the
iShares datum and its moved as-of date, and the Farside and Grayscale challenges. Its readings are
recorded where they are used (§10): the build sequence row carries what TZ-54 is written against —
a scheduler that runs a headless session, a host at its memory ceiling, and the lanes the hunter can
and cannot read — and two rows record what the report found outside its scope: the engine's
exchange-announcement read is a path its own §6 forbids, and the row on the Executor's GitHub reach
rested on a premise that no longer holds.

**Revision 2026-10-01-a** moved no production file. The owner confirmed the architecture on 01.10.2026 and clarified what it is for: the quality and the
timing of the call, with size following the quality rather than restricted by default; the hunter
first; execution manual. **Three Architect files carry it and one TZ starts the build.**
`ANALYST-INSTRUCTIONS.md` `2026-10-01-a` prints every published object the way he executes it — side,
entry, target, stop, confidence `СИЛЬНАЯ` or `СРЕДНЯЯ`, size — with `СИЛЬНАЯ` earned by a named edge,
`⚠` for a side against the market word, and `ПОВЫШЕННЫЙ РИСК` exceptional again, printed exactly where
one of two computed causes applies, because it had stood on every trade that was not a list long.
`analyst/owner.json` v3 sizes by the grade — 1 % of capital on `СИЛЬНАЯ`, 0.5 % on `СРЕДНЯЯ`, halved
under the label, 3 % per side, 5 % for the book, every section ranking `СИЛЬНАЯ` first (§10). His request for a
probability per setup is recorded, not printed: the only honest source is the archive's measured rate,
and the row that builds it is written (§10). TZ-53 reads the VPS before anything is built on it
(§10, row «The assistant's build sequence»).

**Revision 2026-09-30-a** moved no production file. The owner answered on 30.09.2026: capital 10 000 USDT; the risk policy, the agent architecture, the
sequence and every other parameter delegated to the Architect; Telegram as his interface. **Two
Architect files carry it:** `analyst/owner.json` v2 holds the capital and the policy — 0.5 % of capital
per trade, 0.25 % on a `ПОВЫШЕННЫЙ РИСК` row, 2 % per side, 3 % for the whole book, isolated margin at
no more than 3× — and `ANALYST-INSTRUCTIONS.md` `2026-09-30-e` sizes every published trade from it at
its own anchor with production's own `leverageDecision`, `L_MIN` and `FEE_TAKER` and no formula of its
own (§10). Telegram is kept as the interface and the delivery layer is specified around it (§10). **The
revision before this one was never uploaded**, so this one carries it whole: a header quoting
`2026-09-28-a` meets no such anchor in the repository and is BLOCKED, which is the gate working.

**Revision 2026-09-28-a** moved no file. The owner's
objective of 28.09.2026 asked whether an AI trading assistant — several agents if need be, a separate
project if need be — can be built on an iPhone, the VPS, GitHub and Binance Futures, and it is
answered inside this repository: the analytical engine stays one system with exactly one
decision-maker, gains roles rather than a second engine, and places no order on the exchange (§10,
standing decisions). **The answer rests on the first reading this map has ever had of the engine's
own published book against the market:** every trade row of the forty-two day logs of
29.08–26.09.2026 replayed on the perpetuals' hourly archive as an owner acting on each answer would
have filled it — 62 closed trades, +7.85 R, the sum carried by three outside-list trades and −1.36 R
without them, shorts −12.56 R on 31, a peak of 24 open positions (§10). It was taken from the
Architect's session and not from a runner, so it stands behind no product fact (inv. 44) and is the
known answer the scorecard it opens must reproduce. The same session read the repository by
`git clone` at `9242d5d`.

**Revision 2026-09-26-b** was one methodology revision, forced by the audit of the engine's run of
26.09.2026, 12:27 Tbilisi — the first under `2026-09-30-c` — and **no production file moves**, so
every row of the file table below stands. `ANALYST-INSTRUCTIONS.md` `2026-09-30-d` widens what the
hunt reaches and leaves the answer's form unchanged: item 98's mover search asks about both UTC days
the twenty-four hours before the freeze touch, by project and ticker; a refusing host's backoff
suspends the host and never a date §6's `reported` class admits; and the unlock lane reads every
outside-list candidate and every book coin a hit dates a cliff for, not only `tokens[]`. One
objection of that run is ruled — a treasury escrow that re-locks most of each release is not a
cliff — and six are recorded unruled (§10). **That run is the unlock lane's measurement on the
Executor's machine:** thirty of thirty answered 200 on `tokenomist.ai` — seven `next`, fifteen
`fully unlocked`, eight `not covered` — which is the Architect's reading of 25.09 to the coin (§10,
§11). The Architect's session read the repository by `git clone` at `9fa2e65`, and read with a
client that is not the Executor's `bls.gov`'s October schedule, `bea.gov`'s schedule and four
`tokenomist.ai` coin pages; each reading says so where it stands (§10).

**Revision 2026-09-26-a** was one methodology revision, forced by the audit of the engine's run of
25.09.2026, 22:22 Tbilisi, and the measurements it rests on; no production file moved. `ANALYST-INSTRUCTIONS.md` `2026-09-30-c` gives the engine an
unlock lane: the coin page of `tokenomist.ai` — the host TZ-24 closed on its unlock-events page —
states each covered coin's next cliff in its served HTML, and the engine now reads it for every coin
of `tokens[]` on every run, keyed by the CoinGecko ids of `TOKENS`, which are the site's own slugs
(§10, §11). A cliff of at least 1 % of released supply inside the holding window closes the coin's
long side and opens no short — the standing production already gives an unlock in its registry
(§3.15, inv. 31) — and that threshold is a decision, not a measurement (§10). The same audit found a
mover search that asked about a price and a feed read without its text, and the methodology now
names both computations. **The Architect's session read the repository itself:** `git clone` of the
public `seahomebatumi-ai/crypto-auto` answered a session with a shell on 25.09.2026 at `e90f1fa`, and
the Project's mirror of the methodology reproduced the repository's MD5
`b038ed58ed627621748b15fe0b9468ea`. This map's readings of `tokenomist.ai` and of DefiLlama's unlock
datasets were taken from that session and not from the Executor's machine, and say so where they
stand (§10).

**Revision 2026-09-25-a** was one implementation merged, one report-only measurement read, and the
methodology revision that measurement forced. **TZ-51 is merged** — pull request #42, merge
commit `e8b8681` over implementation `065ba72`, as TZ-52's session read the graph on 25.09.2026 —
so `--verify` reads the archive AT production's instant wherever the archive holds the bar that
contains it, and no threshold, class or comparability rule moved (§3.10). Its report checked the
repair against run #25's own `attrib.txt`, still a live artifact: on `r7`, `r14` and `r30` TAO's
production value lies strictly between the archive's last close and `T_end`, so the new reading
returns production's own value and the cell reads 0.000 pp. **That is a reading of the
artifact's printed terms and not a replay** — the dispatch cache is not retained — so the first
dispatch after the merge is still the reading (§10). Gate steps 4 and 14 moved, read off the
runner (below). **TZ-52 measured each coin's own site, four reporter feeds, Upbit's market list,
two publishers of record for class S and the declared perpetuals' klines** from the Executor's
machine on 25.09.2026 between 11:09:07Z and 11:23:54Z — 245 requests, one per URL, and no file
written but its report. What it decided went to the methodology and not to production:
`ANALYST-INSTRUCTIONS.md` `2026-09-30-b` admits seven site rows and drops SKY's forum on its
host's `robots.txt`, gives item 90's move a named computation — the perpetuals' from
`fapi.binance.com`'s daily klines — and replaces a test of a lane's activity with a test of the
record that announced the change (§10, §11). **No production file moves**, so every row of the
file table below stands. The Project mirrors of this map, both contracts, `index.html` and
`main.py` reproduced TZ-52's figures to the byte before this edit; the Project's
`bench/backtest_bench.py` is TZ-51's pre-change copy, and nothing here was read from it.

**Revision 2026-09-22-b** was a dispatch reading and one specification, and moved no file. Run #25 of `backtest_bench.yml` (commit `3758dc6`, 21.09.2026,
`coeffs.json` built 10:50:25Z) is the first dispatch whose `--verify` exited 1 under per-symbol
comparability: one `unexplained` cell, TAO `r7`, +1.748 pp against a 1.50 bar, and `--target`
measured 29 coins with TAO out of its arms. **The cell is the archive's own last bar, not a
disagreement between the two sources**: production's instant lay inside the archive's
10:00–11:00 bar, and on all three horizons TAO's production value sits between the archive's
value at its last close and the value the same window takes with the previous close at its end —
`--attrib`'s printed Δ −1.748 / −1.571 / −1.881 pp against `T_end` −3.136 / −2.783 / −3.309 pp.
The comparison read the archive at 11:00 for a production built at 10:50, on a day the analysis
engine's own run measured BTC +6.5 % over 24 hours, which is §0's own 13.09 finding — one bar moves a return by the order of its threshold — arriving
as a failure. **TZ-51 was specified to read the archive AT production's instant wherever the
archive holds the bar that contains it**, and moves no threshold, class or comparability rule
(§10). The same artifact READ inv. 71's conditioning half and did NOT read the regime-gate
step, which its own input left at `false` (inv. 71, §10). **The frozen dispatch cache cannot be
repaired at its key alone**, and why is recorded in its row (§10).

**Revision 2026-09-22-a** was a methodology revision answering the owner's question of 20.09.2026:
**no direction engine enters through the methodology file.** Patterns, candlesticks, indicators
and sentiment all produce a direction from price history, which inv. 32 denies and the
`--control` run failed to find; a directional method enters through `bench/backtest_bench.py`
on the three-year archive or it does not enter, on the terms §3.12 already gives the own-trend
geometry. What replaces the forecast is measured and was already in hand: `# BTC` now prints
the distance and the seven-day touch probability of each regime boundary — `touchProb` on the
`btc` row's own volatility, a driftless lower bound (§7), not a claim about where the window
ends. A §6a lane whose host refuses three next-attempt dates in a row is re-sourced to another
publisher of record rather than waited on: `sec.gov` held the class-S lane unread for five
consecutive runs and `bls.gov` has been 403 for longer, which is the scheduled-event coverage
the owner named as most valuable. `ANALYST-INSTRUCTIONS.md` `2026-09-22-a`, §2, §4, §6a, item 84.

**Revision 2026-09-21-a** was a methodology repair of the revision before it, found by the first
run that executed it: the `RR_MIN` floor `2026-09-20-a` put on outside-list setups is
`pos / (1 − pos)` by construction and tested nothing, and behind it the engine **shorted three
vertical moves** — coins up 12 %, 31 % and 42 % on the day — with stops of 2.3 to 4.2 %, a
tenth of their own daily ranges, while its list rows carried stops of about one full range.
The short form of §3B now requires the coin's own day to be falling, the floor is retired, the
stop prints beside the day that produced it, and a `СОЗРЕВАЕТ` item stops printing the
survival constant the previous revision had just removed from the table
(`ANALYST-INSTRUCTIONS.md` `2026-09-21-a`, §2, §3B, §4, item 83). **The defect was in the
methodology file and not in the run**, which passed all eighty-three items and recorded the
`СОЗРЕВАЕТ` objection itself before sending.

**Revision 2026-09-20-a** was a methodology revision and the owner's decision of 19.09.2026:
**the engine ranks by what a trade is worth** rather than by how near its limit sits, and a
measure that cannot differ between rows leaves the answer for the log
(`ANALYST-INSTRUCTIONS.md` `2026-09-20-a`, §0 «СТАНДАРТ ТРЕЙДЕРА», §2, §3B, §7 items 79–83).
The run of 19.09 passed all seventy-eight checklist items and still printed a book with one
constant standing in for three quality figures, its cheapest trade at the top of the table and
its only actionable trade held to a looser floor than the rows beside it — none of which is a
property of a rule, which is why §0 now carries the standard the rules are read against. §10
gains the per-trade sizing gap. `2026-09-19-a` cut the own-trend stop from the 24-hour extreme
its zone rests on, through `invalidationInfo`'s own floor, instead of from the 30-day extreme
whose capped distance production itself declares no stop, and §10 records the measurement that
geometry is owed. `2026-09-18-a` gave inv. 30 its analytical-engine clause and restated §10's
direction row.
**No production file, bench or workflow moves**, so every row of the file table below stands.
The code baseline is revision `2026-09-17-a`, one branch TZ, merged:
**TZ-50** made the `--regime-gate` artifact writable, gave every artifact write one writer,
returned the driver's answer under a push-time pin and moved the regime-gate step out of the
path of four unrelated readings. `sm["agree"]` — the two-annotator agreement — was keyed by
`(word, word)` tuples, so `json.dump` raised `TypeError` and `regime_gate_raw.json` had
**never been written on any run in the mode's existence**; the failed dump left a truncated
stub and the upload carried it. The record is now a two-level map, sorted at both levels,
which `_out_fields` counts as one leaf per pair exactly as the tuple key did — so no lab
figure and no gate count moved with the shape (§3.10). All six artifact JSONs write through
`_dump_raw`, which serialises before touching the filesystem and leaves NOTHING at the path
when anything fails (inv. 72). Gate step 14's check 33 now pins the exact key set of `prod`,
where TZ-36 and TZ-48 had both added fields one level below what that check reached. And the
`--regime-gate` step is last before the artifact upload under `inputs.regime_gate &&
!cancelled()`, so neither its cost nor its failure falls on `--res7`, `--funding`, `Прогон`
and `Сверка` any more (inv. 71). Report
`CryptoReports/TZ-50-agree-map-and-artifact-write-report.md`, accepted; implementation
commit `2ecefc7`, pull request #41, merged.

**No production file moves at this revision, and two benches and one workflow do.**
`index.html`, `main.py`, `catalysts.json` and `bench/exhaustion-calibration.txt` appear in no
diff and sit at the four rows of the file table below; `git diff --name-only` over the
implementation names exactly `bench/backtest_bench.py`, `bench/backtest_guard_bench.py` and
`.github/workflows/backtest_bench.yml`. **The audit re-derived the one expectation TZ-50
registered** — the nine keys of `TARGET_DRIVER`'s `prod` literal at `:3334`–`:3343` — from
production itself rather than from the report, and re-counted the write change's own
enumeration, which is CLOSED: ten `json.dump` sites in the file, six artifact writes moved,
four left untouched (the two bridge job files carrying `allow_nan=False` on a hot path and
the two cache writes).

**The Project mirrors were MATCHED against the tree, not assumed.** Before this revision's
edits the mirrors of this map (2759 / `7f8fd2e8e553109cb7cffed329bd56e1`),
`EXECUTOR-INSTRUCTIONS.md` (864 / `02abb1969626d2af150a0d1f6e02f2a7`), `index.html`, `main.py`
and the pre-change `bench/backtest_bench.py` (5795 / `ed4db7c2bab9076e92982c664c6fc2f6`) each
reproduced the report's figure exactly. **The two files the mirrors do not carry were read
from the branch itself**: the post-change guard and workflow came back at 2513 /
`622b844efcca4292df2a157680ca4324` and 175 / `84efa8826db35837a810e3ad884dfa4b`, their
report figures to the byte. So mirror and repository were the same bytes, and this revision
is an edit of that reading. **That is a computation and never an inheritance:** a mirror
whose version line is behind the repository is not a weaker source but a wrong one, and
nothing but a hash of both says which it is.

**The latest DISPATCH is 21.09.2026's, run #25**, taken on commit `3758dc6` and read from the
`backtest-report` artifact the Boss forwarded; it carried no code and moved no file. `--fetch`
reached 31 of 31 coins through `vision`, every one refetched because the restored cache still
carries no observed venue (§10), the spot series ending at the 11:00 close and the five
perpetuals at 00:00. **The run was retained and conditioned**: `--verify` exited 1, and
`attrib.txt` and `regimes.txt` are both in the artifact, so the two steps inv. 71 conditions
executed behind a failed step for the first time. `--regime-gate` did not run, and not because of
the failure: its condition is `inputs.regime_gate && !cancelled()`, `!cancelled()` held for the
two steps before it, so the input stood at its default `false`.

**The return family came back on one cell, and the cell is the archive's own last bar.**
`--verify` compared 30 coins: 24 spot `clean`, TAO `unexplained` on `r7` alone (+1.748 pp
against 1.50, archive minus production), the five perpetuals `unverified` on their returns at
+10.8 h with four level cells `venue-basis`. TAO's `r14` +1.571 and `r30` +1.881 sat under their
bars with the same sign, and its `max_price` and `max30` +1.50 % under 2 % — one end-instant level
reaching every field that reads the window's end. `--attrib` places it: production's value lies
between the archive's value at its last close and the value the same window takes with the
previous close at its end, which is where a production built at 10:50 must lie when the
comparison reads the archive at the 11:00 close. **That is the 13.09 sensitivity arriving as a
failure, not a new mechanism**, and the 09.09 signature — one quantity at four horizons, one sign
across the list — is what the same end-instant offset produces at +0.8 h, where the archive holds
no bar to read at (§10).

**What `--attrib` says on the archive, first reading.** 90 cells compared, 75 attributed;
the 15 unattributed are the perpetuals, whose end instant lies outside their own archive
because the tail cannot be topped up (inv. 64). Production's construction reproduces exactly
— `eff14` residual 0 on 30 of 30 coins, `f` derived two-point on 30 of 30 for `r7`, `r14` and
`r30` — so the instrument is executing production and not an imitation of it (inv. 21, 38).
**Where Δ is ~0 the decomposition does not discriminate**: on the spot set the end-instant and
start-instant terms reach ±5.5 pp and cancel against the residual while Δ itself stays under
1.2 pp, which measures the instrument's sensitivity to one bar of window shift rather than a
disagreement. That sensitivity is itself the reading worth carrying: **a single bar moves a
return field by the same order as its own threshold**, so the return thresholds sit near the
quantisation floor of the comparison, and `d_end` is still not available to net against it
(§10).

**The 09.09 dispatch — the one this map waited on since TZ-36 — and what it answered.**
Taken
09.09.2026T21:44–22:07Z, twenty-one minutes after the merge, and read here from the
`backtest-report` artifact the Boss forwarded. **Its run number is not stated**: the runs API
answered this session a rate limit, and an unread run is not a numbered one (inv. 44).
`--fetch` reached **31 of 31 coins** and printed no `связь исчерпана` line, so nothing was
lost to the network; every cached document was refetched because none carried an observed
venue, which is TZ-34's repair firing across the whole universe at once. `--target` produced
the first archive figure the anchored arm has ever had (§3.10a). `--verify` refused, on a
class this map has never seen at this size, and that refusal is what set the universe every
gated mode then measured on (§7, §3.14, §10).

**What the dispatch does NOT establish is that TZ-38's code ran**, and that is a second new
row in §10 rather than a doubt about the merge. The artifact carries TZ-37's `D4a`/`D4b`
pair, so the tree is at or past TZ-37; TZ-38's only visible signature is a line that prints
exactly when a coin dies, and nothing died. **A repair whose whole evidence is the absence of
a failure has no reading of its own** (inv. 22, 43): `--fetch` prints the retry seconds it
spent only inside its `dead` branch, so a run that slept 599 s and a run that made one
attempt per URL print the same output.

**Step 14's count stood at `94` in two other sections while the step itself ran 174, then
203, 266, 323, 373, 467, 475, 487 and now 488.** §3.10 and §10 both carried the figure TZ-30 measured, and neither
moved when the step did. **The count lives in this section only** and both sites point here:
a count carried in three places goes stale in silence (inv. 20), and the calibration record
is the one exception in this tree only because gate step 12 compares its two copies on every
push (inv. 46).

**The revisions before this one, in one line each.** `2026-09-16-b` recorded TZ-46 — class 2
probed for the two coins TZ-45 left owed one, ETH on the Ethereum Foundation's blog feed and
ADA on the `IntersectMBO/cardano-node` release list, both `primary-dated`, the third
candidate withheld by the stop rule, and the reading reaching the engine as an Architect edit
(`ANALYST-INSTRUCTIONS.md` `2026-09-16-c`, 29 channels in methodology §6a, `c2` in its §11
schema) rather than as a TZ; `2026-09-16-a` recorded TZ-45 — one
catalyst channel measured for every member of `tokens[]` from the Executor's own machine,
class by class and reading no content: 27 answered with dated records, 15 on a Discourse
forum and 12 on a release channel, and ONDO, HYPE and LIT have no protocol channel that dates
anything (§10); `2026-09-14-a` recorded TZ-44 —
comparability decided per symbol and per field before the class, guard I9 re-registered as a
pair and section K added on `_cell_comparable` — beside TZ-43, correctly BLOCKED on a §4
unsatisfiable by construction; `2026-09-13-b` recorded no code at
all — the dispatch the three TZs before it were built for, read from the artifact;
`2026-09-13-a` recorded TZ-39, TZ-40
and TZ-41 — the transport outcome decided after the last failing step, the return gap split
into instants and residual, and that split retained and conditioned; `2026-09-10-a` recorded
TZ-38, the
bench's transport layer — one helper `_http` at one site, three outcomes where the code had
two, and exhaustion failing the COIN rather than the run; `2026-09-09-b` recorded TZ-37 —
`--lab-selftest`'s D4 re-registered as an anchor-off identity plus a live partition, its
construction named `d4_partition` and running in gate step 14 section G; `2026-09-09-a`
recorded TZ-36, the anchored recorders — `anchor`/`decA`/`invA` and `ssrc` in the journal,
`prod_anchor` beside `prod` in `--target` — which closed inv. 66 at both its sites;
`2026-09-08-b` recorded TZ-34 and TZ-35, the venue actually fetched recorded as an
OBSERVATION and the reconciliation reading it (inv. 67, 68); `2026-09-08-a` recorded TZ-33,
the anchored publication price. **None of the revisions after it moved a production file
either**, and each one's attribution lives in its own immutable report rather than here.
**The numeral this sentence used to carry is gone** — it said «seven» over eight entries,
which is inv. 20 inside the block that states the rule.

Contract **v26** — 991 lines, MD5 `d7bd23785656896a119e0cb7f0fddad5`. **v26 closes the
deployer's check** — every commit that changed `vps/` since the one the deployer last accepted,
never the newest alone — turns Claude Code's auto memory off for every session in this repository,
and puts `DONE TZ-NN` in the closing message (§10, row «The assistant's build sequence»). v25 — 963
lines, `ef21a864f6c93d1c59d72b9e16eb967f` — repaired the floor TZ-54 measured: a model session
under its own unprivileged user, the deploy key counted, the run's own Claude login admitted, and
the deployer installing only a tree GitHub signed. v24 — 929 lines, `7d7e335d1fc1871ca4404128da54a93d` — moved
the floor TZ-54 waited on: two credentials admitted on the VPS, the VPS writer given a workflow
step's standing, `vps/**` classed, and merge made the VPS's deployment as it is Pages'. v23 —
864 lines, `02abb1969626d2af150a0d1f6e02f2a7`. **Six versions moved since `2026-09-14-a`, and
none touches a production file.** v21 — 831 lines, `5b125d9a39bc4ccd4e935d01ed1aa1e8`,
measured by TZ-45's session and matched on the copy the Architect edited — narrowed what an
analysis run reads of the contract to its role-2 operative set, because an analysis run never
loads this map (contract §5). v22 — 849 lines, `ba6ef34b108d70c287e02412dd84955e`, measured
by TZ-46's session — makes the fingerprint gate take its anchor list from this
block's table, so a header that omits an anchor is BLOCKED instead of passing on the anchors
it happened to quote (§10). **v23 says how that list is CUT**, because v22 said only where it
comes from: TZ-46's gate read this table and filtered it through seven anchor names, which
compares the filter and reports it as the table (§10).

**`bench/backtest_bench.py` has no row in the file table, and six consecutive TZs have now
had to explain the absence.** The table pins the four files a TZ header fingerprints: three
production artifacts plus the calibration record, and the record is there only because it is
one of exactly two places `DAY_RANGE_ABNORMAL = 1.39` exists (inv. 46). A bench in that table
would put a hash in every TZ header for a file that moves whenever a bench moves — the
argument §11 already makes for `live-gate.sh`. A TZ needing the figure states it in its own
`§0`. **Current pairs, each measured on the implementation commit of the TZ that last moved
it:** `bench/backtest_bench.py` **5929 lines**, `ac203e2dc54104b79e08186644337832`;
`bench/backtest_guard_bench.py` **2578 lines**, `101ec7304467ef966c661a1f5349ae14`;
`bench/verify_bench.py` **643 lines**, `ec82368f44356c34c656ebcbcb5733da` — all three moved by
TZ-51 at `065ba72`, and TZ-52's session read the same three pairs in the merged tree.

**The ladder of every past value this block used to carry is GONE, and its absence is the
repair.** It ran from TZ-28's figure to TZ-44's and stopped there, so six consecutive TZs
opened on a value three implementations stale and each had to report a map lag that was never
anything but this sentence — and the retired numerals are not repeated here, because a
reader grepping one of them would find this paragraph and read it as current. It was also
history, which this map's first paragraph sends to git and `CryptoReports/**`: the pair a
reader needs is the CURRENT one, and every earlier pair is in the header of the TZ that
measured it.

**The journal's two files leave this block for §3.13, and that is a narrowing of an
obligation, not a loss of a figure.** Contract §5 makes every pair in `§ 0` a measurement
every report must take; no TZ touching the backtest gate opens `journal/**`, so those two
pairs were an obligation nobody honoured — TZ-50's report measured seven of the nine files
this block listed, and the gap reached the audit rather than the gate.

**`bench/backtest_guard_bench.py` gets no row either, and for the stronger reason:
its control is being a gate step.** It executes on every push at step 14, so a hash in a TZ
header would pin a file whose behaviour is already under a control that runs — exactly the
argument §11 makes for `live-gate.sh` at step 13. A fingerprint entry buys a second, weaker
check and costs one line in every future TZ header.

Every TZ header quotes this block IN FULL — every anchor of the table below and the file
table, never a subset. The Executor takes the anchor list from that table, cutting it by the
table's own rows and never by the anchor names it expects (contract §5 step 2, since v23),
matches each as an
exact substring against the repository copy before any work and records the text each match
returned (contract §5); any mismatch is BLOCKED, and since contract v22 a header that omits one
is BLOCKED as well. **The number of anchors is not restated in this sentence** — it is the
height of the table, and a count carried beside a table it does not control goes stale the
first time the table grows (inv. 20).

**An anchor is a string COPIED out of this file, never one recalled from the rule it names,
and it is verified as a literal substring before this block is published.** The inv. 68 anchor
carried at `2026-09-08-b` read «must flip and which must not» while the invariant itself reads
«must FLIP and which must NOT», so no exact-substring matcher could satisfy it — and TZ-36's
report recorded all seven anchors as present as exact substrings anyway. **An anchor nobody
can match does not fail loudly**: it fails in whichever direction the matcher happens to be
written, and a blocking gate is the one control that may not have such a direction.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-09-f.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` |

Live files at this revision — the set every TZ header and every report fingerprints:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

The calibration record is fingerprinted, unlike every other bench artifact, because
it is one of exactly two places `DAY_RANGE_ABNORMAL = 1.39` exists and gate step 12
compares the two on every push (inv. 46).

**That record describes the universe of its OWN run and is never edited to match a later
one.** Its header reads «25 spot of 28 declared tokens … HYPE, XMR, LIT», which was true
of the run that produced it and is the sentence TZ-25 §4.4 and TZ-26 §2.3 both refused to
touch. Nothing calibrated in it moved when the universe reached 30: both added coins are
`fut:true`, the measure never counted them, and the spot basis is still 25 (§3.16).
Rewriting the header would make the description of one sample describe a different one,
which is inv. 46 read backwards — the constant would then agree with a record that no
longer names the run behind it. It goes stale by design; the reader is told so here.

Gate at this revision: `bench.yml`, **14 steps, 1 336 181 checks**. TZ-51 moved two steps and
nothing else any step reads: step 4 59 → **74**, case 12's fifteen checks over lanes P1–P6, and
step 14 488 → **506**, the new section L at **18** — `1 336 148 + 15 + 18 = 1 336 181`, summed step
by step from the runner's own log of run `35704029320`. TZ-50 had moved step 14 by exactly one —
487 → 488, the check-33 pin on `prod`'s key set: `1 336 147 + 1 = 1 336 148`. `2026-09-14-a` is
where TZ-44 moved TWO steps,
which no single TZ before it did — step 14 475 → 487, section I 94 → 95 where the I9 pair puts
two checks where one stood plus the new section K at **11**, and step 4 40 → **59**, the
nineteen lane assertions added to `verify_bench.py`; `1 336 116 + 12 + 19 = 1 336 147`.

**The runner's own per-step COUNTS were first read at `2026-09-17-a`.** TZ-50's
session took them out of the log body — `gh run view <id> -R seahomebatumi-ai/crypto-auto
--log`, 87 802 and 89 096 bytes on the two `Bench gate` runs of implementation commit
`2ecefc7`, `35223415269` (push) and `35223439860` (pull_request), both `success` on every job
step: step 4 `checks run: 59   FAIL 0`, step 14 `checks run: 488   FAIL 0`, sections E 32,
F 29, G 63, H 107, I 95, J 8, K 11. The negative control read the same step RED on the same
instrument — `488   FAIL 1` on run `35225366648`, one FAIL line, every other step `success`
— so the count and the gate's ability to fail were read together. TZ-51's session read them the
same way on run `35704029320`, `success` on every step: step 4 `checks run: 74   FAIL 0`, step 14
`checks run: 506   FAIL 0`, sections E 32, F 29, G 63, H 107, I 95, J 8, K 11 and **L 18**. **A conclusion is a
measurement and a count is a different one** (inv. 22, 43), and until now only the first had
ever been read off a runner; the clause in inv. 44 that said the second could not be is
corrected there, not here. **Neither figure was replayed by the Architect**, then or now: what
the audit verifies is the arithmetic and the committed text, and at `2026-09-17-a` that was
`487 + 1 = 488` against a diff of `+10 / −0` in one hunk, at this revision `59 + 15 = 74` and
`488 + 18 = 506` against bench diffs of `+103 / −0` and `+65 / −0` — which is also why no check could
have been renumbered, since renumbering requires a deletion. **Step 5's own count has never
been recorded in this map**: it is the residual that makes the recorded total add up
(255 708) and it is arithmetic, not a reading.

**A step number in a report is the jobs API's, not this block's, and the two run +5 apart.**
The API counts the implicit setup and teardown steps around the job, so the figures above read
14 YAML steps here and 19 on the run page, `verify_bench.py` at step 4 here and step 9 there,
the garrison at step 14 here and step 19 there. The offset is uniform, and reading one
numbering as the other manufactures a map lag that does not exist — this audit nearly filed
one.

**Step 7 (`journal_bench.js`) moves with verdict CONTENT, not only with control
volume.** It counts numeric leaves of the records it writes, and a verdict that
returns before geometry writes no `geo` object, so a change in verdicts moves it
without moving a single control. A fall in step 7 is attributed, never assumed
benign, because a defect that nulls a field lowers it identically. It stands at **774 130**
since TZ-36 and every delta since has been attributed field by field in the report that
caused it (§10).

**The one delta this map ever attributed by arithmetic of its own was wrong, and the
correction is the rule.** TZ-33 cost step 7 **−2 059** leaves; this map named the population
that lost them, and a per-JSON-path census on both trees refuted that population twice over —
the count that actually moved is every row whose FIRST pass carried `geo.wait`, 3.7× the
number the map had named, while the population it did name ROSE. **A population named in a
map is a hypothesis until someone reads the paths** (inv. 43). The closure is recorded in
§10; the arithmetic is in TZ-36's report and is not restated here (inv. 20).

---

## 1. Data flow

```
iPhone Shortcut → workflow_dispatch → GitHub Actions → main.py
   → CoinGecko /market_chart (90d hourly; BTC + 30 alts = 31 calls)
   + CoinGecko /coins/markets (ranks, FDV = 1 call)          32 calls/run
   → metrics → PATCH Gist → WebApp (GitHub Pages) on iPhone
```

| Module | Path | Runs | Reads | Writes |
|---|---|---|---|---|
| Data bot | `main.py` | hourly, Shortcut-triggered | CoinGecko | Gist: `coeffs.json`, `debug.json`, `history.json` |
| Calculator | `index.html` | in browser | Gist + Binance + `catalysts.json` | localStorage (order, side) |
| Catalyst registry | `catalysts.json` | static, served by Pages | — | edited by the Architect through a TZ |
| Verdict journal | `journal/write.js` | `journal.yml`, 13:00 UTC | Gist, `data-api.binance.vision`, `catalysts.json`, `index.html` | `journal/data/**`, `journal/out/**`, `journal/runs.jsonl` |
| Benches | `bench/**` | `bench.yml` on push/PR | production files at runtime | nothing tracked |
| Backtest | `bench/backtest_bench.py` | `backtest_bench.yml`, **manual dispatch only** | `index.html` + `main.py` at runtime, `data.binance.vision` archive | artifacts only |
| Calibration | `bench/exhaustion_calib.py` | `calib.yml`, `workflow_dispatch` + push on `claude/**` — never on `main` | `data.binance.vision` archive | `bench/exhaustion-calibration.txt` on a PASSING run; artifact always |
| Analytical engine | `ANALYST-INSTRUCTIONS.md` + `analyst/**` | Boss-triggered, in a Claude Code session | `analyst/live.json`, `analyst/state.json`, `index.html` (`tokens[]`) | `analyst/state.json`, `analyst/log/**` |

**Schedule is not cron.** The only regular trigger is the Boss's iPhone
Shortcut: hourly from 09:00 to 01:50 local = **17 runs/day ≈ 16.3k CoinGecko
calls/month** since the universe reached 30, plus rare `push` runs on `main.py` /
`main.yml`. Cron in `main.yml`
was removed deliberately (June 2026): a second scheduler is a second source of
truth for freshness. Automation outside the repository belongs to the Boss and is
never duplicated or switched off from inside it.

**The 7 h 10 min night pause is part of the design.** Between 01:50 and 09:00
there are no runs, `coeffs.json` ages to ~7 h and `STALE_CRIT` lights every night
on a fully healthy system. Hence inv. 4: «schedule asleep» and «update failed»
are different states.

**Second scheduled run — the verdict journal** (`journal.yml`, 13:00 UTC, §3.13).
It never calls CoinGecko: it reads the finished Gist and prices from
`data-api.binance.vision`, executes production functions out of `index.html`, and
appends the day's record.

**Third file served by Pages — `catalysts.json`** (§3.15), next to `index.html`,
read by the frontend over plain XHR. The bot does not write it and it never
enters the Gist. If it fails to load, the layer goes dark with a banner and the
board keeps working (inv. 40).

**Venue is declared, not observed (§3.14):** 25 coins are Binance Spot, five —
**XMR, LIT, HYPE, MORPHO, ARB** — Binance Futures only.

**Gist files**

- `coeffs.json` — `generated_at` + `btc` (min/max/price_pos/volatility + r7/r14/r30) + `analysis_data[]` (incl. `rank`, `rank_prev`, `fdv_mc`)
- `debug.json` — per coin: `candles_total`, `matched_90d/14d`, `returns_90d/14d`, `error`, `ranks_fetched`, `fdv_fetched`
- `history.json` — ≤ 720 points (~30 days): ub/ur/db/dr/ub90/db90 + rank `r`

**Frontend's own three Binance sources**

- spot ticker `api/v3/ticker/24hr?symbols=` — 30 s, only pairs without `fut:true`
- futures ticker `fapi/v1/ticker/24hr?symbol=` — 30 s, one request per `fut:true` token
- funding `fapi/v1/premiumIndex` — 5 min

**Universe: 30 pairs.** Frozen at 28 from June 2026 until **03.09.2026**, when the Boss
added MORPHO and ARB as declared futures-only assets. The freeze stands again at 30: a
coin enters only on an owner decision, and that decision moves the contract's hard floor
before it moves any code (inv. 2, inv. 59).

---

## 2. Bot mathematics — `main.py`

- Bucketing: `floor(ts_ms / 3.6e6)` → hourly buckets; keys common to BTC ∩ coin.
- Returns: **only between adjacent buckets**; returns across gaps are dropped.
- Betas: OLS with intercept, separately up (BTC hour > 0) and down (< 0); windows 14d and 90d. Minimums: 24 matched (14d), 120 (90d); < 5 returns in a direction → `None`. The intercept (alpha) is deliberately unused: at 14d its standard error is comparable to the estimate itself.
- `up_beta_90`/`up_r2_90` and `down_*` are always paired: `fit_stats` returns either (float, float) or (None, None).
- `corr_90`: Pearson over all 90d returns. `volatility`: std of hourly returns over 90d. `min`/`max`/`price_pos`: over 90d.
- `btc.volatility` — BTC's own hourly volatility over 90d; the frontend uses it to size the BTC-crash ceiling (§3.2).
- `btc.r7` / `btc.r14` / `btc.r30` — BTC's own return over 7/14/30 days, from the already-downloaded series: **zero new API calls**. Needed for `res7` (§3.9). `null` is a normal state and the frontend must survive it (inv. 9). Windows are cut from the LAST point of each series; a few minutes of offset between BTC and an alt is below noise at a 7-day horizon.
- `fdv_mc` = `fully_diluted_valuation / market_cap` from the same `/coins/markets` call as ranks (zero new requests). Values < 0.95 and > 100 are discarded as supply-data garbage. `None` is normal: coins without a max supply (ETH, XMR) return FDV `null`.
- `error = true` ⇔ too few 14d points or a failed request → the card renders NO DATA.
- The bot does not depend on a spot pair existing: betas come from CoinGecko.

**Integrity cross-check.** From the single-factor identity `σ_BTC = σ_alt·√R²/|β|`,
BTC's hourly volatility recovered from five independent cards reads 0.316–0.393 %/h
(mean 0.367 %, spread ±11 %): betas and R² are computed correctly.

---

## 3. Frontend mathematics — `index.html`

- `ratio = (target − btc)/btc`; `1 + ratio = target/btc > 0` always.
- `rawBeta` = up_beta | down_beta by the sign of `ratio`; null / non-number → card shows **NO BETA**.
- `beta = rawBeta × stress` (normal 1.0 / panic 1.3 / crash 1.8).
- Forecast: `growth = (1+ratio)^beta`; `pPct = (growth−1)·100`; `pred = cur·growth`.
- Liquidation from `pred`, isolated, `LIQ_MMR = 0.0125`: LONG `pred·(1 − 1/L + MMR)`, SHORT `pred·(1 + 1/L − MMR)`. Fees and funding excluded. **Base on the card is `pred`; on the board it is the entry price `E`.**
- `LIQ_MMR = 0.0125` was recovered by back-calculation from three of the Boss's real positions (XMR 1.28 %, YFI 1.25 %, LIT 1.13 %); the earlier 0.01 placed liquidation further away than reality — an error in the dangerous direction.
- Confidence (0–100): `0.45·R²₁₄ + 0.25·R²₉₀ + 0.20·(1−min(div90,1)) + 0.10·(1−min(vol%/3,1))`; missing components drop out with renormalisation. Colours: ≥ 70 green, 40–69 yellow, < 40 red.
- **R² in both rows (14d and 90d) shares one scale:** < 0.30 red, 0.30–0.60 yellow, ≥ 0.60 green.
- ρ (`corr_90`): ≥ 0.75 green, 0.5–0.75 yellow, < 0.5 red. There is no separate 14d/90d beta-divergence glyph — divergence is already inside Conf.
- **МДЛ gate** (`gateState`, pure display): red when `Conf < 40` OR `R²₁₄ < 0.25` OR (`corr_90` present AND `|ρ| < 0.5`); green when `Conf ≥ 70` and the rest hold; yellow otherwise. High Conf measures correlation-model quality, never direction.

**Boss-approved display conventions — unchanged without his explicit request:**
funding colour = payment direction for the pressed side, «зелёный = мне платят,
красный = я плачу» (§3.1) · 14d beta on the card next to R² · МДЛ is the single
model-trust signal, no duplicate icons · Min/Max blinking and the running edge
borders are never removed (inv. 19); improvements may be proposed, never silently
applied.

**Production constants, one place each (inv. 20).**

```
LIQ_MMR 0.0125 · H_NOISE 168 · H_BTC 168 · H_REACT 12
L_CAP 7 · L_MIN 2 · INV_FLOOR_SD 2.0 · INV_CAP_SD 6.0 · MAX_MARGIN_LOSS 0.35
EFF_TREND 0.6 · PACE_Z 0.25 · VOL_ABNORMAL 2.0 · VOL_HARD 0.02 · VOL_STOP 0.03
RES_Z 1.0 · RES_R2_CAP 0.90 · FEE_TAKER 0.0005 · FUND_PAY_7D 21 · ARM_R 1.0
RR_MIN 2.0 · TGT_SIGMA_MIN 1.0 · ENTRY_CHASE_SD 0.5 · REG_STRESS_Z 2.0
DAY_RANGE_ABNORMAL 1.39 · CAT_WINDOW_D 14 · TIER_STRONG 70 · TIER_MID 50
TIER_MIN 35 · STALE_WARN_MIN 75 · STALE_CRIT_MIN 130
```

### 3.1 Trade side — explicit input

`currentSide ∈ {long, short}`, default `long`, set by the ЛОНГ/ШОРТ buttons, not
persisted to localStorage.

**Slider direction ≠ position side.** The slider sets a BTC scenario; the header
reads `BTC ВВЕРХ` / `BTC ВНИЗ`.

From `currentSide`: the leverage formula (§3.2) and the funding colour. From the
sign of `ratio`: beta choice, slider/button/arrow colours, both liquidation rows.

**Funding colour = the economic effect for the PRESSED side** — green «мне
платят», red «я плачу». Deriving the side from `ratio` inverted the colour
exactly when risk was being measured.

### 3.2 Leverage engine — three independent ceilings

All three are computed at a **7-day horizon** (`H_NOISE = H_BTC = 168`); the
minimum wins, rounded DOWN.

```
Invalidation level (invalidationInfo):
  ref   = min30 / max30   (absent -> min90 / max90, inv. 9)
  ref beyond entry -> src = 'вход'      no structure left, only noise
  structPrice = ref ∓ ½σ_day
  dist = clamp(dStruct, 2σ_day, 6σ_day)          INV_FLOOR_SD, INV_CAP_SD

1. STRUCTURE  L = 1/(dist + 1.645·Vol·√12 + MMR)          H_REACT = 12 h
2. NOISE 7d   need = LONG 1−e^(−q), SHORT e^q−1,  q = 1.645·Vol·√168
              L = 1/(need + MMR)
3. BTC CRASH  D = 2·btc.volatility·√168
              move = |(1 ∓ D)^β_adv − 1|                  L = 1/(move + MMR)
              β_adv = |β90 of the opposite direction|, tightened by the tail
              beta only when tail_r2 ≥ 0.10

RESULT = floor( min(three ceilings, cap) )
cap: L_CAP 7 · vol7/vol90 > 2 -> 3X · Vol ≥ 2 %/h -> 2X · Vol ≥ 3 %/h -> no leverage
RESULT < L_MIN -> «БЕЗ БЕЗОПАСНОГО ПЛЕЧА» + fixHint
```

**Why exactly three.** Structure — «can I exit at my own level before the
exchange does, plus 12 hours of reaction time». Noise — «will chop alone take me
out within a week». BTC crash — «do I survive a systemic move». They rest on
different quantities (distance to the reference / Vol / β), so the binding
ceiling differs per coin and the board names which one binds (`dec.binding`).

**Both distance clips are mandatory.** Without the 6σ cap an entry mid-range
produced «no leverage», reading a distant reference as huge risk instead of as
absent guidance; under `capped` the card says plainly that there is no nearby
reference and the stop must be held manually. Without the 2σ floor a move smaller
than two daily sigmas — noise, not a broken idea — would be promised as an exit.

**Horizon 7 days, not 30.** 30 days was the single most sensitive parameter in
the system — alone it moved the verdict two leverage steps. 7 days is the upper
bound of the Boss's typical hold.

### 3.3 Liquidation-touch probability — `liqTouchProb`

```
d = 1/L − MMR;   LONG b = −ln(1−d)   SHORT b = ln(1+d)
P(touch within H) = 2·(1 − Φ( b / (Vol·√H) ))     reflection principle, drift = 0
```

Shown as a 7d / 14d / 30d ladder from the **pressed** leverage button
(`currentLev`), not from the RESULT.

**Liquidation is a TOUCH event, not a terminal value** — the reflection principle
doubles the probability against the naive estimate. Risk is heavily back-loaded:
at Vol 1 %/h and 3X it is ~0 % over 7d, 3 % over 14d, 15 % over 30d. The touch
formula lives once, in `touchProb(vol, b, hours)`; break-even (§3.11) and
§3.17 use the same function — two copies of the reflection principle would
inevitably diverge.

**R² deliberately does not enter.** The position is not hedged against BTC, so
liquidation is caused by the coin's full move, not by the idiosyncratic part.

Side asymmetry is built in: price is unbounded upward, so at equal leverage a
short is always riskier than a long (Vol 1.0 %/h, 3X: long 14.6 %, short 29.6 %).

### 3.4 Margin risk — the fourth ceiling, HARD

`MAX_MARGIN_LOSS = 0.35`: exiting at the structural stop must not cost more than
35 % of margin. Professional replacement for «keep the stop within 10 %» — the
distance is set by the coin's structure, so what gets limited is the LEVERAGE,
not the stop. The division `MAX_MARGIN_LOSS / dist` lives in exactly one function,
`lMoney(dist)` (inv. 20).

```
hard mode      ⇔  inv.capped === false
contribution   =  max( lMoney(dist), L_MIN )
decision fields   parts.money · moneyHard · moneyBelowMin
```

**The condition is exactly `capped`, nothing else.** A clause `src ≠ 'вход'` was
rejected as arbitrary: at two different entries `dist` hits the same 2σ floor, so
the stop is mathematically identical and the rule must behave identically — with
the clause, an entry BELOW a broken low would have *lifted* the limit.

**The 2σ floor participates in hard mode, the 6σ cap does not.** A stop cannot be
placed quieter than noise, so 2σ is an honest minimum distance and money rules
apply to it. A level clipped by the 6σ cap is drawn, not tradable; the row stays
informational.

**The `L_MIN` floor is mandatory (inv. 26).** `loss/margin = dist·L` is
independent of position size, so the money rule speaks about the SHARE OF THE
ACCOUNT, not about survival. Without the floor, 538 of 1230 control setups
received «no safe leverage»; with it, none. When the stop does not fit even at
`L_MIN`, `moneyBelowMin` rises and the board says to take a smaller share of the
account instead. Measured price of the rule: 22 % of control setups get lower
leverage; across 3243 comparable setups on both sides not one case of leverage
rising.

### 3.5 FDV

`fdv_mc` in the badge next to the rank. Thresholds: grey < 1.5, yellow 1.5–3, red
> 3. **Context for unlock risk, never a standalone long/short trigger** — it says
how large future issuance is relative to float, i.e. which coins to check by hand.
Optional field (inv. 9); no max supply → not drawn.

### 3.6 Forecast uncertainty band — NOT IMPLEMENTED, reasoning fixed

`pred` is the conditional mean of only the part of the move BTC explains. The
idiosyncratic part is unforecastable by construction:

```
σ_idio(hour) = Vol·√(1−R²)      signal/noise = √(R²/(1−R²))
```

At typical R² = 0.15–0.36 signal/noise = 0.42–0.75, i.e. **the coin's own move
exceeds the part explained by BTC**. A 5–15 % simulation-vs-fact divergence is the
expected width of the distribution, not a model defect. A separate «signal/noise»
metric is therefore meaningless — it is identical to R², already on the card (§8).
The practical answer to this risk is the liquidation probability (§3.3), not a
band on the forecast.

### 3.7 Board CRYPTO FUTURE — the work surface

Full-screen overlay (`#board`, z-index 5000), opened from a card. The card is the
shop window, the board is the desk; there is no duplication by construction. One
coin at a time, session state only.

**Block order lives ONLY in the concatenation at the end of `boardHtml`** — the
blocks are computed above in their original order because of variable
dependencies. Reordering means moving 14 strings, never the code (inv. 15).

```
1 ИТОГ·СТОРОНА·ПОТОЛОК   2 ПОЧЕМУ ЭТА МОНЕТА   3 ДИАПАЗОН 90 ДНЕЙ   4 ТОЧКА ВХОДА
5 ВЫБОР ПЛЕЧА   6 РИСК ВЫНОСА   7 РАЗМЕР ПОЗИЦИИ   8 ГРАНИЦЫ СДЕЛКИ
9 ЦЕНА ВРЕМЕНИ   10 ЕСЛИ ИДЕЯ НЕ СРАБОТАЕТ   11 ЕСЛИ СРАБОТАЕТ   12 ЗАЩИТА ПОЗИЦИИ
13 ОТКУДА ПЛЕЧО   14 ДОВЕРИЕ К МОДЕЛИ
```

«РИСК ВЫНОСА» sits sixth deliberately (§3.17): it is the direct consequence of the
pressed leverage button (inv. 14) and must be read BEFORE size is chosen; it
declares no variable of the size block. «ЗАЩИТА ПОЗИЦИИ» sits twelfth: 10 and 11
are outcomes, 12 is the only action that converts unrealised profit into inability
to lose, and 13–14 are methodology and diagnostics. «СТОРОНА ПРОТИВ СТРУКТУРЫ» and
«ВНИМАНИЕ» come straight after the verdict: they are alarms, not sections.

**Position size — two input units.** `sizeMode ∈ {usdt, coin}`.

```
Identity: notional = qty·E = mrg·L.  ONE number is entered, the other derived.
usdt: mrg = posMargin;  notional = mrg·L;  qty = notional/E
coin: qty = posQty;     notional = qty·E;  mrg = notional/L
```

Switching the unit does not move position volume (recomputed through the identity
in `setSizeMode`, using the exact entry price from `entryState`, never a rounded
HTML attribute). In coin mode a leverage change keeps quantity and moves margin —
the correct order for «I want 1000 UNI» (inv. 16).

**Pressed-button highlight is one law of the board (inv. 17).** Exactly one button
lights in each group: side, leverage, size unit, entry point. For the entry point
the lit button is the preset price matching the current one within 0.25 % — half
the 0.5 % step of the −/+ buttons; if none matches, the pencil lights and that is
«своя цена».

**Funding in money:** `costUsd = |fr|·21·notional` (21 = 3 payments/day × 7 days),
identical to `cost% = |fr|·21·L·100` of margin. Both are shown; the block's colour
is the economic effect for the pressed side.

**Scroll anchor is mandatory (inv. 18).** The board re-renders wholly through
`innerHTML` on every action and every 30 s with the ticker. Restoring absolute
`scrollTop` caused a jump, because block heights ABOVE the reading point change
between renders. What is remembered is the section under the top of the screen and
the offset inside it; the key is the text of its `.bd-h`. Section gone → previous
behaviour; `scrollTop < 4` → no anchor.

**Metal on the frames.** The ring is a SECOND background layer: the block fill is
clipped to `padding-box`, the metal to `border-box`, and the border-wide gap shows
`linear-gradient(148deg, …)`. Radii stay exact (`border-image` breaks them) and no
new nodes, pseudo-elements or masks appear — decisive on a surface that re-renders
every 30 s. Highlights are near-white deliberately: at 1px and DPR 3 a soft
gradient collapses into one grey line.

**Switch is `:not([style])`.** Inline `style` on `.bd-sec` exists on exactly two
blocks — the alarms «СТОРОНА ПРОТИВ СТРУКТУРЫ» (red) and «ВНИМАНИЕ» (amber) —
where the border colour carries meaning. **Trap:** any new inline style on a
`.bd-sec` kills the metal on it; if an inline is needed, use a class.

### 3.8 «ШОРТ СОЗРЕЕТ, КОГДА»

Lives INSIDE block 2 «ПОЧЕМУ ЭТА МОНЕТА»; no separate section, so the block order
and anchor keys (inv. 15, 18) stay untouched. Drawn only when `boardSide = short`
and the bot supplied at least one of the two numbers.

Two PACE conditions — exactly the ones that currently cut a short candidate's
score in `scoreCandidate`:

```
1. eff14 <= EFF_TREND (0.60)      above -> the rise went in a straight line, score ×0.5
2. r7   <= r30·(7/30) − PACE_Z·sd_day·√7        PACE_Z = 0.25
```

Both thresholds are read from the same constants as the score (inv. 20).
Counter `N / M` in the header: `M` is how many conditions could be checked at all.
Colours: green when `done = known`, amber when partial, grey at zero. **Red is
deliberately unused** — «not ripe yet» is waiting, not danger. The block's own
caption states that these are conditions of PACE, not of PRICE: price belongs to
«ДИАПАЗОН 90 ДНЕЙ» and to the «СТОРОНА ПРОТИВ СТРУКТУРЫ» alarm and is not duplicated
here.

### 3.9 Residual to BTC — `res7`

The coin's weekly move decomposes EXACTLY, with no remainder:

```
r7 = mkt + own      mkt = β₉₀·btc.r7 (market part)     own = res7 (its own)
```

**Beta by the sign of the REALISED `btc.r7`**, not by the slider: `up_beta_90` when
`btc.r7 ≥ 0`, `down_beta_90` when `< 0`. The slider is a hypothetical future; `res7`
measures the past seven days, and a scenario has no right to influence a
measurement of the past. No discontinuity at zero: the multiplier `β·btc.r7 → 0`
there. This beta may therefore differ from `b=` in the `90d:` row, which is chosen
by the slider's sign — the divergence is normal and is named on the board.

**The measure is the sigma of the RESIDUAL, not the coin's full sigma.**

```
σ_res(hour) = Vol·√(1−R²)                    single-factor identity (§3.6)
z = own / ( Vol·√H_NOISE·√(1−R²) )           H_NOISE = 168 h
R² is the one PAIRED to the beta used: up_r2_90 / down_r2_90
R² clipped to [0, RES_R2_CAP], RES_R2_CAP = 0.90 — guard against dividing by ~0
```

Full sigma would systematically understate `|z|` (at R² = 0.42, by 24 %). No R² →
fall back to full sigma, which is conservative. No `volatility` → `z = null` and
the number is shown raw and called raw.

**Threshold `RES_Z = 1.0`** — a residual of exactly one weekly residual-sigma;
fires in ~32 % of weeks by chance. 0.5 was rejected: 62 % of weeks says nothing.

Four states (`cls`), each caption correct for ANY signs of `own` and `mkt`:
`own` (`|z| ≥ RES_Z`, green if `own ≥ 0`, red if `< 0`) · `market` · `quiet` ·
`unknown`. **Colour = significance, not trade side** — grey means «no own move»,
not «bad for a long».

Shown on the card as one line `Своё 7д: +X.X% · Zσ`, visible in all screen modes,
and on the board inside block 2 with the full audit. **Not in `scoreCandidate`** —
pure display, measured at zero predictive value (§3.10a, inv. 27). Missing inputs →
the block is not drawn and the rest of the card lives (inv. 9).

### 3.10 Scoring backtest — `bench/backtest_bench.py`

Separate file, production untouched. Answers one question: does `scoreCandidate`
sort coins better than a lottery.

**Construction.** Zero copies of production math (inv. 21). Each run cuts the scoring
functions and the constants they read out of `index.html`, assembles them into one bundle
and executes it with node; the fields
`cur/min/max/volatility/r7/r14/r30/vol7/eff14/vol_ratio` come from a block cut by
AST from `get_token_betas` in `main.py`. Editing either production file changes
the bench automatically. **`cur` is computed by that block and published nowhere** — it is in
neither `CD_FIELDS` nor the row `main.py` writes — so the reconciliation compares no
end-of-window level and `--attrib` has nothing to net its start-instant term against
(§10). Measured 12.09.2026 by TZ-40, which had been specified against a `cur` cell that does
not exist.

**The extraction MANIFEST is deliberately not enumerated here, and the omission is the
repair (inv. 60).** This paragraph used to list the five names `JS_FUNCS` carried, which
made the map a second copy of a list that lives in the bench — and both copies went stale
on the same day, when production split `scoreCandidate` into `qualityScore` + `scoreFinish`
and neither the code's list nor this sentence learned it. The authority is now
`_assert_js_closed`: it derives the identifiers a bundle references from the bundle's own
text, compares them against what the bundle, its driver and one short explicit `JS_GLOBALS`
list define, raises at BUILD time naming the first identifier defined nowhere, counts what
it compared and refuses to pass on zero (inv. 22). The globals list is short on purpose —
every entry on it is a name the check can no longer catch.

**Data.** `data.binance.vision` monthly ZIPs (3 years of hourly candles), tail
topped up from `data-api.binance.vision`. Pair list from the frontend's `tokens[]`.

**The monthly archive is published with a LAG, and the lag is not the same on both venues.**
Measured 05.09.2026: the monthly ZIP for the last COMPLETE month answers 200 on `futures/um`
and 404 on `spot`, while both venues already carry that month's DAILY files. The old refill
loop filled only the CURRENT month from dailies and expected the last complete month to
arrive as a monthly ZIP, so on `futures/um` it did and on `spot` it did not: **744 h,
interior, on every spot pair and on no perpetual**, for as long as the lag lasts. A
publication schedule therefore read as a venue asymmetry in the code, and the tail top-up
could not cover it either — the hole sits BEHIND the last row, not in front of it.
`_vision_rows` now records every month the monthly ZIP did not carry and refills each
from that month's daily files, whatever the reason it was absent; months before the pair's
first archived month are skipped, and that window is read off the data — the first month
that answered 200 — never declared. **The repair does not depend on the lag being
permanent**, which is the whole point: a fix keyed to «spot publishes late» retires silently
on the day the schedule changes.

**The tail is topped up from the SPOT endpoint and no futures mirror exists (inv. 64).** A
`fut:true` series therefore ends at the archive's last daily file and carries a visible tail
deficit of about a day, which the census prints rather than hides. Run #16: **31 of 31
symbols cached**, 26 spot pairs at tail 0, five perpetuals at 20 h of tail each, and one
interior gap in the whole set — GRAM's 53 h at the rename joint (inv. 63).

**Metric.** Excess return against the list mean: the score decides «which of the
30», not «where the market goes». IC = rank correlation of score with the future
per date, averaged, CI by block bootstrap; plus top-3 vs mean, worst drawdown by
score tercile, and three controls (shuffled score, «proximity to min90 only»,
«r7 only»).

**Modes:** `--probe` · `--selftest` · `--fetch` · `--fetch-funding` · `--verify` ·
`--attrib` · `--run` · `--regimes` · `--regime-gate` · `--stops` · `--res7` · `--funding` ·
`--target` · `--lab-selftest`. **This list has no producer and was stale in three places at
once**: `--fetch-funding` and `--regime-gate` had never been in it and were found by TZ-39,
`--attrib` arrived with TZ-40. The authority is `main()`'s own argparse block; a mode missing
here is a defect in this map and never in the bench (inv. 20, 58).

**Every artifact JSON is written by ONE helper, and a failed write leaves nothing behind.**
Since TZ-50 the six artifact writes — `regimes.json`, `stops_raw.json`, `target_raw.json`,
`regime_gate_raw.json`, `res7_dates.json`, `run_raw.json` — go through `_dump_raw`, which
serialises the whole object before it touches the filesystem, writes a temporary file in the
same directory and renames it onto the target, and on any failure removes both the temporary
file and the target before re-raising (inv. 72). Exit behaviour is unchanged: serialisation
still raises and the step still exits non-zero. **Four `json.dump` sites sit deliberately
outside it and none is an artifact**: the two bridge job files, which carry `allow_nan=False`
on a hot path, and the two cache writes, which carry no such flag. **NaN stays bare** —
`json.dumps` writes it and Python reads it back, so every raw artifact shares one convention;
refusing it would make two of them unwritable again and mapping it to `null` would move
artifacts no TZ was touching (§10).

**`sm["agree"]` is a two-level map, and the shape is decided by a counter rather than by
taste.** The two-annotator agreement of `--regime-gate` is keyed
`{marketRegime word: {btc_regimes word: count}}`, sorted at both levels so the artifact is
deterministic; a tuple key is what made that artifact unwritable for the whole life of the
mode. **A list of records was refused**: `_out_fields` turns each dict key into a path
segment and returns one leaf per scalar, so a tuple key and a two-level map both give one
leaf per pair while a record of three scalars gives three — which would have moved section
E's field count and its comparison total for a reason having nothing to do with agreement
(§3.10a). Joining the pair into a delimited string was refused separately: both words are
free text from two sources, and a delimiter there is a parse waiting to be wrong. The printed
table is byte-identical across the change, because `sorted()` over the tuples and the nested
walk produce the same order.

**`--verify` is the only mode that can fail in the DANGEROUS direction** — print
«matches» where nothing matched. Its rules are locked by `bench/verify_bench.py`
(offline): the measure is chosen by FIELD TYPE (levels `rel`, returns `pp`,
`eff14` `abs`); a non-zero exit code on any failure; comparisons counted PER FIELD,
not per coin; fields not comparable because of the archive's ~1-day lag are named
in the verdict; cache files starting with `_` are skipped.

**Since TZ-29 a failing cell is CLASSIFIED and the class decides the verdict**, because one
threshold table was reporting three different causes as one number. `venue-basis` is read
off the calculation that already prints the «БАЗИС ПЕРП/СПОТ» line and is reference (§3.14);
`coverage` is decided by the field's OWN window — read out of `main.py`'s AST rather than
written down a second time (inv. 20) — against the coverage census; `unexplained` is
everything else. The last two return non-zero and **remove the SYMBOL from `--target`'s arms
rather than removing the run.** The gate is computed inside `--target` and never read out of
a file `--verify` writes, because the workflow runs `--target` first and a control whose
answer depends on step order is not a control (inv. 62). Deviations carry their sign; the
comparison is on the magnitude. **This retired the v3 single-outlier licence, and it is a
tightening:** that licence let one coin over the bar exit 0 at any magnitude, and it existed
only because the verdict had no way to name a cause.

**Since TZ-34 the venue actually fetched is an OBSERVATION and the classifier reads it.**
The fetch loop tries spot then futures for a coin not declared `fut:true` and keeps the
longer series, which is unchanged; what changed is that the leg which won is now written to
`cov["venue"]` at the site that knows it, and `venue-basis` is granted where the SERIES is a
perpetual rather than where the ASSET was declared one. Before TZ-34 the cache label came
from `fut` — a fact the loop knew before it fetched anything — so a coin silently cached on
the perpetual measured its basis against CoinGecko's spot index and fell into `unexplained`,
«everything else», which is in `HARD_CLASSES` and removes the symbol from `--target`'s arms.
**A document carrying no `venue` is never read as spot**: the fetch side refetches it and the
read side refuses and names every affected symbol, because a default in the reading direction
reproduces the same defect one layer down where nothing would report it (inv. 67).

**Since TZ-44 comparability is decided per SYMBOL and per FIELD, before the class.** The old
window was derived once for the whole cache, from the newest last bar anywhere in it, so the
symbols that needed it — the perpetuals, whose own bar is never the newest (inv. 64) — were
exactly the ones it never described; and a cell announced as not compared was classed anyway,
because `over` was computed with no reference to the announcement. Now each symbol's OWN end
instant is measured against production's `generated_at`, and `_cell_comparable` decides the
cell from that gap alone — reading no venue, no census and no threshold, because comparability
is a fact about instants. **The window is TWO-SIDED** at `CMP_GAP_H = 3.0`, one module
constant, with the sign carried into the printed reason and never into the decision; before
this, an archive LATER than production was compared at any distance with nothing announced.
**An incomparable cell carries no class, no threshold verdict, no contribution to any count of
agreement and no exclusion from `--target`** — it is read, printed and named in `nocmp`. A
symbol holding one is `unverified`, a class in neither `CLASSES` nor `HARD_CLASSES`, ranked
after any hard class and ahead of `venue-basis`: **`clean` may never mean «nothing was
compared»**, which is this mode's dangerous direction written as a class. `never` reads
PRESENCE, not comparisons — a field absent from the live `coeffs.json` still fails the run, a
field present everywhere and comparable nowhere is an operational state and is named — and the
agreement line lists only fields with a comparison behind them, each printing `сверок N из M`.
**`--attrib` is deliberately NOT filtered by comparability**, which is precisely why it can
attribute the cells `--verify` declines; its return carries `nocmp` where it carried `skip`.

**Since TZ-51 the archive is read AT production's instant.** A price is stamped at the END of its
hour, so the comparison used to take the archive at its last close whatever the gap — a
production built at 10:50 against the archive's 11:00 value, which is run #25's one cell. Where
the archive holds the bar containing production's instant, `_archive_at` builds the reading on
that bar — the windows ending at its two stamps, each with its own close and then with the other
stamp's close at its end — and `_nearest` takes production's own value where it lies inside that
span, else the bound it lies beyond; the cell's `dv` is taken from that. **Where no bar holds the
instant — production built after the archive's last close — the reading stays at that close**
(§10), and the span is bounded by the enclosing CLOSES, not by the bar's high and low. `"a"` keeps
its meaning, the archive at its last close, because `--attrib` checks it against its own build;
`--target`, `--regime-gate` and `--attrib` read the same classes and moved with them. `--verify`
prints how many symbols it read at production's instant and how many at the last close.

**Since TZ-33 the `--target` PRODUCTION arm mixes two prices, deliberately and at a cost
that has to be named.** Production's own call sequence changed, so the driver takes the
second pass too and `prod.g` is the ANCHORED geometry — a driver still making one call would
execute a sequence production no longer performs (inv. 42, 48). What did NOT move is the
reference leg every arm is scored against: `stop`, `dist`, `b_log` and the first-touch
resolution stay at `E`, because they are shared with the substituted arms and moving them
would move those arms too. **The production arm is therefore ADMITTED at the anchor and
RESOLVED at `cur`**, so on a waiting row it counts the outcome of an entry production would
not have taken, and its `R` pairs an anchored `rr` with a barrier pair measured somewhere
else. The decision is right for the substituted arms and wrong for the production one, and
the repair is a SECOND arm rather than a moved leg. **TZ-36 built it.** `prod_anchor`
is ADDITIVE — `stop`, `dist`, `b_log` and the `E`-based first-touch resolution are
byte-identical, so every arm already measured keeps its numbers — and it computes its own
levels and calls the resolver a second time: entry at the anchor, stop at the anchored
`inv.price`, target the same 90-day extremum, plus a FILL GATE, because an arm admitted at the
anchor and resolved from `cur` counts trades production would not have taken while an arm
resolved at the anchor with no fill gate counts trades that were never entered — both are
fictions and only the pair repairs it. The window runs from the fill hour to the SAME horizon
end, since lengthening it would move the one quantity every standing result is truncated by
(§3.10a D3), and a fifth outcome class `unfilled` is counted apart from «никуда». `Ω` is taken
over FILLED setups only, with `P(unfilled)` and `P(никуда | filled)` beside it, and the bar is
`1 / RR_MIN` read from `index.html` at run time (inv. 65). **The arm now has its archive
figure — measured 09.09.2026, and it is the WORSE of the two arms on both sides** (§3.10a).
Filling costs 13-15 % of the setups outright, and of those that fill two thirds go nowhere
inside the horizon; `Ω` falls from 0.083 to 0.036 on the long side and from 0.034 to 0.006 on
the short. **That direction is the whole argument for having built the pair**: the arm
admitted at the anchor and resolved at `cur` was counting the outcome of an entry production
would not have taken, and it was counting it FAVOURABLY. The verdict does not move — every
CI95 on both arms sits entirely below the 0.50 bar — and the two arms are not a comparison
across instruments, since both were taken on the same run and the same twelve coins.

**Since TZ-30 the failing set has ONE definition site — `HARD_CLASSES` — and two readers.**
`verify_against_live` decides the exit code from it and the module-level `target_gate`
decides which symbols leave `--target`'s arms, so the two cannot disagree about what
«failing» means, and a widening of the constant now turns two gate steps red from two
directions: step 4 on the reconciliation and step 14 on the constant itself. Neither the
constant nor the lift of the arm gate out of `main()` changed a number, and that is
demonstrated rather than asserted — the old inline expression was cut by text out of the
previous revision and run beside the new function over the exhaustive product of five
symbols × ten per-symbol states, **100 000 cases, zero differences**, with the same differ
shown able to see 40 951 against a deliberately wrong gate (inv. 45).

**Selftest is mandatory before trusting any number.** Three worlds — pure random
walk (the reference factor must read 0), mean reversion (+), momentum (−) — ten
seeds each, because at SE(IC) ≈ 0.03 a single seed strays 2 SE about one run in
twenty. Plus a look-ahead check: the record for date `t` built from the full
series must be byte-identical to the one built from the series truncated at `t`.
Below ten seeds the selftest raises a FALSE ALARM by construction — it errs
towards declaring itself broken, never healthy.

**A stale cut fails LOUDLY at the run and SILENTLY at the trigger, and no published number
is affected.** With `scoreFinish` missing from the bundle, node compiled it without
complaint — `node --check` sees syntax, not reference — the driver's per-row
`catch (e) { r = null; }`, which exists so an unscorable row yields `null` instead of
killing the run, converted the reference error into a DATA value, and every row came back
`null`; the run then died hundreds of lines downstream on `'>' not supported between
instances of 'NoneType' and 'NoneType'`, naming neither the function nor the file. That is
a crash, not a wrong answer: a null column produces no IC, and `--selftest` never reached
its three world blocks at all. **Every standing result below therefore predates the split
and none of them is contaminated** — what the split destroyed is the instrument, not its
output. What made the destruction invisible is the TRIGGER rather than the defect
(inv. 62): `backtest_bench.py` runs only under `backtest_bench.yml`, which is
`workflow_dispatch` only, so the file it cuts its arithmetic out of moves on every
production TZ while the only thing that would complain waits to be asked. It was dead at
step 2 of its own job, under `bash -euo pipefail`, until TZ-27 tripped over it.

**Since TZ-30 the garrison is `bench/backtest_guard_bench.py`, gate step 14, offline; its
check count is §0's and is not restated here** (inv. 20). It loads this module by path and
never re-implements a rule it checks (inv. 21): every assertion calls a production function by
name and compares its return, and every fixture is synthetic input to that function. **Its sections
are not enumerated with a count here** (inv. 20): the authority is the file's own `# X.`
headers, and the next letter is READ from them and never counted — two sections share the
letter `E`, so counting gives the wrong one, and §10 carries why. That count went stale
between TZ-30 and TZ-41 while it stood in this paragraph. What the garrison covers today: the
four bundles build, close and pass `node --check`, with three
negative controls · `_vision_rows` offline, including the refill, the pre-listing window,
inv. 64 and the last-complete-hour stop · the coverage census on hand-built buckets ·
`_splice`'s arithmetic, admission and refusal · what `target_gate` does with a class · the
venue recorded as an OBSERVATION · the anchored production arm · `d4_partition` on
hand-built dates (TZ-37) · `_cell_comparable`'s decision, section K (TZ-44) ·
and the reading at production's instant, section L (TZ-51). `requests` is stubbed and every assertion about a host that
must not be contacted reads that stub's record, so the step opens no socket — **asserted by
construction, which is its own limit**: a future reach to the network through something
other than `requests` would be invisible to it.

**What the garrison narrows is inv. 62 and it does not retire it.** The gate now proves that
every function this bench cuts still exists in `index.html` and that each bundle is closed
under reference; it proves nothing about the arithmetic inside those functions. Production
may change what `qualityScore` computes, every bundle will still build and close, and the
standing results below remain what they were measured on. **A stale CUT is now caught on
every push; a stale RESULT still needs a dispatch.**

**Standing result — the model is an attention sorter with measured zero
predictive power.** `scoreCandidate` IC across both sides and 3/7/14d horizons
lies inside [−0.006; +0.026] with CI95 crossing zero, on 145 weekly dates × ~24
coins, at a power that resolves |IC| ≥ 0.041. Shuffled control −0.033…+0.000.
Rank-1 follow-up: №1 beats the list median on 50 % / 48 % of dates. **Weights are
never tuned** — the rule «do not touch the weights under any outcome» was
registered before the run and holds.

**Re-measured on the repaired instrument and on the wider universe — same answer.** Run #16
(05.09.2026; 144 dates × 26.9 coins, 31 of 31 symbols cached) reads IC across both sides and
3/7/14d inside **[−0.026; +0.032]**, every CI95 crossing zero, shuffled control
−0.008…+0.030, both verdicts «ШУМ». **That retires the caveat above:** the standing result no
longer rests only on runs predating the `scoreFinish` split, and the universe going 28 → 30
moved nothing. A null measured twice on two instruments is still a null (inv. 32).

### 3.10a Experiment lab — pre-registered measurements

Additive modes of the same bench; production untouched; rules registered BEFORE
data (inv. 23). One PRIMARY claim per experiment; everything else is exploration
at a doubled bar (|IC| ≥ 0.10, CI99). **A positive primary wires NOTHING into the
product by itself: the standing gate is a fresh confirmation run after +26 weeks
of new data.**

| Experiment | Primary claim | Result | Consequence |
|---|---|---|---|
| `--stops` | pooled measured/model calibration of the invalidation layer at 7d | **re-measured 09.09.2026 on 30 coins:** LONG 0.89 [0.69; 1.09], SHORT 0.85 [0.71; 1.00] — CI covers 1 on both, and the short side now covers it **at its upper bound**. Previous reading 0.88 [0.68; 1.07] / 0.88 [0.74; 1.03], run #16 | touch model honest; no multiplier in §7. The short side is the cell to re-read first on the next dispatch: one more step in the same direction and the CI stops covering 1, which would make the model OPTIMISTIC about stop touches |
| `--res7` | LONG · 7d · contrarian residual, IC ≥ +0.05 | **re-measured 09.09.2026:** −0.030 [−0.067; +0.004], control +0.020, 144 dates; previously −0.009 [−0.048; +0.030]. All exploration cells fail | `residual7` stays display-only |
| `--funding` | SHORT · 7d crowding-z, IC ≥ +0.05 | **re-measured 09.09.2026:** −0.024 [−0.055; +0.011], control −0.027, 144 dates; previously +0.003 [−0.030; +0.039]. All exploration cells fail | no crowding factor; funding stays a cost. **The shuffled control is the size of the signal here**, so this cell says nothing beyond «not +0.05» |
| `--target` | `Ω = n_tgt / n_stop` on the production arm, pooled per side, against the bar `1/RR_MIN = 0.50` | **measured 09.09.2026 on TWELVE coins** — the reconciliation removed eighteen (§7, §10). Production arm: LONG `Ω` 0.083 [0.040; 0.146] on 714 setups × 135 dates; SHORT 0.034 [0.006; 0.070] on 502 × 134. **Anchored arm `prod_anchor`, its first archive figure ever:** LONG 0.036 [0.010; 0.074] on 619 filled of 714 × 135 dates; SHORT 0.006 [0.000; 0.020] on 428 filled of 502 × 134; pooled 0.022 [0.008; 0.041] on 1047 filled of 1216. Every CI95 **entirely below 0.50**. Superseded reading: run #16, 05.09.2026, 30 coins, single-pass instrument — LONG 0.025 [0.010; 0.043] on 1740 × 136, SHORT 0.016 [0.002; 0.036] on 1095 × 137 | the 90d extremum does not pay the odds its own R:R promises at 168 h — and neither does any continuation rung. **No `k*` exists in the grid on either side**, so nothing crosses into `index.html` and §3.12's veto stands (inv. 32) |

**The production arm's figure MOVED between the two runs and the move is unattributable, which
is why the verdict and not the number is what stands.** `Ω` long reads 0.025 on run #16 and
0.083 here, and TWO things changed at once: the instrument (single-pass → the TZ-33 two-pass
geometry) and the universe (30 coins → 12). Neither reading supersedes the other on the
number. **What survives both changes is the only thing the experiment claims** — every CI95
on both runs, both arms and every rung sits entirely below 0.50.

**The twelve-coin universe is not a random twelve** (§3.10b). It is the seven coins the
reconciliation called `clean` — ALGO, BCH, ETH, GRAM, HBAR, SKY, TRX — plus all five
perpetuals, which carry the `venue-basis` licence and therefore never fail. **Perpetuals are
5 of 12 here against 5 of 30 in the real universe**, so the sample over-weights them two and
a half times, and the eighteen removed coins are removed by a class that names no cause
(§10). A figure taken on it describes it and nothing wider.

**The continuation channel was measured on the same run and it does not open either.** The
grid sets the target at `k · vol·√H_NOISE` and `Ω(k)` falls monotonically on both sides —
exactly as D2 requires, and in the wrong direction for the hypothesis:

| k | LONG n / dates | LONG `Ω` [CI95] | SHORT n / dates | SHORT `Ω` [CI95] |
|---:|---:|---|---:|---|
| 1.0 | — | no setups — unreachable through `RR_MIN` (§3.12) | — | no setups |
| 1.5 | 994 / 120 | 0.202 [0.118; 0.338] | — | no setups on the archive |
| 2.0 | 1525 / 137 | 0.095 [0.049; 0.162] | 867 / 132 | 0.107 [0.041; 0.205] |
| 2.5 | 1871 / 143 | 0.074 [0.045; 0.119] | 1104 / 137 | 0.061 [0.023; 0.116] |
| 3.0 | 2048 / 143 | 0.047 [0.023; 0.087] | 1298 / 141 | 0.045 [0.014; 0.088] |

**Re-measured 09.09.2026 on the twelve-coin universe, and the finding is confirmed on a
different sample**: `Ω(k)` still falls monotonically on both sides, every rung's CI95 still
sits below 0.50, and **`k*` is still absent from the grid on both sides**. The rung figures
themselves are not restated here — they are a second sample of a withdrawn hypothesis, and
carrying two grids would put one finding in two tables (inv. 20).

**The nearest reachable rung is the best of them and its CI95 tops out at 0.338 against a bar
of 0.50**; every wider target is worse, and `P(никуда за 168ч)` climbs 52 % → 69 % as `k`
grows. **The ordering is the one inv. 32 predicts and it is not an opportunity:** a nearer
target buys first-touch odds and sells reward at the same rate, so on a driftless walk it
buys nothing — and the nearest rung of all is the one `RR_MIN` refuses outright. What the
ladder rules out is the OPPOSITE hypothesis, that a farther continuation target would pay
better than the extremum. Reference on the production arm: mean `1/RR` 0.213 long and 0.293
short, so the admitted set sits far above `RR_MIN` and the generous 0.50 bar was generous by
a further factor of two.

Descriptive, no action by registration: 35 % / 42 % of stopped setups return to
entry within 7d; the only cell where measured exceeds model is the 6σ-capped LONG
bucket (3.5 % vs 0.9 %, n = 681), consistent with the fat-tail prior in §7.

**Lab selftest (`--lab-selftest`)** — known-answer worlds, offline: flat-vol GBM
→ stops ratio must read 1 (reads 0.93–0.98); wick world (one-sided intra-hour
spikes invisible to close-based σ) → must exceed 1 (reads 1.45–1.63); res-null /
res-reversion worlds → 0 / strongly positive; uncoupled / coupled funding worlds
→ 0 / +0.24…0.27. Two lessons recorded before real data: volatility clustering at
the 2σ floor pushes the stops ratio BELOW 1 (errs safe), and symmetric diffusive
jumps stay inside the estimated σ — only wick-like moves can push the ratio above 1.

**Section D (`--target`) is nine controls rather than a world, and the count is stated here
because a stale one has already cost a cycle**: TZ-36 specified «two new controls beside
D1–D6» while D7 was already taken by TZ-32, and the Executor had to renumber its own controls
to avoid two D7s in one output. The nine: D1 target calibration, D2 monotonicity of `Ω(k)`,
D3 the limit as the window grows, D4 an identity differ, D5 truncation invariance, D6 a side
swap (TZ-27, re-registered by TZ-28) · D7 the regime-word partition (TZ-32) · D8 the anchor
partition and D9 the anchor-off identity of `prod_anchor` (TZ-36). **D2 and
D3 shipped red, and the reason is inv. 61 — both bars named an object the author had
assumed rather than derived.** D2 required `Ω(k)` to fall across five grid points when
production's own `RR_MIN` can never admit the first one, so the claim was unevaluable
rather than false; D3 required `P_none < 0.05` at a fixed rung where escape still measures
0.154, so a correct resolver was refused by three times the numeral. **Both now derive
their object at run time.** D2 probes the unmodified `tradeGeometry` for the `rr` each grid
point can reach (`k=1.0` 1.6169 · 1.5 2.6940 · 2.0 4.0023 · 2.5 5.5914 · 3.0 7.5214) and
asserts two things: emptiness coincides exactly with unreachability, and the fall is
strict across the points that clear quorum. D3 walks a registered ladder
`H = m·H_NOISE`, `m ∈ {1, 4, 8, 16, 32}`, and asserts SHAPE — escape decays, the gap to the
closed form shrinks, and `Σq/Σ(1−q)` lands inside `Ω`'s CI95 at the rung where escape has
decayed. On the driftless world it reads `P_none` 0.639 → 0.304 → 0.154 → 0.055 → 0.000 and
`Ω` 0.026 → 0.146 → 0.213 → 0.250 → 0.293 against `Σq/Σ(1−q) ≈ 0.25`, converging exactly at
`m = 16`; **no numeral in the rule names that rung — D3c finds it** (inv. 49).

**The negative control is section D's acceptance criterion and it now passes.** Inverting
`_touch_calc`'s long/short branch turns D1, D2, D3 and D6 red; D4 and D5 correctly do not
fire, because an identity differ and a truncation check both run the inverted resolver on
each side of their own comparison. Under the OLD bars D2 and D3 were red before the
inversion and unchanged by it — they could not tell a broken resolver from a healthy one,
which is the whole cost of a bar written rather than derived.

**D4 has been RED since TZ-33 and the lab has said so to nobody.** It compares the `prod` arm
against `ident` — a substituted arm handed production's own 90-day extremum, which must
therefore reproduce `prod` exactly — and TZ-33 made `prod`'s geometry the ANCHORED one while
`ident` stays at `E`. **The control is CORRECT to refuse**; what is wrong is that it asserted
an identity without naming the world that makes it one (inv. 69), and `--lab-selftest` runs
only under `backtest_bench.yml`, so the verdict «НЕИСПРАВНА» has been the lab's answer on
every dispatch across two TZs with no push able to surface it (inv. 62).

**Measured here 09.09.2026 on the merged tree, offline and reproducible by anyone holding the
repository** — `--lab-selftest` prints the line, and the decomposition is `run_target` on the
same seeded world, so this is a computation over repository content and not a fetch (inv. 44).
**The 1 165 closes exactly and every difference is on a row the chase rule fired on.** Of
7 926 comparisons, 118 are presence mismatches and 1 047 are field differences:

- **455 rows the chase rule never fired on** — bit-identical across all eight compared fields,
  both arms present, zero differences.
- **521 waiting rows** — `rr` and `tgtSig` differ on EVERY one; `first`, `hit`, `p`, `a` and
  `b` differ on NONE; `R` differs on exactly those whose `first` is `tgt`, because `R` is `rr`
  there while the mark-to-market, the stop return and the tie return are shared.
- **118 presence mismatches, and they carry a direction.** 113 are `prod` present with `ident`
  absent, all anchored-admitted — the anchored pass admits setups the R:R veto refused at
  `cur`, which is the defect TZ-33 exists to repair — and 5 run the other way, refused at the
  anchor and admitted at `E`.
- **With the anchor forced off**, the same run reads 7 848 comparisons, **zero** differences
  and **zero** presence mismatches.

**That the resolution leg did not move is the strongest thing in this reading**, and nothing
currently checks it: §3.10 asserts it in prose, and the partition above is the measurement.
**The repair is therefore a partition, never a narrower field set** — deleting `rr` and
`tgtSig` from the comparison would be an assertion removed to make a bench pass (hard floor
item 2) and would stop checking the very leg the prose promises. Reserved as TZ-37 (§10,
inv. 69). **Closed by TZ-37, merged.** D4 is now the pair inv. 69 requires: `D4a`, the identity
re-asserted with the chase rule forced off — 7 848 comparisons, zero differences, zero presence
mismatches — and `D4b`, the partition on the live path over the same 7 926, with both
populations non-zero and every defect bucket at zero. The reading above is what `D4b` now
asserts field by field rather than what a session measured once. **Its construction is a named
function and gate step 14 calls it**, so the partition cannot rot between dispatches the way the
identity it replaced did (inv. 62), and both of the wrong repairs inv. 69 names stayed refused:
no field was dropped from the comparison and the flag alone was not accepted as the answer.

**Capital-efficiency question, answered by identity.** P&L per dollar of margin =
`L · move`, and the engine sets `L ≈ risk_budget / dist`, so ranking by capital EV
is ranking by expected R-multiple and nothing else. Measured with a handicap
favouring the hypothesis: LONG IC(score, R) −0.027, SHORT +0.014; №1 above the
list median R on 47 % of dates. Cost spread between candidates is ~6 % of a
typical move whose sign is unpredictable. **No EV ranking.**

**Regime follow-up.** Look-ahead-free buckets (trend-up > +5 % 51 dates · range
±5 % 50 · trend-down < −5 % 41; expansion split 70 / 72) — all ten cells null at
the doubled bar.

### 3.10b Resolution ceiling — what this bench can and cannot see

Detection threshold is set by universe width, and the width is a decision rather than an
accident: **|IC| ≈ 0.06–0.07 for a single pre-registered test, ≈ 0.09 for any search.**
Every cell below was measured at 28 coins and the list is now 30, which moves the ceiling
by less than the third digit — the ceiling falls with the SQUARE ROOT of the cross-section,
so escaping it needs a universe four times wider, not two coins wider (§3.10c). The
measurements are not re-stated at 30 and are not re-run: a sample is described by the
universe it was taken on. ~40 directional cells have been measured here; all
lie inside the null distribution for that number of tests. Effect sizes in the
external literature are produced on cross-sections of 84–500+ coins and locate the
profit in small, illiquid, high-cost assets — the exact complement of a 30-coin
top-perp list.

**Operative rule.** A new ranking factor is admissible ONLY on an external prior
that names an effect size THIS sample could resolve, on a cross-section shaped
like ours, at a 7–14 day horizon. «It predicts in the literature» is not such a
prior.

### 3.10c Next architectural gate

**THE GATE, IN ONE LINE.** The wide research bench is built the first time a named
tier-1 hypothesis arrives carrying an external effect size **≥ 0.030 IC, measured
on a LIQUID cross-section (top-100 by volume or equivalent), at a 7–14 day
horizon.** An effect size from a small-cap universe, or a claim of predictiveness
with no number attached, does not open the gate.

If triggered: Binance USDⓈ-M perpetuals, target **n = 120** (150 buys only
0.026 → 0.023 for 25 % more fetch; below 100 the tier-1 unlock is lost). Filters,
in order: ≥ 3 years of continuous hourly candles with no listing gap > 48 h
(binding filter) · median 24h notional ≥ $30M · exclude wrapped duplicates,
pegged assets and 1000X-style pairs · **delisted perps MUST be included for the
period they traded** — today's 30-coin bench is survivorship-biased by
construction. Bench-only, production untouched, no new runtime dependency.

**Transfer gate is a VETO, never a confirmation.** Any factor passing on the wide
universe is re-measured on the 30 traded coins; required: same sign, and the
30-coin point estimate inside the wide-universe CI95. That test resolves only
|IC| ≥ 0.060, so it can KILL a factor but can never bless one.

**The prize, sized honestly.** A validated IC = 0.030 factor is worth 0.57 % per
selection to the top-1 pick — about $34 per trade at $1.5k margin × 4X, ~$890/year
at 26 selections, and it would take ~2300 live trades to separate from luck. Even
a fully validated factor could never be confirmed by the Boss's own trading
experience; using it would be an act of trust in the bench. That is why the gate
is deliberately expensive.

**Build trigger is not perishable.** `data.binance.vision` is historical, so
building the wide bench in 2027 yields 2027's history including everything back to
2023. Building it now with no hypothesis queued buys a fishing expedition.

### 3.11 Position protection — «ЗАЩИТА ПОЗИЦИИ»

The other thirteen blocks answer *«may I open this, and how big»*. This one answers
the question that exists only once the position does: **when can the trade stop
being able to lose money, and what does that cost.**

```
break-even  BE  = E·(1 ± c),  c = 2·FEE_TAKER + f,  f = ±|fr|·FUND_PAY_7D
                  sign of f = economic direction for THIS side (§3.1)
                  c clamped to [−0.9, +0.9] — pathological-rate guard only
arm price   ARM = E·(1 ± ARM_R·dist),  dist from invalidationInfo (§3.2)
                  never closer than BE — below BE a "break-even stop" locks a loss
scratch     P   = touchProb(|ln(ARM/BE)|, H_NOISE)           §3.3
                  armed → the row switches to |ln(cur/BE)|
top-up      add = notional/L_ceiling − mrg → liquidation moves to liqPrice(E, L_ceiling)
```

**Why 1R and nothing else.** R — entry to structural stop — is the only risk unit
this system measures. Any other trigger would be a newly invented constant.

**Taker on both legs.** A stop exit is a stop-market order; charging entry as
taker too errs to the safe side. Round trip = 0.10 % of notional = 0.10 %·L of
margin. **Seven days everywhere,** so the leverage engine, the funding block and
this one cannot disagree.

**No threshold on the scratch probability, deliberately.** Whether a 47 % chance
of scratching is worth removing stop risk depends on the Boss's own hit rate,
which the system has never measured. A traffic light would look like a measured
verdict without being one. The scratch number is the point of the block: moving a
stop to break-even is normally believed free, and on XRP-like inputs (Vol 0.9 %/h,
1R = 9.1 %) noise drags price back to break-even within 7 days in **47 %** of weeks.

Degenerate cases are named, not hidden: `inv.capped` → the arm inherits a drawn
stop and says so · costs ≥ 1R → the arm collapses onto break-even and the
probability row is dropped · no `volatility` → probabilities disappear,
break-even survives · no invalidation level → break-even alone · no funding rate →
fees only. **Exactly one probability on screen at any time** (`pArm` before the
arm, `pNow` after).

Pure display: no output enters leverage, score, ranking or the invalidation level
(inv. 27).

### 3.12 Direction engine — veto cascade

**Principle: direction is decided by a CASCADE OF VETOES, not by a sum of
weights.** Nothing in it predicts anything. Each layer either asserts «the
geometry of this trade is bad» or «this prior is not admitted right now»; both are
measurable without a forecast. It therefore does **not** reopen the predictive
layer closed in §3.10b: no ranking factor is added and no weight is tuned.

```
Layer 0  REGIME     one per list      trend | range | stress
Layer 1  GEOMETRY   veto, no forecast R:R · noise floor · money · entry chase
Layer 2  CHANNEL    exactly one       mean reversion  XOR  continuation
Layer 3  CATALYSTS  veto only         manual registry, cannot raise a score
Layer 4  VERDICT    default = NO      trade | wait | watch
```

**Layer 0 — `marketRegime(btcStats)`**

```
z   = btc.r7  / (btc.volatility·√H_NOISE)          BTC's weekly move in its own σ
eff = btc.r14 / (btc.volatility·√(2·H_NOISE))      clipped to ±3
stress  if  btc.volatility ≥ VOL_HARD  or  |z| ≥ REG_STRESS_Z
trend   if  |eff| ≥ EFF_TREND,  dir = sign(eff)
range   otherwise
```

`eff` is deliberately the same formula the bot uses for a coin's `eff14`, compared
against the same `EFF_TREND`: one threshold per system (inv. 20). **Known
property, measured:** under a driftless random walk `eff ~ N(0,1)`, so
`|eff| ≥ 0.6` labels ~55 % of pure-noise windows «trend». Accepted, because a
false trend label cannot produce a wrong direction — it narrows the admissible
side to one, and on a driftless market both channels are worth exactly zero.

**Stress is symmetric, and that is the whole point of the layer.** The comparison
is on `|z|`: a four-sigma week UP admits no side either — a one-sided lower branch
once printed «ТРЕНД ВВЕРХ» in green on days when geometry refused 24 of 25 covered
coins. `out.dir` stays 0 under stress: `dir` is read only on `trend`, and handing
a direction to a state that admits neither side would be a contradiction in one
object. The banner picks its wording by the SIGN of `reg.z` — «РЫНОК ПЕРЕГРЕТ»
above, «СТРЕСС РЫНКА» below, red in both. The cost is by design: on a stress day
every `action` is `none` on both sides.

No `btcStats` or no `volatility` → `mode = 'range'`, `known = false`, which is
exactly the pre-engine production behaviour (inv. 9). The regime label says WHICH
state the market is in and never HOW FAR into it the session sits; that second
quantity is measured in §3.16 and printed in §3.17, and no threshold in this
engine reads it.

**Layer 1 — `tradeGeometry(cd, E, isLong, dec, hi24, lo24)`**

Turns numbers the board already prints from advice into prohibition. Nothing is
recomputed: the target is the 90-day extremum, the risk is `dec.inv.dist`, the
money veto is read from `dec.moneyBelowMin` (inv. 20).

| Veto | Condition | What it prevents |
|---|---|---|
| target passed | `tgt ≤ E` (long) / `tgt ≥ E` (short) | trading toward a target already behind price |
| reward/risk | `reward/risk < RR_MIN` | a trade that must be right more often than wrong |
| noise floor | `reward/(vol·√H_NOISE) < TGT_SIGMA_MIN` | targets the market reaches by chop |
| money | `dec.moneyBelowMin` | a stop costing more than `MAX_MARGIN_LOSS` even at `L_MIN` |
| leverage | `!dec.ok` | «БЕЗ БЕЗОПАСНОГО ПЛЕЧА» becoming a tradable card |

**`E` is a PARAMETER and the caller decides which price it is.** Every number the function
returns — reward, `rr`, `tgtSig`, risk and the `wait` limit — is measured from the `E` it
was handed, and `dec` must be the decision taken at the SAME price: a risk leg cut at one
price against a reward measured at another is not a ratio.

**Entry discipline — `wait`, not a veto.** Anchor = the 24-hour low for a long,
the 24-hour high for a short (already in the Binance ticker — zero new requests).
Beyond `ENTRY_CHASE_SD` daily sigmas from that anchor the card enters ЖДАТЬ and
prints the price to wait for. It forbids not «buying high» but «buying AFTER the
move» — chasing, not strength.

**Layer 2 — `momentumScore`, and the ban on adding channels.** `scoreCandidate`
is the mean-reversion channel and is not modified. The continuation channel is its
mirror: trend intactness (`eff14` in the side's direction), own strength (`res7`
z), weekly vs monthly pace, quality. **The two are NEVER summed** — summing
opposite priors is exactly what produced one coin ranked both long and short on
the same data. The regime admits one; the other is not computed. Quality and
penalties are shared through `qualityScore` / `scoreFinish`, lifted out of
`scoreCandidate` without a single arithmetic change (proven on 200 000 random
inputs, 0 mismatches). `trendPenalty = false` removes exactly the two `eff14`
penalties: continuation wants the trend intact, mean reversion wants it broken.

**Layer 3 — `catalystCheck`** (registry §3.15). Events older than one day
(`−1` back edge) or further out than `CAT_WINDOW_D` are ignored; first note wins.

```
conf !== 'confirmed'  →  may ANNOTATE its own side only, never veto      (inv. 39)
conf === 'confirmed'  →  dir !== my side  →  VETO, early return          (inv. 31)
                         dir === my side  →  note
dir = 'both'          →  vetoes both sides: two-sided event risk, zero code change
```

**Layer 4 — `directionVerdict`.** Default is NO TRADE. A side is emitted only when
everything lines up: regime admits the prior → channel ranks the coin → geometry
passes → no catalyst veto → the entry is not a chase. The score is computed
ALWAYS, at any outcome: a card without a score is invisible to sorting, and the
prohibition lives in `action`, not in silence.

**One coin can never receive both ЛОНГ and ШОРТ — structurally, not empirically:**

```
stress → neither side
trend  → only the side matching reg.dir
range  → only the side with the HIGHER mean-reversion score (tie → neither)
```

The range rule is load-bearing: a coin mid-range with a wide 90-day range can
clear R:R ≥ 2 on both sides simultaneously. Geometry filters bad trades; it does
not arbitrate direction. The regime does (inv. 30).

**Two passes, and the trade is decided on the SECOND one (TZ-33).** The first pass runs at
`cur` for one purpose — to locate the ANCHOR, the price this verdict publishes as its entry:
`geo.wait` where the chase rule fired, `cur` where it did not. Where it fired,
`leverageDecision` and `tradeGeometry` run again AT that anchor, every level the card prints
is computed there, and the veto is read off that pass ALONE — a coin refused at `cur` must
reach the anchor before it can be refused. The signature therefore takes `btcStats`: the
second `leverageDecision` needs the BTC ceiling, and a caller passing thirteen arguments
drops that ceiling silently and nothing else.

```
geo    = tradeGeometry(cd, cur, …, dec)        pass 1 — anchor only, no veto read
anchor = geo.wait !== null ? geo.wait : cur    what the card publishes as the entry
decA   = leverageDecision(cd, anchor, …)       pass 2 — only when wait fired
geoA   = tradeGeometry(cd, anchor, …, decA)    the geometry the veto is read off
```

**Termination is a property, not a hope: `geoA.wait === null` whenever `geo.wait` is not.**
`lim` is built from the 24-hour anchor and `sigmaDay(vol)`, neither of which depends on `E`,
so it is the same number in both passes and the second tests `E > lim` at `E === lim`.

**The single-pass form was biased in exactly ONE direction and both halves of the bias
pointed the same way.** `invalidationInfo` clips its distance FROM AN ENTRY, so a stop cut at
`cur` and published against `geo.wait` sat closer to the published entry than `INV_FLOOR_SD`
permits — on every waiting row, in the dangerous direction. And at the lower entry the reward
`(tgt − E)/E` strictly rises while `dist` can only fall or hold at the 2σ floor, so `rr` is
strictly LARGER at the anchor: the old R:R veto refused setups that cleared `RR_MIN` at the
very price the card named, and never the reverse. Neither error was reachable on a `СЕЙЧАС`
row, where the anchor IS `cur` and `decA` is `dec` object-identically — which is why the
defect survived every board bench that never built a waiting row.

**`row.dec` is not the anchored decision and must not become it (inv. 14).** The board, the
card and every leverage control keep deriving from the current-price decision; `v.decA`
reaches one surface — `planLine` — and nothing else. The score is not re-run either: it is
fixed before the anchor exists, and a score moving with a hypothetical price would reorder
the board on a price nobody paid.

**Display contract** — inv. 33–36 carry it: number and word mean PLACE IN THE
RANKING and STRENGTH OF ATTENTION, the glyph (`stateMark`) means ENTRY STATE
(empty = trade, `~` = wait for the pullback with its price, `✕` = no trade); the
tier badge reads «Сильный / Средний / Кандидат / Фон» at thresholds 70/50/35;
`planLine` prints entry and target only where the engine allowed the trade, and every number
on that line comes from the ANCHOR — `vd.decA.inv.price` for the stop, the anchored `geo.rr`
for the ratio (inv. 35, 66); a card
below `TIER_MIN` moves to the expandable strip rather than vanishing; degraded
rows are never hidden.

**Known structural tension, deliberately not fixed.** `tradeGeometry` does not
take the regime: the target is always the 90-day extremum, i.e. a MEAN-REVERSION
target, while in `trend` the ranking comes from the CONTINUATION channel. A coin
with strong momentum sits near its 90-day extremum, so remaining reward is small
and R:R breaks against `RR_MIN`. The veto is substantively CORRECT in the observed
cases, and «a continuation target would have produced a better outcome» is a
hypothesis without a backtest, which inv. 32 forbids acting on.
**Opening condition MET and the answer is NO — measured 05.09.2026, run #16.**
`bench/backtest_bench.py --target`, built by TZ-27, repaired by TZ-28 and gated on the
reconciliation by TZ-29, ran the archive with both arms off one shared risk leg, so
`inv.dist`, `inv.price`, `moneyBelowMin` and `ok` are the same numbers in both and only the
reward moves. Above quorum on both sides: the production 90d extremum reads `Ω` 0.025
[0.010; 0.043] long and 0.016 [0.002; 0.036] short, and the continuation channel reads 0.202
at its nearest reachable rung and falls from there (§3.10a). **Every CI95 on every rung is
entirely below `1/RR_MIN = 0.50`, and `k*` does not exist in the grid on either side.** The
tension named above is therefore REAL and its obvious repair is REFUTED: swapping the
mean-reversion target for a continuation one does not buy the odds `RR_MIN` is asking for.
The veto is not merely correct in the observed cases — it is correct against the alternative
that motivated the doubt. **Re-measured 09.09.2026 on a different twelve-coin universe and on
both `--target` arms, the verdict is the same** — every CI95 below the bar, no `k*` on either
side (§3.10a) — so the refutation now rests on two samples that share neither instrument nor
membership. **`tradeGeometry` therefore keeps the extremum target**, §10's row
on it is withdrawn rather than open, and a TZ proposing the change now argues against a
measurement rather than against a silence (inv. 32).

**The run also says the TARGET was never the binding constraint — the HORIZON is.** At 168 h
most setups resolve nowhere: `P(никуда)` is 69 % long and 60 % short, so `Ω` is computed on
the minority that resolve and is truncated far below its untruncated value. D3's ladder shows
where it stops being truncated — the gap to the closed form `Σq/Σ(1−q) ≈ 0.25` closes at
`H = 16 · H_NOISE`, sixteen weeks (§3.10a). This system trades 1–14 days. **No target
geometry repairs a horizon**, so this paragraph is re-opened by a change of holding period
and by nothing else (§8: the 7d/30d horizon switch is closed).

**One fact about the continuation target is already established, through production's own
arithmetic rather than through a market: the NEAR target is untradable.** `RR` is largest
exactly at the invalidation floor `INV_FLOOR_SD · sigmaDay = 2·vol·√24 = 9.80·vol`, and at
`k = 1.0` the reward `exp(vol·√H_NOISE) − 1` reaches a maximum `RR` of **1.611** across the
entire range in which leverage is issued at all (`0 < vol < VOL_STOP`), on both sides,
against `RR_MIN = 2.0`. So `RR_MIN` does not merely prefer the far target — it refuses the
near one outright, on every coin and in every world, which is this section's own fact that
reward/risk is monotone in target distance with no ceiling, running the other way. Any
future continuation design starts at `k ≥ 1.5`, and that is a property of the product, not
of a bench.

### 3.13 Verdict journal — «вход → вердикт доски → факт»

**Built and running** (`journal.yml`, 13:00 UTC). A daily record of what the board
said about every coin — inputs, verdict, the catalyst registry in force, the engine
fingerprint — plus, 7 and 14 days later, what the price did. A measuring
instrument: nothing is displayed, nothing feeds back into any calculation
(inv. 27). It exists because the verdict is not reconstructible after the fact:
`history.json` keeps betas, R² and rank only, while `scoreCandidate`,
`tradeGeometry` and `leverageDecision` need exactly the fields it does not keep —
every unjournaled day is lost permanently.

**Fingerprints, carried here rather than in `§ 0` because no TZ touching the backtest gate
opens this subsystem:** `journal/write.js` **849 lines**, `19722fb53d75b6d25a8f957f74f97422`;
`bench/journal_bench.js` **1177 lines**, `993271f44995c8ae21c54935a3f80adf`. A TZ opening
either states the pair in its own `§0`, exactly as one opening a backtest bench does. What
`§ 0` still owns about `journal_bench.js` is its COUNT, which moves with verdict content and
not only with control volume.

**Layout — one file per unit of work, never reopened.**

| Path | Written | Content |
|---|---|---|
| `journal/data/YYYY-MM-DD.jsonl` | once per date | `k:"s"` snapshot line per covered coin, `k:"x"` skip line per uncovered one |
| `journal/out/YYYY-MM-DD-h7.jsonl`, `…-h14.jsonl` | once per date × horizon | `k:"oh"` BTC header, then `k:"o"` per coin |
| `journal/runs.jsonl` | appended per run | `k:"r"` run line, `k:"g"` gap line per unrecorded date |

**Snapshot fields.** `d · ts · sym · pair · gen · age · px{src,cur,p24,qv,hi,lo,cnt}
· reg · cd (analysis_data row verbatim) · btc (coeffs.btc verbatim) · rp ·
long{…} · short{…} · cat{acting,hash} · fp{script,commit}`. Side block, since TZ-36:
`rel · score · tier · ch · action · why · note · verdict · wait · tgt · geo · dec · inv ·
anchor · decA · invA`.
**A production return is stored as a NAMED PROJECTION, unrounded — and this map said WHOLE
for four revisions.** «Whole» was the intent and is not the code: the writer lists the members
it keeps, and `inv` is not a member of `dec` in the record at all, it is hoisted to a sibling.
That is why the anchored stop lives in `invA` and never in `decA.inv`, and the distinction is
load-bearing rather than pedantic — a reader written against the old sentence looks for
`decA.inv`, finds nothing, and silently resolves against the other price; TZ-36 caught exactly
that in its own Stage B before commit, and only because its fixture mirrored the record's real
shape instead of a convenient one. Unrounded still holds and is the part the corpus depends
on: a field not written today cannot be recovered from a year-old record, and it costs bytes.
**The members are deliberately NOT enumerated here** — an enumeration of a production return
is a second copy of a shape this map does not own, and every such copy in this document has
gone stale (inv. 20, 60). The authority is the WRITER rather than the function, and the
projection is precisely why. Outcome line: `p0 · p1 · hi ·
lo` plus, per side, the ISO hour of first touch of `tgt` / `stop` / `wait`,
`first ∈ tgt|stop|tie|null`, and since TZ-36 `sstop` — the level the resolution actually used
— beside `ssrc ∈ decA|dec`, which names the recorded object that level was read from. `tie` means both levels fell inside one hourly candle
and the order is genuinely unresolvable — recorded, not guessed.

**Since TZ-33 `geo` is the ANCHORED geometry** — `rr`, `reward` and `tgtSig` measured at the
price the card published, `geo.wait` null on every waiting row by the termination property
(§3.12), the wait price itself unaffected because it lives in the side block's own `wait`.
For one revision `dec` and `inv` stood beside it still describing `cur`, so a waiting row
recorded a stop the board did not print while `planLine` printed the anchored one, and the
outcome layer timed its touch against a stop no card ever named: the same SHAPE, a different
MEANING, invisible to every schema check (inv. 66).

**Since TZ-36 the record carries a complete set at EACH price, and the epoch boundary is
readable from the record itself.** `geo` + `anchor` + `decA` + `invA` describe the published
entry; `dec` + `inv` describe `cur` and did NOT move, because the board, the card and every
leverage control derive from the current-price decision (inv. 14) and the record must keep it.
`decA` is written UNCONDITIONALLY, including on a `СЕЙЧАС` row where it is `dec`
object-identically: storing it only where it differs would put production's pass-2 rule inside
every future reader of the corpus, and a field whose absence means «look up the rule» is not a
record. The outcome layer resolves against `invA.price` where the snapshot carries `decA` and
against `inv.price` where it does not, and `ssrc` records which on EVERY line — a default in
silence is the defect, a default that names itself is the disclosure (inv. 67). **Records are
immutable (inv. 38), so the fourteen days written between TZ-33 and this merge are disclosed
and never repaired**: they carry no `decA`, resolve through `ssrc:'dec'`, and any analysis
pooling outcome lines across the boundary splits on that field, which is what it is for. The
writer's call to `directionVerdict` already passed `btcStats` as the fourteenth argument —
TZ-33 added it in the same commit that created the second pass — so the failure that would
have dropped the BTC ceiling out of the anchored decision on waiting rows alone never existed
in this tree.

**Three standing decisions.**

1. **Daily, not hourly.** Daily resampling is worth exactly 1.00× against weekly
   at a 7–14 day horizon (consecutive dates share 6/7 of the forward window);
   hourly buys 24× the storage and zero independent observations. Reversed if the
   Boss starts trading intraday.
2. **Coverage is 25 of 30 by construction** — the five `fut:true` assets have no
   spot leg in this system (§3.14) and Binance production hosts answer HTTP 451 from
   Actions (inv. 24). They are attempted every run and recorded as explicit skip lines, so
   the gap is measured rather than assumed. The venue test short-circuits ahead of
   all five classifier branches, so a `fut:true` asset can never increment
   `hardSkip`; the reason string still records what was observed:

   | Observed | Reason string | `hardSkip` |
   |---|---|---|
   | no row at all | `futures-only: no spot mirror pair` | no |
   | row present, dead | `futures-only: delisted spot mirror row` | no |
   | row present, **alive** | `futures-only: spot mirror row unexpectedly alive` | no |

   The third case pushes `fut:true asset trading on spot: <SYM>` into `run.note`. A dead
   **spot** pair still hard-skips and still degrades `status`. **Since 03.09.2026 that
   third string is no longer necessarily a contradiction, and the map says so before the
   note starts firing:** MORPHO and ARB were declared futures-only by the owner for this
   system, not because Binance lacks a spot market for them, so if the mirror answers
   alive the note names them every single run and stops distinguishing anything. The
   note's information content is the §10 item, not this row; the classification is
   correct either way, because the declaration decides the venue and the host never does
   (inv. 41).
3. **`#N` is NOT recorded.** The board's number is produced inside `update()` by
   `byScore` → strip filter → `assignRanks`, which is not callable in isolation;
   recording it would mean reimplementing it (inv. 21 forbids that). It is fully
   derivable at analysis time from `score`, `rp`, `rel`, `tier`. The same standing
   applies to the day-range reading (§8).

**What it is for, in order:** an audit trail of what the Boss actually saw · the
compensating control that makes `catalysts.json` safe (the acting set and its hash
sit next to every verdict) · eventually a live sample. It is NOT a backtest and
carries no predictive claim: §3.10b's resolution ceiling applies unchanged, and a
year of daily records is ~52 independent 7-day windows.

**Growth:** ~73 KB per day of snapshot data, plus outcome files. This is the only
unbounded artifact in the repository and the one thing the monthly audit watches.

### 3.14 Asset venue contract — 25 spot, 5 futures-only

**Boss's architectural decision.** Five of the 30 assets — **XMR, LIT, HYPE, MORPHO and
ARB** — exist for this system on **Binance Futures only**. The other 25 trade on Binance
Spot. This is a declared property of the asset inside this list, not an observation about
what some host answered on a given morning.

```
fut:true   XMR · LIT · HYPE · MORPHO · ARB     perpetual only in this system
default    the remaining 25                    spot ticker + perpetual funding
```

**The two sets have different reasons and the same standing.** XMR, LIT and HYPE have no
usable spot leg. MORPHO and ARB were declared futures-only on 03.09.2026 because that is
where the Boss trades them, and whether a spot market exists for either is not a question
this system asks. That is the whole force of «declared, not observed»: a rule that reads
the host would have classified the two sets differently and would have been wrong about
both.

**Consequence 1 — price source (inv. 12).** `fut:true` tokens are excluded from
the spot `?symbols=` list and priced only from `cachedFutTickers`; the dead-market
detector works on `count` alone.

**Consequence 2 — a ghost spot pair does not revoke the declaration (inv. 41).**
`data-api.binance.vision` still answers for `XMRUSDT` and `LITUSDT` with a
delisted, zero-volume row. The row exists; the market does not. Classifying by
what the host returned disagreed with the declaration and showed up as a
permanently degraded `status`.

**Consequence 3 — the bench divergence in §7 is a source property; the CLASS held and the
MAGNITUDE was refuted.** Measured 05.09.2026 on all 30 coins (run #16): the reconciliation
classed 21 cells `venue-basis`, 0 `coverage` and 0 `unexplained`, and the five coins carrying
every one of those cells are exactly the five `fut:true` assets. **Since TZ-34 the basis licence follows the SERIES and not the declaration**, so that count is
no longer a property of the `fut:true` set: a declared asset whose archive is spot earns
nothing, and an undeclared coin cached on the perpetual earns the licence. Both directions are
asserted end-to-end through `--verify`'s own exit code, and a third assertion holds that the
declaration changes NOTHING — the two lanes must agree exactly (§3.10, inv. 67).

**Two later readings break the second half of that sentence and not the first, and the
second of them is much larger than the first.** On 08.09 UNI, XLM and ZEC classed
`unexplained`; on 09.09 **eighteen coins did, across 35 cells** (§7, §10), and the licence
count fell 21 → 20. Every one of the eighteen is a SPOT asset, so this venue contract
does not explain any of them: it explains a perpetual measured against a spot index, and
none of these is a perpetual. **A class meaning «everything else» explains nothing by
itself**, and the size of this one is what moved it out of §3.14 and into a specification
of its own. **The prediction
that MORPHO and ARB would show «the same divergence for the same reason» was wrong in both
directions**: this map wrote 7–9 pp on returns, MORPHO reads 2.4–3.8 pp and ARB reads
14.3–24.8 pp. The reason was right and the size was carried over from three other coins and
stated as an expectation. **A divergence CLASS is predictable from the venue contract; its
SIZE is a property of the individual asset's basis and is not** — the same rule inv. 52 makes
for a reachability reading, applied to a number this map produced itself.

**Consequence 4 — coverage is 25/30 and every added futures-only asset widens the gap.**
Every statistical statement built on the journal or on the day-range measure is a
statement about 25 assets, and it stayed 25 while the list grew by two. Closing the gap
would require a second price source bought for five rows.

A `fut:true` row is reversed by an owner decision — for XMR or LIT, a Binance relisting
with real volume would be the occasion — and since TZ-15 that is four moves in one change,
not two: `tokens[]`, this paragraph, the §3.17 caption, and the exact-string expectation
section M pins it with. The gate stays red until all four move together, which is the safe
direction — a declaration and the sentence describing it cannot drift apart quietly
(inv. 20, 50). **TZ-26 proved the coupling by paying it:** the caption's spot count 25 did
not move when the list reached 30 and its futures count did, «три фьючерсные» →
«пять фьючерсных», in `index.html` and in the section-M expectation together. Both counts
in that caption are code sites of this contract in everything but syntax, and the futures
one is now also hand-written in `bench/journal_bench.js` and in the calibration record's
header (§10).

### 3.15 Catalyst registry — `catalysts.json`

The only external input of the direction engine, served next to `index.html` and
read by the frontend over ES5 XHR. **The data lives in the file; the rule lives in
`catalystCheck` and did not move.**

**Schema v1.**

```
{ "v":1, "updated":"YYYY-MM-DD",
  "items": { "SYM": [ { d, dir, kind, t, conf, src[], added } ] } }

d      ISO date of the event       dir    long | short | both
kind   unlock | protocol | listing | macro     CLOSED set, gate-asserted
t      the string the card prints  conf   confirmed | disputed
src    array of source URLs        added  ISO date the entry was written
basis  why the date is believed    OPTIONAL; MANDATORY at conf 'disputed'
```

The file is ASCII-only and the printed string `t` is `\uXXXX`-escaped.

**The `kind` enum is CLOSED.** It was once written with an ellipsis and read as open, so a
TZ proposed a fifth value and the gate refused it — one rule living in two places and
disagreeing (inv. 20). A new member is additive, needs its own TZ, and arrives with the
entry that consumes it, never speculatively.

**`basis` is invisible to production.** `catalystsApply` copies `items` wholesale and
`catalystCheck` reads `d`, `dir`, `conf` and `t` only, so an unknown key is inert by
construction (inv. 1, inv. 9) — measured, not assumed: the identifier appears in no
production file. It is inside `cat.hash`, so it sits beside every journalled verdict.

**Authority — `conf`, and the quorum behind it (inv. 39).** A registry edit
bypasses the TZ → Executor → pull request → audit chain, so the compensating
control is that only `conf === 'confirmed'` may close a side, compared exactly and
case-sensitively, and **`confirmed` requires at least one PRIMARY source** — the
protocol, the exchange or the foundation, matched by host on a dot boundary
against the allow-list in `bench/catalyst_bench.js`. Two aggregators repeating each
other are **not** a quorum: authority, not repetition, is the bar. The PRIMARY list
is the registry's trust root and changes only through a TZ (contract §7 item 13).

An unverified entry annotates **only its own side**: the note prints under an
*allowed* trade and therefore reads as an argument *for* it, so a
contrary-direction event there would lie in the loudest place on the board.

**Unavailability is not emptiness (inv. 40).** Every failure path — HTTP ≠ 200,
unparseable JSON, `v ≠ 1`, missing `items`, network error, `status 0` — lands in
the same state: registry `{}`, `CAT_LOADED = false`, `CAT_ERR` set, banner on
screen with the reason. The board keeps working and says it is running without the
layer. Known inert edge: opening the board over `file://` gives `xhr.status 0`.

**The journal reads the same file** and refuses to record a day whose registry it
could not read, in every mode, with a non-zero exit. `cat.hash` is sha256 over
canonicalised `items` — object keys sorted, array order preserved, because within
a coin the order decides which note wins.

**Registry content is analyst work under a TZ.** Current content: one `confirmed` ZEC
entry, `dir:'both'`, primary source, for the NU7 vote resolution on 14.09; one `disputed`
ENA entry, `dir:'short'`, for a derived unlock date on 05.09.

**Three classes of standing, and the third is why `basis` exists.**

| The primary publishes | Treatment |
|---|---|
| the date | `conf:'confirmed'` per inv. 39 |
| the mechanism but not the date | `conf:'disputed'`, **`basis` mandatory** |
| nothing about the event at all | the entry is deleted, never demoted |

The third row is the original rule, unchanged: a `disputed` entry annotates its own side,
so keeping one built on nothing keeps printing an argument nobody can check. The second
row is a case that rule did not name. Ethena publishes a 25 % cliff one year after TGE on
2024-03-05 and three years of linear monthly vesting thereafter, so monthly steps fall on
the 5th and 2026-09-05 is DERIVED from a primary-published rule rather than asserted
against silence. `basis` records the derivation in the file, which answers the objection
the third row raises — the argument is no longer unrecorded, and it can be argued with.

**An owner's assertion is not a source.** The date may be set by the Boss; `conf` may not.
`confirmed` is the compensating control over an externally editable file, and a flag that
can be set by assertion has stopped being one (inv. 39).

**Two scope rules, both closed permanently.**

1. **Coin-scoped events only.** A macro release, a central-bank decision, an index
   rebalance never enters this file. Market-wide risk is measured by §3.12 Layer 0, and a
   `dir:'both'` macro entry would close both sides on all 30 coins for fifteen days out of
   roughly forty-five. A `"*"` key is therefore not a missing feature, and the
   `items key "<sym>" is in tokens[]` assertion that refuses it is correct.
2. **Resolving events only.** An event qualifies when something the market prices becomes
   known or irreversible on `d` — an unlock releases supply, a vote concludes, a listing
   goes live, an agency decides. An administrative milestone on the path to one does not:
   a comment-period deadline, a filing date, a hearing being scheduled. Nothing resolves,
   and the veto would spend fifteen days of both sides on a non-event. TZ-20's ONDO row
   was closed by this rule with its date fully verified — the date was never in doubt, the
   event was.

Both rules also live in `bench/catalyst_bench.js`'s editing-rules comment, which is where
an editor meets them.

### 3.16 List exhaustion — the day-range measure

**Live, thresholded, printed; compared against one constant and forbidding
nothing.** It closes the gap that `regimeBanner` names the regime and says nothing
about how far into it the session already sits.

```
dayRangeRatio(hi, lo, cur, vol) = (hi − lo) / ( cur · sigmaDay(vol) · √(8/π) )

E[range] = σ·√(8/π) for Brownian motion — the denominator is DERIVED, not chosen
sigmaDay is the single site of the daily-σ conversion (inv. 20); this function
never recomputes vol·√24 of its own
null on any missing or non-finite input, on cur ≤ 0, vol ≤ 0, hi ≤ lo, on an
underflowed denominator and on an overflowed ratio — a missing measurement never
arrives downstream as a zero

listExhaustion(rows) -> { median, n, abnormal }
n counts only rows that produced a ratio; n < 8 → median null, abnormal false
```

**The reference value is 1, not «somewhere above 1» — and the archive confirms
the scale.** `E[range] = σ·√(8/π)` makes the ratio unbiased when σ is right, so a
diffusive day reads 1 on average. The archive measures a pooled coin-day mean of
**0.9509** against a null simulated in the same run at **1.0012** — a 5.03 % gap,
inside the 15 % the rule allowed: the denominator is correctly scaled, and a
mismatch between the bot's `volatility` and a reconstructed one would have moved
the mean and did not. The earlier claim that close-based σ pushes the reading above
1 by construction is **withdrawn** — the intra-hour understatement and the √24
scaling of microstructure-inflated hourly returns cancel to within noise.

**What the archive does show is over-dispersion against the null**, on both
objects. Coin-days (TZ-11): median 0.81 vs 0.93, p90 1.59 vs 1.38, maximum 15.6 vs
3.2. List medians (TZ-13, the object the consumer thresholds): p0 0.2407 vs 0.5850,
p50 0.7769 vs 0.9325, p90 1.3911 vs 1.2393, p100 10.6653 vs 2.6604. That is
volatility clustering (§7) thinning the middle and fattening both tails — the
property the banner exists to surface, not an artefact to calibrate away.

**The null is a floor on what a quiet market reaches, never a model of this one.**
It is a constant-σ common-factor construction with no vocabulary for a market that
alternates between very quiet and very violent regimes: the empirical distribution
is wider than it on BOTH tails, and the worst journaled date sits five times the
null's p99.9. Its whole job is to say where a quiet market stops, so that an
admissibility band can be drawn without writing one down (inv. 49). Reading a
percentile of it as the probability of a real day is a category error; the figure
printed on screen is a measurement of the day, not a likelihood.

**Nothing predictive is added.** This measures what the session already did, in
the same standing as §3.12 Layer 1: it asserts «the geometry of entering right
now is bad», which is measurable without a forecast. No ranking factor, no weight,
and §3.10b's resolution ceiling is untouched.

**Quorum `n ≥ 8` is load-bearing.** A statement about the list computed from three
coins is not a statement about the list, and the banner is the one list-wide
element on screen.

**The estimator and its calibration share a universe: 25 spot assets (inv. 41).**
The three `fut:true` assets read their range off the perpetual while `volatility`
comes from a spot index (§3.14 Consequence 3), so `listExhaustion` skips rows whose
`tokens[]` entry carries `fut:true`; the venue test short-circuits AHEAD of the `cd`
test, so such a row can never reach `dayRangeRatio` whatever fields it carries, and
the quorum is applied AFTER the exclusion — a list reaching eight only by counting
`fut:true` rows has no median.

**The threshold and its consumer are the same random variable (inv. 47).**
`listExhaustion` compares the **median of the list**, so the constant is a
percentile of the distribution of per-date list medians, never of individual
coin-days: averaging 25 correlated coins removes idiosyncratic dispersion and moves
the upper tail. Measured on the same archive and the same 24 384 coin-days:
coin-day p90 **1.59**, list-median p90 **1.39** — the object was the error, the
data never moved.

**The adoption rule (inv. 23, 49).** The object is the per-date LIST MEDIAN produced
by production's own `listExhaustion`; the statistic is the 90th percentile; the
admissibility band is not written down but derived in the same run from a simulated
driftless null of that same statistic; once adopted, the constant is pinned to the
run that produced it (inv. 46). A hand-written band once refused a correct number —
TZ-11's `1.60 … 4.00` sat above the p99 of this run's null — and a band is never
widened to admit an observed number.

**The rule ran and returned `DAY_RANGE_ABNORMAL = 1.39`.** Run `Calibration
(archive)` #2, id 32667872706, seed 20260823, reproduced byte-for-byte on every
statistic by #3 on a second runner with a warm cache. The record is
`bench/exhaustion-calibration.txt`, fingerprinted in §0.

| Quantity | Value |
|---|---|
| object | per-date list median, produced by production's own `listExhaustion` through a node hop |
| sample | 1 110 dates, 2023-08-09 … 2026-08-22, none dropped below quorum |
| universe | 24 of the 25 declared spot assets; `GRAM` has no three-year archive |
| per-date contributing count | median 22, range 19 … 24 |
| ρ, MEASURED per date | mean 0.6196, range 0.4557 … 0.8265, negative on zero dates |
| null | 248 640 simulated date medians, p90 **1.2393**, MC s.e. 0.00117 |
| empirical p90 | **1.3911** → **1.39** at two decimals |

All four registered conditions passed, none marginally: the coin-day mean sits
5.03 % from the null's against an allowance of 15 %, and the empirical p90 lands
above the null's p95 (1.3626) and below its p99 (1.6271) — high enough that a quiet
market does not reach it a tenth of the time, low enough not to be a broken
pipeline. The known-answer control read **0.99980** over 10⁶ coin-days against a
registered 1.000 ± 0.005, and the same walk built from hourly CLOSES read 0.8613 —
the control detects the exact error it exists to catch. Step counts of 24/48/96/240
per day move the control by less than 0.0002, so the Brownian-bridge day is exact
in distribution rather than a discretisation.

**The row is the contract, with exactly one parse site per quantity (inv. 48).**
`update()` assigns `row.cur`, `row.hi24` and `row.lo24` from the ticker once,
immediately after the `nopair` early return and before the dead-market test, for
EVERY row that has a ticker — `fut:true` included, because the venue rule lives in
`listExhaustion` and a row filtered at the producer would put that declaration in
two places (inv. 41). Every consumer then reads the row: the `sideOn` branch, the
board header, §3.17 row 2, the off-list relevance filter, the dead-market card and
the card header. Only two `parseFloat(…lastPrice)` sites survive anywhere in
`index.html` and both read `btcObj` — BTC is the regime measurer, is not a member of
`rows[]` and never reaches the measure. The gate's wiring section derives both
sides of the contract from the source — `update()` writes `cd, coin, cur, dec,
hi24, idx, lo24, sc, state, t, vd`; `listExhaustion` reads `cd, cd.volatility,
cur, hi24, lo24, t, t.fut` — and, run against a file whose rows lack the three
fields, names them as missing and exits non-zero.

**State at this revision.** The measure runs live, reads 25 on a full board, and has
one threshold and two readers. `DAY_RANGE_ABNORMAL = 1.39` is declared once in
`index.html`, compared once — inside `listExhaustion`, with `>=` — and worded once,
by `dayStateNote`; those three are the identifier's only code sites and the gate
enumerates them (inv. 20). `reg.day = listExhaustion(rows)` is written in
`update()` unconditionally and above the `sideOn` branch, because whether the day
is abnormal is a fact about the session and not about the pressed side. The board
keeps its own `listExhaustion(lastRows)` call: one pure function over one array
cannot disagree with itself, while routing the board through `lastCtx` would force
every board fixture to invent the field — the shape inv. 48 exists to catch.

**`abnormal` is a printed word and nothing else (inv. 27).** No output enters
`scoreCandidate`, `tradeGeometry`, `leverageDecision`, `directionVerdict`,
`liqPrice`, the tier badge, `byScore`, `assignRanks`, `planLine` or the journal
writer — proven by perturbation rather than inspection: scaling `hi24`/`lo24` until
`abnormal` flips moves no compared field on either side and leaves the record
`journal/write.js` would write byte-identical. The one field that moves under that
perturbation, `geo.wait` on SHORT, moves identically on the pre-TZ-14 revision — the
entry-chase anchor's long-standing dependency on the 24-hour range. That two-sided
form of the test is the general one: a perturbation that moves a field on both
revisions has proven nothing about the change. TZ-15 ran the identical protocol on a
harness written fresh and read 0 of **1 240** fields with the record byte-identical
again; the two field counts are properties of each harness's enumeration, and the
result replicating across two independent harnesses is worth more than either run.
**TZ-33 widened that confound and did not weaken the proof.** `hi24`/`lo24` now feed the
anchor, so the same perturbation moves `anchor`, `decA`, `geo` and every level derived from
them rather than one field — the entry-chase dependency this paragraph already names,
reaching further. The two-sided form is what carries it, and it now has a precondition: the
comparison revision must also have the second pass, or the control proves nothing.

`[решение принято мной]` Discarded: making exhaustion a Layer 1 veto. At the
adopted line it would close roughly a tenth of all sessions on both sides on the
strength of zero measured evidence that entering on such a day ends worse, and
inv. 32 forbids acting on that. Reopened only by a journal-based measurement of
outcomes conditioned on the day state, which needs no new recorded field (§8:
recording the reading is closed). **The decision now carries a text dependency, and
it is mechanical rather than remembered:** since TZ-15 the caption tells the Boss
that this is «мера дня, а не запрет», so a TZ reopening the veto repairs that
sentence in the same change (inv. 50) — and cannot forget, because gate section M
pins the caption as one exact string and turns red on any rewrite.

Two decile tables are on file: the coin-day one in
`CryptoReports/TZ-11-exhaustion-threshold-report.md`, the list-median one in the
record itself. Replayed on journaled days through the production functions:
**1.69** on 2026-08-21 (6 of 25 coins above 2.0) and **2.43** on 2026-08-22 (20 of
25) — against 1.39 both are abnormal days, which is what two of the most violent
sessions of the quarter should read. Days are not a distribution and bound nothing.

### 3.17 «РИСК ВЫНОСА» — the day's own risk

Sixth board block (§3.7). It answers a question none of the other thirteen asks:
**not «is this trade sound» but «does the position survive TODAY»** — the horizon
is 24 hours, everywhere else it is seven days. Three rows, all read from existing
production functions; nothing is recomputed and no formula is duplicated
(inv. 20, 21).

```
1  запас до ликвидации   liq = liqPrice(E, currentLev, isLong)   PRESSED lever, inv. 14
                         b   = |ln(liq/E)|
                         dist = b / sigmaDay(vol)      touch = touchProb(vol, b, 24)
2  день уже вынесен      own  = dayRangeRatio(hi24, lo24, cur, vol)      §3.16
                         list = listExhaustion(rows) -> median, n
3  стоп против шума      read from dec.inv: capped | floored | dist/sd
```

**The 24-hour horizon is the block's reason to exist and is not a duplicate of the
7/14/30d ladder in «ЦЕНА ВРЕМЕНИ».** The ladder answers «will this position live
out the week»; a four-sigma session asks whether it lives out the afternoon. Both
come from the single `touchProb` (inv. 20), so the two horizons can never
disagree, and the ladder is not repeated here.

**Row 2 compares, and forbids nothing.** Whenever the list median reaches
`DAY_RANGE_ABNORMAL` the row gains a third line: the one sentence `dayStateNote`
builds, in amber, byte-identical to the sentence the regime banner prints above the
card list (inv. 33). Amber is the «ВНИМАНИЕ» alarm's standing — attention without
prohibition — and it is deliberately not applied to the regime line itself, which
would make one line carry two independent facts and would overwrite the stress red
exactly when it matters most. On a quiet day and on a below-quorum list both
surfaces are silent, so the sentence's presence is itself the measurement, and its
absence is not an omission. The two raw numbers above it stay interpretable without
a threshold because the unit is derived, not chosen: `E[range] = σ·√(8/π)`, so 1,0
is an ordinary day. This is the standing of §3.12 Layer 1 — an assertion about
geometry that needs no forecast — and it adds no ranking factor, so §3.10b's
resolution ceiling is untouched.

**The caption states what the day line means and denies nothing the block has
(inv. 50).** It names the threshold as the 90th percentile of the list median over
the three-year archive, a measure of the day and not a veto, and keeps the half that
is true and proven (§3.16): the number reaches no score, no leverage and no verdict.
It never prints the number — `DAY_RANGE_ABNORMAL` keeps exactly three code sites
(inv. 20), and the value is already printed one line above on the days it matters.
Gate section M scans this one block for six denial phrasings on both the quiet and
the loud render, pins the caption as one exact string, reads the constant through
the live context, and carries its own control: a copy with the old caption fires the
scan by name, the clean source is silent. Any future TZ that legitimately changes
this caption updates section M in the same change.

**Degradation is stated, never hidden** (inv. 9): no `volatility` → the sigma
distance and the 24h probability go, the block lives; `E ≤ 0` or non-finite `liq`
→ row 1 is dropped; `median === null` → the list line says how many coins had a
measure and that eight are needed; no `dec.inv` → row 3 is dropped.

Pure display in the standing of inv. 27, and the probability is a LOWER bound
(§7) — the caption says so, because a 24-hour number is the one most likely to be
read as a promise.

---

## 4. Invariants — DO NOT BREAK

Numbers are stable identifiers: production comments, benches, TZs and the contract
cite them, so an invariant is rewritten in place and never renumbered.

1. `coeffs.json` schema is **additive-only**; the bot's `err_result` is key-synchronous with its success result.
2. New coins enter only through `TOKENS` (bot) + `tokens[]` (frontend); check CoinGecko id, spot pair, futures pair, quota. No spot pair but a perp → `fut:true` is mandatory, and a perp the owner intends to trade as a perp gets it too — the flag is a declaration, not a report on Binance (§3.14). **The universe is frozen between owner decisions, never against them:** it stood at 28 from June 2026 to 03.09.2026 and stands at 30 now, and a coin arrives only the way MORPHO and ARB did — an owner decision that moves the contract's hard floor first, then `TOKENS`, then `tokens[]` (inv. 59). Three further couplings are not optional: the CoinGecko id is unverified until `debug.json` shows `error: null` and `matched_90d > 120` on a runner, the payload's own symbol list must gain the coin or the analytical gate refuses every price (§11), and the per-run CoinGecko call count moves with the list (§5).
3. `history.json` ≤ 720 points; reads must handle `truncated` via `raw_url`.
4. `STALE_WARN 75` / `STALE_CRIT 130` min ↔ the hourly Shortcut tempo (no cron, §1); change only as a pair. **Inside the 02:00–09:00 night pause a red threshold does not by itself mean failure:** age is compared against the last SCHEDULED run at 01:50, tolerance one missed hour; two missed hours is a failure.
5. Spot ticker `?symbols=`: HTTP 400 → the frontend sticks to the full 1.2 MB ticker until reload. Keep delisted pairs out; mark futures-native ones `fut:true`.
6. `applySavedOrder`: new coins go to the END of the saved order.
7. The client-side password is decoration. Secrets live only in GitHub Actions env — **with exactly four exceptions, all on the VPS (contract §7 item 6):** the Telegram bot token and the Binance API key with reading permission only, bound to the VPS's address, since contract v24; the repository's deploy key the VPS's clones push with, which v24 left uncounted; and, since v25, the analysis run's own Claude login. Each lives in a root-only file outside the repository, reaches only the unit that uses it as a systemd credential, and is never printed, logged or committed. **A unit that runs a model session runs as its own unprivileged user, never as root, and holds its own Claude login and the deploy key and nothing else** — `InaccessiblePaths=` is not a boundary against root, and TZ-54 measured the root run unit reading what it hid (§10, row «The assistant's build sequence»). A key with trading rights exists nowhere (§10, row «The engine places no order on the exchange»).
8. Every bot `requests` call carries `timeout=30`.
9. **The frontend must survive the absence of any new coeffs field** — both bot↔frontend combinations must work.
10. Rebranding a coin: change the display name and the Binance pair; **KEEP the CoinGecko id** — ids are permanent, a new id loses 90 days of history.
11. Three protective card states: «НЕТ ПАРЫ» · «ТОРГИ ОСТАНОВЛЕНЫ» (`count = 0` or empty book → calculations off) · amber «Расхождение источников» (price outside 0.5×min…1.5×max).
12. `fut:true` tokens: price only from `cachedFutTickers`, excluded from the spot `?symbols=` list; the dead-market detector works on `count` alone.
13. **Leverage math is validated — change only with a full bench re-run.** Three ceilings (§3.2), 7-day horizon for all three, minimum, round DOWN. Margin risk is the fourth (§3.4).
14. **Everything the Boss controls must derive from `currentLev`.** A block computing from the RESULT while the pressed button says otherwise produces a screen where liquidation moves and probabilities do not.
15. Board block order lives ONLY in the concatenation at the end of `boardHtml`; the block code must not be reordered (variables `notional`, `qty`, `mrg`, `qtyTxt` are declared in the size block and used below).
16. **Size unit identity `qty·E = mrg·L`.** One number is entered, the other derived; switching `sizeMode` never changes position volume. The entry price for the recomputation comes from `entryState`, not from a rounded HTML attribute.
17. **Exactly one button lights per group** (side, leverage, size unit, entry point). The 0.25 % entry-highlight tolerance is tied to the 0.5 % −/+ step: change only as a pair.
18. **Board scroll is restored by SECTION ANCHOR, never by absolute `scrollTop`.** The anchor key is the `.bd-h` text, which must stay unique within the board.
19. Min/Max blinking and the running edge borders are Boss-approved: never remove; improvements may be proposed, never silently applied.
20. **One number per threshold, system-wide.** `EFF_TREND` and `PACE_Z` are read by both `scoreCandidate` and «ШОРТ СОЗРЕЕТ, КОГДА»; `RES_Z` and `RES_R2_CAP` only inside `residual7()`; `FUND_PAY_7D`, `FEE_TAKER`, `ARM_R` likewise; `touchProb()` is the single touch formula and `probTxt()` the single probability-to-text rounding; `lMoney()` the single `MAX_MARGIN_LOSS / dist`. A threshold hardcoded in a second place will eventually diverge, and the screen will start explaining the score with the wrong number.
21. **A bench contains no copy of production math.** Formulas are cut out of `index.html` and `main.py` at every run. A hand-pasted copy diverges silently and the bench starts verifying code that is not in production.
22. **A check that passes with no data is forbidden.** Any validator must count the objects it compared and fail on zero.
23. **Experiment rules are fixed BEFORE the data, and the implementation of the rule is proved by a known-answer control BEFORE real data.** A naive price-on-time regression called 70 % of pure random walks a trend — the rule was right, the implementation was broken; replacing it after seeing results would have been fitting.
24. **Binance production hosts are unreachable from GitHub Actions — HTTP 451.** Only `data.binance.vision` and `data-api.binance.vision` work from a runner.
25. **`| tee` in a workflow step returns `tee`'s exit code, not Python's.** Without `set -o pipefail` a failed step looks green. All bench steps run `shell: bash -euo pipefail`.
26. **The money ceiling never kills a trade.** Margin risk participates in the `min` but with an `L_MIN` floor: `loss/margin = dist·L` is size-independent, so it is a rule about the SHARE OF THE ACCOUNT. Only the first three ceilings may produce «БЕЗ БЕЗОПАСНОГО ПЛЕЧА».
27. **«ЗАЩИТА ПОЗИЦИИ» and `res7` are pure display.** No output of either enters leverage, score, ranking or the invalidation level. Making a display block influence a decision is a separate change with its own justification.
28. **A class assembled by concatenation is invisible to text search.** `renderButtons` builds exactly two: `'side-btn' + ' a-' + mode` and `'stress-btn' + ' s-' + mode`. Any future CSS cleanup must resolve such sites by enumerating THEIR OWN loop; merging the two enumerations invents `s-long`/`s-short` and hides real orphans. Automated in `bench/clean_bench.py`.
29. **A verifying mode must RETURN an exit code.** A function without `return` yields `None`, `sys.exit(main() or 0)` turns it into zero, and a failed comparison looks successful while the screen honestly prints the failure. Printing is not returning.
30. **One coin — ONE side.** The guarantee comes from the regime layer, not from geometry: stress → neither, trend → only the market's direction, range → only the higher mean-reversion score. A mid-range coin passes R:R ≥ 2 on BOTH sides; removing the regime rule restores the contradiction. **The analytical engine keeps the guarantee and changes its source** (owner decision 18.09.2026, `ANALYST-INSTRUCTIONS.md` §2): its side is the coin's OWN regime read at the frozen price — a coin has one own trend, so the side stays unique — and the market word marks that side instead of gating it, a side against the word printed `⚠` and graded `СРЕДНЯЯ` at most (`2026-10-01-a`); market stress still closes both sides and a coin in its own range still carries none. Neither gate carries measured directional information (inv. 32), and the market gate had kept the engine's answer empty for two weeks while hiding a coin in its own uptrend. The board's mapping above is unchanged.
31. **A catalyst can ONLY veto.** It can never raise a score and never override a geometry veto. A catalyst placed above geometry is what produced a short on the floor of a range.
32. **Geometry does not predict and is not required to.** On a random walk `E[R] = 0` under ANY selection — a theorem, confirmed by the `--control` run (−0.001 at 2SE 0.080). Any future claim that «a veto raised accuracy» must first explain where drift or costs came from.
33. **One channel, one meaning, and no channel argues with the glyph.** NUMBER + WORD speak about PLACE IN THE RANKING and STRENGTH OF ATTENTION; the GLYPH (`stateMark`) speaks about ENTRY STATE: empty = trade, `~ $price` = wait for the pullback, `✕` = no trade. The distinction may never be carried by colour alone and may never erase the number. Both surfaces take glyph and verdict text from the SAME functions (`stateMark`, `verdictNote`) — a board silent about the card's prohibition is the same defect. Colour carries STATE, not score quality: at `action === 'none'` the badge fades to `#888` while the tier colour remains on `trade` and `wait`. Tier vocabulary is «Сильный / Средний / Кандидат / Фон», badge format «Сильный #1 — 91», thresholds `TIER_STRONG/TIER_MID/TIER_MIN` = 70/50/35. The market-cap rank carries no «#»: that symbol belongs to the score ranking alone.
34. **The number is a PLACE IN THE RANKING and every scored card has one.** Order is strictly by score (`byScore`, a 0.05 tie window resolved by market-cap rank), numbering continuous 1..N over the displayed list. Entry state may neither reorder the list nor take a number away. Only rows without a score and rows collapsed as irrelevant to the side (`row.off`) go unnumbered. `byScore`, `assignRanks`, `tierBadge`, `stateMark`, `verdictNote` are separate functions precisely so a bench can check them.
35. **Only an allowed trade prints an entry price and a target, and every number on the line is computed at ONE price — the one the line names as the entry.** `planLine` is empty at `action === 'none'`: printing «entry / target» where geometry or regime refused invents a recommendation the model does not have. Nothing on the line is recomputed and nothing is mixed: the entry is `vd.wait` on a waiting row and `cur` otherwise, the stop is `vd.decA.inv.price` — the decision taken AT that entry — the ratio is the anchored `geo.rr`, and the target is the same 90-day extremum `tradeGeometry` used (inv. 20, 66). **The earlier form of this invariant named `dec.inv.price` and was DISPROVEN by TZ-33:** that is the decision taken at `cur`, true only on a `СЕЙЧАС` row, and on a `ЖДАТЬ` row it prescribed a line whose stop sat closer to its own published entry than `INV_FLOOR_SD` permits (§3.12). An invariant naming a source field rather than a source PRICE cannot distinguish the two. The line exists only for tiers Сильный and Средний.
36. **A score below `TIER_MIN` leaves the main board but never disappears silently.** Such coins go into the same expandable strip as coins at the irrelevant edge of the range, with separate reason counters. Check order is fixed: weak score first, then position — otherwise one coin lands in both groups and the counters stop matching the strip length. Degraded rows (no pair / dead market / no metrics) are NEVER hidden: they are operational warnings, not candidates.
37. **Silence must be explained, and the explanation must be machine-readable.** A run that recorded nothing must return a NON-ZERO code; every run must leave one grep-able line with `generated_at`; the night pause must differ from a failure by rule (`freshnessState`), not by eye. A gap in the sample with no recorded reason is indistinguishable from «no events», and a sample with unexplained gaps supports no statistical statement. Hence the journal writes a missing date as a gap LINE, not as an absent line. **A bench not wired into `bench.yml` never executes and is not a control.**
38. **The journal is an instrument, and a record in it is immutable.** (1) The verdict is produced by EXECUTING the production script — functions are cut out of `index.html` and called by name (inv. 21). **A second implementation of any rule, threshold or formula is banned in any language and any file.** (2) A file once written is never reopened — not to append an outcome, not to fix a typo; the outcome lives in a separate file joined by key, and a re-run that finds an existing file writes `dup` and exits zero. Immutability is physical, not promised, because a record that can be rewritten stops being evidence exactly when the result is unwelcome. (3) Next to the verdict lies what can explain it: the acting catalyst set and its hash, the script fingerprint and the commit.
39. **Only a CONFIRMED catalyst may veto.** The registry is a freely editable file and a veto changes the verdict, so the right to close a side is granted by exactly `conf === 'confirmed'` — exact, case-sensitive; a missing field, `'CONFIRMED'` or any typo is NOT a confirmation, and every refusal errs safe. Confirmation requires a **primary source** (protocol, exchange, foundation) matched by host on a dot boundary against the PRIMARY allow-list; aggregators repeating each other are not a quorum, and the allow-list changes only through a TZ. An unconfirmed entry may annotate, and only its OWN side. Inv. 31 is neither weakened nor strengthened by this.
40. **An empty registry and an UNAVAILABLE registry are different states and must render differently.** A loader that did not get the file for any reason must leave the registry `{}`, raise `CAT_ERR` and put a banner on screen carrying the reason, while the board keeps working (inv. 9). The journal is stricter: a day whose registry could not be read is not recorded AT ALL, with a non-zero exit, in every mode — a verdict without a known catalyst set is not explainable after the fact (inv. 38(3)).
41. **The declared venue is read BEFORE the degradation ladder.** `fut:true` is a DECLARATION (§3.14), not an observation, so a skip on such an asset is DECLARED coverage in any form it takes and never raises `hardSkip`. The reverse order already cost the `status` field: a mirror served a delisted row and a healthy system reported `partial` every day. The reason is still MEASURED in three distinct strings, and a live spot pair on a `fut:true` asset must reach `run.note` — a contradiction of the declaration may not pass quietly. The rule is wider than the journal: any future consumer of `tokens[]` asks the declaration, not the host. **What it does NOT cover is the mirror question, and reading it as though it did cost three coins of every measurement: inv. 67.** This invariant is about an ASSET, where a host's answer may not revoke a declaration; a record of what a FETCH DID is about an artifact, where the declaration is the one thing that must not be trusted, because the fetcher is free to disagree with it and does. **What the note cannot do is stay informative once the declaration stops implying an absent market:** two of the five declared assets were declared for the owner's own reason, so `run.note` may name them every run, and a line that fires daily is a label rather than an alarm. The invariant is unchanged — the note must still fire, and silence would be worse — but reading it as «something is wrong» is now the reader's error and is recorded as such in §10.
42. **A bench must execute production with the SAME external input as production.** Three board benches ran the board with an empty `CATALYSTS` for eight days because the sandbox has no `XMLHttpRequest`: the loader failed silently and the benches reproduced a configuration that exists neither for the Boss nor on Pages. Therefore: the registry is read from the checkout by the SAME loader as production (inv. 21), injection happens AFTER `vm.runInContext` (otherwise the production line `var CATALYSTS = {}` overwrites it), and a missing or corrupt file fails the bench NON-ZERO — there is no fallback to an empty registry.
43. **A check count must be a count.** The number a bench prints as «checks» is used as proof of control volume and as the input to inv. 22, so it must count comparisons, not be estimated as a product of unrelated quantities. The counter is incremented at the comparison site, the gate total is the sum of those counters, and any discrepancy is explained term by term. A quantity that is merely measured and printed — scenarios, rows, lists — is not a check.
44. **A fetch may stand behind a product fact only if anyone can reproduce it; a session fetch cannot.** The earlier form of this invariant said external data is fetched on a runner and never in an implementation session, and gave reachability as the reason: an Executor session refused every market host at CONNECT. **That measurement no longer reproduces** — TZ-20 reached four hosts from the VPS and read 200 on all four — and a rule resting on a measurement falls with it (inv. 52). What survives is a rule about STANDING, not about reach. A runner fetch is recorded, repeatable by anyone holding the repository, and its inputs are named in a workflow file; a session fetch is none of those, because the session ends, the market moves, and the only trace is a sentence in a report. Therefore: **forbidden in a session** — fetching an external FACT that enters the product (a price, a date, a figure, an event) as the standing behind it; such a stage is specified as a workflow step and nothing else, and a TZ asking for it in-session is blocked before it starts. **A program in this repository that a VPS unit runs, and whose output that unit commits, has the same standing** (contract v24, §7 item 9): its code is named in the repository, its output is committed beside that code, and anyone holding the repository can run it again — which is more than the Shortcut's payload has ever offered, its producer being code nobody here can read. A session running the same code by hand does not acquire it. **Permitted in a session** — measuring the session's OWN ENVIRONMENT (egress, tool availability, host reachability), because the artifact IS the measurement, the command is recorded beside its result, and re-running the command is the reproduction; this class produces no product fact. **A CI figure is two artifacts and a validation item must say which one it wants.** Per-step CONCLUSIONS come from the jobs API and answer unauthenticated on a public repository; per-step CHECK COUNTS exist only in the log body, which answers `403 Must have admin rights to Repository` to a session holding no token. An item asking for a count off a run page is therefore unrunnable as written, and its answer is the owner's to read — TZ-35 §5.6 asked for exactly that and correctly returned a stated gap instead of substituting the local number. **That half no longer reproduces either, measured 17.09.2026**: TZ-50's session read the log body of three runs — 87 802, 89 096 and 86 511 bytes — and took step 4's and step 14's own counts out of it, including the negative control's `FAIL 1`. The 403 was a fact about a session holding no token, not about the endpoint, so this narrows rather than falls, in exactly the standing of the reachability clause above: **a validation item MAY ask for a runner count, and must say what to report if the read is refused** — and a figure the session could not read is still not one it may quietly replace with a local run's. TZ-10 Stage B remains the cautionary case for the first class: the instrument was correct, complete, self-tested — and returned no number. TZ-20 is the case for the second: reachability was asserted from an old measurement and was wrong.
45. **A differ returns zero on identical input.** Any comparison offered as no-regression evidence is first run with the SAME revision on both sides and must report zero differences, and a transformation applied to one side is applied to the other. `prot_bench.js`'s optional baseline suite strips one section from the candidate only, so it reports six failures against a byte-identical baseline — a stale expectation a self-comparison would have caught the day it was written. Identity is the known-answer control of a comparator (inv. 23); a comparator never proven on identity supports no claim about a real diff.
46. **A calibrated constant is checked against its calibration record.** A production number derived from a measurement lives in two places — the constant in the source and the committed output of the run that produced it — and a bench inside the gate compares them on every push. Inv. 23 fixes the rule before the data; this fixes the number to its run afterwards. A constant that agrees with nothing can be moved silently in either direction, and the move is invisible precisely because the number looks measured.
47. **A threshold is calibrated on the distribution of the quantity its consumer compares.** A constant thresholding a LIST MEDIAN is measured on the distribution of list medians, never on the distribution of the individual readings the median is taken over: averaging across correlated members strips idiosyncratic dispersion and moves the upper tail (driftless null at ρ = 0.75: coin-day p90 1.38, list-median p90 1.27). Inv. 46 pins a constant to its run; this pins it to the right random variable. A percentile measured on the wrong object looks fully calibrated and is wrong by exactly the amount nobody can see, and an admissibility window drawn around that object inherits the error.
48. **A bench that builds its own input proves the function, not the wiring.**
    Where a production function reads an object assembled somewhere else in
    production, at least one check must prove the assembling site supplies every
    field the reader takes: the fields read off the object are derived FROM THE
    SOURCE and compared against the fields the producer writes. `listExhaustion`
    was green in two gate steps on fixtures carrying `hi24`, `lo24` and `cur`
    while the live row object carried none of them, so the measure returned
    `n = 0` on every render and the board printed a caption claiming a coverage it
    never had. Inv. 42 makes a bench take production's EXTERNAL input; this makes
    it take production's INTERNAL shape. A green bench on invented input is
    evidence about arithmetic and never about reach.
49. **An admissibility band is derived from a null computed in the same run.**
    A band that decides whether a MEASUREMENT is plausible — «is this reading
    consistent with a quiet market, or is the pipeline broken» — is computed from a
    simulated null of the SAME statistic inside the run that produces the number,
    never written into the rule as a numeral. A hand-written band is a prior about
    the answer disguised as a control: TZ-11's `1.60 … 4.00` sat above the p95 of
    both relevant nulls and was ~15 % too high before any data existed, so a
    correct rule refused a correct number. Inv. 23 fixes the rule before the data;
    this says a rule carrying a numeral about the outcome is not yet a rule. A band
    stating what is WORTH acting on is a different object and may be written down
    (§3.10c's `IC ≥ 0.030` is one): the first is a fact about the measurement, the
    second is a decision about its value.
50. **A stated absence is a dependency of the thing it denies.** A caption, an
    on-screen sentence or a checklist clause asserting that some mechanism does
    NOT exist — «порога нет, сравнения нет», «no threshold word appears anywhere
    in the block» — is load-bearing text that turns false the moment the mechanism
    is built, and no bench comparing BEHAVIOUR catches it: such a bench measures
    the specification, while this is a claim ABOUT the specification. Therefore a TZ
    that builds a mechanism enumerates every place that currently denies it and
    either repairs them in the same TZ or records the contradiction together with
    the TZ that closes it. A denial that outlives its subject is the board
    contradicting itself in the reader's own language, two lines apart, and the
    reader has no way to tell which half is stale. TZ-14 adopted
    `DAY_RANGE_ABNORMAL`, printed «порог 1,39» in §3.17 and left the caption
    beneath it denying any threshold; the Executor was right to obey its file list
    and the specification was wrong to omit the sentence. **TZ-15 repaired it and
    supplied the general remedy:** a denial escapes the gate only while it is prose,
    so the sentence is asserted as one exact string beside a control that plants the
    old wording back and must fail. A stated absence nobody can plant and catch is
    not yet checked.

51. **A freshness check is two-sided, or it is not a freshness check.**
    `now − ts ≤ limit` is satisfied by every payload timestamped in the future, so a
    producer whose clock runs ahead delivers a stale snapshot that presents as fresh —
    the exact failure the check exists to prevent, arriving through the check itself
    and reported as a pass. An age window therefore has a floor as well as a ceiling,
    and the floor is the producer's plausible clock skew rather than zero: the phone
    that writes the payload and the machine that reads it are different clocks, and
    a hard zero would refuse healthy data every time they disagree by a second. The
    one-sided form is invisible in testing because every fixture a author writes is
    in the past.
52. **A filter is measured on the runner, never derived from the pattern.**
    Glob semantics differ between matchers on exactly the cases that matter, so a
    reading of a pattern is a hypothesis about a third party's code and never a fact
    about it. This entry exists because the Architect derived one and was wrong:
    `'**/*.md'` was declared unable to match a root-level file, an invariant was
    written on that reading, and a corrective TZ was issued — while the repository's
    own run history already showed three pushes of root-level Markdown, none of which
    started the bot. The pattern had always matched. **The evidence was older than the
    error and nobody had looked.** Therefore: any claim about a `paths` or
    `paths-ignore` entry is settled first against runner history for paths that have
    actually been pushed, and only where history is silent by evaluation against a
    changed-file list taken from `git diff --name-only` rather than typed — in **both**
    directions, with the pattern and without it, and against a control path that must
    still fire, since a filter matching everything also passes every «must not run»
    row. This is inv. 45 applied to a matcher, and inv. 23's known-answer discipline
    applied to a belief about someone else's implementation. Where two readings of a
    pattern disagree, the pattern is replaced by one that reads the same under both —
    `'**.md'` over `'**/*.md'` — because closing an ambiguity is a real gain even when
    the behaviour does not move. A `paths-ignore` list with no `paths` allow-list
    beside it still fires on every path nobody thought to name; that was `main.yml`'s
    shape until TZ-23 replaced it with an allow-list of two literal paths, and the
    literals are deliberate — a glob is a hypothesis about a third party's matcher,
    two exact strings compare equal or they do not.
53. **A control is not wired until the trigger that reaches it has been measured.**
    Inv. 37 says a bench outside the gate is not a control; this says a bench inside the
    gate is not one either while the trigger excludes the commits that would exercise it.
    `analyst/live-gate.sh` was step 13 of a green gate and sat under an ignore written for
    the analyst's DATA, so a commit changing only the gate script started nothing — the
    control existed, was wired, was green, and could not be reached by the one change it
    exists to judge. The failure is invisible by construction, because the thing that would
    have complained is the workflow that does not run. **An exclusion is written for a class
    of file, but it is applied to a path**, so whenever one is added or widened the question
    is not «is this data» but «does this path also hold a control». Proof is a real push
    carrying only that file (inv. 52), never a reading of the pattern. The converse is the
    price and is the right direction to fail in: a narrowed list must be extended whenever
    the writing set grows, and a forgotten entry costs runner minutes loudly instead of
    costing a control silently.
54. **An immutable record cannot contain the outcome of the action that stores it.**
    This binds every record the repository never reopens — the analyst's day log, a TZ
    implementation report under `CryptoReports/**`, any future artifact in that standing.
    Such a record is written, then committed, then pushed, so every sentence it
    carries about its own commit or push is a forecast of a step that has not run — and
    the first one written was wrong in the dangerous direction, declaring a push that had
    in fact succeeded to have failed. A reader of an immutable record cannot tell a
    forecast from a measurement inside it, and the record's whole value is that the
    distinction never has to be made. The remedy is not more care in wording: it is that
    the outcome belongs to the NEXT record, where it is history. This is inv. 38's
    immutability read forwards — a file that may not be corrected must not contain the
    class of statement most likely to need correcting.
    **It is enforced by the report template, not by care.** TZ-21 named this prohibition
    in its own §8 and the report violated it anyway, in the section that always carries
    that sentence — the second occurrence in two consecutive TZs. A clause an author must
    remember is not a control; a template with no such line is.

55. **A specification is checked against the text it must obey, never against memory of it.**
    Six defects across two consecutive TZs came from one mechanism: the Architect
    wrote a requirement from a correct recollection of a rule and a wrong recollection of
    its detail — an enum's members, an allow-list's host, a hard-floor clause, a count of
    entries. Each was caught downstream, which is the design working, and each cost a
    full Executor session. Therefore every TZ, before it ships, reads FROM THE REPOSITORY
    every constant, enum and allow-list it names and every hard-floor clause its stages
    touch, and quotes them into the TZ where the Executor can compare. Inv. 21 bans a
    second implementation of a rule; this bans a second recollection of one. The failure
    is invisible at authoring time by construction — a specification never runs, so
    nothing contradicts it until a session has been spent on it.
56. **A recorded state is not a current state unless it carries the date it was measured.**
    §10 is this system's own register of what is true, and a row in it is read as a fact
    about today. A row whose State rests on a MEASUREMENT — a host's answer, a machine's
    ceiling, a producer's output, a third party's behaviour — therefore carries the date
    and, where it exists, the time of that reading, inside the State cell. **A State with
    no date is a DECISION and may be read as standing; a State with a date is a READING
    and expires.** Before a dated row is repeated as current state it is re-measured, and
    the cost of re-measuring is exactly one command in every case that has arisen.
    Inv. 52 says a rule resting on a measurement falls with it; that was written about
    somebody else's matcher, and this says the same thing about this map's own rows. The
    failure it names has happened: the row recording a malformed `analyst/live.json` was
    written when it was true, was never re-measured, and was reported to the Boss as an
    active blocker while a valid payload sat one command away. **Nothing in a flat table
    distinguishes a fact from a fossil**, and the reader who is most likely to be misled
    is the author, because a row he wrote reads like a thing he knows.
57. **A verdict computed from a frozen measurement is dated, not timed, and no clock revokes it.**
    Where a process cannot take a SECOND measurement, re-deciding a question after time
    has passed uses the same evidence and can only lose: the second answer is not a
    check, it is the first answer with the confidence removed. A measurement expires; a
    verdict about a named minute does not — it is true of that minute or false of it,
    and the clock says nothing either way. **The remedy for an ageing verdict is
    disclosure, never deletion:** the moment is printed, the anchoring number is printed
    beside the claim, and the reader who can see the current number resolves it in a
    second. Where no reader can, the claim is not published at all — but that is a fact
    about who is reading, never about the clock. The analytical engine produced this
    twice in two days. `ANALYST-INSTRUCTIONS.md` revision `2026-09-01-a` moved a
    fifteen-minute ceiling off the LEVELS after it deleted seven computed setups, and
    left the same ceiling on the STATUS; on 01.09 that demoted the one live trade the run
    had correctly found, printed «сделок нет» above a table it had computed correctly,
    and asked the Boss for a fresh snapshot it did not need. **A ceiling moved to a
    smaller object is not a repair — it is the same rule costing less per occurrence**,
    and this one occurred on every thorough run, so it cost more. Inv. 56 says a recorded
    state expires; this says a recorded VERDICT does not, and confusing the two throws
    away work that was right.
58. **A rule that names an object without naming how to compute it has named nothing.**
    Such a clause is not ambiguous and does not read as ambiguous: it is correct, it is
    read correctly, and it is obeyed in good faith by a reader who must supply the missing
    computation and cannot know he supplied one. The four defects the 02.09 analysis run
    produced are one defect four times. «A settled DATE cannot expire for want of a
    re-read» named no test, so the run tested settledness by judgement and protected two
    unlock dates no primary had ever published. «The MD5 of the §6 + §6a text» named no
    span, so the run hashed the whole file, marked all eight discovery lanes stale on one
    unrelated revision and left four unopened — the exact outcome the clause beneath it
    forbids, arriving through the clause itself. «Reported in the same answer» named no
    artifact to compare against, so four closures were archived in silence. And «an
    analysis run never starts from a branch» named a checkout where it meant a tree, so a
    run that had brought its tree to `origin/main` correctly had to argue past the rule in
    its own log. **The remedy is dull by construction and that is the point:** name the
    field, name the command, name the artifact the check reads — `dclass`, `sed -n
    '/^## 6\./,/^## 7\./p'`, the diff of `items`, `git push origin HEAD:main`. Inv. 55
    bans a second recollection of a rule and inv. 52 bans a derivation of somebody else's
    behaviour; this bans a rule that requires either. **The failure is invisible to the
    author and to the reader alike** — the author knows the object he meant, and the
    reader has an object that fits, so nothing anywhere reports a disagreement until the
    two objects produce different answers on a live run.
59. **A standing decision is amended in the floor before it is amended in the code.**
    «No new coins» lived in four places — contract §7 item 3 as a HARD FLOOR, this map's
    inv. 2 and §1, and the Architect's canon — and TZ-25 amended it in its own text, which
    is the one move a hard floor exists to refuse. The Executor blocked, correctly, and the
    block cost a full session; the work then proceeded on a lift spoken in chat, so for two
    commits the repository carried a 30-coin universe against a contract and a map that
    both said 28. **The order is not ceremony, because the floor is what the NEXT TZ
    reads:** a specification arriving in that window is checked against a clause its own
    subject has already outlived, and nothing anywhere reports the disagreement — the
    fingerprint gate compares a revision string and cannot see that the sentence under it
    is retired. An owner decision that contradicts a hard floor therefore lands as a
    contract version and a map revision FIRST, and the TZ that consumes it cites those
    versions in its own gate. Inv. 55 bans writing a specification from a recollection of
    a rule; this bans writing one against a rule that is already gone. The cost of doing
    it in the wrong order is measured and it is two sessions and three disagreeing
    documents; the cost of doing it in the right order is one upload.
60. **An extraction manifest is a second description of production's call graph, and it is
    proved closed rather than maintained.** Inv. 21 makes cutting production code out of
    the source mandatory; nothing made the LIST of what to cut correct, and that list is a
    hand-written copy of a call graph the author does not own. Production splits one
    function into three, the list keeps naming one, and the failure is invisible in every
    direction an author looks: `node --check` passes, because a bundle missing a definition
    is syntactically valid and only referentially broken; the driver's per-row `catch`,
    which exists so an unscorable row yields `null` instead of killing the run, converts
    the reference error into a DATA value; and the run dies far downstream on a type error
    naming neither the function nor the file. **A build failure and a row failure must not
    share a channel, because one of them is data and the other is not.** Measured:
    `scoreCandidate` gained `qualityScore` and `scoreFinish`, `JS_FUNCS` did not, and
    `--selftest`, `--run` and `--regimes` were dead on `main` until a later TZ tripped over
    it — while this map's own §3.10 carried the same stale list in prose, which is why it
    now carries none. The remedy is a closure check at bundle-BUILD time, ahead of
    `node --check` and ahead of any row: references derived from the bundle's own text,
    compared against bundle + driver + one short explicit globals list, counted (inv. 22)
    and proved by a known-answer control that removes a name from each half and must raise
    (inv. 23).
61. **A control's bar names an object, and the object is derived from production at run
    time, never assumed by its author.** Inv. 49 says a band about a MEASUREMENT is
    computed from a null in the same run rather than written down as a numeral; this is
    the same rule where there is no null to simulate, and it reaches the two cases inv. 49
    does not: a bar quantified over a SET the product cannot populate, and a bar naming
    the POINT at which a limit is reached. Both shipped red in one TZ, and both were right
    about the world and wrong about the product. A monotonicity claim was registered across
    five grid points when production's own `RR_MIN` refuses the first on every coin, so the
    claim was unevaluable rather than false. A convergence claim was registered at a fixed
    horizon where escape still measures 0.154 against a bar of 0.05, so a correct resolver
    was refused by three times the numeral. **The repaired form asserts SHAPE and lets the
    data locate the point:** the admissible set is probed through the very production
    function that does the refusing, and the limit is asserted as a ladder — escape decays,
    the gap shrinks, the closed form falls inside the CI at the rung where escape has
    decayed — with no numeral naming a rung. The cost of getting this wrong is not only a
    specification cycle: a red control is indistinguishable from a product defect inside an
    immutable report, and the report outlives the bar.
62. **A workflow that runs only on demand is not a control over the files it reads.**
    Inv. 37 says a bench outside the gate is not a control, and inv. 53 says a bench inside
    it is not one while the trigger excludes the commits that would exercise it. This names
    the third case, where the trigger is CORRECT and the decay arrives from upstream.
    `backtest_bench.yml` is `workflow_dispatch` only and must be — it needs a three-year
    archive and a warm cache, which no push can pay for — while `backtest_bench.py` cuts
    its arithmetic out of `index.html` at every run, so any production TZ can retire it and
    the only thing that would complain runs when a human asks. It sat dead at step 2 of its
    own job for as long as nobody dispatched it, and the repository's evidence was a
    silence indistinguishable from health. **The remedy is that the coupling is asserted
    where something already runs, not that the workflow is re-triggered:** `calib.yml` is
    the same shape and already has it, because inv. 46's bench compares the constant to its
    record on every push, whereas this bench's only thread into the gate was a step that
    imports the module — which proves it imports, not that a bundle builds. **A manual
    workflow's silence is not evidence, and the interval over which it decayed is not
    recoverable afterwards.** **TZ-30 applied the remedy in the form this invariant names:**
    `bench/backtest_guard_bench.py` is gate step 14 and builds all four bundles on every
    push, so the coupling is now asserted where something already runs. The residual is
    named rather than closed — the step catches a stale CUT and not a stale RESULT (§3.10),
    so a production change to what a cut function COMPUTES still decays this bench silently
    until someone dispatches it.
63. **The archive is keyed by TICKER and production by CoinGecko id.**
    Inv. 10 says a rebrand keeps the id and moves the pair; this names what that costs the
    bench. `main.py` fetches by the id in `TOKENS`; `backtest_bench.py` fetches
    `<SYMBOL>USDT` ZIPs from `data.binance.vision`. An id survives a rebrand and a Binance
    pair does not, so the one event inv. 10 makes INVISIBLE to the product silently
    truncates the bench's history to the post-rename leg — and a shorter series raises
    nothing, it is a smaller sample that still answers. **The repair is a splice whose
    admissibility is ARITHMETIC and derived, never a table of trusted pairs (inv. 49):**
    the joint's own return is admitted only if it lies inside the hourly-return extremes
    the two legs themselves exhibit, taken between adjacent buckets, inside each leg
    separately — production's own gap rule, never measured across the joint being judged.
    Measured 05.09.2026 on the only two the list carries, and the rule did both of the
    things a rule must do. `TON → GRAM` ADMITTED: joint +0.0069 over 54 h against extremes
    [−0.1937; +0.0972] on 18 147 hourly pairs, and GRAM carries 18 149 h. `MKR → SKY`
    REFUSED: joint −1.0000 against [−0.1318; +0.0803] on 26 365 pairs — a redenomination,
    not a price move — and SKY enters on its 8 484 post-rename hours alone. **A refusal is
    a correct outcome and must READ as one:** the census reports the best attempt across
    legs, because a short-but-real spot leg falling through to a futures leg that does not
    exist for the symbol printed «0 rows» for a coin with 8 484 hours.
64. **A tail top-up must serve the instrument it tops up.**
    `data-api.binance.vision` carries a spot klines endpoint and no futures one (measured
    05.09.2026: `/api/v3/klines` 200, `/fapi/v1/klines` 404), and `fapi.binance.com` is
    banned from CI code by inv. 24. The top-up nevertheless called the SPOT endpoint for
    every series, so each `fut:true` archive was having roughly a day of SPOT candles welded
    onto its tail. **A wrong join fabricates a move that every downstream measure then
    measures**, and it is invisible in the one way that matters: a spliced tail looks exactly
    like a complete one, and the perps duly read 0.0–0.1 % missing while the spot pairs read
    a month. The top-up is now spot-only and a perpetual's tail deficit is PRINTED by the
    census instead. **The price of the repair is a number getting worse** — perps now show
    ~20 h of missing tail — and reaching the old figure again would require splicing the
    wrong instrument, which is what hard floor item 2 forbids. The top-up also stops at the
    last COMPLETE hour and never at `now`, or the hour in progress enters the series as an
    hourly close.
65. **A bar derived from the constant it judges moves with it.**
    Inv. 61 says a control's bar names an object and derives it from production at run time,
    because a bar written by hand names what the author assumed. This names the cost of
    obeying that rule all the way down: a check whose EXPECTATION is read from the very
    constant under test cannot fail when the constant is wrong — it recomputes itself and
    passes. **Measured 05.09.2026**: section D of the garrison read its expected failing set
    from `HARD_CLASSES` throughout, exactly as its specification required, and widening that
    constant to swallow `venue-basis` left the section green at 97 checks and 0 failures. A
    derived bar is therefore derived from a DIFFERENT authority than the thing it judges, or
    two constants are read against each other rather than one as the other's expectation:
    here, that every member of `HARD_CLASSES` is a class `CLASSES` can produce, and that the
    subset is PROPER — some class is still reference (§3.14). Both are facts another section
    of the map owns; neither is a restatement of the constant. **The narrowing direction is
    not covered by the same check and must be named where it is:** removing a class leaves
    the derived section green too, and what catches it is step 4's `verify_bench.py`, a
    different step with a different authority.
66. **A published level and the price it was computed at are one fact, and moving that price
    is a schema change everywhere the level is recorded.**
    TZ-33 moved production's publication price from `cur` to the anchor, correctly. Two
    instruments record what production publishes and neither moved with it, in two different
    ways and from one cause. The journal's `geo` became the anchored geometry under the same
    field names and the same shape, so every schema check, field census and leaf counter
    reads it as unchanged, while the `dec`/`inv` beside it now describe a stop the card did
    not print and the outcome layer resolves against that stop. `--target`'s production arm
    was moved on its ADMISSION leg and left on its RESOLUTION leg, so it counts the outcome
    of an entry production would not have taken. **Neither failure is visible by comparing
    shapes, and neither is visible to the instrument itself**, because an instrument records
    what it is pointed at and cannot see that its subject moved. Therefore a TZ that changes
    WHICH price a published number is computed at enumerates every recorder of that number
    and either re-points it in the same change or records the boundary together with the TZ
    that closes it — inv. 50's rule for a stated absence, applied to a stated MEANING.
    Where the records are immutable (inv. 38) the boundary is disclosed and never repaired,
    and it must be readable FROM THE RECORD: `fp{script,commit}` is what makes the journal's
    epoch recoverable, and a store without such a field cannot carry a meaning change at all.
    Inv. 20 bans one number living in two places; this bans one FIELD meaning two things.
67. **A declaration answers «what should this be»; an observation answers «what happened».
    Storing one where the reader needs the other is invisible to every schema check.**
    The archive fetcher tried two venues and kept the longer series, while the label it wrote
    into the cache was derived from `fut:true` — the declaration the loop already held before
    it fetched anything. The variable that knew which venue actually answered went out of
    scope unwritten, so the venue was recorded NOWHERE, and the reconciliation then granted
    its basis licence off the declaration: a coin silently cached on the perpetual measured a
    perp against a spot index and classed `unexplained`. Nothing about the document's shape
    was wrong; the field answered a different question from the one its reader was asking.
    **Inv. 41 is the same distinction from the other side and the two are not in tension:**
    for an ASSET in production the declaration is authoritative and a host's answer may not
    revoke it; for a RECORD OF WHAT A PROCESS DID the declaration is the one input that must
    not be trusted. Therefore a field recording an action names the variable that performed
    it, at the site that has it, and is never re-derived downstream from a declaration, a
    label or a filename — and where the observation is absent the reader refuses rather than
    defaulting, because a default in the reading direction rebuilds the defect one layer down.
68. **A negative control names which items must FLIP and which must NOT.**
    TZ-35's first cut placed its declaration fixture inside the directory `make_cache`
    empties, so every lane ran with nothing declared and every lane passed. The bench was
    green while asserting nothing about the only input it exists to vary — the exact failure
    a re-registration is most exposed to, because the red it replaces is the only evidence it
    was ever wired to anything. A control demanding merely «something goes red» would have
    shown three reds and looked correct. The specified control named a partition — one lane
    green, two red — the reading came back inverted, and the defect was located in one step.
    Therefore: a control that flips EVERYTHING has localised nothing, one that flips NOTHING
    has not run (inv. 45), and a control whose partition is not written into the TZ is not a
    control but a hope. This is inv. 23's known answer applied to a set rather than a value.

69. **An identity control names the WORLD in which the identity holds.**
    Where production made that identity false, the repair is a PARTITION and never a narrower
    comparison. Inv. 45 says a comparator is proven on identity before it is trusted on a
    diff. This says the identity has PRECONDITIONS, that they are part of the control, and
    that a control stating an unconditional identity converts the next legitimate production
    change into a report about itself. `--lab-selftest`'s D4 asserted that a substituted arm handed
    production's own target reproduces production's arm; TZ-33 gave production a second pass,
    `prod`'s geometry became the anchored one while the substituted arm stayed at `E`, and the
    claim became false on every waiting row — correctly, and with nothing to say about which
    of the two facts had changed. **The two repairs a red identity invites are both wrong.**
    Deleting the fields that moved is an assertion removed to make a bench pass (hard floor
    item 2), and it silently stops checking the leg that did NOT move — here the resolution
    leg, whose immobility is the whole claim `--target`'s additivity rests on. Retreating to
    the flag alone is weaker than what the run can prove: the live path still has a knowable
    answer. **The repaired form is a pair** — the identity re-asserted in the world where it
    holds, and a partition on the live path naming field by field what must differ and what
    must not, both populations non-zero (inv. 22, 68). The cost of leaving it red is set by
    inv. 62 rather than by the control: D4 stood red across two TZs because the only trigger
    that reaches it is a manual dispatch, so the repair also puts the control's CONSTRUCTION
    where something already runs.

70. **A transport failure is NOT an absence of data.**
    A reply is data whatever its status: `404` on a monthly ZIP means that month is not
    published, and the census counts it, refills from the dailies and says so. A request that
    never completed is a fact about the NETWORK, and merging the two is how a loud failure
    becomes a silent one. **Measured 09.09.2026**: `backtest_bench.yml` run #19 died at
    `--fetch` because `_vision_rows` calls `requests.get` with no handler, and one reset ended
    the download of thirty-one coins — loud, attributable, and it cost a dispatch.
    **The obvious repair is worse than the crash.** Catching the exception and counting the
    month absent writes a series short by exactly the hours the reset covered, and inv. 63
    already records what a short series does: it raises nothing, because it is a smaller sample
    that still answers. The repair is therefore THREE outcomes where the code has two —
    answered, absent, exhausted — with exhaustion failing the COIN, naming itself in the census,
    never reaching `_save` and never incrementing the counter that means «not in the archive».
    **Retries are bounded, the bound is stated where a reader meets it, and the seconds spent
    are printed**: an unbounded retry turns a black-holed host into a job that times out with
    nothing to show, and a policy nobody can see turns a slow host into an unexplained runtime.
    **A leg that never answered is evidence about nothing** (inv. 44), so it may not win a
    comparison against a leg that did — the one place this rule reaches arithmetic rather than
    reporting, and the place where a naive repair would silently truncate a series that
    production then measures.
    **The first implementation of this rule broke it, and where it broke is worth carrying
    here rather than only in a queue row.** TZ-38's `_http` sets its success flag before it
    parses the body, so a reply it could not READ returns as a reply that ARRIVED — and the
    fold that counts exhaustion reads exactly that flag. The rule therefore has a shape, not
    just a statement: **the outcome is decided after the LAST thing that can fail**, and a
    control that stubs the parse step so that it cannot fail is not a control over this rule
    (inv. 22). Measured 10.09.2026 offline; **closed by TZ-39, merged** — the outcome is now
    written at exactly two exits, success after the parse and failure after the ladder, and
    section H holds a fixture for every body a parse can meet. The parse failure joins the
    caught set by INHERITANCE (`JSONDecodeError` is a `RequestException` since `requests`
    2.27, unpinned in both workflows), which is a dependency nothing asserts (§10).

71. **A measurement that is not RETAINED was not taken, and a step that is not CONDITIONED
    does not run on the day it matters.**
    Two halves of one class, both measured on `backtest_bench.yml`, both invisible to every
    offline control. **Retention:** TZ-40's `--attrib` printed its whole reading into the job
    log while the artifact carried eighteen other files, so a measurement built over one TZ
    would have lived as long as a log page and then stopped existing. An instrument's output
    PATH is part of the instrument — the standing inv. 37 gives a harness, applied to a
    reading. **Conditioning:** a step placed after one that legitimately exits non-zero is
    SKIPPED by default, and `--verify` exits 1 on every `coverage` or `unexplained` class,
    which is precisely the run on which there is something to attribute. TZ-40 saw that for
    its own step and wrote `if: ${{ !cancelled() }}`; TZ-41 found `Деление по режиму BTC`
    in the same shadow, where it has sat directly behind `--verify` since before TZ-40 put
    `--attrib` between the two — so every run with something to attribute skipped the regime
    split as well, and no report ever said so. **`if:
    ${{ !cancelled() }}` is not `continue-on-error`**: the job still fails, which is the
    difference between taking a measurement and forgiving a failure. **This is upstream of
    inv. 62 rather than a case of it** — inv. 62 asks whether a control fires at all, this
    asks whether the run that fired it kept the answer, and whether the steps downstream of a
    legitimate red ever execute. Neither half can be caught by a bench: both live in the
    workflow, and the only instrument that reads them is a dispatch. **Retention was read
    13.09.2026** — `attrib.txt` came back inside the artifact — **and conditioning was read
    21.09.2026**: run #25's `--verify` exited 1 and both `--attrib` and `Деление по режиму BTC`
    executed behind it (§10).
    **The shadow has a second end, and it was read 17.09.2026.** A step that can legitimately
    fail also COSTS every unconditioned reading BEHIND it: `--regime-gate` sat at position 12
    of `backtest_bench.yml` under `bash -euo pipefail`, holding the one artifact that could
    never be written, so on every dispatch that asked for it `--res7`, `--funding`, `Прогон`
    and `Сверка` were skipped for a defect in none of them — one measurement failing cost
    four unrelated readings, and no report ever said so. TZ-50 moved it last before the
    artifact upload and gave it `inputs.regime_gate && !cancelled()`. **ORDER is therefore
    part of the instrument too:** the expensive step that can fail goes where nothing stands
    behind it, and a step's condition is decided by what stands behind it and not only by what
    stands in front. This third half is read by a dispatch like the other two, and the first
    one after the move, run #25, left `regime_gate` at its default `false`, so the step was
    skipped by its own input and the half is still unread (§10).

72. **A write that fails leaves this run's product or nothing — never a partial file and
    never the previous run's.** A reader cannot tell a stale complete file from a fresh one,
    and the stale one is the more convincing of the two, which makes the truncating write the
    MILDER failure: `regime_gate_raw.json` left 36 735 bytes ending `, "agree": {` on every
    run for as long as the mode existed, and a partial JSON in an artifact reads as data
    (inv. 70) but at least refuses to parse. The rule is therefore one writer per artifact
    class — serialise the whole object BEFORE touching the filesystem, write a temporary file
    beside the target, rename it over, and on any failure remove both and re-raise.
    **Removing the TARGET is the load-bearing half**, and it is the half the first attempt got
    wrong: truncate-then-serialise leaves an unparseable stub, while serialise-then-write
    leaves the previous run's complete artifact under this run's name. This binds every file a
    later reader treats as the current run's output — the bench's raw artifacts,
    `analyst/state.json`, and any future producer whose consumer runs minutes later and cannot
    ask when the bytes were written. **A control over it must write TWICE**, once succeeding
    and then once failing at the same path, because a first write into an empty directory
    cannot tell the two designs apart (inv. 22).

---

## 5. Limits

- **CoinGecko: the bot runs WITHOUT a key.** `main.yml` passes only `GIST_TOKEN`, so `api_key = None` → public access, no monthly quota, IP-rate-limited on the runner, handled by `REQUEST_GAP_SEC = 1.0` and three retries.
- **The free Demo key must NOT be attached at the current schedule.** Demo gives 100 calls/min but caps at 10 000/month; consumption is 17 runs/day × 32 calls ≈ 16 300/month plus `push`-triggered runs, and it rose by ~1 000/month when the universe reached 30. A Demo key would create a cut-off around the 18th–19th that does not exist today. Attach only together with a cut to ≤ 9 runs/day. **The keyless quota is the real ceiling on universe width:** each added coin costs 17 calls a day, so the list has room and the limit is worth naming before it binds rather than after.
- Binance spot ticker with `symbols`: weight 40, ~12 KB (full ticker: weight 80, ~1.2 MB).
- Binance `fapi/ticker/24hr?symbol=`: weight 1 × number of `fut:true` tokens, every 30 s.
- Gist API: files > 1 MB are truncated (handled through `raw_url`).
- Detection ceiling of the bench: |IC| ≈ 0.06–0.07 single test, ≈ 0.09 for a search (§3.10b).
- The day-range measure sees one day at a time and has no memory: it says how far
  the session has already gone, never where it goes next (§3.16, §3.17).
- **An implementation session reaches no market host at all** — archive, mirror, production and CoinGecko are all refused at CONNECT. Every fetch happens on a runner (inv. 44).

---

## 6. Release checklist

1. `python3 -m py_compile main.py`; `node --check` on the extracted `<script>`.
2. `debug.json`: every coin has `matched_90d > 120`, `returns_14d ≳ 300`, `error = null`.
3. Frontend: no NO DATA / NO BETA cards; Conf, ρ, МДЛ and both R² coloured; slider edges → `pred > 0`.
4. `fut:true` cards: price arrives, and the spot list does not contain them (ticker ~12 KB, not 1.2 MB).
5. Board: block order per §3.7; exactly one button lit per group; `notional` unchanged when switching МОНЕТЫ/USDT; a leverage change in coin mode moves margin, not quantity; funding shows both sum and % of margin; «ЦЕНА ВРЕМЕНИ» computes from the pressed button, not from the RESULT (inv. 14). Reference case (UNI, E = $10.00, 4X): 1000 USDT → notional $4000, 400 UNI; switch to coins → 400 UNI, margin $1000, same notional; `qty = 1000` → notional $10 000, margin $2500; at 2X margin $5000, notional unchanged. Funding +0.0100 %/8h at notional $11 110 → $23.33 per 7 days.
6. Board in SHORT mode: «ШОРТ СОЗРЕЕТ, КОГДА» shows `N / M` and both thresholds; absent entirely in LONG; on a `coeffs.json` without `eff14`/`r7`/`r30` the block disappears and the rest of the card lives.
7. Two-way compatibility (inv. 9).
8. `coeffs.json`: `btc` carries non-null `r7/r14/r30`; the frontend works on an OLD `coeffs.json` without them.
9. Frames: all board blocks and the hero show the metal ring; the two alarms keep red/amber borders WITHOUT metal; corner radii intact.
10. `res7` (§3.9): the `Своё 7д` line with its sigma on the card, visible in ОБЗОР; the board block inside «ПОЧЕМУ ЭТА МОНЕТА»; `market + own` reconciles with `r7` to the displayed digit; on a coin without 90d betas the block disappears and the card lives; at `sc = null` the section stays and says the score was not computed.
11. Direction engine: no coin carries both ЛОНГ and ШОРТ; a card with `action = 'none'` prints no entry or target; the glyph and the tier badge agree (inv. 33–35).
12. Catalyst layer: with the file served, the banner is absent and a `confirmed` entry vetoes the opposite side; with the file removed, the banner appears with a reason and the board keeps working (inv. 40).
13. Hard margin ceiling (§3.4): at `capped = true` the fourth row stays informational without the «← ограничитель» marker and the caption reads «Три независимых потолка…»; at `capped = false` it joins the list, can bind the RESULT, and the caption reads «Четыре…». Under no data does it produce «БЕЗ БЕЗОПАСНОГО ПЛЕЧА» (inv. 26).
14. Position protection (§3.11): the block is twelfth; break-even is further from entry when funding is «я плачу» and nearer when «мне платят»; with price at entry the status line says so; on a coin without `volatility` only the probabilities disappear.
15. «РИСК ВЫНОСА» (§3.17): the block is sixth, between «ВЫБОР ПЛЕЧА» and «РАЗМЕР
    ПОЗИЦИИ»; row 1 moves when the leverage BUTTON moves and not when the RESULT
    does (inv. 14); the list line names a coin count that matches the spot rows on
    screen, never zero; the threshold is named inside this block and nowhere else
    on the board or the card, and inside it only through the `dayStateNote`
    sentence and only when the day is abnormal; the caption denies no mechanism
    the block has AND states the ones it does — the derived unit, the object of the
    threshold, the inv. 27 words, the 25-coin spot coverage and the count of excluded
    futures assets — equal to its
    specification character for character (inv. 50, gate section M); the `.bd-sec`
    carries no inline `style`, so the metal ring survives (§3.7).
16. Regime symmetry (§3.12): a BTC week at `z ≥ +REG_STRESS_Z` prints «РЫНОК
    ПЕРЕГРЕТ» in red and no card is tradable on either side; at `z ≤ −REG_STRESS_Z`
    the wording is «СТРЕСС РЫНКА», also red; `dir` is 0 in both.
17. Row contract (§3.16): on a full board the §3.17 list line reads 25 coins, not
    zero; removing `highPrice` from one ticker drops it to 24 and changes nothing
    else; `lastPrice` / `highPrice` / `lowPrice` are parsed at exactly one site per
    field per row, and the only survivors elsewhere read `btcObj`.
18. Day state (§3.16, §3.17): on a list whose median reaches `DAY_RANGE_ABNORMAL`
    the amber sentence appears BOTH under the regime banner and inside «РИСК
    ВЫНОСА» and is byte-identical in the two places; on a quiet day and on a
    below-quorum list it appears in neither; the regime line's own bytes and colour
    are unchanged in every regime × side combination, so the `abnormal === false`
    banner is a strict prefix of the `abnormal === true` one; and the source
    literal equals `bench/exhaustion-calibration.txt` (inv. 46).

**Bench triggers.** Editing `verify_against_live` → run `bench/verify_bench.py`
(offline, ~20 s, must give 0 failures). Editing `scoreCandidate` **or anything
`scoreCandidate` calls**, `window_stats`, `window_vol` or `volume_expansion` → run
`bench/backtest_bench.py --selftest`. **That trigger is prose and has already been missed
once** — splitting `scoreCandidate` into `qualityScore` + `scoreFinish` was editing it, and
nothing fired (inv. 60, 62) — so the mechanical form is the closure check the bench now
runs at bundle-build time, and **since TZ-30 that check runs in the gate itself, at step 14**,
which leaves this line a human backstop for the RESULT and no longer for the cut.
Any production edit → the full `bench.yml` gate, 14 steps.

---

## 7. Deliberate simplifications

- Beta on simple returns ≈ log returns at an hourly step.
- Liquidation: one MMR = **1.25 %** for everyone, no tiers, no fees, no funding.
- Reaction buffer of 12 h — an estimate of how long a position may stand unattended (sleep, work). Not measured, chosen. It sets the structural ceiling directly: doubling `H_REACT` cuts leverage by about a quarter.
- Card range min/max is 90d; the invalidation reference is 30d with a 90d fallback.
- Funding in money uses the CURRENT rate extrapolated over `FUND_PAY_7D = 21` payments. The rate floats — this is an estimate, not an exchange commitment.
- One fee for everyone: `FEE_TAKER` = 0.05 % per leg, both legs taker, no VIP tiers, no BNB discount, no slippage. The error points to the safe side.
- BTC→alt lag is not modelled: hourly bars are coarser than the real lag. Revisit only on minute data.
- Alpha (the regression intercept) is not extrapolated — at 14d it is indistinguishable from zero.
- Unlocks are deliberately NOT automated in production: the board's registry is written by hand and vetoes only on a confirmed primary (§3.15, inv. 39). The analytical engine reads every coin's next cliff on every run since `ANALYST-INSTRUCTIONS.md` `2026-09-30-c`, and uses it only to close a long (§11).
- Liquidation probability (§3.3) assumes normality and constant volatility. Crypto tails are fatter and volatility clustering is unmodelled → **the true probability is higher than computed**; the figure is a LOWER BOUND. Measured at 7d and typical 2σ–6σ distances the same touch formula is honest and even conservative (measured/model 0.88, CI95 covers 1 on both sides); beyond the 6σ clip the far tail confirms the prior (3.5 % measured vs 0.9 % model on the long side). **Crediting the 0.88 into the calculation is REJECTED:** the CI covers 1, the understatement is explained by clustering (so the correction would break exactly in an expansion regime), and `touchProb` does not enter leverage at all — all four ceilings are distance-based.
- The backtest reconstructs 82.5 % of the long score and 86 % of the short: market-cap rank and Binance turnover are historically unavailable, so the quality block runs on `vol_ratio` alone, through production's own missing-field path (inv. 9). Both inputs move slowly across the list, so their contribution is close to a constant tilt. **`vol_ratio` itself has NO ARCHIVE ANALOGUE and therefore carries no threshold — it is reference-only in `--verify`.** Production builds it as `volume_expansion(c_data['total_volumes'])`, CoinGecko's composite turnover across every venue; the bench builds it from the archive's own Binance quote turnover. Two different turnover series, each divided by its own 90d median, give one scale-free ratio that is not a function of the other — so no bound derived from any price field can constrain it. Measured 05.09.2026: worst cell XMR **+317 %**, while `vol7` and `volatility` on the same coins sit under 3 %, and on synthetic data with identical prices and a substituted turnover series the derived bound is identically 0.000 % against a deviation of 134 %. **It is NOT `vol7 / volatility`** — that quotient is `volRegime` in the frontend, the §3.2 leverage cap, and is not a `coeffs.json` field at all. A TZ attaching a threshold here is attaching one to a quantity the archive cannot reproduce (inv. 49).
- **Backtest vs production reconciles on 29 of 30 coins — measured 21.09.2026, run #25, and the one refusal is the archive's own last bar (§10).** `--verify` compared 30 coins: 24 spot `clean`, TAO `unexplained` on `r7` (+1.748 pp against 1.50), five perpetuals `unverified` on their returns at +10.8 h with four level cells `venue-basis`. Worst spot cells: levels 1.50 % (TAO `max_price`, `max30`) against 2 %, `volatility` 1.91 % against 10 %, `vol7` 3.12 % against 25 %, returns 1.75 / 1.57 / 1.88 pp against 1.50 / 2.00 / 3.00, all on TAO. `--target` measured 29 coins with TAO out of its arms. The cell is production's 10:50 instant read at the archive's 11:00 close; since TZ-51, merged, the archive is read at production's instant, and no dispatch after the merge has been read (§10).
- **[SUPERSEDED 21.09.2026] Backtest vs production reconciles on 30 of 30 coins — measured 13.09.2026, and the reading below it is SUPERSEDED as current state (inv. 56).** `--verify` returned `unexplained` 0 and `coverage` 0 on 30 coins: 25 spot `clean`, five perpetuals `venue-basis`. Worst cells: levels ≤ 0.73 % against 2 %, `volatility` 2.30 % against 10 %, `vol7` 16.2 % against 25 %, returns ≤ 1.18 pp on spot against 1.50 / 2.00 / 3.00 pp. `--target` ran on 30 coins with none excluded, so the twelve-coin universe is retired. **The 09.09 reading below is not withdrawn — it happened — and it is no longer a description of the system**, because a phenomenon measured once is a property of that run until a second run reproduces it. What differs between the two is not separable here: the transport repair of TZ-39, a gap of −0.2 h against +0.8 h, and four days of market. The record of 09.09 follows, unaltered.
- **[SUPERSEDED 13.09.2026] Backtest vs production reconciles on 12 of 30 coins — measured 09.09.2026, and the mechanism TZ-34 repaired is REFUTED as the cause.** 35 cells on **eighteen** coins class `unexplained`, and that class removes a SYMBOL from `--target`'s arms rather than removing the run (§3.10), so every gated mode measured twelve; the ungated modes — `--run`, `--stops`, `--res7`, `--funding` — read the whole cache and measured thirty, which is why their figures are comparable to run #16's and `--target`'s is not (§3.10a). **Every one of the 35 cells is in the return family — `r7`, `r14`, `r30`, `eff14` — and not one is a level or a volatility.** Across the 25 spot coins the levels agree to **0.47 %** worst against a 2 % bar and `volatility` to 2.4 % against 10 %, while the returns miss by up to **+5.15 pp** and the sign is POSITIVE on 24 of 25. `eff14` is not a second cause: it is `r14 / (volatility·√336)`, and on the 23 spot cells where `eff14` moved enough to divide, the ratio Δ`r14`/Δ`eff14` reproduces that coin's own `volatility·√336` to within 2 % on sixteen, 3 % on nineteen and 11 % on all twenty-three — the residual being the quotient's second term, since `volatility` itself differs by up to 2.4 %. So 35 cells are **one quantity at four horizons**. The one spot coin whose return cells are all inside their thresholds is TRX, whose returns over every window are themselves near zero; what that implies about the cause is the specification's to establish, not this map's. The time gap was 0.8 h, inside the 3 h window, so the returns were compared rather than skipped. **The clause that stood here — that a larger gap would have hidden this — is FALSE, measured false 12.09.2026 by TZ-40 on a three-coin world**: `reconcile()` computes `over` with no reference to `skip`, so at a 30 h gap the run prints «НЕ СВЕРЯЛОСЬ» for the return fields and classes the same cells `unexplained` in the same output, exits 1 and removes the symbols from `--target`'s arms. The skip reaches the printed line and `never`, never the verdict, and it is one-sided at `gap > 3` (§10). **Both of those are retired by TZ-44** (§3.10): the refusal now reaches the verdict and the window is two-sided. A systematic sign is not noise and «everything else» is not a diagnosis; the attribution is reserved as a specification (§10). The superseded readings are run #16 — 30 of 30, zero `unexplained` — and 08.09's three coins. The 20 `venue-basis` cells stand and are reference: ARB `r7` +24.8 pp and `r30` +20.5 pp, LIT `r7` +13.0 pp and `r30` +11.5 pp, XMR `r14` −3.2 pp — all perpetuals, all reference by §3.14. **The archive is no longer the limiting factor**: 31 of 31 symbols cached with nothing lost to the network, 26 spot pairs at zero tail, five perpetuals at 21 h of tail because there is no futures mirror to top up from (inv. 64), and two interior gaps in the whole set — GRAM's 53 h at the rename joint and LIT's 17 h. The MKR → SKY splice was REFUSED on its own hourly extremes and SKY entered on its post-rename leg alone, which is inv. 63 working as specified.

---

## 8. Closed decisions — do not re-propose without a new argument

| Idea | Why it is closed |
|---|---|
| 5d beta / R² | SE(β) at 5d is ±17…31 % vs ±10…18 % at 14d — adds variance, not information |
| «Signal/noise» as its own number | identical to √(R²/(1−R²)) — a duplicate of the R² already displayed |
| Automating unlocks in PRODUCTION | the registry vetoes only on a confirmed primary (inv. 39), and a vesting dataset is not one; dates drift. A free source of the next cliff exists since 25.09.2026 — the coin page `ANALYST-INSTRUCTIONS.md` `2026-09-30-c` reads for the engine, subtractively (§11) — so what keeps this row closed is standing, not supply |
| TVL | applies to a quarter of the list, moves conviction over weeks — REVIEW material, not card material |
| Futures liquidity | on top Binance perps the Boss's size does not move the book; a dead market is caught by the detector |
| Token identity layer | over-engineering |
| Aurora animation | built and removed by the Boss: `mix-blend-mode: screen` on a dark theme raised grey, not colour, and two blurred 200 %×220 % layers at DPR 3 cost tens of MB of GPU texture |
| Global highlight of the «recommended» leverage button | the recommendation is per coin; a global button cannot express it |
| Liquidation heat map | no free source — vendor maps are models rebuilt from OI and price, and Binance `forceOrder` returns at most one liquidation per second per symbol. Squeezes live for hours; the Boss holds 1–14 days |
| «TP before SL» probability | without drift it equals `b/(a+b)` — identical to the risk/reward already in «ГРАНИЦЫ СДЕЛКИ». The system cannot estimate drift (§3.6), so the number would look like a measured edge without being one. **A calibrated EMPIRICAL rate is a different object and is not closed here** — the archive's own frequency of target before stop for a class of setup, printed with its sample size (§10, row «A probability per setup») |
| Spot/perp basis | `premiumIndex` already returns `markPrice` and `indexPrice`, but Binance computes mark price from the same premium index as funding: basis and funding are mechanically one quantity in two forms, and funding is already on the board |
| Tuning `scoreCandidate` weights | measured zero over 3 years and 28 coins at sufficient power. Turning weights against a null result is pure overfitting; the rule «never touch the weights» was registered before the run |
| Market regime as a scoring switch | ten of ten cells null at the doubled bar on a powerful split (51/50/41 dates, expansion 70/72). Expansion is already implemented where it is legitimate — in the risk ceilings §3.2 |
| CoinGecko as a bench source | free tier gives 365 days → 39 dates → resolves only \|IC\| ≳ 0.060. Fine for reconciliation, not for a test |
| **Open Interest — closed permanently, as signal AND as display** | (1) funding is the market-clearing PRICE of the same imbalance and is measured at zero with a tight CI, so the conditional probability that the quantity measure carries a signal the price does not is far below 10 %; (2) power: our sample resolves \|IC\| ≳ 0.06 and a plausible OI effect at 7–14d sits below that — a test without resolving power is not run; (3) the display «new money / position closing» rested entirely on future directional use. Reversed only by external evidence at an effect size our sample could resolve |
| Ranking by expected profit on capital ($1–2k) | reduces by identity to ranking by expected R-multiple; measured with a handicap favouring the hypothesis — IC −0.027 / +0.014 |
| Nonlinear factor-interaction layer | (1) the source locates the profit in small, illiquid coins — the complement of our list; (2) a 5×5 double sort needs ~20 coins per bucket and we have ~24 in total; (3) a family of 45–66 interactions needs a true \|IC\| ≈ 0.087–0.089, more than any effect ever measured here |
| Order flow / microstructure as a ranking factor | the published predictor is **world order flow** — one number per date, common to all coins, so its cross-sectional IC is identically zero. The quoted R² are contemporaneous, not predictive, and the data is a paid multi-venue aggregate |
| Cross-sectional term-futures basis | (a) perpetual basis = the premium index behind funding, measured zero; (b) the term contracts overlap our list on six coins, and a cross-section of six resolves only \|IC\| ≳ 0.18; (c) the factor decays exactly at our 7–14d horizon |
| ML rankers, GARCH, on-chain/TVL as ranking inputs | 28 coins × ~145 dates guarantee overfit; ±30 % vol forecast error sits inside one leverage step and is absorbed by rounding down; on-chain moves on a weekly scale and covers a quarter of the list |
| Literature momentum at a 7-14d horizon on a liquid cross-section | swept 02.09 against §3.10c's gate and it did not open. No published study carries a named IC on a liquid cross-section at 7–14 d: the strong horizon results (Dobrynskaya 57–70 % ann. at 1–2 wk hold) are measured on ~2 000 coins above $1 M cap — the small-cap tail §3.10b already names — and everything on a real liquidity screen reports t-stats or quintile spreads and no effect size. The practitioner spec closest to ours (30 d formation / 7 d hold, ≥ $5 M ADV) reports its own out-of-sample top quintile at −2.35 % ann. **The one study reporting IC in our units measured the same object we did and got the same answer:** ten Binance USDT perpetuals, rank-IC −0.010 … +0.024, the one nominally significant cell net-negative after costs, against our own [−0.006; +0.026]. Grobys & Shahzad 2026 additionally show crypto momentum portfolios have infinite return variance, so the t-statistics the positive half of that literature is built from are formally undefined |
| 7d/30d horizon switch | deliberate: scaling is manual (√H) and an extra control invites tuning the horizon to the desired leverage. Revisit if the holding period starts changing systematically |
| Recording the day-range reading in the journal | fully derivable at analysis time: the snapshot already carries `px.hi`, `px.lo`, `px.cur` and `cd.volatility`, so the coin-day ratio and the list median are reproduced by cutting production's own `dayRangeRatio` / `listExhaustion` (inv. 21) — the standing of `#N` (§3.13). Writing it would add bytes to the only unbounded artifact and create a second place for one number to be wrong. The analysis note that matters: the journal's `px.hi`/`px.lo` are the 13:00 UTC kline day, the board's are the rolling 24 h ticker |
| Whale and top-trader positioning as a direction signal | the positioning this system can measure was measured at zero (`--funding`, §3.10a) and open interest is closed permanently (the Open Interest row); on-chain whale flows have no free, labelled source. **The test itself is buildable:** `data.binance.vision` archives Binance's top-trader and taker ratios per perpetual — `futures/um/daily/metrics/BTCUSDT` answered 200 for 2022-06-01, 2024-01-01 and 2026-09-27 from the Architect's session on 28.09.2026 — so it opens exactly as any directional method does: an external prior naming an effect size this sample could resolve (§3.10b), then the bench, never a live signal first (`ANALYST-INSTRUCTIONS.md` §4) |

---

## 9. History

Removed. The migration log lived here until revision 2026-08-22-b; the record is
git history plus `CryptoReports/**`, both permanent and immutable. Nothing in this
map depends on it.

---

## 10. Open queue and gates

Each item states its trigger. Nothing here is scheduled work; an item is picked up
only when its trigger fires. Items with trigger «nothing» are recorded so that the
monthly audit stops rediscovering them.

**The State column carries a CLOSED vocabulary, and a measured state carries its date
(inv. 56).**

| State | Means | Dated |
|---|---|---|
| `open` | live work, nobody has done it | no |
| `watched` | known, deliberately not acted on | only if it rests on a reading |
| `closed by TZ-NN` / `closed by contract vNN` | done and in `main` | no — the TZ number is the date |
| `closed, deliberately` | decided not to do, permanently | no |
| `declared dead` | built or specified, will never land, retained as evidence | no |
| `withdrawn` | the claim behind it was false | no |
| `measured DD.MM.YYYY[Thh:mmZ]` | a reading of a host, machine or producer | **yes, always** |
| `not built, gated` | waits on a named external condition | no |
| `built, unmeasured` | the instrument exists and is self-tested; the measurement it was built to take has not been taken | no — but the row names what would take it |

**A `measured` row is re-measured before it is cited as current state**, and the reading
that replaces it replaces the date with it. A row carrying `measured` with no date, or a
reading whose date was never recorded, says so in the cell and is treated as unverified
until someone re-runs the command.

| Item | State | Trigger to act |
|---|---|---|
| Class-A coin channels had never been measured | **measured 15.09.2026T22:35–22:39Z by TZ-45 and 25.09.2026T11:09–11:23Z by TZ-52 — 27 of 30 coins served, on 35 rows** | a run recording one of the channels refused or landing on another host, which is the re-measurement. Methodology §6a (`ANALYST-INSTRUCTIONS.md` `2026-09-30-b`) names them with the one command form each was measured with: fourteen Discourse forums read at `/latest.json`, eleven release lists on `api.github.com`, one on `gitlab.com`, and nine site rows — RENDER's feed on `rendernetwork.medium.com`, the Ethereum Foundation's on `blog.ethereum.org`, and the seven TZ-52 read: SUI's blog feed, ADA's news feed, and the sitemaps of LINK, AAVE, SOL's news, XLM and ONDO — **35 rows for 27 coins**, ADA carrying three. SKY's forum left the table on its host's `robots.txt` (row «HYPE, LIT and SKY have no protocol channel»). Two rows land elsewhere — `forum.algorand.org` on `forum.algorand.co`, `www.stellar.org` on `stellar.org` — and the lane records the host that answered. **What TZ-52 read on the sites it did not admit:** NEAR's sitemap carries placeholder `lastmod`s under a comment saying so, with no feed and its Medium publication behind a challenge; ENA's, SKY's, HBAR's and ALGO's sites are dated and held nothing in their moves' windows; FET's, XMR's and ZEC's own feeds and sitemaps have been silent for months; XRP's post sitemap restamps its records; YFI's and BNB's sites stamp every page with one date and TAO's, RENDER's foundation's and LIT's carry none; ARB's answers a challenge; GRAM's, TRX's and BCH's answer 404 for a sitemap and advertise no feed; AVAX's index names no child the keyword rule selects; MORPHO's is dated and unscreened, its move then untaken; and Medium's platform index is no coin's channel, 0 of its URLs lying under any of the seven publication paths. **What was measured is a dated STREAM and not an event date:** each date field says when a record was made, and whether a channel carries class-A dates in its content was deliberately left unread. Two residuals are properties of the channels rather than defects: each read is one page, so a busy forum can outrun a weekly read and the methodology records the unread stretch instead of an absence; and the eleven GitHub lanes share one unauthenticated quota, 60 requests an hour as measured, so a refusal there is one refusal of all eleven. **A coin with no row costs no request**, so HYPE's unestablished candidate on that host is not a twelfth lane — TZ-46's own risk list counted it as one and the methodology says so in one clause |
| ETH and ADA are read on forums that do not date their upgrades | **closed by TZ-46 and `2026-09-16-c`** | a run recording either class-2 lane refused or landed elsewhere, which is the re-measurement; go-ethereum's release channel is unmeasured rather than negative, and a TZ naming it is the only thing that would establish it. **Measured 16.09.2026T09:23:06–09:23:17Z**, one request per candidate with TZ-45's own instrument: ETH answers on `blog.ethereum.org` with `pubDate` on every item of its one page — a 527 621 B page, the whole Foundation blog rather than an upgrade stream — and ADA on `IntersectMBO/cardano-node`'s release list with `published_at` on five of five, mixing versions and carrying `draft` and `prerelease` flags a consumer can filter. ETH's request to `/feed.xml` is answered at `/en/feed.xml` on the same host, which the methodology now names as no channel change, because the lane is recorded by the host that served the records and not the path. Original entry: class 2 probed for both with TZ-45's instrument. `ethereum-magicians.org` is where Ethereum's improvement proposals are argued and `forum.cardano.org` is Cardano's community forum; both answered with dated records and both are admitted and read, but neither is where the event that moves either coin is DATED — a network upgrade is scheduled and announced on a release channel. TZ-45's stop rule ended both coins at class 1, correctly, so class 2 was never requested. **Until TZ-46's reading is named in methodology §6a, both coins' upgrade dates arrive only through §6's type lanes** |
| HYPE, LIT and SKY have no protocol channel | **measured 15.09.2026T22:35–22:39Z by TZ-45 and 25.09.2026 by TZ-52 — ONDO left the row, SKY joined it** | a named candidate channel arriving as a TZ — for HYPE the unlock primary-source measurement is the likeliest carrier, LIT first needs the protocol behind its symbol established in this repository, and SKY's forum returns only if its host's `robots.txt` stops refusing this client. **ONDO has a channel since `2026-09-30-b`:** TZ-52's V2 read `ondo.finance/sitemap.xml` — declared in its own `robots.txt`, 198 URLs, dated across 167 days, a record on 16.09 before the move of 17.09 — while CoinGecko registers `ondo.foundation`, which serves nothing this client can read. **SKY:** `forum.sky.money` lands on `forum.skyeco.com`, whose `robots.txt` gives Google's crawler `Allow: /` and every other client `Disallow: /`, so the methodology removed the row; `sky.money/sitemap.xml` is dated and held nothing in the window of the 18.09 move. TZ-45's readings — ONDO: `forum.ondo.foundation` did not resolve, `blog.ondo.finance/rss/` landed on `ondo.finance` as a 404, and `eth.blockscout.com` answered the token contract keyless with state and no dated record — **the first reading of methodology §6's contract-state lane, and it dates nothing**, because a cliff lives in a vesting contract whose address is the protocol's own. HYPE: `hyperliquid-dex/node` releases answered an empty list, no forum is known, and the native asset of its own L1 has no token contract. LIT: no candidate in any protocol class, and **LIT = Lighter is the Executor's inference, backed by nothing in this repository**. At TZ-45's reading all three were served only by Binance's announcement list, which answered with dated records and carried no title naming any of them among its latest fifty per catalogue; the methodology names HYPE, LIT and SKY unserved on every run |
| Lane coverage counted a lane's activity | **closed by `ANALYST-INSTRUCTIONS.md` `2026-09-30-b` — the first run under it re-measures all thirty** | that run's `analyst/state.json`: every `coverage` record carrying the new `sec6_md5`, every `охвачена` naming its record by title and date. TZ-52 read the state as the engine wrote it on 24.09: 11 `охвачена`, 14 `неохваченная`, 5 `неизмерима`. **The test passed any record dated inside the window, so it measured activity:** NEAR stood `охвачена` by `gov.near.org`, the forum methodology §6a records as unable to carry NEAR's launch; AAVE on nine records in 48 hours; TAO on two releases a day apart; ZEC on a topic read outside its lane's page. 13 of the 14 `неохваченная` records carry no `carried_by`, which item 90 required. The five `неизмерима` were the declared perpetuals, for a move the structural file cannot hold (row «The five declared perpetuals have no structural row»). The status word stood `неизмеримо` in the methodology and `неизмерима` in the state, so an exact reader matched it in neither; the methodology adopted the state's form, which agrees with the other two. TZ-52's own screen took each move's day from the state, and its narrative put NEAR's on 17.09 against the state's 18.09; the move now has a named computation, so its day is one by definition |
| Sixteen §6a rows have no `robots.txt` reading of their path | **open** | the next TZ that measures a channel. Methodology §6 admits a channel only where its host's `robots.txt` permits its path (`2026-09-30-b`). TZ-52 read that permission for eight of the nine site rows — RENDER's Medium feed is the ninth — and `api.github.com` answered 404, which RFC 9309 reads as no restriction, for all eleven GitHub rows; the fourteen forum rows' `/latest.json`, RENDER's feed and BCH's `gitlab.com` row were never tested against their host's file, and nine of those hosts were never read at all: `gov.yearn.fi`, `gov.ethenafoundation.com`, `forum.cardano.org`, `ethereum-magicians.org`, `forum.bnbchain.org`, `forum.morpho.org`, `forum.arbitrum.foundation`, `rendernetwork.medium.com` and `gitlab.com`. **An untested permission is not a granted one**; one read per host closes the row |
| Class-S publishers of record answer this machine | **measured 25.09.2026 by TZ-52 — not admitted** | a lane form that reaches back a week, then an Architect edit. The Federal Register's API answered 200 with the twenty newest SEC documents, publication days 24.09 and 25.09 only — one page is a one-to-two-day window — carrying 2 «Longer Period» titles, 1 «Proceedings» and no crypto asset by name. SEC's full-text search refused the undeclared client 403 — «Your Request Originates from an Undeclared Automated Tool» — and answered a client declaring `crypto-auto` and a contact 200 JSON, 1 215 hits. **Neither is a lane at `2026-09-30-b`:** the measured register form is unfiltered and shorter than a lane's seven-day age, and SEC's declared client would carry the owner's contact into a public day log. Methodology §6a's re-sourcing already reaches the register for a regulatory proceeding whose own host refuses |
| Reporter feeds and Upbit's market list | **measured 25.09.2026 by TZ-52 — not admitted** | a rule that would consume either, which does not exist. CoinDesk, The Block, Decrypt and Cointelegraph answered 200 with 109 dated items over a union window of 48.46 h; 14 titles name a list coin, and of 15 naming a book base, 9 match only through word collisions. They are aggregators by methodology §6 and could only ever be discovery, which the per-coin search already is. Upbit's `market/all?isDetails=true` answered 855 markets, 289 `KRW-`, 23 of them list coins; no list coin carries `warning`, and GRAM, RENDER, ENA, LIT and MORPHO carry a `caution` flag. **A lane no rule reads is surface** |
| The Senate and `congress.gov` publishers refuse this machine | **measured 15.09.2026 — all five refused on the analysis run of that date; the time is in its day log and was not read here** | any egress change, and re-measure before citing this row as current (inv. 56). `dailypress.senate.gov`, `periodicalpress.senate.gov`, `democrats.senate.gov`, `lummis.senate.gov` and `congress.gov` refused in a row on a day whose one regulatory event — a cloture vote — was dated inside the run's own trading day. **Not a closed lane:** a public body publishes its own calendar, so the refusal is a fact about this client and the date does not stop existing. Methodology `2026-09-15-a` gave that case `dclass:'reported'`, admitted on two sources that are not aggregators of one another and purely subtractive, and a run never routes around the challenge. Same standing as `home.treasury.gov`'s row |
| The side of every trade rests on a fortnight threshold | **open** | a backtest TZ, and nothing in production before its reading. `marketRegime`'s `eff` decides the side on every list coin, and it is the fourteen-day return in units of the coin's own fortnight volatility — `r14 / (volatility·√336)`, signed — so it does point; what it cannot see is a climb smaller than `EFF_TREND` = 0.6 of that sigma, which reads `ДИАПАЗОН` while it climbs. Methodology can change how the engine USES the word — since `2026-09-18-a` it takes a coin's side from the coin's own regime at the frozen price and prints the market word as a risk tier (inv. 30) — and cannot change the threshold, which is production's. **The reading comes first and no repair is presumed:** §8 closes the regime as a scoring switch on ten null cells, hard floor item 1 closes `marketRegime` to edits without a completed backtest (§3.10b), and the instrument that takes the reading is `bench/backtest_bench.py` on the three-year archive |
| Per-trade sizing is declared in methodology §10 and delivered nowhere | **closed by `ANALYST-INSTRUCTIONS.md` `2026-09-30-e`; re-graded by `ANALYST-INSTRUCTIONS.md` `2026-10-01-a` and `analyst/owner.json` v3** | nothing on the rule; the values move by an owner decision or at the gate of row «The engine places no order on the exchange». **The owner declared 10 000 USDT and delegated the policy on 30.09.2026**, which removes the objection this row carried — a risk per trade chosen inside a methodology file is a tuned threshold about his money (inv. 49) — because the value is now his decision, delegated and recorded in his own file, and the methodology holds only the arithmetic. **On 01.10.2026 he asked that size follow the quality of the setup and not be restricted by default, so v3 sizes by the grade. The values and what derived them:** 1 % of capital on a `СИЛЬНАЯ` object and 0.5 % on a `СРЕДНЯЯ` one, halved where `ПОВЫШЕННЫЙ РИСК` prints — the grade is the engine's own statement of how much it knows (methodology §8), and 1 % is the professional ceiling for one discretionary trade on an engine with no demonstrated edge: the replay's −11.21 R drawdown of 28.09.2026 costs −5.6 % of capital at 0.5 % and −11.2 % at 1 %, so the full step is taken only where the run can name an edge; 3 % per side and 5 % for the book, because same-side rows on coins moving with the market are one bet (methodology §2) and the replay held 24 open at once — concentration is controlled by the budget, not by starving the row, and the budget spends in the answer's order, which ranks `СИЛЬНАЯ` first in every section; isolated margin at no more than 3×, under production's `L_CAP` and never above the `L` `leverageDecision` returns. **The grade is a definition and is measured next:** the scorecard reads `СИЛЬНАЯ` against `СРЕДНЯЯ` on outcomes, and a grade that does not separate them loses its size step. **The owner's half is his and is never printed:** the engine cannot know what he holds (owner's decision of 24.09.2026), so he counts his open positions against the same budgets; a day that costs 2 % of capital — two full-size stops — ends his new entries until the next day, a week that costs 5 % — one full book — halves his risk for the week after, and a 10 % fall from the account's peak — the replay's drawdown at 1 % — stops new entries until the scorecard has been read with the Architect. Original entry: methodology §10 read «Risk first: sizing from the stop» since the file existed and no section output a size — the answer printed the stop's distance in per cent and stopped there |
| The analyst's own-trend geometry has never met the archive | **open — recorded 19.09.2026** | a backtest TZ, and nothing in production before its reading. Since `ANALYST-INSTRUCTIONS.md` `2026-09-19-a` an own-trend pullback publishes a zone cut from the 24-hour extreme, a stop cut from the same extreme at `invalidationInfo`'s floor and a target at `RR_MIN` times that risk — a swing geometry scaled to the coin's own day — while the board keeps its 30-day stop. Measured 19.09 on the run's own rows: the 30-day stops sat 12–33 % from entry with a weekly touch probability under 1 %, the re-cut ones 2.0–12.7 % at about a third. **Its expectancy is unmeasured and nothing here forecasts it** (inv. 32, 54): the instrument is `bench/backtest_bench.py` on the three-year archive, and the reading decides whether the board adopts the geometry or the engine gives it back |
| The five declared perpetuals have no structural row | **open — measured 25.09.2026 by TZ-52: `fapi.binance.com` answers the Executor's machine** | an Architect decision on the source, then a TZ. The structural rows the engine reads are the bot's `analysis_data` rows, and the five `fut:true` assets carry none by construction (§3.14, inv. 41), so the engine builds no setup for five of the thirty coins — the assets the owner trades as perpetuals. The methodology carries the absence as declared coverage and never prints it as a gap, which is right for the answer and says nothing about whether the row should exist. **The source is the whole question:** the bot runs on a runner, where Binance production hosts answer 451 (inv. 24), and the futures archive's tail cannot be topped up from any mirror (inv. 64). **TZ-52 read the source a session can reach:** `fapi/v1/klines?symbol=<pair>&interval=1h&limit=3` answered 200 on all five pairs, three rows of twelve fields each, the last the forming hour. Methodology `2026-09-30-b` takes one thing from it — item 90's largest single-day move for the five, in the endpoint's daily form — and it stands behind no level: a session read is not a runner fetch (inv. 44) and a runner still answers 451 (inv. 24), so the structural row for SETUPS remains this row's open question |
| Unlock dates have no primary lane | **discovery half re-closed by `ANALYST-INSTRUCTIONS.md` `2026-10-08-a` on DefiLlama's `emissionsIndex`, measured 2026-10-08T05:27–05:29Z from the Architect's session; primary half open** | the first run under `2026-10-08-a`, whose read of the index is its measurement on the Executor's machine; a run recording the index refused, landing off its host or changed in shape re-opens this row whole. **`2026-10-08-a` names the replacement:** one read of the index for the list and the book, each coin's row matched by `gecko_id` to its CoinGecko id, the next cliff the earliest `unlockEvents[]` entry after the freeze with cliff allocations, its share over `circSupply`; and a refused read is no longer taken for a read — a book long on a refused or uncovered read waits on one unlock search (methodology §6a, item 104). Until then the trigger this row carried — a run recording the lane refused or landing off its host — fired on 07.10.2026. **The Executor's reading:** the first run under `-30-c` read `tokenomist.ai/<id>` for all thirty — 200 on every one, landing on the host — and returned seven `next`, fifteen `fully unlocked` and eight `not covered`, the Architect's reading of 25.09 to the coin. **The book stood outside it:** that run published two outside-list longs with no read and held five book cliffs on aggregators alone. Read the same day from the Architect's session, with a client that is not the Executor's, the dataset's pages give EIGEN's next cliff 01.10 to early contributors — the aggregators' date — OP's 11.10 against the aggregators' 30.09, PIXEL's 19.10, outside that run's window, and a 404 at `talus-network`; `2026-09-30-d` sends every outside-list candidate and every book cliff to the lane. **What the lane gives:** `tokenomist.ai/<id>`, `<id>` the CoinGecko id of `TOKENS`, answered 200 for all thirty; the site carries 22, and its served HTML states for seven the next cliff in one sentence — tokens, value, date, recipient and released supply — and for fifteen that the coin is fully unlocked; the eight it does not carry — XRP, GRAM, TRX, BCH, SKY, HBAR, XLM, XMR — answered with neither. The methodology treats the sentence as `reported`: it closes a long, prints `НЕ ПОДТВЕРЖДЕНО`, and backs no level. **What stays open is the primary:** a published date, `XXX до ДД.ММ` and a short resting on a cliff still need the protocol's own schedule, read per material cliff as a lookup, and the one contract-state reading taken — TZ-45's, on ONDO — dates nothing, because a cliff lives in a vesting contract whose address is the protocol's own. **This is the engine's rule, not the calculator's:** §8's closure of automating unlocks stands for production. **Re-opened whole on 07.10.2026:** the run of 07.10 requested forty ids at 19:11:44Z, and every page and `robots.txt` answered 403 with the host's refusal of automated access, naming its paid API instead, so every cliff of the list and the book went unread — and that run published three outside-list longs, NMR, ORCA and MOVR, sized and levered, with no cliff read. Whether §6a's «read before it can be published» admits a refused read is the question of that run's audit; the replacement is the next revision's, and DefiLlama's datasets are the one candidate measured (row «DefiLlama's unlock datasets are a second vesting source nobody has measured from the Executor's machine») |
| The mover search asked about the wrong day | **closed by `ANALYST-INSTRUCTIONS.md` `2026-09-30-d`** | the first run under it whose list mover has a cause, read with item 105: whether the search pair found it or the methodology's own text did. Measured 26.09.2026, 12:27 Tbilisi: «ethena news 26 September 2026» — `-30-c`'s named form, the freeze's UTC day — returned a market wrap while Ethena's own post was dated 25.09 11:00:27Z, fifteen and a half of the twenty-four hours before the freeze lying on that day; the cause reached the answer through `-30-c`'s own header, and «sky news 26 September 2026» returned astronomy. Item 98 now names two queries, the freeze's day and the one before, each carrying the project and the ticker |
| `bls.gov` dates the week's largest print and refuses this machine | **open — measured 26.09.2026 from the Architect's session** | a report-only TZ measuring a primary route to the issuer's release schedule from the Executor's machine, then an Architect edit. The Architect's session — a client that is not the Executor's — read `bls.gov/schedule/2026/10_sched_list.htm`: «Friday, October 2, 2026 · 08:30 AM · Employment Situation for September 2026», and `bea.gov/news/schedule`: personal income and outlays and the third GDP estimate at 30.09 08:30. The engine's `curl` has met 403 on `bls.gov`'s pages since before 20.09 (§11), and the run of 26.09 held the date at `none` behind the host's backoff, so the September employment report reached a book of seventeen same-side longs in no form. `2026-09-30-d` prints such a date at `reported` on two independent calendars, and it stays `НЕ ПОДТВЕРЖДЕНО` until a primary route is measured. **A client that declares itself is the likeliest route and the one this map already declined once** — SEC answered a declared client, and the declaration would carry the owner's contact into a public log (row «Class-S publishers of record answer this machine») |
| Six objections of the run of 26.09.2026 are unruled | **open — recorded 26.09.2026** | the next engine audit. That run's appendix raised seven; `2026-09-30-d` rules the first, the XRP escrow. The six: §2's «median of c» against §3B's list median — +0.13 with BTC, +0.30 without; `ИЗБЕГАТЬ` against «produces nothing» for a coin in its own range; the order of `ИТОГ`'s `ЖДАТЬ` field when the table has waiting rows and `СОЗРЕВАЕТ` is empty; filter 3 read as refusing a token with no protocol; no turnover floor for a list row — YFI at $2.8M of turnover was removed only by item 86; and a table key that ranks by stop width, because every target is `RR_MIN` times its stop — NEAR and UNI at −13 % stood first. **The last is a question about the book and not about a rule**, which is the class the audit reads |
| Unlock materiality is a decision, not a measurement | **open — recorded 26.09.2026** | a backtest TZ, and nothing in the methodology moves before its reading. `ANALYST-INSTRUCTIONS.md` `2026-09-30-c` closes a long on a cliff of at least 1.0 % of released supply inside the holding window — a line drawn in the gap the seven cliffs of 25.09.2026 left between routine monthly releases (FET 0.11 %, AVAX 0.30 %, SUI 0.32 %, ENA 0.45 %) and insider cliffs (ARB 1.56 %, HYPE 2.09 %, ONDO 36.4 %). **Nobody has measured whether a cliff of either size moves a coin of this list inside a week** (inv. 32, 49). The parts of the instrument exist: DefiLlama's datasets carry dated historical cliffs with tokens per allocation (row below), and `bench/backtest_bench.py` carries three years of the list's prices. The reading is each coin's move against BTC over the seven days before and after its cliffs, by size, against a null of the same coins on dates with no cliff |
| DefiLlama's unlock datasets are a second vesting source nobody has measured from the Executor's machine | **admitted by `ANALYST-INSTRUCTIONS.md` `2026-10-08-a` as the unlock lane's one source — `emissionsIndex` measured 2026-10-08T05:27–05:29Z from the Architect's session; the Executor's machine measures it on the first run under that revision** | a report-only TZ reading them from the Executor's machine, then an Architect edit naming them as the second source beside the coin page. `defillama-datasets.llama.fi/emissionsProtocolsList` answered 200 with 372 names and `/emissions/<name>` 200 keyless JSON — dated cliff and linear events with tokens per allocation, each document carrying its own `gecko_id`; `api.llama.fi/emissions` answered 402. Against the coin pages on 25.09: ARB's 92 645 833 tokens agree to the token, dated 15.10 against 16.10 — a day boundary; SUI's 01.10 and its early-contributor recipient agree while the tokens do not, 7 368 013 against 13 260 415; AVAX's date disagrees, 24.10 against 08.11. It carries GRAM (`ton`), TRX, HBAR and SKY, which the coin pages do not, and not FET, which they do. **A second source that disagrees is worth more than a second copy that agrees**, and AVAX's pair is the case a single dataset cannot see. **Measured again 08.10.2026 from the Architect's session, and the second source became the only one:** the coin pages refuse this machine since 07.10, and `emissionsIndex` answered 200 with 22 325 402 bytes and 370 rows, each carrying `gecko_id`, `circSupply` and the whole `unlockEvents[]` — one read for every coin, where the per-protocol documents run 0.4–3.6 MB each and are named by slug rather than by id; `robots.txt` 404. It carries 20 of the 30 ids of `TOKENS` — six with a cliff ahead, ARB 15.10 1.32 %, GRAM 23.10 1.19 %, AVAX 24.10 0.38 %, SUI 31.10 0.05 %, MORPHO 20.11 0.15 % and ONDO 17.01.2027 35.1 %, and fourteen with none, HYPE's monthly cliffs among them recorded only once paid. Parsed whole it took 108 MB in Python and 52 MB row by row, which is why the methodology parses it row by row inside the run unit's memory ceiling |
| TZ-33 moved the publication price and two recorders did not follow | **closed by TZ-36, merged** | nothing. Both sites moved and inv. 66 is satisfied: the journal records `anchor`/`decA`/`invA` beside `dec`/`inv` and resolves outcomes through `ssrc`, and `--target` carries `prod_anchor` beside `prod`. **The `prod_anchor` archive reading is OUTSTANDING and is its own row.** Original entry: One cause, two sites (inv. 66). `journal/write.js` records `geo` as the anchored object while `dec`/`inv` stay at `cur`, so a waiting row's stored stop is not the stop the card printed and the outcome layer times its touch against it — and the record is immutable, so **every 13:00 UTC run adds another one while this waits**. `bench/backtest_bench.py`'s `--target` production arm is admitted at the anchor and resolved at `E`; the repair there is a second arm, never a moved reference leg, because that leg is shared with the substituted arms. The journal is the primary and the arm is additive. **First read of that TZ:** whether the writer passes `btcStats` into `directionVerdict`'s fourteenth parameter — a thirteen-argument call drops the BTC ceiling out of the anchored decision only, which is invisible on every `СЕЙЧАС` row. **It also closes §0's open attribution for free:** it opens the journal, so it can count the side blocks carrying `wait !== null` and say whether that number is the 2 059 leaves step 7 lost |
| `--lab-selftest`'s D4 has been red since TZ-33 | **closed by TZ-37, merged** | nothing. D4 is the pair `D4a`/`D4b`, its construction is the named `d4_partition` and gate step 14 section G calls it on every push; run #19's step 8 read the lab GREEN on a runner, which is the first push-independent confirmation (§3.10a). Original entry: the reading is taken and the repair is specified. The control asserts an unconditional identity between `prod` and `ident`, TZ-33 made `prod` two-pass, and the claim is now false on every waiting row and true on every other (§3.10a, inv. 69). **The lab has printed «НЕИСПРАВНА — результатам не верить» on every dispatch for two TZs and no push could say so**, because `--lab-selftest` runs only under `backtest_bench.yml` — inv. 62 with the trigger correct and the decay arriving from upstream. TZ-37 re-registers D4 as an anchor-off identity plus a live partition and puts the partition's CONSTRUCTION into gate step 14, where something already runs. **A red control is indistinguishable from a product defect inside an immutable report** (inv. 61), and this one has been quoted as «the lab is broken» once already |
| `prod_anchor` has no archive figure | **closed — measured 09.09.2026** | nothing on the figure; the universe it was taken on is the row two below. The arm read LONG `Ω` 0.036 [0.010; 0.074] on 619 filled of 714, SHORT 0.006 [0.000; 0.020] on 428 of 502, pooled 0.022 [0.008; 0.041] — every CI95 entirely below 0.50, and **the anchored arm is the WORSE of the two on both sides** (§3.10, §3.10a). Filling costs 13-15 % of the setups and two thirds of those that fill go nowhere inside the horizon. **The direction is the finding**: the arm admitted at the anchor and resolved at `cur` was counting entries production would not have taken, and counting them favourably, so TZ-36's pair repaired a bias and not a rounding. Original entry: the arm exists, is self-tested offline in `--lab-selftest` D8/D9 and in gate step 14 section F, and nothing is known or forecast about what it says on the archive (inv. 43, 44) |
| The bench's fetch layer has no transport handling | **closed by TZ-38, merged** | nothing on the shape; two residuals carry their own rows below. Six of seven `requests.get` sites had no handler and one reset ended the download of thirty-one coins; the repair is one helper `_http` returning a record, three outcomes where the code had two, a leg that aborts on first exhaustion, an exhausted leg that may not win a comparison, and a transport verdict that runs before `_save`. Gate step 14 section H asserts all three outcomes offline, 57 comparisons. **What is NOT closed is whether any of it has ever executed**: the dispatch of 09.09 lost no coin, and a repair whose only evidence is the absence of a failure has no reading of its own |
| `_http` reports a reply it could not READ as answered | **closed by TZ-39, merged** | nothing on the shape; two residuals below carry their own rows. `_http` set `ok` before `r.json()`, so a `want_json` call whose body did not parse returned `ok: True, status: None, json: None` after retrying to exhaustion, and `_tx_add` — which folds on `not ok` — counted an exhausted request as an answered one. The repair is an ORDERING and no new constant: each attempt holds `status` and `why` in locals, and only two exits write the record — success after the parse, failure after the ladder. A parse failure is now a failed ATTEMPT and rides the existing retry ladder; the body is parsed at `status == 200` alone, which is the status all three `want_json` callers already read `json` under, so a `404` served as text is answered once as a 404 instead of retried three times into `status: None`. Section H holds 107 comparisons over every body a parse can meet, and the negative control that restores TZ-38's ordering turns 13 of them red. **`fetch_cg`'s `TypeError` and `reconcile`'s `AttributeError` — the tracebacks TZ-38 §6 was written to remove — are gone by consequence**, each caller taking the exhaustion path it already had with no line added to any of them |
| `--fetch` prints its retry budget only when a coin died | **closed by TZ-39, merged** | the next `backtest_bench.yml` dispatch, which is what reads it. `fetch_prices` and `fetch_funding` now print the existing `связь исчерпана на N монет(ах): … — ретраи потратили S с из BUDGET` line once per pass, outside `if dead:` and before the `ok < 8` exit; the string, its arguments and `_http_spent()` are verbatim, so the edit is a dedent and moved no check count. **The dispatch of 09.09 is what this closes**: 31 of 31 with no line printed, and whether the transport layer spent one attempt per URL or three hundred seconds was unknowable — a constant whose consumption nobody can see is a constant nobody can move. **The wording is now wrong on the happy path and deliberately unchanged**: a clean pass prints «связь исчерпана на 0 монет(ах):  — ретраи потратили 0.0 с из 600», an alarm word over an empty list, and rewording it is a decision this map records rather than a defect TZ-39 was free to fix. **It also carries the TZ-38 row's residual**: the first dispatch to print a non-zero S is the first evidence that any of the transport layer has ever executed |
| The return family disagrees with production and the levels do not | **repaired by TZ-51, merged — the reading is the first dispatch after the merge** | that dispatch, read from its artifact. TZ-51 merged as pull request #42, merge commit `e8b8681`, and its report checked the inequality below against run #25's own `attrib.txt`: under the new reading TAO's three return cells read 0.000 pp. One `unexplained` cell, TAO `r7` +1.748 pp against 1.50, and `--attrib` places it inside the archive's own last bar: on `r7`, `r14` and `r30` alike production's value lies between the archive's value at its last close and the value the same window takes with the previous close at its end (Δ −1.748 / −1.571 / −1.881 pp against `T_end` −3.136 / −2.783 / −3.309). **The comparison read the archive at 11:00 for a production built at 10:50**, which is the one-bar sensitivity `--attrib`'s first reading measured on 13.09 (§0). TZ-51 reads the archive AT production's instant where it holds the bar that contains it, and moves no threshold, class or comparability rule. **What it does not reach is a positive gap** — production built after the archive's last close, the 09.09 shape at +0.8 h — where no bar holds production's instant and the reading stays at the last close (row «One dispatch reads production up to four times»). 09.09's 35 cells and 13.09's zero are both consistent with this mechanism and neither is re-read here: the first needed a positive gap on a moving market, the second a negative one on a quieter hour |
| One dispatch reads production up to four times | **open — recorded 22.09.2026** | a TZ on the reconciliation's acquisition path. `reconcile()` fetches the live `coeffs.json` itself, and `--target`, `--verify`, `--attrib` and `--regime-gate` each call it at their own instant, so a bot run landing between two of them gives one dispatch two productions — `--target`'s arm gate resting on one and `--verify`'s verdict on the other. On run #25 both classed TAO alike, and no divergence is established. **It also decides the sign of the gap**: the archive ends at the last complete hour before `--fetch`, and a reconciliation that runs after the bot's next publication reads production past that close, where TZ-51 has no bar to read at — the 09.09 shape. One snapshot per dispatch, taken beside the fetch, would give every reconciliation the same production and the archive's own bar to read it in whenever the fetch lands before the next publication; it is a new artifact under inv. 72 and a change to `verify_bench.py`'s stub, so it is its own TZ |
| The Architect's TZs have reached the Executor with defects it could have run | **open — recorded 22.09.2026** | the next revision of the Architect's canon. The owner reported it as a pattern: the Executor finds errors or inconsistencies in the specifications it receives. On TZ-51 the Architect's own second pass found five in its two files — a step order stated backwards, a revision string not in the contract's format, a validation grep a line wrap could break, wording a strict reading of contract §7 item 2 could block on, and two stale labels in this map — and no content assertion could have seen any of them, because each assertion checked that the text was the text intended. **The rule that closes the class is a run, not a reading**: before a TZ ships, the Architect executes it as the Executor will — the fingerprint gate against the map being delivered, the baseline, an implementation written from the TZ's text alone and never from the Architect's own reference, the checks inserted where the TZ says, every registered count and the negative control re-measured — and a TZ that has not survived that run is not deliverable. TZ-51 is the first specification that did |
| `venue-basis` holds a mixture the licence cannot separate | **open — measured 13.09.2026** | **TZ-44 removed one of the two mixtures and the row survives it**: a 20 h tail is a WINDOW fact and is no longer forgiven as a price-level one, proven by the L3 pair — the licence now keeps the LEVEL and loses the RETURN. What stays open is the mixture INSIDE the licence, which is per CELL while the licence is per SERIES, and no re-measurement of it exists after the merge. Original entry: the next TZ on `--verify`'s classifier; it belongs with the skip row below, because both are the same question about what a class is allowed to forgive. Nine cells took the licence and the attribution splits them differently one from another: ARB `r7` is Δ −8.241 pp with `T_start` −7.500, so the START INSTANT carries 91 % of the biggest cell of the run, while HYPE `r14` is Δ −2.035 with `T_start` −0.003 and ARB `r14` has a start term of +2.449 against a Δ of −1.220 — larger than the gap and the other way. **The licence is granted per SERIES and the deviation is per CELL**, so a cell whose gap is the perp's 9.8 h tail is forgiven under a name that says «basis». **No perp cell can be fully attributed until the tail closes**: `T_end` needs an archive bar at production's end instant and there is no futures mirror to top up from (inv. 64), which is why all 15 sit in the unattributed count |
| The retry ladder has still never been seen to fire | watched — **measured 21.09.2026, run #25: 0.0 s of 600 on both passes** | the first dispatch that prints a non-zero figure. TZ-39's line now prints on every pass — `связь исчерпана на 0 монет(ах):  — ретраи потратили 0.0 с из 600` on `--fetch` and on `--fetch-funding`, 31 of 31 coins cached, nothing lost — so the budget is visible and the reading is a zero. **A visible zero is worth more than the invisible number it replaced and is still not evidence that `_http`'s ladder has ever executed**: the same output follows from a run that needed no retry and from one whose retries the code never reaches. `HTTP_BUDGET_S` stays where TZ-38 derived it until a run spends some of it |
| The dispatch cache is frozen at 05.09 and every run refetches the universe | **open — measured 21.09.2026, run #25** | any TZ opening `backtest_bench.yml`. `actions/cache@v4` is keyed `bench-${{ inputs.source }}-${{ inputs.years }}y-v4`, and a cache is saved only when its key MISSES; the key has hit since the run that created it, so `bench/cache` is restored at documents ending **2026-09-05T20** on every dispatch and the run's own fetch is thrown away at the end of the job. Two consequences, visible in the 13.09 artifact and again in run #25's: every coin prints «площадка не записана — перекачка» and pays a full history download, which is TZ-34's venue observation being re-derived and re-discarded on every run; and the map's reading of 09.09 — «every cached document was refetched because none carried an observed venue» — was the same freeze rather than a one-off. **The freeze is not a correctness defect**: each run measures on the archive it just fetched. It costs a full refetch per dispatch and makes a permanent line look like a finding. **A repair of the KEY alone would freeze the ARCHIVE**, which is worse than the defect: `fetch_prices` refetches a cached document only when it records no venue and otherwise prints «уже в кэше» and moves on, so a cache that is actually saved would come back with an observed venue and never be topped up — every mode would measure on an archive ending at the previous dispatch, `--verify` would read the stale document's own stored census with its tail at 0 and name no coverage class, and the only symptoms would be returns going `unverified` and levels drifting as the gap grew. The freeze is what keeps each dispatch fresh today. The repair is the fetch path extending a cached document to the last complete hour, landing with the key change in one TZ that opens `bench/backtest_bench.py`'s fetch layer and `backtest_bench.yml` together; its value is runtime alone. Run #25 repeated the reading: 31 refetches, documents restored ending 2026-09-05T20 |
| Inv. 71's conditioning half has no reading | **closed — measured 21.09.2026, run #25** | nothing. Run #25's `--verify` exited 1 on one `unexplained` cell, and `attrib.txt` and `regimes.txt` are both in its artifact, complete: the two steps under `if: ${{ !cancelled() }}` executed behind a failed step, which is the reading this row reserved. Original entry: `attrib.txt` and `regimes.txt` were both in the 13.09 artifact, but that run's `--verify` was GREEN, so neither step had stood behind a failure. **A repair whose evidence is the absence of the failure it prevents has no reading of its own** (inv. 22, 43) — and this one now has one |
| `--attrib` has never met the archive | **closed — measured 13.09.2026** | nothing on the instrument; what it found opens the two rows below. 90 cells compared, 75 attributed, and the 15 unattributed are the perpetuals, whose end instant sits outside their own archive. **The instrument certified itself on the archive**: `eff14` reproduces with residual 0 on 30 of 30 coins and `f` derives two-point on 30 of 30 for `r7`, `r14` and `r30`, so it is executing production's own construction and not an imitation (inv. 21, 38). **Its first reading is a null and a sensitivity.** Δ on the spot set is under 1.2 pp everywhere, so there was nothing to attribute; the end-instant and start-instant terms nevertheless reach ±5.5 pp and cancel against the residual, which is the field's response to ONE bar of window shift and is the same order as the field's own threshold. `d_end` is still unavailable, so `d_start_implied` is still not net of it |
| `--verify` announces a skip and classes the same cells anyway | **closed by TZ-44, merged — read 21.09.2026, run #25** | nothing. The first dispatch after the merge read the repair on the archive: the five perpetuals at +10.8 h are `unverified`, their 20 return cells named under «НЕ СВЕРЯЛОСЬ» and compared nowhere, and all five are admitted to `--target`'s arms; the 25 spot coins at −0.2 h were compared per symbol. The decision shipped was comparability per symbol and per field before the class, `unverified` where nothing was compared, a two-sided window (§3.10). Pull request #39, implementation commit `99e4b0a`. The lane that proves the repair is L1: exit 1 with all three symbols out of the arms before, exit 0 with all three `unverified` after. **Original entry:** an Architect decision first, then a TZ; it is the one item between the attribution and a clean reading of it. `reconcile()` computes `over` with no reference to `skip` — `skip` feeds `never` and the printed line and nothing else. Measured on a three-coin world with BBB `r7` +5 pp: at −24 h and +0.5 h the cell classes `unexplained` and the run exits 1 with no skip announced; at +30 h the run prints «НЕ СВЕРЯЛОСЬ (разрыв во времени 30.0 ч): r7, r14, r30, eff14» **and classes BBB's `r7` `unexplained` in the same output**, exits 1, and removes the symbol from `--target`'s arms. `verify_bench.py` case 5 («big gap still exits 0») passes only because its big-gap world carries no disagreeing return — inv. 22, one layer inside a control that reads correct. **The skip is also one-sided**: it reads `gap > 3`, so an archive LATER than production is compared at any distance with no announcement at all. Two coherent behaviours exist — a skip that reaches the verdict, or an announcement that admits it is cosmetic — and which one is intended is not the Executor's to choose |
| A coin whose legs all ANSWER with no rows is reported as exhausted | **open — measured 12.09.2026 offline** | the next TZ on the fetch layer, or the first dispatch that prints it. `_fetch_best` sets `won_clean = bool(rows) and … exhausted == 0`, so an empty winner is «not clean» at zero exhausted requests; `fetch_prices` then takes the transport branch and prints «СВЯЗЬ ИСЧЕРПАНА: 0 запрос(ов) без ответа () — монета НЕ сохранена», appending the coin to `dead`. **This is inv. 70 merged in the OTHER direction** — an absence reported as a network failure — and the `НЕТ ДАННЫХ` branch below it is unreachable for `rows == []`. It did not fire on 09.09 (31 of 31); a newly listed or delisted pair fires it. TZ-39 left it deliberately, its own §7 closing that session to any caller that already had an exhaustion path, and TZ-39's budget line now puts it in a line every pass prints |
| Two `_http` callers read an ANSWER as a valid payload | open — measured 12.09.2026 offline | any TZ opening the fetch layer. `reconcile` checks `ok` and never `status`, so an answered non-200 gist reaches `live.get(...)` on `None` and raises `AttributeError`; `_rest_rows` validates no shape, so a 200 whose body is valid JSON of the wrong type raises `ValueError` inside its comprehension. Both are **the correct side of inv. 70** — a code error rather than a network verdict — and both end the fetch. Measured before and after TZ-39: the traceback is identical, and what its repair changed is that the 404 arrives as a 404 in one attempt instead of as `status: None` after three |
| `coeffs.json` publishes no end-of-window level | **open, unowned — measured 12.09.2026** | any TZ opening `main.py`; it is one field, not a project. `--attrib`'s `d_start_implied` follows from `log(1+r) = ln P(end) − ln P(start)` and is therefore `d_start − d_end`, printed as such with the absence on its own line rather than read as zero. `cur` is computed by the AST-cut block (§3.10), is in neither `CD_FIELDS` nor the published row, and recovering it inside the bench as `min + price_pos·(max − min)/100` is a second implementation of a production formula (inv. 21, 38). **The specification that needed it named it as an existing cell** — a specification is written against the repository, and this one was written against the map's own field list, which had carried `cur` since before it stopped being published |
| `backtest_bench.yml` carries a comment above the wrong step | open, unowned | any TZ opening that workflow. «Артефакт нужен именно тогда, когда что-то упало.» stands immediately above `Деление по режиму BTC` and describes the `upload-artifact` step's `if: always()` **three steps below it since TZ-50**, which moved the regime-gate step between the two and correctly left the comment alone — §4.4 authorised one move and one condition. Same class as `index.html:799` and `.gitignore`'s enumeration, and the same repair — move it or delete it, never a second copy (inv. 20) |
| A §0 anchor could not match, and was reported as matched | **re-opened — measured 16.09.2026 on TZ-46's gate; closed by contract v23** | nothing on the cut; the next gate is what reads it. **v22's closure was incomplete and the measurement is TZ-46's own gate script**: it read this block's anchor table and then filtered it through seven anchor NAMES, compared seven of seven correctly — the table held exactly those seven — and printed «anchors in map table: 7», which is the height of its own filter and not of the table. **A list cut by the names it expects cannot see a row nobody told it about**, so the eighth anchor this block gains would be skipped silently and the gate would pass, which is the direction v22 exists to remove. v23 makes step 2 cut by the table's rows and print the table's own row count beside the number compared, and this block no longer restates that count in prose. **Previous entry, closed by v22:** the Architect side is the anchor rule in §0, the Executor side contract §5 step 2, which takes its list from this block's table, BLOCKS a header that omits an anchor and records the text each match returned instead of a verdict. **The trigger this row carried was missed once** — v21 was a contract edit for another reason and carried none of it — so a trigger naming «the next edit» of a file is a reminder only while that edit's author reads the row. **The second instance arrived before the repair did:** TZ-45's header quoted the revision and the file table and none of the six content anchors, and the gate as written could not see it, because it compared only what a header quoted. Original entry: the inv. 68 anchor at `2026-09-08-b` differed from the invariant in case alone (`flip`/`FLIP`, `not`/`NOT`), so an exact-substring match was impossible, and TZ-36's report nevertheless recorded all seven as present as exact substrings. **Either the comparison was case-insensitive or it was not performed, and both are worse than a mismatch**, because the fingerprint gate is the one control that runs BEFORE any work and its whole value is that it blocks. Anchors are now copied and verified as literal substrings here before publication; what is not yet written anywhere is that the Executor must report the MATCHED SUBSTRING and not the verdict |
| TZ-45's probe validation flag pattern is blind to the tool | **open** | an Architect decision in the next TZ that carries the pattern, then nothing else. The pattern exists to prove no `curl` in a channel probe carried a user-agent, header, proxy, cookie or retry flag, and it matches those flag letters wherever they appear: `grep -c`, `wc -c` and `git branch -a` are local counting reads and it flags all three. **TZ-46 therefore re-ran four local reads with long-form options so the report would scan clean**, disclosed as its Deviation 3 — the artifact was changed to satisfy the check, which is the shape a control must never have, even though nothing was hidden and no pattern was weakened. **The property is established by the instrument, not by the prose**: `probe.py` is quoted verbatim and matched by MD5, and every request came from it. Scoping the pattern to `curl` invocations tests the same property and stops forcing edits to prose that makes no request |
| `bench/backtest_guard_bench.py` has TWO sections lettered `E` | watched, deliberate | any TZ adding a section there, which chooses its letter from the FILE and never by counting. TZ-32's regime-gate section and TZ-34's venue-observation section share `E`, and only the second prints a section line, so the first is unlabelled in the gate's output. **Renaming is refused for the reason invariant numbers are never renumbered**: a section letter appears in the immutable report of the TZ that created it, and moving it makes that report unreadable against the file. Same class as the D7 collision TZ-36 hit in `--lab-selftest`, and the same repair — the next section is chosen deliberately and the collision is stated |
| `journal/write.js` cites `§4.1` four times and no document has a §4.1 | open, unowned | any TZ opening that file. The reference is to a superseded specification's own numbering, and `§` means this map everywhere else in the tree. Same class as `index.html:799` and `.gitignore`'s comment, and the same repair — **name the map section or delete the citation**, never invent a §4.1 to satisfy it |
| UNI, XLM and ZEC class `unexplained` | **closed — measured 09.09.2026; the mechanism is REFUTED as the cause and the finding is five times wider** | nothing on this row; the return-family row below replaces it. TZ-34's mechanism — an undeclared coin cached on the perpetual, its basis measured against a spot index — was repaired, every cached document was refetched with an observed venue, and the class did not go away: it grew from three coins to **eighteen, across 35 cells**. All eighteen are spot, so no venue argument reaches them. **Both branches this row wrote down were wrong, and that is what a dispatch is for**: the answer was neither «perp, so the arms return to 30» nor «spot, so one candidate is eliminated» — the candidate was eliminated and the population tripled in the same reading |
| Gate counters unread at revision `2026-09-08-a` | **closed 08.09.2026 — read on the runner** | nothing. Run #145 on `main` at `a76cecf` gave steps 4, 7 and 14 off the run page; §0 carries the new total and the two replaced terms. **The row closed on its own trigger — the next push — which is what a trigger costing nothing is for.** What it did NOT close is the attribution of step 7's −2 059, which moves to the TZ-36 row: a figure read is not a figure explained |
| The number TZ-34 was issued under had been used once already | **closed — recorded so the history reads** | nothing. `13ebbaf` added `CryptoTZ/TZ-34-futures-archive-census.md`, `96c88ab` deleted it and `b5757f9` added `TZ-34-fetched-venue-observed.md`: a different specification under the same number. No report ever carried the first, so it never executed and the number was free to reuse. **The reuse was legitimate and invisible**, which is the reason for this row — a reader finding `13ebbaf` in the log has nothing else to tell them why |
| `Bench gate` run #145 carries one unread annotation warning | **open** | the next time the run page is open. The run concluded `success` and the warning blocks nothing; it is recorded because an annotation nobody reads is a signal the gate is emitting into a void |
| Three specification defects in one cycle, all in TZs written here | **closed by inv. 67, 68 and the clause added to inv. 44** | nothing; the rules are the repair and an assurance about attention would not be one. **(1)** TZ-34's `Touches` list omitted `bench/verify_bench.py`, so a correct change turned gate step 4 red and cost a whole extra specification — a TZ that changes a classifier enumerates every bench asserting it, and negative assertions that cover only the STRINGS a change falsifies say nothing about the ASSERTIONS it falsifies. **(2)** TZ-34 §5.2.2 was unsatisfiable in one of its four cells, because the declaration legitimately decides the leg ORDER; the Executor held the legs fixed and varied the declaration, which is the separation the item existed to prove. **(3)** TZ-35 §5.6 asked for a runner CHECK COUNT, which no session can read — inv. 44. **All three were found by the Executor running the specification, none by the Architect reading it**, which is the argument for validation items that name their artifact and their source |
| Wide research universe (n = 120) | not built, gated — **gate probed 02.09.2026, did not open** | a named tier-1 hypothesis with external effect size ≥ 0.030 IC on a liquid cross-section at 7–14d (§3.10c). The probe was a full literature sweep of cross-sectional predictability in liquid perpetuals 2019–2026 and it returned nothing that clears all three conditions at once; §8 carries the reading and the one external IC that matched our own measurement. **A run never re-sweeps this on its own** — the gate opens on a hypothesis ARRIVING, never on another search for one, and re-probing a closed lane is the failure this repository exists to prevent |
| Regime hysteresis | not built | the Boss reports the regime label flapping between renders. Not built pre-emptively: a second trend constant on speculation violates inv. 20 |
| Continuation target for `tradeGeometry` | **measured 05.09.2026 — hypothesis withdrawn** (run #16); **confirmed 09.09.2026 on an independent twelve-coin universe, and again 13.09.2026 on the full 30** — LONG `Ω` 0.063 [0.029; 0.116] on 1 978 setups over 141 dates against a mean 1/RR of 0.208, SHORT 0.034 [0.010; 0.067] on 1 271 over 140, the anchored arm pooled 0.017 [0.008; 0.028] on 3 249 setups of which 2 775 filled; `P(никуда за 168ч)` 70.0 % on the long side, so the binding constraint is still truncation and not the target**; — `Ω(k)` still monotone, every rung's CI95 still under 0.50, `k*` still absent on both sides | nothing. Above quorum on both sides and on every reachable rung, every CI95 sits entirely below `1/RR_MIN = 0.50` and **no `k*` exists in the grid**: LONG 0.025 [0.010; 0.043] on the production extremum and 0.202 [0.118; 0.338] at the best continuation rung, SHORT 0.016 [0.002; 0.036] and 0.107 [0.041; 0.205]. §3.12's veto is now measured rather than argued. **Re-opened only by a change of holding period**, because the binding constraint is truncation at 168 h and not the choice of target (§3.10a D3, inv. 32). The arm behind it is the pre-TZ-33 single-pass one (§3.10) and the withdrawal is unaffected: no entry price shortens a horizon |
| Journal outcome layer at scale | running | nothing — h7/h14 files appear automatically 7 and 14 days after each snapshot |
| Journal storage growth | watched | ~73 KB/day. Act if the repository becomes unwieldy; records are immutable (inv. 38), so the answer is archival, never deletion |
| Catalyst registry content | live, one confirmed entry | analyst work, delivered as a TZ; entries never promoted to `confirmed` without a primary source (inv. 39) |
| The §3.17 caption's own couplings | live, deliberate | any TZ that rewrites the caption (gate section M2 fails until the bench moves with it), reopens the exhaustion veto (§3.16) or relists a `fut:true` asset on spot (§3.14) — each must move the sentence in the same change |
| Re-running the calibration | frozen, deliberately | nothing at present. `calib.yml`'s paths filter names `calib.yml` itself, so ANY edit to that workflow re-fires the whole 3-year run on the branch and commits a fresh record on a longer archive, which can move the p90 away from the adopted constant and turn the inv. 46 bench red. Editing it is a re-calibration, never a touch-up; the stale `(TZ-11 stage B)` in its hardcoded commit message stays until a TZ genuinely needs a new run |
| `calib.yml` commits the record only on a PASS | correct by design | nothing. The commit step has no `if: always()`, so a refused run leaves no repository record and only an artifact — a record pinning no constant would look authoritative and pin nothing |
| `badge_bench.js`, `clean_bench.py` unwired | deliberate, documented in `bench.yml`'s own header | nothing. Both are two-input differs needing a `before` file the repository does not carry: manual tools, not controls (inv. 37) |
| The closure check does not run inside `bench.yml` | **closed by TZ-30 — narrowed, not retired** | nothing on the cut; a dispatch is still what tests the result. Gate step 14 (`bench/backtest_guard_bench.py`, whose count is §0's) builds all four bundles on every push and asserts zero missing identifiers, so `_assert_js_closed` — the one check that catches a stale cut — now fires where something already runs. **TZ-29's wider gap is closed in the same step:** the coverage census, the derived splice rule and the `--target` arm gate were locked only by validation-time controls and by a harness that lived OUTSIDE the repository, and a harness not in the tree is not evidence for the next session (inv. 37); it is in the tree now. The residual is stated in inv. 62 and in §3.10 and is not this row: a stale RESULT still decays silently |
| `.gitignore`'s comment enumerates the bridge files | open, unowned | any TZ opening `.gitignore`. The RULE is the prefix `bench/_*` and covers `bench/_tgt_bridge.js` correctly; only the explanatory list is one name short. Same class as `index.html:799` and the same repair — **delete the enumeration**, do not synchronise it, or one list lives in two files (inv. 20) |
| Every raw artifact can carry bare `NaN` | watched — **measured 17.09.2026 on four files** | nothing. `target_raw.json` emits it when a pooled arm records zero stop touches; `regime_gate_raw.json` carried **27** such tokens on the world TZ-50 measured; `stops_raw.json` takes it wherever a pool has no finite `p` and wherever every bootstrap draw is refused; `run_raw.json` propagates it from a NaN `volatility`, which is truthy and survives the `or 1e-9` guard. Python's `json` reads them all back and strict parsers refuse them. **The convention is now one across four files and that is the reason not to touch it**: repairing one alone would create two (inv. 20), and refusing NaN outright would make two of them unwritable again — the defect TZ-50 removed |
| The moved regime-gate step has never run on a runner | **open — measured 21.09.2026, run #25** | the first dispatch with `regime_gate` ticked. Run #25 was the first dispatch after the merge and did not run the step: its condition is `inputs.regime_gate && !cancelled()`, `!cancelled()` held for `--attrib` and the regime split just before it, so the input stood at its default `false` and the step was skipped by its own input rather than by `Сверка`'s failure. The new position and condition therefore still stand on a parsed-YAML comparison and on nothing that has executed, and nothing here forecasts what the dispatch will show (inv. 54). **The same dispatch is also the first reader `regime_gate_raw.json` has ever had** |
| `run_raw.json` would now fail by ABSENCE on a numpy scalar in `r7` | **open** | the next TZ touching the bench's artifacts; TZ-50 §7 read it and was forbidden to repair it. `f_r7` is `cd["r7"]` passed through unchanged from `main.py`'s coeffs block, so its type is whatever production returns — every world TZ-50 built gave a Python `float`, and a numpy integer, boolean or `float32` there would raise inside `_dump_raw` and leave no file at all. Louder than the truncation it replaced, and still a lost reading. **The repair is a cast at the site that knows the type, never a converter at the write boundary**, which would launder exactly the class inv. 72 exists to surface |
| The repository is not web-readable from the Architect session | **open — measured 17.09.2026** | the Architect's canon, whose note recording the opposite is dated 16.09.2026 (inv. 56). A blob fetch needs a URL the session has already seen in a search result, and the search index does not carry `seahomebatumi-ai/crypto-auto`, so the route that settled «does this exist, and what does this passage say» did not answer at all. **The route that DID answer is the Boss's upload**: three files, two from the implementation branch and one from `main`, reproduced their report figures byte for byte — which the web route never could, since its extraction drops blank lines and indentation, so neither an MD5 nor an exact quote was ever available from it |
| D3b compares the first ladder rung to the last, and the ladder overshoots | watched | a growth of section D, or an archive short enough to thin the last rung. Measured gap 89.5 % → 41.1 % → 14.5 % → **0.0 %** → 17.2 %: convergence is at `m = 16` and `m = 32` walks back out as its sample falls to 622 setups over 51 dates. D3c is what locates the limit and it selects `m = 16`, so the bar holds comfortably today; the clause a shorter history could break is D3b, not the ladder |
| The closure check's blind spots | **open, unowned — the standing claim was falsified 05.09.2026** | an Architect judgement on widening the scan, which is a call about false positives and belongs in a TZ. It recognises three declaration forms — `function NAME(`, `var NAME`, declared parameters — and collects references in two, `NAME(` and an ALL-CAPS token. This row used to close on «no such name exists in any of the four bundles today», and TZ-30 measured otherwise: `JS_DRIVER` declares `var cachedFunding` and the score bundle genuinely reads it, but as `cachedFunding[sym]`, a property access neither pattern collects. **The real instance of the thing the check exists to catch is invisible to it**, and the direction is the unsafe one: an unrecognised DECLARATION raises loudly, an unrecognised REFERENCE passes silently. The same run measured `resolved ONLY by driver: []` on all four bundles — 45, 23, 14 and 116 references seen — so the driver half of the `known` set is load-bearing for nothing today and the check's driver arm has never fired |
| `_skip_to_matching_brace` could rewind on an unterminated block comment | **closed by TZ-28**, as a consequence rather than a request | nothing. `str.find("*/", …)` returns `−1`, so the scanner jumped to index 1 and rescanned the file from the top. A single shared description of string and comment traversal (inv. 20) cannot rewind or the stripper loops, so the factoring had to fix it; unreachable on any well-formed `index.html`, and the direction of the change is a stop where the old code could loop |
| `journal_bench.js` count is content-sensitive (§0) | watched; **774 130 since TZ-36**, and every delta attributed | the first step-7 delta that cannot be attributed field by field, or any TZ touching `journal/write.js`. The −2 059 that opened at TZ-33 is closed (§0) and it is the cautionary case: the map named a population, the population was wrong twice over, and only a per-path census closed it |
| `NaN% от входа` at `E ≤ 0` in «ГРАНИЦЫ СДЕЛКИ» | pre-existing, unreachable live | any TZ touching that block. `Math.abs(liqSel / E - 1)` at `E = 0` is `0/0`; entry price is never zero on a live board, so it buys a diff and no safety |
| Raw Cyrillic literal at `bench/prot_bench.js:177` | pre-existing, bench-only | any TZ editing that bench. It violates the ES5/escape rule the frontend keeps, in a file no browser loads |
| `prot_bench.js` optional baseline suite | repaired in TZ-11 — neither side stripped, unconditional identity run inside the default suite, comparison counter with a zero-comparison guard | nothing; inv. 45 is satisfied by the gate itself |
| Hosted gate evidence per TZ | watched — structural, not a reading | an Executor session cannot start GitHub Actions, so its 13-step table is a LOCAL measurement with the workflow's own step list. The hosted `Bench gate` fires on `pull_request` and on push to `claude/**` and `main` regardless, so the evidence exists; the audit reads it rather than taking the report's word |
| `bench.yml` Node 20 pin | watched — **measured, date unrecorded; re-measure before citing** | GitHub already forces the actions onto Node 24 with a warning. Act when a step fails or the whole gate can be re-run as the validation |
| `CryptoTZ/TZ-03-report-delivery.md` | never executed; declared dead by TZ-04 and retained as evidence, so no report exists by design | nothing — a specification without a report is never resurrected (contract §13) |
| Analyst engine transport | **closed by TZ-17**: no network path; the payload is a file in the tree, the gate exits non-zero on stale, short or corrupt input, step 13 holds it | nothing. Re-opened only by a fresh egress measurement (§11) |
| `live-gate.sh` check 3 is one-sided | **closed by TZ-18** | nothing. Window is `−120 … +900` s, both sides named in stderr, both constants single-site |
| `'**/*.md'` root-level claim | **withdrawn by TZ-18** | nothing. The claim was false: runner history shows three root-Markdown pushes and no bot run. `'**.md'` was adopted anyway, for the ambiguity, not for a repair (inv. 52) |
| `live-gate.sh` sits under `bench.yml`'s `analyst/**` ignore | **closed by TZ-19** | nothing. Proven on the runner: a push carrying only the script now starts the gate |
| `bench.yml`'s analyst ignore must grow with the written set | **closed — measured 06.09.2026 on the runner** | nothing. TZ-30 added `analyst/owner.json` to `paths-ignore` as an exact literal (inv. 52) and the proof inv. 53 demands has now been taken: a push carrying ONLY that file — one field of it, `updated` — started `pages build and deployment` and started **no** `Bench gate` at all. The two `.md` uploads that preceded it behaved the same way under `'**.md'`. **The reading is what closes this, not the literal:** an entry that has only been read as a pattern is exactly what inv. 53 refuses, and this row carried it as OWED for one revision on that ground. The original coupling stands for every file the analyst DOES write — a forgotten entry burns a gate per run, loud rather than silent |
| `analyst/live.json` producer emits a stray newline | **closed — measured 31.08.2026T10:03:40Z on a live payload** | nothing. The Shortcut no longer emits the raw LF inside the symbol list: a payload of `n:29` parses, `n == len(c)`, every `p`/`h`/`l` casts to a finite positive, no symbol carries whitespace, no duplicate. **The row above it was stale for days and nobody re-measured it** — the Architect read a recorded blocker as current state and reported the engine unusable when it was not. That is inv. 52 applied to this map's own rows: a row resting on a measurement falls with it, and a blocker is re-measured before it is repeated |
| First live analysis runs | **31.08 two runs, 01.09 one run, 02.09 one run, all measured** | nothing. The gate's freshness window is `−120 … +900` s and is a GATE budget, not a RUN budget. The 14:29Z run of 31.08 passed the gate three times and published no level; the 20:32Z run froze levels at gate step 4 and published two setups. **The 01.09 run proved the repair incomplete rather than wrong:** the freeze held every level, and the same window then demoted every status, so the answer carried a correct strategy table under «СДЕЛОК СЕЙЧАС НЕТ». The constant has still never moved; the object it governed was wrong twice, each time smaller than the last (inv. 57). **The 02.09 run is the first with no clock defect at all** — gate green at 116 s after a fetch that had moved the payload, one freeze, levels traced to the payload and to a 14.7-hour-old journal file, and not one number off the open web. Its four defects were all of the kind inv. 58 names, and none of them touched a price |
| A rule moved between environments is re-derived, not copied | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-01-a** | nothing. The 15-minute price age was written where the Boss pasted the payload into chat, so «re-pull before sending, or the coin leaves the answer» had two live exits; moving the reader into the repository closed the first and left the sentence untouched, and the file's own provenance table certified the clause carried «byte-equivalent in substance». Byte-equivalence WAS the defect. Appendix A now records that a provenance table asserting a clause unchanged is asserting the environment did not matter |
| A cache keyed by a stage's NAME hides a widening of its CONTENT | **closed by `ANALYST-INSTRUCTIONS.md` §6a, and it paid on the first run** | nothing. Each stored sweep now records the contract MD5 it was read under and is stale when that differs, whatever its age. The motivating case and the first catch are the same one: the international-institutional lane and its named host were added on 30.08, the 31.08 morning run found `horizon` two days inside a seven-day limit and never opened the host, and the evening run — forced to re-sweep by the MD5 rule — found a G20 finance ministerial in session with digital assets on its published agenda. Without the rule that event stayed invisible for six more days |
| The engine reads `fr` but not `oi` or `mark` | **closed by the run of 02.09** | nothing, and it is now checklist item 23. The FIL refusal was built on rising open interest with positive funding — fresh buying rather than short-covering — and that read is what kept the coin out of a short into strength. Four runs printed funding alone before an item existed to check the columns beside it, which is the whole argument for §7 growing by measurement. Original entry: Every row of `analyst/live.json` carries funding, open interest and mark beside the price, so positioning is a read of a file already open and costs nothing. Methodology §5 step 6 has mandated it since `2026-09-01-a`; **three runs have now printed funding and none has read the column beside it.** Not a defect in the payload and not a missing source — an unexecuted clause, which is the class §7's checklist exists to convert into a check |
| The freeze aged out the STATUS after `-a` moved it off the LEVELS | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-01-d; inv. 57** | nothing. There is one clock in a run and it stops at the freeze: the `СЕЙЧАС`/`ЖДАТЬ` split is decided once, against the frozen price, and prints that price in its own cell. **The measurement behind the demotion never existed** — the engine cannot re-pull, so every later moment compared the same number against a longer wait. Measured 01.09: gate green at 65 s, ADA short at 0.1998 inside 0.1985–0.2020, composition past fifteen minutes, and the section printed «СДЕЛОК СЕЙЧАС НЕТ» over a correct table |
| Outside-list candidates had no price lane | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-01-d** | nothing. §3B now prices them from the payload's `x` array — the exchange's own book from the Boss's own network, frozen with everything else — and the two-source web rule is retired: membership of `x` and tradability on a USDⓈ-M perpetual are the same fact, so nothing is left for the old rule to govern. Measured 01.09: APT (unlock 11.09) and CELO (hardfork 10.09) were fully argued and dropped for want of two web quotes, while both prices sat in the file the run had open |
| An analysis run's direct push has no failure branch | **closed by contract v17** | nothing. `git pull --rebase` and push again; a second rejection is one reported line and the answer is still sent. Four clauses said `analyst/**` goes straight to `main` and none said what happens when that push is REJECTED — which is ordinary, because the Shortcut writes `analyst/live.json` to `main` while the run composes. With no branch defined the run fell into §8's pull-request fallback, written for role 1 and carrying no role qualifier, and the engine's own state waited on a human merge. §8 now opens by putting role 2 outside every branch clause in it |
| `analyst/live.json` growth in git history | watched | ~280 KB per LIVE SNAP, several snapshots a day — hundreds of MB a year, in the one file that is replaced in place and therefore keeps every version as a distinct blob. Act if the clone becomes unwieldy. **The answer is archival, never a smaller snapshot:** the payload's width is what made §3B's price lane possible, and trimming it to save history would spend a capability to buy disk. Same standing as `journal/**` growth, and recorded here so the monthly audit stops rediscovering it |
| `home.treasury.gov` refuses this machine | **measured 31.08.2026T20:32Z — timeout on direct fetch** | any egress change. The G20 finance-track text was read from a documentary archive carrying the same release verbatim, and `ANALYST-INSTRUCTIONS.md` §6 now names that class: an archive of a primary's own words is admissible for a DATE and a FACT while the primary is unreachable, for nothing else, and the primary is re-attempted every run. Re-measure before citing this row as current (inv. 56) |
| CANON Part I amputation | prepared, held | one verified analysis run. Removing the Architect's engine before its replacement has produced a correct answer leaves no fallback |
| ETF flow figures have no reachable primary lane | **closed, deliberately** — the three probe rounds behind it are **measured, date unrecorded** | a named machine-readable endpoint from an issuer or a listing venue, arriving as a TZ. Three probe rounds from the VPS found none: issuer pages 403/429, Bitwise 200 alone is not the dominant fund, Cboe and Fidelity answered 404 on guessed paths, an NYSE quote page carries price and not creation/redemption. A figure is therefore not published and a direction is not published; press-sourced readings still inform the run internally (methodology §6). **A run never re-probes this** — rediscovering a closed lane every day is the failure this repository exists to prevent |
| Producer clock drift is unmeasured | watched | the floor refuses a payload more than 120 s ahead and nothing tracks approach. `age_sec` is signed and already recorded in the day log, so drift becomes visible before it becomes a refusal |
| Beta history in `history.json` | reserved | future analysis of beta stability and horizon calibration |
| The payload's symbol list against `tokens[]` | **closed — measured 03.09.2026 on `analyst/live.json`** | the next universe change, and nothing else. The `c` array carries `MORPHOUSDT` and `ARBUSDT`, so the exit class 5 this row was written about no longer fires and price levels reach the answer for all 30. **The row is closed, not deleted, because the producer is outside the repository and no TZ can reach it:** every coin added after this one reopens the same gap between the merge and the Boss editing the iOS Shortcut, and during that window `live-gate.sh` strips **every price level** from the market answer while the regime, the catalysts and the verdict survive (§11). The reading is re-measured before it is cited as current (inv. 56). The wide `x` array was never affected — it is the whole perpetual book and carried both coins throughout |
| MORPHO and ARB CoinGecko ids | **closed — measured 03.09.2026 on `debug.json`** | nothing. The arbiter this row named answered on a runner: both rows carry `error: null` and `matched_90d 2160` against a floor of 120, with `matched_14d 337` and `returns_14d 336`, so `morpho` and `arbitrum` are confirmed by the bot's own fetch rather than by the Architect's declaration (inv. 2, inv. 44). `ranks_fetched 30` and `fdv_fetched 30` in the same file close a second question nobody had opened as a row: the single `/coins/markets` call covers the widened list, so §1's 32-calls-per-run arithmetic is now measured and not predicted |
| The `fut:true` count is derived in two places of five | watched | the next venue change, or any TZ opening those files. TZ-26 derived `journal_bench.js:641` and `:644` from the declared set and left `:592` a literal on purpose — derived, it would assert `FUT.length === FUT.length` and control nothing (inv. 22). The three hand-written counts left are the §3.17 caption in `index.html`, the same sentence in `exhaustion_bench.js`'s expectation, and `bench/exhaustion-calibration.txt`'s header, which is frozen by §0 and correctly stale. This is inv. 58's residue: the count is prose in the places a reader reads, and prose has no producer |
| `run.note` names a declared futures-only asset every run | watched | the first journal run after the merge, which measures whether the spot mirrors answer alive. If they do, the note carries MORPHO and ARB permanently and stops separating «declared» from «unexpected» — the repair is a per-asset expectation in `journal/write.js`, not the removal of the note (inv. 41), and it is worth a TZ only once the note is actually constant |

| `index.html:799` restates the registry schema | open, unowned | any TZ that opens `index.html`. The comment lists seven fields and the schema now has eight. **The repair is deletion, not synchronisation** — replaced by a pointer to `bench/catalyst_bench.js`, or the schema keeps living in three files (inv. 20) |
| `main.yml` `paths` allow-list | **closed by TZ-23, merged** | nothing on the filter. The residual is a coupling, not a defect: the list must grow the first time `main.py` reads a repository file, no bench can enforce it (§11), and today's derivation is nil so the list is as small as it can be. A second reading arrives free — `journal/**` used to qualify to start the bot and was stopped only by `[skip ci]` in every journal commit subject, so a message convention was the whole control; the allow-list removes that dependency |
| `claude/tz-20-catalyst-registry-content` was never merged | **declared dead — do not merge** | nothing. `federalregister.gov` is absent from `PRIMARY` on `main` (measured), while TZ-20's immutable report describes adding it. Merging now would reintroduce a PRIMARY host for regulatory and macro events — **the exact class §3.15 closed permanently** — and would roll `catalysts.json`'s ENA entry back to the version TZ-21 superseded. The branch is retained as evidence in the standing of `CryptoTZ/TZ-03-report-delivery.md`. If TZ-20's four `QCASES` boundary cases are wanted, they arrive in their own TZ on their own merits, never as a side effect of a merge |
| A coin refused on both sides never reached the Boss | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-01-d** | nothing. `ИЗБЕГАТЬ` now carries two classes — a bare name for an entry refusal, `XXX до ДД.ММ` for one that lifts on a dated event — and a coin refused on both sides is named rather than absent. Measured 01.09: HYPE was barred for the 06.09 unlock, the reasoning was in the internal appendix, and the answer said nothing about HYPE at all. A refusal that is not printed is indistinguishable from a coin nobody examined (inv. 37) |
| Four methodology clauses named an object and no computation | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-02-b; inv. 58** | nothing. The audit of 02.09 found one mechanism four times, in the most disciplined run this engine has produced. `dclass` now records who established a date and is read by both rules that needed it — the counter's exemption and §2's dated prohibition class; the §6a hash is a written command over a named span and its field is `sec6_md5`; checklist items 25–28 compare the answer against `items`, against state and against the horizon store rather than against the run's memory of what it wrote. **The run kept two items alive at `unver 2` to avoid lifting a prohibition that its own `signal` items were already holding** — a rule broken to buy something already owned, which is what deciding in the minute before publication looks like from outside |
| An analysis run's landing place depended on its checkout | **closed by contract v18** | nothing. The 02.09 run executed inside a harness worktree with no upstream, brought its tree to `origin/main` by ff-only merge — correctly — and then had to argue past a clause reading «never starts from a branch», which named a checkout where it meant a tree. §4b step 2 now states the two facts it was always about (tree byte-identical to `origin/main`, reached without a merge commit) and step 8 pushes `HEAD:main` by explicit refspec. **The refspec is the load-bearing half:** inv. 54 forbids the day log from reporting its own push, so a target that depends on the checkout is a landing nobody can name until the next run reads a stale state. Whether that run's own commit reached `main` is still unknown here and is reported by the next run under methodology §12 |
| A carried catalyst printed a verified status on an unread source | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-01-d** | nothing. Status `НЕ ПРОВЕРЕНО`, purely subtractive in the standing of inv. 31, counted per item and closing as `ИСТЕКЛО` on the second consecutive run. **A DATE established by a primary is permanent and is never re-established; the ASSESSMENT built on it decays** — the distinction the engine reached by hand three times on 01.09 with no rule to reach it by |
| Nothing verifies that an accepted TZ's branch reached `main` | open, unowned | the next TZ touching the audit procedure. TZ-20 sat unmerged across four subsequent TZs and a monthly audit without being noticed, because §13's rule reads «executed ⇔ a report exists in `CryptoReports/`» and a report exists for work that never landed. **The gate count masked it rather than exposing it:** step 8 agreed at 23 062 the whole time, and the agreement was evidence that nothing on `main` ever reflected TZ-20, not evidence that it had. The check is one command — `git merge-base --is-ancestor <branch> origin/main` per open branch — and it belongs in the audit, not in a bench |
| The Executor's VPS cannot run gate step 5 under `bench.yml`'s own command | watched — **measured 31.08.2026**, TZ-23's session; reproduced by TZ-27 and pre-empted by TZ-28, **dates unrecorded in either report** | nothing. `direction_bench.py --control` exhausts V8's default old-space on a 955 MB single-CPU host; reproduced on a pristine `origin/main` tree and cleared by `NODE_OPTIONS=--max-old-space-size=2600`, so it is a ceiling and not a defect. TZ-27 cleared the same step with 8192 and TZ-28 set 4096 pre-emptively and therefore never measured whether it was needed — a raise applied in advance stops being a reading (inv. 56). `ubuntu-latest` has no such ceiling. Recorded so a future session does not read the OOM as a product failure and does not edit a bench to make it pass |
| `tokenomist.ai`, `cryptorank.io` egress | **measured 30.08.2026T18:07Z (TZ-22) — both open at the network layer** | nothing on egress. The reading is a point in time behind Cloudflare and is replaced by a later reading, never argued with (inv. 52). What remains is not an egress question and carries its own row |
| §6a discovery host | **`tokenomist.ai` reopened on its coin page by `2026-09-30-c` — measured 25.09.2026 from the Architect's session; `cryptorank.io` stays closed on TZ-24's reading of 30.08.2026T20:42Z** | nothing on `cryptorank.io`, and a run never re-probes it. **The closure of `tokenomist.ai` rested on the page TZ-24 probed**, `/sui/unlock-events`, which serves a boolean and no schedule; the coin page `/sui` of the same host states the next cliff in its served text and was never probed (row «Unlock dates have no primary lane»). What TZ-24 read stands as a reading of that page. Permission was answered — `tokenomist.ai/robots.txt` grants `Allow: /` to a group naming `ClaudeBot`, `Claude-SearchBot`, `anthropic-ai` and `Claude-User`; `cryptorank.io` names no agent beyond `*`. **Extractability was answered and it is what closes the lane:** the unlock-events page serves the boolean `isUnlockScheduleEmpty` and no schedule, nine schedule key names return zero across 617 540 bytes, and a fund's rounds page serves dated round records whose element schema carries no amount, valuation or investor key. Both load those figures client-side from a credentialed API. §6a records the closure of `cryptorank.io` and of that page so no future run spends a fetch rediscovering either |
| A reachability control that fails only at DNS | **partly closed by TZ-24, measured 30.08.2026T20:42Z; one layer still unproven** | any future egress TZ. TZ-24 added `192.0.2.1` (RFC 5737) beside the `.invalid` host and the exit codes differ — 6 at resolution, 28 at connection — so the instrument is now known to distinguish the two layers. **The residual is mine and is the reading that matters most:** TEST-NET-1 is blackholed, so control 3 times out (28) rather than being refused (7), and a REFUSED connect is the old cloud sandbox's exact signature. A third control returning exit 7 — a loopback port that actively rejects is enough, since the claim is about the instrument and not about egress — belongs beside the other two |
| Report template lets inv. 54 rest on the author's care | **closed by contract v15** | nothing. **Not a TZ, and the row that said so was wrong:** `EXECUTOR-INSTRUCTIONS.md` is Architect-owned and arrives by Boss upload (contract §2), so the Executor may never write it (contract §7.14) and a TZ asking it to would be defective. The repair is an Architect edit forced by TZ-22, in the standing of v13 and v14. §8 now names the two TZ classes once and every branch clause is silent on a report-only TZ instead of deviated from; §10's `## Commit` and `## Pull Request` read off the class; a hash appears only for a commit already pushed. **A bench over `CryptoReports/**` was considered and is impossible**: a report is pushed direct to `main` on a path both workflows carry in `paths-ignore` as `'**.md'`, so such a control could never fire — the template is the only place this rule can live |
| Three `analyst/**` paths had no class in the contract's §2 | **closed by contract v20** | nothing. `analyst/owner.json`, `analyst/live-gate.sh` and `analyst/README.md` were in the repository with no row in the table that opens «every file belongs to exactly one class», so the contract's own closure claim was false and the Executor's check for an unclassed file could not fire on three real paths. TZ-30 reported all three and correctly acted on none: `EXECUTOR-INSTRUCTIONS.md` is Architect-owned, the Executor may never write it (contract §7.14), and a TZ asking it to would be defective. **The repair is an Architect edit forced by a TZ, in the standing of v13, v14 and v15**, and the omission was one-sided rather than a disagreement — §11 of this map already named the owner of each of the three |
| Executor has no GitHub API access | **closed, deliberately** | nothing. **The premise moved and the conclusion stands:** the row read «`gh` is absent and no PAT exists», and `gh` is installed and authenticated on the Executor's machine — TZ-49 read a pull request with it, TZ-50 opened one, and TZ-53 read `gh auth status` exit 0 on 01.10.2026; the deploy key `crypto-auto-vps` carries git write. A fine-grained PAT cannot separate «push a branch» from «merge to main» — both need `Contents: write` — and the hosted-gate reading it would automate is already performed by the actor who opens the pull-request page to merge. The gap is closed in the CONTRACT instead: CI evidence left the Executor's acceptance criteria and became an audit step (contract §9) |
| The engine's published book had never been scored | **measured 28.09.2026 and re-measured 10.10.2026, both from the Architect's session — not a runner fetch** | a TZ building the scorecard as a workflow on a runner — the day logs parsed, the perpetuals' hourly klines read from `data.binance.vision` (inv. 24), every row resolved and written to an immutable record the engine never reads (owner's decision of 24.09.2026) — with this reading as its known answer (inv. 23). **The replay:** every trade row of the forty-two logs of 29.08–26.09.2026 — list rows, `ТОП-3` rows and `СОЗРЕВАЕТ` items, 292 after deduplication by run, coin and side — followed as an owner acting on the latest answer would: a pending order not re-published is cancelled at the next freeze, a re-published row replaces it, a filled position keeps its bracket; a `СЕЙЧАС` row fills at the open of the first hour after the freeze unless that open lies beyond the zone, where it rests as a limit; exits on hourly bars, the stop first when both levels share a bar, a time exit at 168 h, 0.10 % round-trip fees. **Result, exits at the last printed target:** 62 closed, +7.85 R, median −0.08 R, 48 % winners — **three outside-list trades carry the sum, −1.36 R without them**; longs +20.41 R on 31, shorts −12.56 R on 31 with 20 stopped and 29 published before 19.09; from 19.09, 17 closed at +11.94 R, twelve of them outside the list, on the week BTC rose to $86.6k; 13 still open at the 28.09 00:00Z cutoff. Exits at the first printed target move the total to +10.17 R and nothing else in this row. **The book's shape is the finding a total cannot show:** 24 positions open at once on 06.09, a drawdown of −11.21 R, 15 of 27 stops inside 24 h of their fill and 17 of them inside 03–07.09. **No edge is claimed and none is refuted** (inv. 32): one month, one market phase per method and a sum resting on three trades separate nothing, which is what the scorecard is for. **The reading of 10.10.2026, a second known answer:** the seven logs of 26.09–08.10.2026 parsed — 114 trade objects after deduplication by run, coin and side, every `СИЛЬНЫЕ`, `ЛУЧШИЕ`, strategy, `ТОП-3` and `СОЗРЕВАЕТ` object — and replayed on the perpetuals' hourly klines from `data.binance.vision` (inv. 24) under the protocol above, the book starting empty at 26.09 and the cutoff 2026-10-10T15:00Z; a waiting row's limit rests at its printed entry, the edge of its zone where one printed, and a row needing a daily close fills at the next day's open. **Every row:** 53 filled, 40 closed at −4.53 R — mean −0.11 R, 13 winners, 12 stops, 5 targets, 23 time exits — and 13 open at −0.37 R; every one of the 40 a long, the shorts of 06–08.10 all open. **The sized book alone, as the answers printed it from 03.10:** 16 filled, 9 closed at −7.0 R, eight on their stops and one time exit, about −474 USDT of the owner's 10 000 with the seven open marked; its three `СИЛЬНАЯ` — AAVE 03.10, SKY 04.10, RENDER 06.10 — are three of the stops. **Every publication as its own trade:** 74 closed at −25.6 R, 18 winners, 36 stops against 7 targets. **The phase is the finding:** the book went long on 17 to 22 list coins from 26.09 to 04.10 while BTC rose to $87 250 on 02.10, and short after it reached $80 345 on 08.10; taken as their own trades, the publications of 04.10 and 06.10 closed 24 rows, all 24 on their stops. No edge is claimed and none is refuted, again |
| The engine runs only when the Boss types a trigger | **closed — the owner's decision of 03.10.2026** | nothing. **The owner decided on 03.10.2026, on the first answer the bot delivered, that an analysis runs only when he presses the button:** the button replaces the trigger he typed, no timer and no watcher starts a run, and the watchers push their alerts to his Telegram, so the signal in time this row asked for reaches him while the decision stays his (row «The assistant's build sequence»). What follows is the design that decision replaced, kept as the record: TZ-56 was issued at `2026-10-03-a`, TZ-55 at `2026-10-01-f` and TZ-54 at `2026-10-01-e`; it no longer waits on the scorecard, because the owner ranked timing first on 01.10.2026 and the watcher decides when a run happens, never what it says, so it needs no measured edge to be right. The owner asked for signals in time: a catalyst, a regime boundary crossed or an exchange announcement between two runs reaches him only when he next opens the session, and every run waits on his phone's `LIVE SNAP`. **The parts are measured, not assumed:** `fapi.binance.com` answers the Executor's machine (TZ-52, 25.09.2026), so a program in this repository run by the VPS — never on a runner (inv. 24), never a model's session — can write `analyst/live.json` in the Shortcut's own schema, committed and gated exactly as the Shortcut's payload is (inv. 44), and the engine keeps reading a file, never a host (§11). **The shape decided here:** a watcher in code, never a model, reading prices, the exchange's announcement stream and its dated listing state (`fapi/v1/exchangeInfo`; row «The engine's exchange-announcement read is a path its own §6 forbids»), the unlock dates and the regime boundaries the last run wrote to `analyst/state.json` — the dates and the boundaries once the state names a condition on them (row «The watcher has no calendar and no regime input»); on a named condition it starts a headless analysis run and pushes the answer to the owner's Telegram, beside two scheduled runs a day — 06:00 and 14:30 UTC, the second after the journal's 13:00 write so the structural file it reads is hours old rather than a day — and, once the state can name one, a run around each class-B print (methodology §6). **It never gives advice and never tracks a position** (owner's decision of 24.09.2026): it decides WHEN a fresh, independent analysis runs, and the answer is the engine's. The bot token lives on the VPS only, which inv. 7 admits since contract v24; the Shortcut stays the manual path, and a second writer of one file is admitted because the gate reads `ts`, never the writer (inv. 51). **The owner named Telegram as his interface on 30.09.2026 and it is kept**: it pushes to a locked phone, which no page and no chat session can, it carries the answer in two messages, and its buttons replace the trigger he types — a run started from Telegram, the answer and the alerts back in it. The bot answers the owner's chat id and nothing else, and holds no exchange key. A web page is refused as the channel because it cannot push; the Claude app stays the build channel and the calculator stays the board |
| One agent executes the whole methodology in one run | **closed by `ANALYST-INSTRUCTIONS.md` `2026-10-09-a` and contract v27** | an Architect edit splitting `ANALYST-INSTRUCTIONS.md` by role, with a contract version classing the role files. At `2026-09-30-d` the methodology is 3 724 lines and 298 432 bytes and §7 carries 105 items, 13 of them retired — at `2026-10-08-a` 4 181 lines, 344 556 bytes and 111 items — all read by one agent before a single level is cut; the hunt's tail is dropped whenever a run runs short (methodology §5 step 5), and the audit of the run of 25.09.2026 found two dated facts the run held and did not use. **The roles decided here:** a hunter keeping the horizon store on its own schedule, so a run starts with the calendar instead of spending itself on it; the trader, the one decision-maker that exists today; a risk officer that reads the composed book cold and may only strike or cut a row, never add one — the check §7 cannot make on itself; and two roles in code, never models — the watcher and the scorecard (rows above). **Two or more deciding agents are refused:** summed or voting priors are what printed a long and a short on one coin (inv. 30), and averaged opinions are not a measurement. **The hunter keeps no schedule of its own:** the owner decided on 03.10.2026 that a model session runs only when he presses the button (row «The assistant's build sequence»), so the split gives the hunter its place inside the run he starts, and the same edit gives the state the fields the watcher's alerts on the calendar and the regime read (row «The watcher has no calendar and no regime input»). **The owner asked on 05.10.2026 whether the hunter, the trader and the risk officer run independently. They do not:** the run of 04.10 was one session, which launched four helper agents for its searches and decided everything itself, and §7 is still the engine checking itself. **Decided at `2026-10-05-a`:** the split waits on TZ-60's reading of usage at `high`, because each role is a session drawn from the one account every press draws on, and that account refused a press with 429 on 03.10. **The owner asked again on 09.10.2026; decided at `2026-10-09-c`: the split proceeds, as the next Architect edit.** The reading it waited on was taken by TZ-60 on 05.10 — the completed press at `high` drew 64 turns and 11.02 USD, and the account refused the next press with 429 after 109 turns — so the edit sizes the three roles against that press and that account, and the risk officer it adds reads only the composed book, never the methodology. **Written at `2026-10-09-d`:** methodology §15–§17 and contract v27 — the trader reads the methodology without §16–§17 by one command, §6 and §6a as its rulebook and never as a hunt it runs, launches the hunter on `sonnet` after the freeze and the sheriff on the session's model after item 86, applies the sheriff's verdicts verbatim and commits alone; the hunter writes `horizon`, `sweeps` and its hunt record `<stem>.hunt.md`; the sheriff reads §17, the book and one ticket per priced object, and may only strike or cut. **The reading the split is sized against is the next one, and no bar is written on it** (inv. 49): the run unit's summary lines of the first press under `2026-10-09-a` — `num_turns`, `cost_usd`, `models`, `memory_peak` — read against TZ-60's C run, 64 turns, 11.0167892 USD and a peak of 318 914 560 bytes, by the next TZ that reads the run unit's journal. **The first press under it delivered a status instead of an answer** (row «A headless run delivered a status as its answer») |
| A headless run delivered a status as its answer | **open — TZ-63 executed and accepted on 09.10.2026 (`2026-10-09-f`); in effect when the deployer installs the merge of pull request #51** | TZ-63's merge, then the first press after it, read from the run unit's journal by the next TZ that reads it: its summary lines — `answer_chars` above zero and no line «final message is not an answer» — and the day log it commits. **What happened:** the press whose writer committed `ef89542` at 2026-10-09T13:01:27Z ran methodology `2026-10-09-a`; the trader launched the hunter through the Agent tool, the tool ran it in the background, and the trader ended its turn on a status in English — «The hunter is still running the catalyst, unlock and positioning hunt…» — which `vps/run.py` handed to the outbox as the answer, because its only test was a non-empty result; no state and no log reached `main`. **Why the background:** third-party documentation of Claude Code — the official page refused this session's fetch — states that a subagent runs in the background by default since 2.1.198 and that `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` forces subagents back to synchronous; the VPS runs 2.1.282 (TZ-53, TZ-55, TZ-58). **The repair is three controls, any one of which keeps a status from reaching the owner as an answer:** the methodology's foreground calls and one-turn rule (`2026-10-09-b`, item 113); the variable in the run unit (TZ-63), whose name in the installed CLI TZ-63's C1 reads; and the unit's delivery test (contract v28 §4, TZ-63), which every one of the 48 answers on `main` at `ef89542` passes and the status of 09.10 does not. **The status also said the trader had grepped the previous day's log «to check the log format»** — methodology item 96's breach, by a run whose log was never written; §12 now names the format's source. **TZ-63's reading:** the program the unit starts, `/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`, carries `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` four times and `run_in_background` forty, read with `grep` and never executed; whether the variable keeps the hunter in the foreground is the first press's reading, and where it does not, the delivery test sends «Анализ не завершён.» and the hunt is lost as on 09.10. The hosted `bench.yml` does not run `vps/selftest.py`; the deployer runs it before every install, and that is its gate |
| The positioning classes are unmeasured | **open — recorded 09.10.2026** | a TZ measuring the four classes of methodology §16 on the archive, on a runner. `data.binance.vision` keeps per USDⓈ-M perpetual a daily `metrics` file of five-minute rows — `create_time`, `symbol`, `sum_open_interest`, `sum_open_interest_value`, `count_toptrader_long_short_ratio`, `sum_toptrader_long_short_ratio`, `count_long_short_ratio`, `sum_taker_long_short_vol_ratio` — and a monthly `fundingRate` file — `calc_time`, `funding_interval_hours`, `last_funding_rate` — read from the Architect's session on 09.10.2026: BTCUSDT's metrics answer 200 for 2020-09-01, ZECUSDT's and AAVEUSDT's for 2022-06-01, ZECUSDT's file of 08.10 answered on the morning of 09.10 with its content stamped 06:36Z, and its funding file of 2026-09 carries ninety settlements; inv. 24 admits the host from a runner. **The question is the one the methodology refuses to assume** (methodology §4): whether a coin carrying the large players' class of a side moves that way inside the holding window more often than the same coins in weeks without it, and whether an own-trend trade against that class, or with the crowd's, stops more often than one without — each against the null of the same coins and weeks, rules fixed before the data (inv. 23), and the classes computed by the methodology's own definition at four-hour steps, the archive's `sum_toptrader_long_short_ratio` standing for the live top-trader position ratio and `count_long_short_ratio` for the global account ratio. **Until that reading exists the classes may only take away** — refuse, take `СИЛЬНАЯ` away, halve, order the outside-list slots — and a role beyond that, a grade or a size step, is an Architect decision on the reading and nowhere else (inv. 32, 49). The live read is the exchange's own endpoints — `fapi.binance.com/futures/data/*` and `/fapi/v1/fundingRate` — on the host whose klines and `exchangeInfo` the VPS answers; **its first read is its measurement on that machine** (methodology §16), and the Architect's session cannot take it: that host answered 451 to every request this session made of it on 09.10.2026 — `openInterestHist`, `topLongShortPositionRatio`, `globalLongShortAccountRatio`, `takerlongshortRatio` and `klines` |
| The engine places no order on the exchange | **not built, gated** | the scorecard showing positive expectancy after costs over at least 100 closed trades spanning a rising and a falling BTC phase — a decision about value, not a calibrated band (inv. 49) — and the next step of `analyst/owner.json` — `СРЕДНЯЯ` to 1 % and `СИЛЬНАЯ` above it — is taken at the same gate and nowhere else; the owner's clarification of 01.10.2026 moved `СИЛЬНАЯ` to 1 % before it, on the grade and not on a measured edge. Until then no key with trading rights exists anywhere in this system and every order is the owner's. **The replay of 28.09.2026 is why the gate is written before the capability:** the month's total is about zero once three trades are removed, and an executor of that book would have held 24 positions at once |
| A probability per setup — the owner's request of 01.10.2026 | **open — recorded 01.10.2026** | the book in code and the scorecard (row «The assistant's build sequence»). The owner asked for an estimated probability beside each outside-list trade. **No number exists yet that deserves the word:** on a driftless walk the chance of the target before the stop is `stop / (stop + target)` — 33 % on every row whose target sits `RR_MIN` = 2 stops away — a constant of the construction the answer may not print (methodology item 79) and the object §8 closed as «TP before SL»; a percentage chosen by a model is a prior wearing a measurement's clothes (inv. 49). **The object that does deserve it is EMPIRICAL:** the engine's book cut into code, so the archive bench and the engine build one book from one function (inv. 21, 38); every setup those rules would have published on the perpetuals' three-year hourly archive labelled by the barrier it touched first — target, stop or the 168 h clock — and the rate read per class the answer already prints: side, lane, grade, `⚠`, label — and the same labels measure what the methodology refuses to assume: whether a dated event in the side's direction earns `СИЛЬНАЯ` (methodology §8). A secondary classifier on the same labels — meta-labelling, pre-registered and validated on walk-forward folds it never trained on — may lower a size or strike a setup and never raise either. **The row closes when the printed number is the archive's rate for the setup's class, beside its sample size, and the scorecard reproduces it on the live book.** The honest range was told to the owner: with the target two stops away an edge moves the chance from 33 % to perhaps 40 %, 72 % at ten to one does not exist, and expectancy — the chance times the payoff — is what his capital earns |
| An expert verdict per catalyst and for BTC — the owner's request of 07.10.2026 | **closed by `ANALYST-INSTRUCTIONS.md` `2026-10-08-a`** | the first run under it that prints a verdict, its block read against its appendix (methodology item 110). Until then: the next revision of `ANALYST-INSTRUCTIONS.md`, written after the audit of the run of 07.10. The owner asked, in a file sent on 07.10.2026 and again on 08.10.2026, that every significant upcoming catalyst carry a short verdict — `BULLISH`, `BEARISH` or `NEUTRAL`; the expected BTC reaction as an approximate percentage or range; `PUMP`, `DUMP` or no significant move; and one sentence on the most likely reaction — and that the answer end with BTC's own verdict: its direction, its expected move over the next 24–48 hours and one or two sentences, with the factors behind them left out. **What binds the edit:** each percentage is an approximate expectation and never a guarantee, as the owner wrote, and each is computed from a measurement the appendix names, because a figure with nothing behind it is the failure the live gate exists to stop. **What `2026-10-08-a` does:** the word is the engine's call, made last; every per cent is the instrument's measured move — the median and upper quartile of its absolute close-to-close move on the UTC days of the event's own kind over 365 days, or on its last thirty days where the kind has fewer than four instances — signed by the word; `ПАМП` or `ДАМП` print exactly where that kind moves the instrument more than an ordinary day, and an event that does must be signed; BTC's verdict uses its two-day moves and closes the answer; a coin event's age is measured before the word; nothing in the book moves on a verdict, and each is logged to be scored (row «The verdict record is unscored») |
| The verdict record is unscored | **open — recorded 08.10.2026** | the Architect's audits. Every run since `ANALYST-INSTRUCTIONS.md` `2026-10-08-a` logs one `VERDICT` scoring line per verdict (methodology §12), and the audit scores them — the sign against the instrument's close on the event's UTC day, or BTC's forty-eight hours from the freeze, and the range against the move. **Nothing is ADDED to the book on a verdict until its record does:** an additive role — a size step, a grade raised, a row it creates — is an Architect decision taken on the scored record against the null of a coin flip computed in the same reading (inv. 49), never on a count typed in advance, and a record that does not beat its flip is re-derived. **A subtractive role is the standing every unscored input has here** (inv. 31, row «The positioning classes are unmeasured»), and since `ANALYST-INSTRUCTIONS.md` `2026-10-10-a` the verdict has it in words: its effect takes `СИЛЬНАЯ` away and halves a size through the label, and the sheriff cuts or strikes on it — which `2026-10-08-a` and `2026-10-09-a` already did while a sentence of methodology §2 denied it, and which the run of 10.10 applied under objection. **Scored at the audit of 10.10.2026, the first two lines:** BTC 48 h from 2026-10-08T18:59:44Z, МЕДВЕЖИЙ −1.2…−2.4 % — +1.85 % at 10.10 14:00Z, four hours short of the horizon, against the sign; XRP's amendment day 09.10, НЕЙТРАЛЬНЫЙ ±1.5 % — +1.13 %, inside. Two lines separate nothing. The owner asked for the view on 07.10.2026; whether it carries an edge is what this row measures |
| `СИЛЬНАЯ` rests on a display-only signal | **open — measured 10.10.2026 from the Architect's session** | the scorecard of row «The engine's published book had never been scored» separating `СИЛЬНАЯ` from `СРЕДНЯЯ` on outcomes, or an owner decision on `risk_pct_strong` in `analyst/owner.json`. Methodology §8's condition (4) — `residual7` class `own` with the side's sign — decides the grade, the grade ranks an object first and the owner's file sizes it at 1 % against 0.5 %; `residual7` is pure display by inv. 27 and measured at zero predictive value (§3.9, §3.10a: contrarian IC −0.030 [−0.067; +0.004] on 144 dates, every exploration cell failing), and its `RES_Z` fires in about a third of weeks by chance. **Live, at the reading of 10.10.2026:** the three `СИЛЬНАЯ` objects the sized book filled closed on their stops, −3.0 R; three trades separate nothing, and the definition was written at `2026-10-01-a` as a definition to be measured. **The size step stands by the owner's decision of 01.10.2026** — his file names the policy his to change, or the scorecard gate's — and the audit of 10.10 told him the reading |
| The journal lands four to seven hours after its schedule | **measured 25.09–07.10.2026 from `journal/runs.jsonl`; the methodology's dependence closed by `ANALYST-INSTRUCTIONS.md` `2026-10-08-a`** | a GAP on the date rule — a missed date — and then a TZ on `journal.yml`'s schedule. The workflow runs on `cron: '0 13 * * *'` and writes once per UTC date; its records of 25.09–07.10 landed at 16:58–20:03Z, and 05.10 has none (`{"k":"g","d":"2026-10-05","why":"no run"}`). The run of 07.10 met a file 24 h 17 min 44 s old against the methodology's 24-hour ceiling, the next one landing at 19:15:50Z, seven minutes after its freeze, and refused the owner's whole list. **`2026-10-08-a` measures the file's age in dates** — the freeze's UTC date or the date before it, admitting one late cycle and refusing a missed one — and cuts a spot coin with no usable row on its own day, as a declared perpetual is cut. Moving the schedule off the top of the hour is the workflow's own remedy and waits on a missed date, because a late file no longer costs a run anything |
| The assistant's build sequence | **open — runs start only from the owner's button since TZ-57's merge at `075de0e`; TZ-58 merged at `2416e3f` — `fits=yes`, the stream listed, the list read; the run on `claude-opus-5-5` at `high` since TZ-59's merge at `07126c0`; TZ-60 merged at `6e58aea` on 05.10.2026 — the owner's STOP, installed 05.10.2026T12:26:39Z as TZ-61 read it; the size `open` on two of six runs, read 05.10.2026T10:41Z** | each step's report. The owner confirmed the architecture on 01.10.2026 — one decision-maker, roles in code around it, Telegram as the interface, execution manual — and put the hunter first. **Each step is a TZ written against the previous report:** TZ-53 reads the VPS — the toolchain a scheduler needs, a headless session's exit, and every host the watcher and the hunter would read, answered or refused — and changes nothing; TZ-54 builds on what it measured: the payload written by the VPS in the Shortcut's schema, the scheduler, the Telegram bot and the exchange watcher — the hunter's most time-critical lane, in code; **the hunter's own schedule follows the methodology edit that splits the hunter** (row «One agent executes the whole methodology in one run»), because a timer for a role with no text runs nothing (inv. 58), and it runs in the unit TZ-54 builds, so the calendar is then kept between runs instead of rebuilt inside one; after the run lane, one TZ cuts the book into code, one function shared by the engine and the archive bench, and the next builds the scorecard and the calibration of row «A probability per setup» — each numbered when it is issued, because a number named here in advance moved twice. **The hunter precedes the book in code because the owner ranked timing first, and because it needs no measured edge to be right:** a dated event is a fact before it is a signal. **The floor edit TZ-54 waited on landed at contract v24 and this map's `2026-10-01-e`** (inv. 59): item 6 and inv. 7 admit the bot token and the exchange's read-only key on the VPS — each a root-only file outside the repository, handed to the one unit that uses it as a systemd credential, never printed or committed, meant to be unreadable by the analysis unit, which TZ-54 measured it was not (item (7) below) — item 9 and inv. 44 give the VPS writer a workflow step's standing, and item 15 makes merge the VPS's deployment; TZ-54 is issued against v24. **What TZ-53 read, and what TZ-54 is written against:** (1) a transient system unit — root, `HOME` and `PATH` set, no API key — ran a headless `claude -p` to an exact answer in 2.8 s, and its dry-run push authenticated over the SSH deploy key, so a timer can run an analysis and commit it; systemd 255 and cron are both available and neither is in use; `gh` is authenticated; 2.1.282's help carries no `--max-turns`, so a run is bounded by its unit's `RuntimeMaxSec` and never by a turn count; and each headless run leaves a session record under `~/.claude/projects/` — 180 846 bytes for the probe — so a scheduled run's records need a retention rule — **the owner asked on 01.10.2026 that runs clean up after themselves; decided:** a daily timer keeps the newest records by age and count and removes the rest, every run removes its own scratch when it ends, and every run executes in its own unit under a `MemoryMax` set from the measured peak and under `RuntimeMaxSec`, so a run that overruns is stopped by the host and never takes the host down; a finished run holds no memory, so the cleanup is of disk, and memory is governed by the one-session rule below, not by a count of runs; (2) **the machine is at its memory ceiling** — 1 CPU, 955 MB, 74 MB available and 1 543 MB of swap in use, 68 harness worktrees registered — so TZ-54 first reads what holds the memory and the peak a full analysis run takes, admits a run only when the host's available memory covers the unit's ceiling — on this host, one Claude session at a time — and enables no timer whose run does not fit the memory it measured; the owner chose on 01.10.2026 to build on the host as it is and to decide its size on that measurement: a run that fits stays here, and one that does not is answered by 2 vCPU and 4 GB or by moving the analysis run alone to a GitHub runner fed by the VPS's payload — never the payload itself, which a runner cannot read because `fapi` answers it 451 (inv. 24); **decided at `2026-10-01-e`, before the measurement:** a run fits when its unit's ceiling — 1.5 times the footprint measured in its own cgroup, resident plus swap, rounded up to 16 MiB — is no larger than what the host frees when no other session runs, read as the available memory plus the measuring session's own resident set; a run that does not fit is answered by 2 vCPU and 4 GB and never by the runner, because item 90 reads `fapi.binance.com`'s daily klines and a runner is refused there with 451, so a runner cannot execute the method; (3) `fapi.binance.com` serves the payload's schema to this machine — the bulk 24-hour ticker's row keys equal `x`'s, `premiumIndex` carries `markPrice` and `lastFundingRate`, `openInterest` answers per symbol — and the payload itself shows `c`'s `h` and `l` equal to `x`'s on 31 of 31 rows while `p`, `chg` and `qv` differ on 26, 26 and 30 of them, so the two arrays are not one snapshot; the Shortcut's own mapping stays unread, so the writer is specified against `analyst/live-gate.sh`'s checks of `c`, read first; (4) the hunter's candidate lanes, each read once: answering — FRED's four liquidity series as CSV (`Crawl-delay: 1`), the Federal Reserve's 2026 calendar in served HTML and H.4.1, the Treasury's daily cash balance, DefiLlama's stablecoin supply, iShares' IBIT and ETHA and Bitwise's BITB holdings at their issuers, as of the previous one or two days, Coinbase's spot ticker, and `exchangeInfo`'s dated listing and delisting state; refusing — Grayscale behind a Vercel challenge, its `robots.txt` included, and Farside behind a Cloudflare challenge, both recorded as the reading; (5) Telegram's Bot API host answers this machine, which proves reach and not delivery. **TZ-54 measured on 01.10.2026 and was merged at `966b3f2` on 02.10.2026:** the deployer, the cleanup timer, the exchange watcher and the bot are in effect, and the run lane and the announcement stream are not. (6) **The run did not fit the host:** with nine Claude sessions alive and 65 MB available its unit peaked at 286 MB resident and 180 MB of swap and ended in an error after 83 turns and 605 s, inside the window in which the owner reported reaching his account's usage limit; it used 98 s of CPU. TZ-54's own instrument over-counted — it summed the high-water marks of 112 processes that never coexisted, 938 MB against the cgroup's 291 MB, the Architect's defect in its §12.7 — and the verdict holds without it. (7) **The run unit could read what it was meant to hide:** specified as root behind `InaccessiblePaths=`, which a privileged process undoes, with the trigger's values in a session record under `/root` — the Architect's defect in TZ-54 §12.12 and contract v24, repaired by contract v25 before any run is enabled (inv. 7). (8) **The exchange refused the key's signature** (row «The engine's exchange-announcement read is a path its own §6 forbids»). **Decided at `2026-10-01-f`: the owner chose on 02.10.2026 to test on the 1 GB host before resizing it**, and closed stale sessions himself, leaving about 0.18 GB available with the cleaning session alive. The rule of `-e` keeps its budget and gains a test mode: the budget is 1.5 times the run's footprint — the cgroup's resident and swap peaks — rounded up to 16 MiB; the resident ceiling is the smaller of the budget and what the host frees less 64 MiB; the rest of the budget is the run's own swap, so the run pays for the shortage and the owner's other services do not; and the run fits when it completes under those limits, which TZ-55 measures as the run's own user. **The size is answered by evidence and no longer by the rule of `-e`:** a run killed by its memory or time limit in that measurement — or, among the first six scheduled runs, one killed so or more than one not admitted for memory — is answered by 1 vCPU and 2 GB, because one CPU was a sixth used and 2 GB holds the budget beside the owner's other services and one open session; 2 vCPU and 4 GB is withdrawn. A run that fails for any other reason, the account's limit included, measures nothing about memory and decides nothing about size. **TZ-55 measured on 02.10.2026 and was merged at `2aaa74f` on 03.10.2026:** the run unit runs as `cryptorun` from its own clone, holding its own Claude login and the deploy key and able to read no other credential — its probe read every path as required — the deployer installs only a `vps` tree GitHub signed, and the bot sets aside as `.dead` a file refused in both forms; the run lane and the announcement stream stay off. (9) **No run has completed, and none was stopped by memory:** three full runs of three — TZ-54's and TZ-55's two admitted — ended on the owner's account limit, the last 18 minutes after the limit had reset while the measuring session drew on the same account; its cgroup peaked at 283 MB resident and 39 MB of swap, far inside its limits, and by the rule above it decides nothing. (10) **TZ-55's measurement could not be admitted as written:** its ceiling counted the measuring session's resident memory as free while that session lived, and the admission required the host to free the whole ceiling — the Architect's defect in TZ-55 §10 and §12.4; the owner bypassed it in the measurement's copy only, and the code kept the rule. (11) **The deployer read the newest signed commit alone,** so an unsigned `vps/` push would have been installed at the next legitimate merge, whose signature covers the tree it lands on — closed by contract v26. (12) **The announcement stream answered `REGISTER`**, which TZ-54's program refused because the documented answer is `SUBSCRIBE`; Binance documents no `REGISTER`, so the next TZ reads the stream before it changes the program. (13) **Claude Code kept an auto memory for the run** — a directory of notes that every later session of the repository loads at its start — so one run's conclusions could reach the next, against the owner's decision of 24.09.2026 — closed by contract v26 and the run unit. **Decided at `2026-10-03-a`: the owner decided on 03.10.2026 that a run starts on swap and that he stops no service for one.** The budget stays as measured — `budget_bytes` of `vps/memory-record.txt`, 1.5 times the footprint; the resident ceiling is set at each start from the host at that instant — what it frees less 64 MiB, in 16 MiB steps, never below 160 MiB and never above the budget — and the rest of the budget is the run's own swap, so the run's pages go to swap before any other service's do; a run starts when the host frees its ceiling plus 64 MiB and the free swap holds the rest. **The measurement is the product's own first run, never a session watching it:** a watching session holds the memory and the account the run needs, so every run logs the limits it ran under, its cgroup's resident and swap peaks and its token usage; the bot's button and the watcher's requests are enabled before the fit is decided, the timers wait for one completed run, and the TZ after that run reads its line, writes the record's `fits` and lists them. The answers of `-f` stand: a run killed by its memory or time limit, or more than one of the first six not admitted for memory, is answered by 1 vCPU and 2 GB, and a run that fails for any other reason decides nothing about size. **The account, not the memory, is now the measured constraint:** the twice-daily cadence is confirmed or cut from the usage the first completed runs log, and is never assumed. **TZ-56 measured on 02–03.10.2026 and was merged at `4c67ebe` on 03.10.2026:** a run sets its own pair at each start — the probe's unprivileged process read exactly the pair the step before it set, from two different starting pairs — the deployer verifies every signed commit since its own `HEAD`, and Claude Code's auto memory is off; the bot's button and the watchers' run requests went into effect, the timers and the announcement stream did not. (14) **The product ran on 03.10.2026:** the writer committed for two runs, at 10:56Z and 11:38Z, and the second pushed the day's analysis at 11:58Z; their lines are in the run unit's journal, which only the VPS holds. **On that answer the owner decided that an analysis runs only when he presses the button:** no timer starts one and no watcher requests one — the watchers keep alerting him and he decides whether to press — so `crypto-run.timer` leaves the repository, the twice-daily cadence and its measurement are withdrawn, and the hunter keeps no schedule of its own, because it is a model session too. **Decided at `2026-10-03-c`: TZ-57 reads every invocation of the run unit since TZ-56's tree was installed and classes each by its own lines** — killed by its memory limit, killed by its time limit, not admitted, refused by the account (`api_error_status=429`), completed, or other. A kill writes `fits=no` and the host is answered by 1 vCPU and 2 GB as `-f` decided; no kill and a completion write `fits=yes` and the host stays as it is; neither decides anything. **The budget gains the product's own term:** `budget_bytes` is the largest of 1.5 times each footprint the record holds — TZ-54's input, TZ-55's run, and the chosen product run when it completed or was killed by memory, never one killed by time, whose figures measure the limit rather than the need — and `runtime_max_s` takes a completed run's duration the same way; one function in `vps/common.py` computes both, and the run unit's `MemorySwapMax=` and `RuntimeMaxSec=` follow it. **The size is re-read on the first six runs the button starts after TZ-57's merge:** one killed by a limit, or more than one not admitted for memory, answers the host by 1 vCPU and 2 GB — the rule `-f` wrote for six scheduled runs, applied to the runs that remain. **The run's model is pinned and its effort set — the owner's proposal of 03.10.2026, kept:** `claude-opus-5-5` at `--effort high`. The method is a long procedure whose measured failure is a run that stops short of its last steps (methodology §5 step 5; the audit of the run of 25.09.2026), effort governs how much a run reads and verifies before it stops, and Opus 5.5 runs at `medium` unless told otherwise (code.claude.com, «Model configuration», read 03.10.2026); a pinned id moves only by a TZ, where the alias `opus` would move with the next release. With no scheduled run left, his presses are the whole draw on the account, and every run logs its usage. (15) **The same reading decides the announcement stream** from its delivery against the exchange's own list (row «The engine's exchange-announcement read is a path its own §6 forbids»), so size and the stream are decided together, on the product's own record. (16) **TZ-57 executed on 03.10.2026 in a cloud container, not on the VPS:** its header named no host, the session that received it had no route to the server, and every stage that reads the host — the product's runs, the list from the server's own client, the run unit's command line, the stream's handshake — stopped BLOCKED under the TZ's own outcomes. What it could build without the host it built, and the audit accepted: the watchers alert and request no run, `common.request_run` has the button's path alone, `crypto-run.timer` is deleted so the deployer removes it from the host at the merge, the stream's program sends `SUBSCRIBE` and waits for that answer, and `common.record_limits` is the one implementation of the budget rule above — on branch `claude/vibrant-albattani-ddmwh1` at `895d1dc`, `vps` tree `c4eef2b1d03991c05a27464038f60d2a3307c14a`, selftest 18 sections and 200 checks green, reproduced by the Architect's session. **Decided at `2026-10-03-d`:** TZ-58 carries TZ-57's host stages unchanged — the fit and the record, the model's pin, the stream's handshake and the list reader — written against that tree, and starts only after it is merged; **a TZ with a stage on the VPS names its host in its header, and its first stage stops BLOCKED on any other machine before any work,** because a session elsewhere spends itself on every stage the host alone can answer. (17) **TZ-58 executed on 03.10.2026 on the VPS**, after a first session in a cloud container stopped at its host check, and its branch at `a172529` is accepted: the run unit's journal holds two invocations since TZ-56's install — at 10:56Z one admitted and refused after 9 turns and 17 s with `api_error_status=429`, the owner's account exhausted, and at 11:37Z one completed in 1 238 s and 58 turns under a ceiling of 167 772 160 resident and 536 870 912 of swap, peaking at 167 780 352 and 164 888 576 — so the record carries `fits=yes` and the host stays at 1 vCPU and 1 GB; the budget does not move, because 1.5 times that footprint, rounded up to 16 MiB, is 503 316 480 and TZ-54's input term stays the larger. **The completed run drew 83 752 output tokens and 11 941 234 cache-read tokens, 10.09 dollars at the API's price, on the alias `opus` at its default effort:** that is the measured cost of one press, and the next reading measures it at `high`. The stream answered `REGISTER` and then `SUBSCRIBE`/`SUCCESS` on the server's own connection and `crypto-announce.service` is listed; the exchange watcher's list reader read three English children and 8 329 articles, the same count `curl` read. **The model scope stopped on the Architect's defect:** TZ-58's A4 required `high` on the line its `grep` printed, and the binary `/usr/bin/claude` 2.1.282 wraps the levels of `--effort` — `low, medium, high, xhigh, max` — onto the next line, which the session's own probe printed; a known answer registered on the layout of a tool's text is the unprobed expectation the canon forbids. **Decided at `2026-10-03-e`:** TZ-59 pins `claude-opus-5-5` at `--effort high` on that reading, with no stage on the VPS, because every fact it rests on is already in TZ-58's report. (18) **TZ-59 merged at `07126c0` on 03.10.2026, and the button has started two runs since TZ-57's merge,** both on 04.10: the writer committed at 16:43:21Z and 17:15:12Z, and one analysis landed, `6c9645e` at 17:08:41Z. **The owner pressed the second by accident, while reading the first answer, and nothing could stop it** (his message of 05.10.2026). **Decided at `2026-10-05-a`: a word stops the run.** «СТОП», «STOP» or `/stop` from the owner's chat — case and a trailing «!» or «.» ignored, and a message older than ten minutes dropped as every message is — is answered «Останавливаю анализ…» and leaves a stop request beside the run requests; `crypto-stop.path` then starts `crypto-stop.service`, a root oneshot that holds no credential and starts no model, which consumes every stop request first so that its path cannot loop, removes every pending run request, stops `crypto-run.service` — systemd's own stop, which signals every process of the unit's cgroup, the session and its tools included — clears the unit's failed state and its start counter, and writes one notice: «Анализ остановлен.», «Анализ не идёт — останавливать нечего.» or, where the unit still runs, «Остановить анализ не удалось.» While it runs, its runtime directory tells `run.py` that the stop is the owner's, so the run logs that and writes no «Анализ не завершён.». **Root, because stopping a system unit is root's, and no privilege for the bot:** the path unit lets the bot ask for exactly one action, in the shape that already starts a run. **No confirmation is added before a run:** it would slow every deliberate press, and a stop sent before the session starts spends nothing of the account; the messages that confirm a start name the word instead. **A stopped run measures nothing about size** — it is the owner's act, as a refusal by the account is the account's — and TZ-60 registers its class beside the others, ahead of «not admitted», because a stop during admission prints `admitted=no`. **TZ-60 reads, on the VPS, every invocation since TZ-57's install** under the six-run rule of `-c` with that class added, the usage of every run at `high` beside the run of 03.10 at the default effort, and the stream's record against the list's generations (row «The engine's exchange-announcement read is a path its own §6 forbids»); **the size is decided only once six runs are read or a limit kills one**, and a set of six with no completed run decides nothing. (19) **TZ-60 executed on 05.10.2026 on the VPS and merged at `6e58aea` the same day.** The STOP was proven on this host on a transient unit — `stops=1 requests_removed=1 before=active stop_exit=0` ending `after=inactive notice=S13`, and `notice=S14` with nothing to stop — and stops `crypto-run.service` since the deployer installed that merge at 2026-10-05T12:26:39Z, as TZ-61 read it; the first stop the owner sends is its first whole run on the real unit. **Two of the six runs are read, and the size is `open`:** 04.10 at 16:43Z class `C` — 64 turns, 1 551.5 s, 97 177 output and 13 026 278 cache-read tokens, 11.02 USD — and at 17:14Z class `L`, refused by the account (`429`) after 109 turns and 562 s. **Usage at `high`:** the completed press drew 10.3 % more turns, 25.3 % more time, 16.0 % more output and 9.2 % more cost than the run of 03.10 on the alias `opus` at its default effort; no bar is registered and nothing is decided on it. The four presses that remain are read by the TZ that next reads the run unit's journal |
| The engine's exchange-announcement read is a path its own §6 forbids | **closed by `ANALYST-INSTRUCTIONS.md` `2026-10-08-a` — the stream's record and `fapi/v1/exchangeInfo` replace the path; measured 01.10.2026 by TZ-53 (C8) and 2026-10-07T22:29Z by TZ-61 (`W1`)** | a run recording the record absent or unreadable on the VPS, which sends that read to its one-search fallback, or any run reading the `/bapi/` path, which fails methodology item 99. Until `2026-10-08-a`: the next revision of `ANALYST-INSTRUCTIONS.md`, which admits the stream's record in place of the disallowed path — until `2026-10-08-a` the methodology edit that splits the hunter (row «The assistant's build sequence»). `ANALYST-INSTRUCTIONS.md` §6a reads `www.binance.com/bapi/composite/v1/public/cms/article/list/query` «on EVERY run, first», and that host's `robots.txt` disallows `*/bapi/` to `*`, the group that binds `curl` — the Architect's reading and TZ-53's agree — while §6 states that such a disallow is a refusal written down and that a channel is admitted only where its host's file permits its path. **Decided:** the lane leaves §6a, and the exchange's dated listing state is read where it is permitted and documented — `fapi/v1/exchangeInfo`, keyless, whose `onboardDate`, `deliveryDate` and `status` named 15 listings of the seven days before the read and three perpetuals delisting on 05.10.2026 before that day came (TZ-53 C5). The announcement site offers this client nothing dated: its English sitemap carries one generation stamp on 4 973 URLs, and its article pages answer a captcha. **Spot listings keep their lead time through the exchange's own documented channel:** Binance pushes every announcement on `wss://api.binance.com/sapi/wss`, topic `com_announcement_en` — `catalogName`, `title`, `body` and `publishDate` per message, the connection signed with an API key's HMAC, alive up to 24 hours and pinged every 30 s (developers.binance.com, «Announcements», last modified 01.10.2026; read by the Architect's session on 01.10.2026) — so the watcher, a program, holds that stream and acts the moment a listing is published, and the article's own text arrives in `body` without a page the captcha guards. The key is created with reading only — no trading, no withdrawal — and bound to the VPS's address, so the standing decision that no key with trading rights exists anywhere holds (row «The engine places no order on the exchange»), and the stream is measured by TZ-54 before anything relies on it: TZ-54 first reads the key's own permissions from the exchange — reading only, bound to an address, or the stream is not opened — holds the stream for a bounded window, and lets it request runs only once a received message carried all six documented fields. **TZ-54's key check was refused with `-1022`**, a signature the exchange did not accept: the signing code signs exactly the string it sends, and the stored secret had arrived with Cyrillic look-alike letters that no transcription could resolve, so no stream was opened; the owner replaced the key on 02.10.2026 and TZ-55 repeats the check and the bounded window; admitting the stream's record to the method is the edit this row waits on. **The owner's permission of 01.10.2026 to bypass Binance's restriction is not used:** the documented channel carries the same primary source sooner than any poll, and evading a challenge from the VPS would put at risk the one address every live price comes from. Until the edit lands each run still reads that one disallowed path, and this row is the record of it. **TZ-56 read the stream on 02.10.2026:** a connection that sent no command was answered `REGISTER`/`SUCCESS` at 22 ms, and one that sent `SUBSCRIBE` was answered `REGISTER`/`SUCCESS` at 7 ms and `SUBSCRIBE`/`SUCCESS` at 246 ms — so `REGISTER` answers every connection and acknowledges no subscription — and the program built on the first reading held one connection from 22:44Z to 01:44Z, 10 802 s with 356 pings and no data message, which cannot tell a quiet night from a connection subscribed to nothing. **Decided at `2026-10-03-c`:** the program returns to the documented subscription — it sends `SUBSCRIBE` and waits for that answer, as the stream's «General Info» on developers.binance.com shows it (last updated 02.10.2026, read by the Architect's session on 03.10.2026; `REGISTER` appears nowhere in it) — and the service is enabled once the branch's own connection is answered `SUBSCRIBE`/`SUCCESS`. **It requests no run:** the owner decided on 03.10.2026 that only his button starts an analysis (row «The assistant's build sequence»), so a matched announcement reaches him as an alert and he decides, and the six-field condition this row set on a run request has nothing left to gate. **Delivery is checked against the exchange's own list, in code, never by a session holding a stream,** because a waiting session holds the memory and the account a run needs. The list is Binance's English announcement sitemap — `robots.txt` allows `*/sitemap_output/` and disallows `*/bapi/` — which dates no article but is rebuilt daily: read by the Architect's session at 2026-10-03T14:03Z, its index was rebuilt at 02:02Z and names three English children with one `lastmod`, 2026-10-02, holding 8 329 announcement articles — 7 740 under 32-character ids and 589 under older 12-digit ones — beside 144 catalogue pages; TZ-53 had read the first child alone. The exchange watcher reads the index hourly and, on each new generation, logs the articles it added and removed, so the stream's messages and the list's additions are two dated series of one fact, read side by side by the TZ that reads the first six runs after TZ-57's merge (row «The assistant's build sequence»): a silent stream beside a growing list is the defect three measurements could not see. **The run of 04.10 read that path at 16:48:25Z and its newest record was dated 02.10 13:00, while the stream had been listed since the evening of 03.10:** TZ-60 reads the stream's own record over that interval beside the list's generations, so the methodology edit that admits the record is written against a measured delivery. **TZ-60's `D0` is withdrawn at `2026-10-07-a`.** TZ-60 read the stream at 2026-10-05T10:41Z — subscribed throughout, three records, all `Latest Activities` of 05.10, the first published at 02:00:01Z — against list windows of 19 and 14 `new`, and both windows, (2026-10-03T02:02:14Z, 2026-10-05T01:58:16Z], lay inside a span in which Binance published no English announcement: the run of 04.10 read the exchange's list at 16:48:25Z and the newest of its 350 records was dated 02.10, and Binance's channel carries post 9021 at 2026-10-02T09:02:01Z and post 9022 at 2026-10-05T02:04:14Z with no post between. **The list is retired as the stream's reference:** a sitemap entry carries no date and no key a stream message carries, so its additions were never the publications of the window they were counted in and could never be joined to the stream's records, and no verdict should have rested on it before it was compared with a dated source. **The reference is `t.me/s/binance_announcements`**, the public preview of Binance's own English announcement channel, read by the Architect's session at 2026-10-07T17:25:34Z — `t.me/robots.txt` answers 404, so nothing is disallowed: each post carries Telegram's own UTC time, the article's 32-character id in its link — the id the list and the exchange's article pages use — and the announcement's title as its first line, which is the stream's own field, so a post joins the stream by its title. **It is a lower bound, never a census:** the stream recorded `Latest Activities` published on 05.10 at 03:00:01Z and 09:00:01Z that the channel never posted, so a post absent from a subscribed stream is a miss and an empty channel proves nothing. TZ-61 reads the stream's whole record against the posts of 02.10–07.10 frozen in its own text, with no fetch of its own. The list reader's hourly read now feeds no decision, and leaves `vps/exchange.py` with the next TZ that opens that file. **TZ-61 read the stream on 07.10.2026, and it delivers** (`W1`, read 2026-10-07T22:29:25Z): all seven of the channel's posts of 05–07.10 joined a record by exact title, each inside one subscribed interval — none needed the reduced match, and the control post of 02.10 joined none. The record holds twelve publications since `T1`, five of them never posted by the channel, received 1.3–2.5 s after publication and once 32 s; six gaps between subscriptions — the start, two installs, two losses and one planned refresh — left 24 s of the four days unsubscribed. **The owner's chat was quiet because of the alert rule:** eleven titles named no list coin — three of `New Cryptocurrency Listing` among them, one naming no ticker at all — and were recorded only, and the one alert was a `Latest Activities` promotion naming BNB; none of the eleven moved a level in the run of 07.10, which read the collateral-ratio update as no effect and the STG merge as no reaction distinct from the tape. **Admitting the record no longer waits on the role split:** the run unit can read it, by the code — `crypto-run.service` carries `SupplementaryGroups=cryptoauto`, and the record is written `0640` in a `0750` directory of that group (`common.atomic_write`, `vps/install.sh`) — and it spans the lane's fourteen days from 2026-10-17T20:37Z, covering publications since `T1` only until then |
| The owner's alert channel carries promotions and misses contract notices | **open — TZ-62 merged at `d446a6b` on 09.10.2026; measured 09.10.2026T07:00Z on the owner's screenshot: the first alert under the rule, «Binance Will Extend the Monitoring Tag to Include BICO & CVC on 2026-10-09» in «Latest Binance News», a perpetual's monitoring tag the old rule recorded only** | TZ-62's report and its audit, then the merge, which the deployer installs behind the selftest; after it, the first week of `kind=alert` lines read against the record by the next TZ that opens the VPS. **The owner's request of 09.10.2026**, sent with his screenshot of the alert of 13:00 on 08.10: nothing promotional reaches his chat, and everything that bears on the strategy on Binance Futures or on a candidate for his spot portfolio does — listings and delistings of promising coins, funding, order-book depth, unlocks. **The defect is the rule, not the stream** (TZ-61, `W1`): `announce.act` alerted on any title naming a list coin or, inside a listing catalogue, a perpetual, and BNB — a list coin — is the currency of Binance's rewards, so the promotions of 07.10 and 08.10 alerted, while a Futures notice that names its contracts only in its body — as the delisting of 05.10 named PROMPTUSDT, PUMPBTCUSDT and 1000000BOBUSDT (day log of 04.10) — cannot alert at all. **Decided — the rule, first match wins:** the promotions catalogue (`catalogId` 93, «Latest Activities») and wallet maintenance (157, «Maintenance Updates») never alert — every «Latest Activities» record whose title is known, TZ-61's six, all `93`, and the screenshot's, is a promotion, and the one record of 157 a completed token merge; a title on tokenized securities, TradFi or stocks never alerts; in `New Cryptocurrency Listing` (48) a new coin alerts whether or not its ticker is known yet — a spot listing, a HODLer airdrop, a Launchpool, a new perpetual — which closes TZ-61's R-2 for crypto; a title in Binance's promotional words, or on trading pairs, collateral, a quarterly contract or Binance Alpha, never alerts; a title naming a list coin alerts; a perpetual's listing, delisting or monitoring tag alerts; and a Futures notice on delisting, funding, leverage and margin tiers, tick size or price protection alerts when its body names a list contract, those contracts appended to the alert — a delisting off the list already reaches him as `exchange.py`'s A3 once its date is set. **Every pattern is case-sensitive**, because Binance writes headlines in Title Case and tickers in capitals — «Win» is a promotion's word, `WIN` a coin. **Measured on the thirteen records whose catalogue and title are known** — TZ-61's twelve and the screenshot's — none alerts under the rule, the two promotions included; the record's other lines are TZ-62's replay. **What reaches him stays the exchange's own publication:** the record is untouched, the run the button starts still reads all of it (methodology §6a), and A1's text is unchanged but for the appended contracts. **Not alerts, each for a stated reason:** a funding level — §3.10a's `--funding` cell measured no crowding edge, so a threshold would be a prior wearing a control's clothes (inv. 49), and the board shows funding live; order-book depth — no lane reads it and no edge is measured; an unlock — the watcher has no calendar (row «The watcher has no calendar and no regime input»), and the run reads DefiLlama's index. **TZ-62 read on 09.10.2026:** the record's nineteen publications since 05.10 — twelve of «Latest Activities», two of «Maintenance Updates», four on stocks and TradFi, one on collateral — and the rule alerts none, while the old rule alerted twice, the BNB promotions of 07.10 and 08.10; the snapshot of `exchange.py` holds 216 contracts of type `TRADIFI_PERPETUAL`, the four onboarded on 06.10 among them, and A2 alerts `PERPETUAL` alone, so none reaches him. **Watched:** `NOISE`'s `APR` is also a perpetual's base, so a spot notice titled «(APR)» is silent — APR is off the list, its contract's own notice names `APRUSDT`, which still alerts, and A3 dates its delisting; the next TZ that opens `vps/announce.py` drops `APR` from `NOISE`, which no known promotion needs alone. A contract notice reads the record's `body`, and the record carries one — the run of 08.10 read the collateral notice's from it (`analyst/log/2026-10-08.md`, line 167). |
| The watcher has no calendar and no regime input | **open — the fields exist since `ANALYST-INSTRUCTIONS.md` `2026-10-09-a`; the watcher does not read them yet** | the methodology edit that splits the hunter (row «One agent executes the whole methodology in one run»). `analyst/state.json` v2 stores no regime boundary — `# BTC` computes the critical level and its touch probability on every run and keeps neither — and a `horizon` entry carries a date with no class and no minute, so «a regime boundary crossed» and «a run around each class-B print» name objects with nothing to compute them from (inv. 58). Both are additive fields within v2 (methodology §11), written by the run that computes them, and the watcher reads them from the tree like the engine. **Until they exist TZ-54's watcher acts on the exchange alone** — the announcement stream and `exchangeInfo`'s dated listing state — and since the owner's decision of 03.10.2026 it alerts and starts no run, so these fields, once they exist, time an alert and never a run (row «The assistant's build sequence»). The one class-B publisher measured answering the VPS is the Federal Reserve's calendar (TZ-53, E2), while `bls.gov` refuses it (row «`bls.gov` dates the week's largest print and refuses this machine»), so a print-timed alert needs the hunter's calendar first. **At `2026-10-09-d` both fields exist:** every horizon entry the hunter adds or re-reads carries `cls` and `t`, and the trader writes `regime` — `bull`, `bear`, `hot` and `cold` at the freeze — on every run (methodology §11). What remains is the watcher reading them, a TZ against `vps/exchange.py`, and an alert stays an alert: it starts no run (row «The assistant's build sequence») |
| Six sentences name the Shortcut as the only producer and the Boss as the only trigger | **open — recorded 01.10.2026** | the merge that enables the run unit — TZ-55's, when its run fits; TZ-54's merge enabled neither the writer nor the run — then one Architect edit of `ANALYST-INSTRUCTIONS.md` §5 and of this map's §1 and §11. True while the VPS writer and the run unit are not in effect, false from that merge (inv. 50): methodology §5 — «the only network in this system that Binance answers», «the same calls, the same payload, the same producer» and «is written by the Boss's Shortcut and by nothing in this engine»; this map's §1 — the analytical engine's row «Boss-triggered, in a Claude Code session»; and §11 — the writer cell «the Boss's iOS Shortcut» and «Price delivery is unchanged regardless». **None of them changes what a run does** — the gate reads `ts` and never the writer (inv. 51) — which is why they are repaired after the merge and not before it: a sentence describing a writer that is not yet in effect is the same defect pointed the other way |
| A catalyst's age never reached the answer | **closed by `ANALYST-INSTRUCTIONS.md` `2026-10-05-a`** | the first run under it that publishes an object resting on a dated event: its clause read against the record, the search and the candle in its appendix (methodology item 109). The answer of 04.10, 20:44 Tbilisi, printed the XRP amendment's activation on 09.10 and not the publication of that date — its majority on 25.09 at 14:46Z, which the run of 25.09 had found three and a half hours later — and the owner asked on 05.10.2026 to see how fresh a catalyst is, so that he never boards the last car of a move. The publication may be dated by any dated record, because it backs no level; the move is read from `fapi.binance.com`'s klines on the coin's own perpetual and stands behind no level either (§11) |

**Standing decisions.** The universe is closed at 30 and opens only on an owner
decision — it was 28 from June 2026 to 03.09.2026 (inv. 2, 59) · weights are never tuned ·
the
directional layer is closed at the current evidence level: the machine owns risk,
sizing, honesty and geometry, the human owns direction via catalysts and REVIEW · the
analytical engine is one system inside this repository: it gains roles, never a second engine or a
second project, and it has exactly one decision-maker (owner's objective of 28.09.2026) · it places no
order on the exchange until its gate opens (§10).

---

## 11. Analytical engine — `analyst/**`

**The Claude Code Executor carries two roles.** Role 1 implements an approved TZ;
role 2 is the operational market-analysis engine. One process, one contract
(`EXECUTOR-INSTRUCTIONS.md`), two roles, never both in one turn. The methodology —
what is analysed, what is published, in what shape, under what data discipline — is
`ANALYST-INSTRUCTIONS.md`, which stands to role 2 exactly as this map stands to role 1:
binding text the Executor reads and never writes.

**Since methodology `2026-10-09-a` role 2 runs as one session with two subagents of its own** — the
trader, the one decision-maker, launches a hunter after the freeze and a sheriff after the book is
composed, each reading only its own part of the methodology (methodology §15, contract v27), and both in the
foreground since `2026-10-09-b` (contract v28). Neither is a
role of the contract: both run inside role 2's turn, and neither commits.

**This section states what the engine IS.** It carries no analytical rule, because a
rule written here and in the methodology would eventually be written two ways.

| Path | Written by | Retention |
|---|---|---|
| `analyst/live.json` | the Boss's iOS Shortcut | one copy, replaced |
| `analyst/owner.json` | Architect → Boss upload | one copy, replaced |
| `analyst/state.json` | role 2 | one copy, replaced |
| `analyst/log/YYYY-MM-DD.md` | role 2 | **permanent, immutable** |
| `analyst/log/YYYY-MM-DD.hunt.md` | role 2 — the run's hunter (methodology §16) | **permanent, immutable** |
| `analyst/live-gate.sh` | role 1, under a TZ | live |

**The engine performs no network fetch for PRICES, and that is a measurement rather than
a preference (TZ-16).** Measured in the cloud sandbox, every market host was refused at
CONNECT — `fapi.binance.com`, CoinGecko, `gist.githubusercontent.com`, and
`data-api.binance.vision` **which inv. 24 permits from a runner**. The runner's egress and
a session's egress are different networks and neither may be assumed from the other. **Since
methodology `2026-09-30-b` one market read is in the method, since `2026-10-05-a` two, and since
`2026-10-08-a` four, none a price behind a level:** item 90's move for the five declared perpetuals, from
`fapi.binance.com`'s daily klines; item 109's move since a catalyst became public, from the
same host's klines on the coin's own perpetual; each verdict's scale, from the daily klines of BTC and of the
coins the verdicts name; and the exchange's listing state, `fapi/v1/exchangeInfo` (§10). **Since
`2026-10-08-a` the run also reads one file outside its tree:** the announcement stream's record,
`/var/lib/crypto-auto/announcements.jsonl`, written `0640` by `vps/announce.py` in a directory of the group the
run unit joins. **Since `2026-10-09-a` a fifth class, read by the hunter:** the exchange's positioning
statistics — `futures/data/openInterestHist`, `topLongShortPositionRatio` and
`globalLongShortAccountRatio` at four hours over thirty days, and `fapi/v1/fundingRate` — on the same host,
none a price behind a level, each coin classed against its own month (§10, row «The positioning classes
are unmeasured»).

**Since 2026-08-30 the engine runs on a Vultr VPS, and the egress was re-measured there
rather than inherited (inv. 52).** The sandbox proxy is gone and the picture is different
by host class, not uniformly better: `federalreserve.gov` open · `bls.gov` and
`defillama.com` serve their APIs and refuse the rendered page with 403 · `farside.co.uk`
answers a managed bot challenge · ETF issuer product pages refuse the VPS — BlackRock and
ARK 403, Grayscale 429, Bitwise 200. **A 403 on a page whose API answers is not a closed
lane**, which is why the methodology names the machine-readable endpoint as the primary
artifact. **15.09.2026 added two readings of this machine, both carried in §10.** Every host
TZ-45 probed for the coin horizon answered except one that does not resolve, and none refused
— fifteen Discourse forums, `api.github.com`, `gitlab.com`, a Medium feed, `eth.blockscout.com`
and Binance's announcement list — while the five Senate and `congress.gov` publishers the
analysis run of the same date needed all refused it. **25.09.2026 added TZ-52's readings of this machine**
— the Executor's, as its report describes it: Ubuntu 24.04.4, `curl 8.5.0`, no proxy and no curl
configuration. Every protocol site it asked answered except where a managed challenge or
`robots.txt` refused — every Medium publication page, `arbitrum.io`, LinkedIn, `forum.skyeco.com` —
and four reporter feeds, Upbit's API, the Federal Register's API, SEC's search for a declared
client only and `fapi.binance.com`'s klines on all five declared perpetuals answered (§10).

**`tokenomist.ai` and `cryptorank.io` were measured by TZ-22 and both answer this
machine.** Apex and `www` resolve to Cloudflare, TLS completes against a valid
certificate, the rendered page returns 200 carrying its own product title and none of
the four managed-challenge markers, and `robots.txt` serves. Their DATA APIs are
credentialed and this repository holds no key: `api.tokenomist.ai/v4/token/list` answers
401 `x-api-key not found`, and `api.cryptorank.io` declares `X-Api-Key` as its only
security scheme across 76 paths, with `/v3/documentation-json` and `/v3/ping` as the
keyless exceptions — `/v3/ping` returns a server clock and no data. **An open lane is
neither an extractable figure nor a permission, and TZ-22 measured only the lane.** Both
pages are JS-hydrated applications, so whether a figure can be read out of the served
HTML without executing JavaScript is untested; and `tokenomist.ai/robots.txt` carries a
directive group naming `ClaudeBot`, `Claude-SearchBot` and `anthropic-ai` whose contents
that run did not quote. The run's own client was `curl/8.5.0`, which the `*` group admits,
so the measurement is clean — but a methodology naming the host would be admitting it for
an agent the host addresses by name.

**TZ-24 closed both questions, and the answer is no.** Permission: `tokenomist.ai` grants
`Allow: /` to a group naming `ClaudeBot`, `Claude-SearchBot`, `anthropic-ai` and `Claude-User`;
`cryptorank.io` names no agent beyond `*`. Extractability: both pages DO carry a
machine-locatable payload without JavaScript — an RSC flight stream of 352 138 B and a
`__NEXT_DATA__` block of 43 757 B — **and neither payload contains the data a sweep needs.** The
unlock-events page serves the boolean `isUnlockScheduleEmpty` and no tranche array, and nine
schedule key names return zero occurrences across the whole document; a fund's rounds page serves
dated round records whose element schema has no amount, valuation or investor key. The figures
arrive client-side from the credentialed API that answered 401. **A lane can be open, permitted
and parseable and still be closed**, and that is why the two verdicts were kept apart: a single
`usable` label would have named both hosts in §6a and every sweep would have located a payload,
found nothing in it, and reported an empty result indistinguishable from a quiet market.
`ANALYST-INSTRUCTIONS.md` §6a recorded the closure so no run re-probed them.

**25.09.2026 reopened one of the two, on a page TZ-24 did not probe.** The Architect's session —
not this machine — requested the coin page `tokenomist.ai/<id>` for the thirty CoinGecko ids of
`TOKENS`: the site carries 22 under exactly those ids, and its served HTML states each one's next
cliff in one sentence, or that the coin is fully unlocked; the eight it does not carry answer 200
with neither. `ANALYST-INSTRUCTIONS.md` `2026-09-30-c` reads that sentence per coin on every run at
`reported` — a class that closes a side and opens none — and its first read on this machine,
26.09.2026T08:31:33–08:32:01Z, answered 200 on all thirty and reproduced the Architect's reading to
the coin; `2026-09-30-d` extends the same read to the book's candidates and to every book cliff a
hit dates. `cryptorank.io` and the unlock-events page stay closed (§10). **07.10.2026 closed the coin page too, by the host's own policy:** every page and `robots.txt` answered 403 to the run of that evening, refusing automated access and naming the host's paid API, and `2026-10-08-a` moves the lane to DefiLlama's `emissionsIndex` (§10).

Price delivery is unchanged regardless: `analyst/live.json` reaches the engine
through the Boss's Shortcut and the working tree, and no measurement of this machine
reopens that. The one surviving route to the payload was scraping a rendered Gist HTML page;
it was refused as a transport, because a presentation detail with no compatibility
promise fails by returning something rather than by erroring, and a price behind a
stop may not depend on that. The Shortcut's collection is unchanged — same calls, same
network, same payload — and only the destination moved, so the engine reads a file in
its own tree and the transport leaves the design instead of being hardened.

**Since 01.09 the payload carries two arrays, and the second one closed the outside-list
lane the aggregators could not.** `c` is the coin universe plus BTC — 28 plus BTC when
the Shortcut was written, 30 plus BTC since 03.09.2026, when the Boss updated the producer
(§10) — validated row
by row at the gate; `x` is the whole Binance USDⓈ-M perpetual book — 754 rows carrying
symbol, last, 24-hour high and low, change and turnover. **Membership of `x` and
tradability on a perpetual are the same fact**, so `ANALYST-INSTRUCTIONS.md` §3B now
prices an outside-list candidate from it and the two-source web rule is retired: nothing
is left for that rule to govern, because a coin absent from `x` was never publishable.
The lane is filtered on the symbol and the turnover — USDT quote, no `_` (dated and
COIN-M contracts), a nameable crypto underlying, and $10M of 24-hour turnover — and no
name list is written into the methodology, because a typed list is a second universe
(inv. 21). **The payload is read by command and never opened**: it is several hundred
kilobytes, a run needs a handful of rows, and a reader that pulls the whole artifact in
to reach thirty lines has taken the artifact instead of what it needed. The width is not
free — each snapshot is a new ~280 KB blob in git history, which §10 carries as an
archival question and never as a reason to narrow the payload.

**The freshness window is two-sided:** `LIVE_SKEW_SEC = 120` s below, `LIVE_MAX_AGE_SEC
= 900` s above, one declaration site each, both breaches sharing exit 3 and naming their
side in stderr. The floor exists because the producer is a phone and the reader is not:
a one-sided ceiling passes every payload stamped in the future, which is the failure the
check exists to prevent arriving through the check itself (inv. 51).

**That window is a GATE budget and was never a RUN budget, and the two were conflated
until 31.08.** The gate reads a file once; a run reads state, freezes geometry, hunts
catalysts, sweeps, composes, writes state and log, commits, and sends. Methodology §5
measured price age at the moment of SENDING, so a run doing the second job honestly
arrived at composition with the ceiling spent — and its only other exit, re-pulling the
price, does not exist for an engine whose payload is written by the Boss's Shortcut.
Since `ANALYST-INSTRUCTIONS.md` revision `2026-09-01-a` the stage order is binding and
levels are FROZEN at gate step 4, before any search: the anchoring price is fixed with
them, every later stage is subtractive, and an aged freeze demotes `СЕЙЧАС` to `ЖДАТЬ`
instead of deleting the level. **Revision `2026-09-01-d` removed that demotion too, and
the reason is inv. 57.** The demotion rested on no measurement: the engine cannot re-pull,
so a later moment compares the same number against a longer wait and can only subtract.
The `СЕЙЧАС`/`ЖДАТЬ` split is now decided once, at the freeze, and the row prints the
frozen price beside the zone — a dated claim the Boss checks against his own screen in a
second. **Nothing about the constant changed, in either revision.** What changed twice is
the object it was applied to, and the second correction is what made the first one hold:
after `-a` a thorough run still emptied its own best-trades section, because four sweeps,
a catalyst hunt and composition do not fit in fifteen minutes and were never meant to.

**The Boss's production trigger is a third spelling, not a third mode.** `ANALYZE
TODAY'S CRYPTO MARKET AND DETERMINE THE STRATEGY FOR ENTERING ALTCOINS ON BINANCE
FUTURES.` selects role 2 and runs methodology §2's skeleton identically to `Анализ
крипторынка`. It lives in `EXECUTOR-INSTRUCTIONS.md` §4 and in the methodology's §0, and
the pair moves together: §4 is the only place a role is selected, so a string present in
one file and absent from the other is an unrecognised trigger that stops the run.

**`analyst/live-gate.sh` is the blocking gate and returns an exit code** (inv. 29),
one distinct class per failure: unreadable or unparseable 2 · stale 3 · `n ≠ len(c)` 4
· a `tokens[]` symbol absent 5 · a price that does not cast to a finite positive 6 ·
zero rows compared 7 (inv. 22) · `tokens[]` unreadable 8. A non-zero exit removes
every price level from the answer and nothing else; the regime, the catalysts and the
verdict are still produced. The universe is cut from `tokens[]` at run time and never
typed (inv. 21), and the selftest's fixtures are generated from that same parse, so a
change to `tokens[]` cannot leave the selftest behind.

**The cast is explicit because `jq` is not safe on this payload.** Every value except
top-level `n` is a JSON string, and `jq '.p|tonumber'` accepts `"Infinity"` and
`"1e999"` as finite-looking positives while `"NaN"` passes a naive range check *by
failing it*: `NaN > 0` and `NaN <= 0` are both false. The validator uses
`float()` with `math.isfinite(x) and x > 0`, which rejects all four.

**The gate is wired into `bench.yml` as step 13** (inv. 37) — `--selftest`, 14
known-answer cases, 40 assertions, offline (12 failing × 3 + 2 passing × 2). That step, not a fingerprint entry, is why
`live-gate.sh` is trustworthy after the session that wrote it ended; adding the script
to the `## 0` table would put a hash in every TZ header for a file whose behaviour is
already under a control. **`bench/backtest_guard_bench.py` is step 14 on the same argument**
and is likewise absent from that table (§0).

**The two workflows treat this tree differently, on purpose.** `main.yml` ignores
`analyst/**` whole: no file here, script included, is a reason to start the bot, redraw 30
coins through CoinGecko and rewrite the live Gist. Before TZ-17 it ignored none of them, so
the engine saving its own state did exactly that, with a retry doubling the draw.
`bench.yml` ignores FOUR paths in this tree and only three of them are the analyst's:
`analyst/state.json`, `analyst/live.json`, `analyst/log/**`. `analyst/live-gate.sh` is
deliberately absent because it is code whose control is step 13, and the wider form excluded
the gate script from its own gate (inv. 53, measured on the runner: run `33254342462`, a push
carrying only the script, which started nothing under the old filter). `analyst/README.md`
needs no entry; `'**.md'` covers it.

**The fourth path is `analyst/owner.json` and it breaks the rule the other three follow.**
It is written by the Architect and pushed by the Boss, so it is neither the analyst's data nor
a control — and every upload of it fired the whole gate. TZ-30 added it as an exact literal
while opening the workflow for another reason (inv. 52), and **the proof inv. 53 demands was
taken on the runner 06.09.2026**: a push carrying only that file started the Pages build and
no `Bench gate`. The reading is what makes the entry a control; the literal alone was a
reading of the pattern, which is the thing inv. 53 refuses.

**That narrowing creates a coupling and it is deliberate.** Any NEW file the analyst writes
must be added to `bench.yml`'s list, or it starts a 14-step gate on every analysis run.
Making the coupling mechanical would need the written set to exist as data that both the
filter and a bench read, i.e. a second list of three paths — rejected as worse than the
coupling it removes (inv. 20). The failure is loud and costs runner minutes, which is the
direction to fail in.

**Since TZ-23 `main.yml` filters `push` with a `paths` allow-list and no `paths-ignore`.**
The two cannot coexist on one event, so adopting the list DELETED the exclusions rather
than joining them — an allow-list needs none, because everything unnamed is already out.
The list is two literal paths, `main.py` and `.github/workflows/main.yml`, derived from
`main.py`'s source at execution time and never typed: the bot opens no file, imports no
repository module and reaches CoinGecko and the Gist over HTTP only, so `catalysts.json`,
`journal/**` and every future unnamed path now start nothing. `workflow_dispatch` is
unfiltered, so the phone's 17 daily runs sit outside this filter entirely and no list
written here can stop them — that is the whole safety argument and it is checked, not
assumed. **The coupling now runs the other way and into the worse direction:** the list
must GROW the first time the bot learns to read a repository file, and a forgotten entry
withholds a run quietly while `coeffs.json` ages, where inv. 53's forgotten entry only
burned runner minutes loudly. No bench can hold it — a control over a trigger would have
to observe the trigger, and `main.yml`'s `push` filter is unreachable from any `claude/**`
push — so the coupling is carried by the Russian comment beside the list and nowhere
else.

**`analyst/owner.json` is the owner's channel into the engine, and it exists because the
Boss does not talk to the engine.** He addresses the Architect; the role table forbids
making him relay a technical fact between the two systems. Methodology §11 nevertheless
declared a position «on «вошёл в SOL ЛОНГ»» — a clause inherited from the chat-era engine,
where such a sentence could actually be said. **With no channel, the relay was the only
route the information had, and the Architect took it**, telling the Boss to inform the
engine himself. A rule with no mechanism behind it is broken by whoever needs the
information to move. The file is written by the Architect, uploaded by the Boss on the
single existing channel, read at gate step 3 and never written by the engine (§13): an
input a system can edit has stopped being an input. Its content has two
opposite standings — the owner's own facts, `capital` and the `risk` policy he delegated on 30.09.2026,
taken as given, and `vectors`, hypotheses with no authority at all, resolved against a primary or
reported unresolved,
because an owner's assertion is not a source (inv. 39) and the place that rule must hold
hardest is the place it is least comfortable.

**Two states are permanent and different.** `analyst/state.json` is the working set —
one copy, replaced every run, carrying only what is currently true. `analyst/log/**`
is evidence — written once, never reopened, in the standing of a journal record
(inv. 38). Merging them would make the working set grow without bound and the evidence
rewritable, which is the pairing §3.13 already uses.

**The engine never writes `catalysts.json`** (inv. 39). That registry vetoes the
board's verdict and its `confirmed` flag is the compensating control for an
externalised file; an analysis run able to edit it would turn one file write into a
silent change to production behaviour. A discovered event that deserves an entry is a
line in the day log, and the Architect turns it into a TZ or does not.

**The state was seeded empty, never imported.** The Gist copy written by the Shortcut
from a printed chat block carries 211 pairs of typographic quotes and an abbreviated
item schema; it fails `json.loads` at character 1, and an unparseable state file stops
an analysis run outright. Importing it would have stopped every future run — a file
that exists, looks right and is refused.
