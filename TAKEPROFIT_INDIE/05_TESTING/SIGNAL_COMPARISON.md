# TradingView Pine Script vs TakeProfit Indie v5 Signal Comparison

## Architectural Parity Overview
This document compares the native TradingView Pine Script v6 source indicators against their newly engineered TakeProfit Indie v5 counterparts.

---

### 1. HR 9 EMA Buy/Sell (Standalone)
* **Pine Reference**: Derived from `9_EMA_EA.mq5` and `HR_9_21_EMA_Sessions_SMC_LEGACY.pine`.
* **Indie Implementation**: `HR_9_EMA_BUY_SELL.indie`
* **Signal Parity**:
  - Operates independently on EMA 9 without requiring 21 or 200 EMA dependencies.
  - Three user-selectable modes: `Pure Crossover`, `Pullback & Rejection`, `Crossover with Rejection`.
  - Signal suppression state machine prevents sequential repeating BUY/SELL tags while trend persists.
  - Closed-bar confirmation on index `[1]`.

---

### 2. HR 9/21/200 EMA Pullback Pro
* **Pine Reference**: `HR_EMA_Pullback_Indicator.pine`
* **Indie Implementation**: `HR_9_21_200_EMA_PULLBACK.indie`
* **Signal Parity**:
  - EMA 9 (Fast), EMA 21 (Slow), and EMA 200 (Baseline) calculate identical exponential smoothing weights.
  - Multi-Timeframe (HTF) 1H 200 EMA trend filtering mapped to TakeProfit's native `@sec_context` and `calc_on(SecHTF, time_frame=htf_frame)`.
  - Dynamic cloud fill between 9 and 21 EMA (Green on bullish alignment, Red on bearish inversion).
  - ATR trailing stop reference guide rendered as a non-repainting risk level.

---

### 3. HR Liquidity Sweep Reversal Pro
* **Pine Reference**: `HR_Liquidity_Sweep_Indicator.pine`
* **Indie Implementation**: `HR_LIQUIDITY_SWEEP.indie`
* **Signal Parity**:
  - Dynamic BSL and SSL detection using `Highest.new(self.high, lookback_bars)` and `Lowest.new(self.low, lookback_bars)` anchored at bar `[2]`.
  - Normalized ATR penetration filters (`min_sweep_atr` to `max_sweep_atr`) ensure false breakouts are distinguished from momentum breakouts across forex, gold, and indices.
  - Minimum displacement ratio ($>= 50\%$) verifies candle wick rejection back inside the structural level.

---

### 4. HR Market Structure BOS/CHOCH Pro
* **Pine Reference**: `HR_Market_Structure_Indicator.pine`
* **Indie Implementation**: `HR_MARKET_STRUCTURE_BOS_CHOCH.indie`
* **Signal Parity**:
  - Left/right fractal pivot strength logic ($N=3$) avoids look-ahead bias by requiring 3 completed confirmation bars before locking swing high/low levels.
  - RSI(14) momentum gate ($RSI \ge 53$ for Bullish BOS, $RSI \le 47$ for Bearish BOS) identical to the MT5 EA.
  - Confirmed break requires closed bar `[1]` beyond the prior confirmed pivot level.

---

### 5. HR Volatility Expansion Breakout Pro
* **Pine Reference**: `HR_Volatility_Breakout_Indicator.pine`
* **Indie Implementation**: `HR_VOLATILITY_EXPANSION_BREAKOUT.indie`
* **Signal Parity**:
  - Consolidation squeeze detection over `compression_bars` ($N=20$) where Range $\le ATR \times 1.8$.
  - Volume filter set to optional (default `False`) for universal compatibility across Exness OTC and CFD feeds.
  - Closed-bar breakout triggers above/below the compression box with 1H HTF 200 EMA trend confirmation.
