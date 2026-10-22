# Hemanth Ranam — EMA Pullback Pro Strategy Manual

**Product ID**: `HR-PRD-01`  
**Version**: 2.0 (Pine Script v6)  
**File**: [`src/strategies/HR_EMA_Pullback_Pro.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_EMA_Pullback_Pro.pine)  
**Corresponding Indicator**: [`src/indicators/HR_EMA_Pullback_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_EMA_Pullback_Indicator.pine)  
**Corresponding MT5 EA**: `02_TREND_PULLBACK/TREND_PULLBACK_CONTINUATION_EA.mq5`  
**Last Updated**: 2026-10-22

---

## 1. Overview & Strategy Purpose

The **EMA Pullback Pro Strategy** is a quantitative, trend-following mechanical trading system designed for TradingView's native Strategy Tester. It models high-probability continuation setups within established trends by verifying triple-EMA alignment (9/21/200), higher-timeframe macro confirmation (1H 200 EMA), dynamic corridor pullbacks, volatility regime filtering, and confirmed candlestick triggers.

Unlike the companion indicator (which provides visual alerts and indicative levels), the strategy executes simulated orders, tracks open position risk, accounts for commissions and slippage, and records full trade statistics.

---

## 2. Core Methodology & Mathematical Rules

### 2.1 Trend Stacking & Baseline Bias
- **Fast Momentum EMA**: 9-period EMA.
- **Corridor Target EMA**: 21-period EMA.
- **Structural Baseline EMA**: 200-period EMA.
- **Bullish Alignment**: `EMA 9 > EMA 21 > EMA 200` and `Close > EMA 200`.
- **Bearish Alignment**: `EMA 9 < EMA 21 < EMA 200` and `Close < EMA 200`.

### 2.2 Higher-Timeframe (HTF) Macro Filter
- Evaluates the 1-hour (60m) timeframe by default.
- **Non-Repainting Standard**: Uses previous confirmed HTF bar values (`close[1]` and `ta.ema(close, 200)[1]`) with `barmerge.lookahead_off` and `barmerge.gaps_off`.
- **Longs**: Permitted only when HTF Close > HTF 200 EMA.
- **Shorts**: Permitted only when HTF Close < HTF 200 EMA.

### 2.3 Value Zone Pullback Detection
- **Corridor Penetration**: Price must retrace into the dynamic value zone between the 9 and 21 EMAs.
  - *Long Pullback*: `Low <= math.max(EMA 9, EMA 21)` and `Low >= math.min(EMA 9, EMA 21)`.
  - *Short Pullback*: `High >= math.min(EMA 9, EMA 21)` and `High <= math.max(EMA 9, EMA 21)`.

### 2.4 Candlestick Trigger & Resumption
- Requires the trigger candle to demonstrate momentum in the primary trend direction:
  - *Long Trigger*: Candle must close green (`Close > Open`), close above EMA 9, and optionally form a bullish engulfing pattern (`Close > High[1]` and `Close[1] < Open[1]`).
  - *Short Trigger*: Candle must close red (`Close < Open`), close below EMA 9, and optionally form a bearish engulfing pattern (`Close < Low[1]` and `Close[1] > Open[1]`).

### 2.5 Market Regime & Volatility Filters
- **Chop / Compression Filter**: Calculates EMA 9/21 separation normalized by ATR (`EMA Gap / ATR`). Suppresses trades when `Gap Ratio < 0.06` to prevent whipsaws during sideways consolidation.
- **Overextension Filter**: Calculates distance from price to EMA 9. Blocks late entries when `Distance / ATR > 2.5`.

### 2.6 Signal State Machine & Quality Scoring
- Uses a crossover-driven state machine (`ta.crossover(ema9, ema21)`) resetting after each trade to ensure only **one trade per trend phase**.
- A composite Quality Score (0–100) evaluates:
  - EMA Health (slope, gap, stacking): 25%
  - Structural Alignment: 20%
  - HTF Agreement: 20%
  - Candlestick Quality: 15%
  - Market Structure: 10%
  - Session Timing: 10%
- Minimum entry threshold defaults to **Score ≥ 70 (Grade A and Above)**.

---

## 3. Order Execution & Risk Model

| Property | Setting | Rationale |
| :--- | :--- | :--- |
| **Initial Capital** | $10,000 | Baseline account equity standard |
| **Order Sizing** | 1.0% of Equity | Enforces institutional 1% maximum capital risk guardrail |
| **Order Timing** | `process_orders_on_close = true` | Orders submit at bar close and execute on the open of the next bar |
| **Commission** | 0.02% (Percent of Trade Value) | Models realistic retail / institutional broker exchange fees |
| **Slippage** | 2 Ticks | Simulates execution latency on fast-moving momentum bars |
| **Stop Loss** | Entry ± (1.5 × ATR 14) | Volatility-adjusted protective stop distance |
| **Take Profit 1** | Entry ± (1.5 × Risk Distance) | 1:1.5 minimum reward-to-risk limit target |
| **Pyramiding** | 0 (Single Position Only) | Blocks multiple concurrent orders in the same instrument |
| **Cooldown** | 5 Bars | Prevents immediate re-entry after an exit |

---

## 4. Cross-Platform Parity: TradingView vs MT5 EA

| Strategy Element | TradingView Strategy (`HR_EMA_Pullback_Pro.pine`) | MT5 EA (`TREND_PULLBACK_CONTINUATION_EA.mq5`) | Reconciled Logic & Notes |
| :--- | :--- | :--- | :--- |
| **Execution Trigger** | Bar close of signal candle (`process_orders_on_close=true`) | On completed bar 1 (`CopyRates(..., 1, 5)`) | **Identical**: Both systems wait for complete candle confirmation. |
| **Corridor EMAs** | 9 EMA, 21 EMA, 200 EMA | InpFastEMA=9, InpSlowEMA=21, InpMacroEMA=200 | **Identical**: Standard exponential moving average equations. |
| **HTF Filter** | 1H Close vs 1H 200 EMA (`lookahead_off`) | Multi-timeframe trend verification | **Identical**: Strict non-repainting historical alignment. |
| **Protective Stop Loss** | ATR 14 × 1.5 Multiplier | Recent swing low or Slow EMA - 5 pts buffer | **Documented Difference**: Pine uses ATR distance; MT5 uses swing candle extremes. |
| **Take Profit Target** | 1.5R fixed limit | InpRewardToRiskRatio = 2.2 with 1.5R partial close (50%) | **Documented Difference**: Pine closes full position at 1.5R; MT5 scales out 50% and trails runner. |
| **Position Sizing** | 1.0% of equity via TV engine | Lot size calculated by equity risk / tick value | Both enforce the 1.0% maximum risk guardrail. |

---

## 5. Webhook Alert Schema

Every executed order generates a standardized JSON webhook payload compatible with automated order routers (e.g., PineConnector, Capitalise.ai, or custom webhook bridges):

```json
{
  "brand": "Hemanth Ranam",
  "system": "TradingView",
  "strategy": "EMA Pullback Pro",
  "signal": "BUY",
  "symbol": "XAUUSD",
  "timeframe": "15",
  "entry": 2742.50,
  "stop_loss": 2734.20,
  "take_profit_1": 2754.95,
  "score": "82",
  "grade": "A",
  "timestamp": 1729612800000
}
```

---

## 6. Manual TradingView Verification Checklist

Before publishing or distributing this strategy, perform the following verification steps directly in the TradingView Pine Editor:

1. **Open TradingView Chart**:
   - Set symbol to `XAUUSD` or `US500` on the `15m` timeframe.
2. **Load Script**:
   - Open **Pine Editor** at the bottom of the screen.
   - Paste the contents of `src/strategies/HR_EMA_Pullback_Pro.pine`.
   - Click **Save** and **Add to chart**.
3. **Verify Compilation**:
   - Confirm the Console reports **Compiled successfully** with **0 errors and 0 warnings**.
4. **Inspect Strategy Tester Tab**:
   - Verify that trades appear in the **Overview**, **Performance Summary**, and **List of Trades** tabs.
   - Verify that commission (0.02%) and slippage (2 ticks) are reflected in net profit calculations.
5. **Check Non-Repainting Behavior**:
   - Enable **Bar Replay** on historical data. Step forward candle by candle.
   - Verify that entry signals appear only after the trigger bar closes and do not change after subsequent price bars form.
6. **Compare with Indicator**:
   - Add `src/indicators/HR_EMA_Pullback_Indicator.pine` to the same chart.
   - Confirm that strategy entry markers match the indicator's BUY/SELL signal markers.
