# Hemanth Ranam TradingView Strategy Suite — Change Control Register

**Purpose**: Every modification to strategy logic or parameters must be recorded here before and after the change. Undocumented modifications are prohibited.

---

## Change Control Template

```
Date:
Commit:
Strategy:
Reason:
Problem Identified:
Old Logic / Parameter:
New Logic / Parameter:
Expected Effect:
In-Sample Test Result:
OOS Test Result:
Decision: ACCEPTED / REJECTED
Approved By: Hemanth Ranam
```

---

## Change Log

### [CC-2026-001] Phase 2 — Strategy Signature Standardisation

| Field | Value |
| :--- | :--- |
| **Date** | 2026-08-27 |
| **Commit** | Phase 2 commit (see `git log`) |
| **Strategy** | ALL 5 |
| **Reason** | Enforce deterministic order execution in backtesting. Eliminate intrabar slippage anomalies. |
| **Old Logic** | Strategy declarations without `process_orders_on_close` |
| **New Logic** | Added `process_orders_on_close=true` to all 5 strategy declarations |
| **Parameter Changes** | None — execution-model property only |
| **Expected Effect** | Orders fill on confirmed bar close. Eliminates any phantom fills at intrabar prices during historical replay. |
| **Backtest Result** | No logic change — execution timing alignment only |
| **OOS Result** | Pending native TradingView verification |
| **Decision** | ✅ ACCEPTED |

---

*New change entries must be appended above this line.*
