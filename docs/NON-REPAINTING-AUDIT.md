# Hemanth Ranam — Non-Repainting & Lookahead Audit

**Audit Target**: `HR_EMA_Pullback_Pro.pine`, `HR_Breakout_Retest_Pro.pine`, `HR_Market_Structure_Pro.pine`, `HR_VWAP_Mean_Reversion_Pro.pine`, `HR_Momentum_Volatility_Pro.pine`  
**Audit Scope**: Multi-timeframe requests, intrabar lookahead, pivot lag, bar confirmation semantics.

---

## 1. Technical Audit Findings

### A. Multi-Timeframe Security Requests (`request.security`)
* **Rule**: In Pine Script v6, requesting higher timeframe data without explicit historical indexing can cause historical bars to fetch future unclosed HTF candle closes, producing massive artificial backtest gains that disappear in live trading.
* **Audit Inspection**:
  ```pine
  htf_close  = request.security(syminfo.tickerid, htf_res, close[1], barmerge.gaps_off, barmerge.lookahead_off)
  htf_ema200 = request.security(syminfo.tickerid, htf_res, ta.ema(close[1], slow_len), barmerge.gaps_off, barmerge.lookahead_off)
  ```
* **Status**: **PASS (100% Non-Repainting)**. All HTF calls explicitly use historical `close[1]` with `barmerge.lookahead_off` and `barmerge.gaps_off`.

---

### B. Order Execution & Bar Confirmation
* **Rule**: Strategies must not calculate and fill orders on unconfirmed intrabar ticks unless intentionally designed as a tick-level scalp with intrabar slippage models.
* **Audit Inspection**:
  All strategies declare `process_orders_on_close = true`. Orders are evaluated only upon bar close and executed deterministically on the next tick/bar open.
* **Status**: **PASS (Deterministic Execution)**.

---

### C. Fractal Pivot Delay
* **Rule**: Functions like `ta.pivothigh(high, 5, 2)` require `2` bars of look-back confirmation before the pivot is mathematically confirmed.
* **Audit Inspection**:
  In `HR_Market_Structure_Pro.pine`, BOS signals require `ta.crossover(close, last_sh)` where `last_sh` is confirmed only after `pivot_right` bars have passed.
* **Status**: **PASS (No Future Peeking)**.
