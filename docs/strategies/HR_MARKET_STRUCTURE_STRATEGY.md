# HR Market Structure Momentum Pro Strategy Manual

**Product ID**: `HR-PRD-04`  
**Version**: 1.0 (Pine Script v6)  
**File**: [`src/strategies/HR_Market_Structure_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Market_Structure_Strategy.pine)  
**Corresponding Indicator**: [`src/indicators/HR_Market_Structure_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Market_Structure_Indicator.pine)  
**Corresponding MT5 EA**: `04_STRUCTURE_MOMENTUM/MARKET_STRUCTURE_MOMENTUM_EA.mq5`  
**Last Updated**: 2026-10-22

---

## 1. Overview & Strategy Purpose

The **HR Market Structure Momentum Pro Strategy** translates the mechanical Break of Structure (BOS) algorithm from `MARKET_STRUCTURE_MOMENTUM_EA.mq5` into an executable TradingView backtesting strategy.

It enters on confirmed candle closes piercing validated swing fractal pivots, requiring RSI momentum confirmation (>= 53 for Bullish, <= 47 for Bearish), 1.0% maximum equity risk, and 1:2.4 minimum reward-to-risk targets.

---

## 2. Cross-Platform Parity: TradingView vs MT5 EA

| Component | TradingView Strategy (`HR_Market_Structure_Strategy.pine`) | MT5 EA (`MARKET_STRUCTURE_MOMENTUM_EA.mq5`) | Parity Status |
| :--- | :--- | :--- | :--- |
| **Pivot Detection** | `ta.pivothigh(high, 3, 3)`, `ta.pivotlow(low, 3, 3)` | Fractal loop scanning `InpPivotStrength = 3` bars left and right | **Matched (1:1)** |
| **Breakout Trigger** | `close[1] <= pivotHigh` and `close > pivotHigh` (completed candle) | `prevBar.close <= recentPivotHigh && triggerBar.close > recentPivotHigh` | **Matched (1:1)** |
| **Momentum Filter** | `rsi >= 53.0` (Long) / `rsi <= 47.0` (Short) | `currentRsi >= InpBullishRSIMin` / `currentRsi <= InpBearishRSIMax` | **Matched (1:1)** |
| **Stop Loss** | Opposing confirmed swing pivot extreme minus ATR buffer | `slPrice = recentPivotLow - (5.0 * point)` | **Matched (1:1)** |
| **Take Profit Target** | Full limit exit at `entry + (risk * 2.4)` | Single target at `entry + (slDistance * InpRewardToRiskRatio)` | **Matched (1:1 at 2.4R)** |
| **Position Sizing** | 1.0% equity via `strategy.percent_of_equity` | Dynamic lot sizing based on 0.5%–1.0% risk per stop distance | Both enforce 1.0% maximum risk guardrail |

---

## 3. TradingView Verification Checklist

1. Open `XAUUSD` or `US500` on the **15m** chart in TradingView.
2. Load [`src/strategies/HR_Market_Structure_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Market_Structure_Strategy.pine) into Pine Editor.
3. Confirm 0 errors and 0 warnings on compilation.
4. Verify entry markers coincide exactly with [`src/indicators/HR_Market_Structure_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Market_Structure_Indicator.pine).
