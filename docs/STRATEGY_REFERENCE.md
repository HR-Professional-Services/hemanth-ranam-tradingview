# HR TradingView — Strategy Reference Manual

**Domain**: Quantitative Strategy Engineering (HR TradingView / ScaleNova / Hemanth Ranam)  
**Pine Script Version**: v6  
**Execution Paradigm**: Closed-Bar Confirmation (`process_orders_on_close = true`)  
**Last Updated**: 2026-10-22

---

## 1. Architectural Philosophy & Signal Contract

All commercial trading strategies in this repository follow strict institutional execution rules:
1. **Zero Repainting Guarantee**: All multi-timeframe requests utilize `barmerge.lookahead_off` with closed-bar historical indexing `[1]`.
2. **Closed-Bar Execution**: Signals are evaluated and confirmed at bar close (`barstate.isconfirmed`). Orders execute at the open of the following bar.
3. **ATR-Based Structural Risk**: Stops are derived from market volatility (ATR) and swing extremes rather than arbitrary fixed-pip amounts.
4. **Friction Transparency**: Commission (0.02%) and slippage (2 ticks) are modeled directly in the backtest configuration.

---

## 2. Strategy 1: HR EMA Trend Pullback Pro (`HR-PRD-01`)

### Implementation File
- `src/strategies/HR_EMA_Pullback_Pro.pine`

### Mathematical Foundation
- **Fast EMA**: 9 periods on chart timeframe.
- **Medium EMA**: 21 periods on chart timeframe.
- **Baseline EMA**: 200 periods on chart timeframe.
- **HTF Baseline EMA**: 200 periods requested from 1-hour timeframe via:
  ```pinescript
  htf_ema200 = request.security(syminfo.tickerid, "60", ta.ema(close, 200)[1], lookahead = barmerge.lookahead_off)
  ```
- **Volatility Metric**: `ta.atr(14)`.

### Entry Conditions
- **Long Entry**:
  1. Primary trend alignment: `close > ema200` AND `ema9 > ema21` AND `ema21 > ema200`.
  2. HTF confirmation: `close > htf_ema200`.
  3. Pullback criterion: `low <= ema21` (or `low <= ema9`) while `close >= ema50`.
  4. Resumption candle: Bullish closing bar (`close > open`) confirming rejection of the EMA zone.
  5. ATR filter: Current ATR exceeds 0.8 × 50-period ATR moving average.
- **Short Entry**:
  1. Primary trend alignment: `close < ema200` AND `ema9 < ema21` AND `ema21 < ema200`.
  2. HTF confirmation: `close < htf_ema200`.
  3. Pullback criterion: `high >= ema21` (or `high >= ema9`) while `close <= ema50`.
  4. Resumption candle: Bearish closing bar (`close < open`) confirming downward expansion.
  5. ATR filter: Current ATR exceeds 0.8 × 50-period ATR moving average.

### Exits & Risk Model
- **Stop Loss**: Entry Price ± `1.5 * ATR(14)`.
- **Take Profit**: Entry Price ± `1.5 * (Stop Distance)` (1.5R ratio).
- **Position Sizing**: 1.0% equity allocation (`strategy.percent_of_equity`, value 1.0).

---

## 3. Strategy 2: HR Liquidity Sweep Reversal Pro (`HR-PRD-02`)

### Implementation File
- `src/strategies/HR_Liquidity_Sweep_Strategy.pine`

### Mathematical Foundation
- **Swing High/Low**: Calculated over a 24-bar lookback period (`ta.highest(high[1], 24)` and `ta.lowest(low[1], 24)`).
- **Minimum Displacement**: `0.20 * ta.atr(14)` required beyond the swing boundary.
- **RSI Momentum**: 14-period RSI for rejection confirmation.

### Entry Conditions
- **Bullish Reversal (Sweep of Swing Low)**:
  1. Sweep occurrence: `low < swing_low` by at least `0.20 * ATR(14)`.
  2. Institutional rejection: Bar closes back above the swing low level (`close > swing_low`).
  3. Exhaustion structure: Lower wick constitutes at least 40% of the total candle range (`(math.min(open, close) - low) / (high - low) >= 0.40`).
  4. Momentum check: RSI crossing out of oversold (< 35) or demonstrating bullish divergence.
- **Bearish Reversal (Sweep of Swing High)**:
  1. Sweep occurrence: `high > swing_high` by at least `0.20 * ATR(14)`.
  2. Institutional rejection: Bar closes back below the swing high level (`close < swing_high`).
  3. Exhaustion structure: Upper wick constitutes at least 40% of the total candle range (`(high - math.max(open, close)) / (high - low) >= 0.40`).
  4. Momentum check: RSI crossing out of overbought (> 65) or demonstrating bearish divergence.

### Exits & Risk Model
- **Stop Loss**: Placed at `low - (0.2 * ATR)` for Longs; `high + (0.2 * ATR)` for Shorts.
- **Take Profit**: 2.5R target ratio (`2.5 * Stop Distance`).
- **Position Sizing**: 1.0% equity allocation baseline.

---

## 4. Strategy 3: HR Volatility Expansion Breakout Pro (`HR-PRD-03`)

### Implementation File
- `src/strategies/HR_Volatility_Breakout_Strategy.pine`

### Mathematical Foundation
- **Consolidation Box**: 20-period highest high and lowest low.
- **Box Range**: `highest(high, 20) - lowest(low, 20)`.
- **Squeeze Condition**: Box Range <= `1.80 * ta.atr(14)`.
- **Volume Expansion**: Current volume > `1.20 * ta.sma(volume, 20)`.

### Entry Conditions
- **Bullish Breakout**:
  1. Squeeze valid: Prior 20 bars met the volatility compression threshold.
  2. Range breakout: Confirmed close above the upper box boundary (`close > box_high`).
  3. Volume validation: Bar volume exceeds 1.2 × 20-period volume average.
  4. Trend confirmation: Fast EMA(9) > Slow EMA(21).
- **Bearish Breakout**:
  1. Squeeze valid: Prior 20 bars met the volatility compression threshold.
  2. Range breakdown: Confirmed close below the lower box boundary (`close < box_low`).
  3. Volume validation: Bar volume exceeds 1.2 × 20-period volume average.
  4. Trend confirmation: Fast EMA(9) < Slow EMA(21).

### Exits & Risk Model
- **Stop Loss**: Placed at the consolidation box midpoint (`(box_high + box_low) / 2.0`).
- **Take Profit**: 2.5R target ratio from entry based on stop distance.
- **Position Sizing**: 1.0% equity allocation baseline.

---

## 5. Strategy 4: HR Market Structure Momentum Pro (`HR-PRD-04`)

### Implementation File
- `src/strategies/HR_Market_Structure_Strategy.pine`

### Mathematical Foundation
- **Fractal Swing High**: 3 bars left, 3 bars right (`ta.pivothigh(high, 3, 3)`).
- **Fractal Swing Low**: 3 bars left, 3 bars right (`ta.pivotlow(low, 3, 3)`).
- **Confirmation Delay**: Pivot is confirmed strictly 3 bars after the pivot peak/trough.
- **RSI Momentum Thresholds**: Bullish threshold = 53.0; Bearish threshold = 47.0.

### Entry Conditions
- **Bullish BOS (Break of Structure)**:
  1. Price closes above the most recently confirmed fractal swing high (`close > active_pivot_high`).
  2. Macro trend alignment: `close > ta.ema(close, 200)`.
  3. Momentum filter: `ta.rsi(close, 14) > 53.0`.
  4. Duplicate signal filter: No prior active long order within the current structure wave.
- **Bearish BOS (Break of Structure)**:
  1. Price closes below the most recently confirmed fractal swing low (`close < active_pivot_low`).
  2. Macro trend alignment: `close < ta.ema(close, 200)`.
  3. Momentum filter: `ta.rsi(close, 14) < 47.0`.
  4. Duplicate signal filter: No prior active short order within the current structure wave.

### Exits & Risk Model
- **Stop Loss**: Placed at the opposing confirmed fractal pivot level (`active_pivot_low - 0.3 * ATR` for Long; `active_pivot_high + 0.3 * ATR` for Short).
- **Take Profit**: 2.4R target ratio.
- **Position Sizing**: 1.0% equity allocation baseline.
