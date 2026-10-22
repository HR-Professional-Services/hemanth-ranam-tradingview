# HR TradingView — Product Catalog

**Document Status**: Canonical Release Reference  
**Domain**: Trading Systems (HR TradingView / ScaleNova / Hemanth Ranam)  
**Last Updated**: 2026-10-22  
**Verification Baseline**: Python Suite Passed (55/55), Native TradingView Compilation Pending, Backtests Pending

---

## 1. Commercial Product Portfolio

The HR TradingView commercial suite consists of four independently implemented, production-grade strategy families. Each family provides a pair of standalone Pine Script v6 scripts:
1. **Commercial Indicator** (`src/indicators/`): Chart visualization, real-time trigger markers, dashboard diagnostics, and alert emission.
2. **Commercial Strategy** (`src/strategies/`): Dedicated TradingView Strategy Tester implementation with historical backtesting parameters, realistic friction modeling, and execution rules.

```
HR TradingView Commercial Suite
├── HR-PRD-01: EMA Trend Pullback Pro
│   ├── Indicator: src/indicators/HR_EMA_Pullback_Indicator.pine
│   └── Strategy:  src/strategies/HR_EMA_Pullback_Pro.pine
├── HR-PRD-02: Liquidity Sweep Reversal Pro
│   ├── Indicator: src/indicators/HR_Liquidity_Sweep_Indicator.pine
│   └── Strategy:  src/strategies/HR_Liquidity_Sweep_Strategy.pine
├── HR-PRD-03: Volatility Expansion Breakout Pro
│   ├── Indicator: src/indicators/HR_Volatility_Breakout_Indicator.pine
│   └── Strategy:  src/strategies/HR_Volatility_Breakout_Strategy.pine
├── HR-PRD-04: Market Structure Momentum Pro
│   ├── Indicator: src/indicators/HR_Market_Structure_Indicator.pine
│   └── Strategy:  src/strategies/HR_Market_Structure_Strategy.pine
└── HR-PRD-05: Adaptive Market Regime Pro (DEFERRED-RESEARCH-CANDIDATE)
    └── Research lab candidate under multi-regime evaluation.
```

---

## 2. Product Specifications

### HR-PRD-01: EMA Trend Pullback Pro
- **Indicator Path**: `src/indicators/HR_EMA_Pullback_Indicator.pine`
- **Strategy Path**: `src/strategies/HR_EMA_Pullback_Pro.pine`
- **Authoritative MT5 Reference**: `02_TREND_PULLBACK/TREND_PULLBACK_CONTINUATION_EA.mq5`
- **Core Edge**: Trend-following continuation capitalizing on pullbacks within strongly aligned dynamic moving averages.
- **Signal Logic**:
  - Intraday 9 EMA > 21 EMA > 200 EMA (Long) or 9 < 21 < 200 (Short).
  - Higher-timeframe 200 EMA trend filter (1-hour timeframe, historical closed bar `[1]` with `lookahead_off`).
  - Pullback condition: Price touches or penetrates 9 or 21 EMA zone without closing beyond 50 EMA.
  - Resumption confirmation: Strong reversal/expansion candle closing back in trend direction.
  - ATR volatility filter: 14-period ATR exceeding minimum threshold.
- **Execution & Exits**:
  - Stop Loss: 1.5 × ATR from entry.
  - Take Profit: 1.5R (1.5 × Stop Loss distance).
  - Position Sizing: 1.0% equity risk baseline (`default_qty_type = strategy.percent_of_equity`, `default_qty_value = 1.0`).
- **Target Assets**: `XAUUSD`, `US500`, `EURUSD`.
- **Target Timeframes**: Primary 15M (with 1H HTF confirmation).
- **Status**: `LOCAL-VALIDATION-PASSED` | `NATIVE-COMPILATION-PENDING` | `BACKTEST-PENDING`.

---

### HR-PRD-02: Liquidity Sweep Reversal Pro
- **Indicator Path**: `src/indicators/HR_Liquidity_Sweep_Indicator.pine`
- **Strategy Path**: `src/strategies/HR_Liquidity_Sweep_Strategy.pine`
- **Authoritative MT5 Reference**: `01_LIQUIDITY_SWEEP/LIQUIDITY_SWEEP_REVERSAL_EA.mq5`
- **Core Edge**: Mean-reverting institutional liquidity sweeps of key swing highs/lows and false breakout traps.
- **Signal Logic**:
  - Dynamic swing lookback: 24 bars to identify key liquidity pools (swing highs/lows).
  - Sweep verification: Price pierces swing boundary by at least 0.2 ATR (minimum displacement threshold) to trigger stops.
  - Rejection & Reversal: Price fails to hold beyond boundary and closes back inside the previous swing range with an exhaustion wick.
  - Momentum confirmation: RSI out of extreme zone or divergence.
- **Execution & Exits**:
  - Stop Loss: Placed beyond the sweep wick extreme + 0.2 ATR buffer.
  - Take Profit: Fixed 2.5R reward-to-risk ratio.
  - Position Sizing: 1.0% equity allocation baseline.
- **Target Assets**: `XAUUSD`, `EURUSD`.
- **Target Timeframes**: Primary 15M.
- **Status**: `LOCAL-VALIDATION-PASSED` | `NATIVE-COMPILATION-PENDING` | `BACKTEST-PENDING`.

---

### HR-PRD-03: Volatility Expansion Breakout Pro
- **Indicator Path**: `src/indicators/HR_Volatility_Breakout_Indicator.pine`
- **Strategy Path**: `src/strategies/HR_Volatility_Breakout_Strategy.pine`
- **Authoritative MT5 Reference**: `03_VOLATILITY_BREAKOUT/VOLATILITY_EXPANSION_BREAKOUT_EA.mq5`
- **Core Edge**: Explosive directional movement following low-volatility consolidation boxes.
- **Signal Logic**:
  - Squeeze detection: 20-bar consolidation box height strictly <= 1.8 × ATR.
  - Breakout confirmation: Completed bar closing outside the box boundaries.
  - Volume expansion filter: Bar volume exceeding 1.2 × 20-period volume SMA (or tick volume proxy).
  - Directional momentum: Fast EMA slope confirmation.
- **Execution & Exits**:
  - Stop Loss: Placed at the consolidation box midpoint or opposite boundary.
  - Take Profit: 2.5R target ratio.
  - Position Sizing: 1.0% equity allocation baseline.
- **Target Assets**: `USTEC` (`US100`), `XAUUSD`.
- **Target Timeframes**: Primary 15M.
- **Status**: `LOCAL-VALIDATION-PASSED` | `NATIVE-COMPILATION-PENDING` | `BACKTEST-PENDING`.

---

### HR-PRD-04: Market Structure Momentum Pro
- **Indicator Path**: `src/indicators/HR_Market_Structure_Indicator.pine`
- **Strategy Path**: `src/strategies/HR_Market_Structure_Strategy.pine`
- **Authoritative MT5 Reference**: `04_STRUCTURE_MOMENTUM/MARKET_STRUCTURE_MOMENTUM_EA.mq5`
- **Core Edge**: Directional trend initiation following structural Break of Structure (BOS) or Change of Character (CHoCH).
- **Signal Logic**:
  - Fractal pivots: 3-bar left and 3-bar right fractal swing highs and lows (3-bar confirmation lag strictly respected; non-repainting).
  - Structure transition: Confirmed close beyond preceding pivot high (bullish BOS) or pivot low (bearish BOS).
  - Momentum filter: RSI > 53.0 for bullish BOS, RSI < 47.0 for bearish BOS.
  - Trend alignment: 200 EMA macro filter.
- **Execution & Exits**:
  - Stop Loss: Placed at the most recent swing low (Long) or swing high (Short) + 0.3 ATR buffer.
  - Take Profit: 2.4R target ratio.
  - Position Sizing: 1.0% equity allocation baseline.
- **Target Assets**: `US500`, `XAUUSD`.
- **Target Timeframes**: Primary 15M, 1H.
- **Status**: `LOCAL-VALIDATION-PASSED` | `NATIVE-COMPILATION-PENDING` | `BACKTEST-PENDING`.

---

## 3. Deferred Research Candidates

### HR-PRD-05: Adaptive Market Regime Pro
- **Status**: `DEFERRED-RESEARCH-CANDIDATE`.
- **Description**: Multi-regime classification model combining ADX trend strength, ATR volatility clustering, and Kaufman Adaptive Moving Average (KAMA). Excluded from the Phase 7 commercial release pending empirical forward testing and multi-asset regime stability verification.
