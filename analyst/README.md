# analyst/

The market-analysis engine's tree. Nothing here reaches the live calculator and no commit here starts a workflow.

| File | What it is | Written by |
|---|---|---|
| `live.json` | the live Binance Futures payload | the Boss's Shortcut |
| `live-gate.sh` | the gate that reads it; exit 0 means levels may be published | the Executor |
| `state.json` | current analytical state, schema v1 | the analyst role, replaced in place |
| `log/` | one file per analysis run | the analyst role, immutable |
| `paper/` | the copy-trading paper test's record (TZ-64); never an input to an analysis run | `vps/paper.py` on the VPS, immutable |
| `press/` | each run's numbers computed before the model starts (`<stem>.json` the record, `<stem>.md` the brief) and what its session spent (`<stem>-usage.json`, TZ-87); never an input to a later run | `vps/press.py` and `vps/run.py` on the VPS, immutable |
| `score/` | every closed trade of the two ledgers the gate reads, copied as written (`cards/`, `held/`, TZ-87) | `vps/run.py` on the VPS, immutable |

The log is never reopened; the state is one copy, replaced every run.

The methodology — what is analysed, published and refused — is `ANALYST-INSTRUCTIONS.md`. No rule is restated here.
