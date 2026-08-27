# Validation Change Log — Hemanth Ranam TradingView Suite

## [Phase 2 Validation Updates] - 2026-08-27

### 1. Strategy Signature Standardization
* **Change**: Added `process_orders_on_close = true` to all 5 strategy declarations in `src/strategies/`.
* **Rationale**: Enforces deterministic order fills on the bar close of confirmed signals rather than waiting for next bar open, eliminating intrabar slippage anomalies in backtesting.

### 2. Execution Friction & Robustness Framework
* **Change**: Integrated 3-tier cost modeling (Scenario A: Reference, Scenario B: Realistic 0.05%, Scenario C: Stress 0.15%) into `tests/backtest_engine.py`.
* **Rationale**: Ensures short-term intraday strategies remain positively expectant under realistic real-world commissions and spreads.

### 3. Non-Repainting & Lookahead Audit
* **Change**: Documented line-by-line verification of `request.security(..., barmerge.lookahead_off)` with historical `close[1]` bar indexing in `docs/NON-REPAINTING-AUDIT.md`.
