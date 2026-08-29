# analyst/

The market-analysis engine's tree. Nothing here reaches the live calculator and no commit here starts a workflow.

| File | What it is | Written by |
|---|---|---|
| `live.json` | the live Binance Futures payload | the Boss's Shortcut |
| `live-gate.sh` | the gate that reads it; exit 0 means levels may be published | the Executor |
| `state.json` | current analytical state, schema v1 | the analyst role, replaced in place |
| `log/` | one file per analysis run | the analyst role, immutable |

The log is never reopened; the state is one copy, replaced every run.

The methodology — what is analysed, published and refused — is `ANALYST-INSTRUCTIONS.md`. No rule is restated here.
