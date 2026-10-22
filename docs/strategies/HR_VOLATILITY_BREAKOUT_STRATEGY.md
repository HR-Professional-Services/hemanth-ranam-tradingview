# HR Volatility Expansion Breakout Pro Strategy Manual

**Product ID**: `HR-PRD-03`  
**Version**: 1.0 (Pine Script v6)  
**File**: [`src/strategies/HR_Volatility_Breakout_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Volatility_Breakout_Strategy.pine)  
**Corresponding Indicator**: [`src/indicators/HR_Volatility_Breakout_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Volatility_Breakout_Indicator.pine)  
**Corresponding MT5 EA**: `03_VOLATILITY_BREAKOUT/VOLATILITY_EXPANSION_BREAKOUT_EA.mq5`  
**Last Updated**: 2026-10-22

---

## 1. Overview & Strategy Purpose

The **HR Volatility Expansion Breakout Pro Strategy** translates the quantitative volatility squeeze algorithm from `VOLATILITY_EXPANSION_BREAKOUT_EA.mq5` into an executable TradingView backtesting strategy.

It positions during the transition from low-volatility compression into high-volatility trend expansion, maintaining strict 1.0% equity risk controls, 2.5:1 reward-to-risk ratio targets, and explicit friction costs.

---

## 2. Cross-Platform Parity: TradingView vs MT5 EA

| Component | TradingView Strategy (`HR_Volatility_Breakout_Strategy.pine`) | MT5 EA (`VOLATILITY_EXPANSION_BREAKOUT_EA.mq5`) | Parity Status |
| :--- | :--- | :--- | :--- |
| **Compression Window** | `compressionBars = 20` | `InpCompressionBars = 20` | **Matched (1:1)** |
| **Squeeze Condition** | `boxHeight <= atr * 1.8` | `boxHeight <= (currentAtr * InpMaxCompressionATR)` | **Matched (1:1)** |
| **Volume Expansion** | `volume >= avgVolume * 1.25` (Optional, default OFF for spot FX) | `triggerBar.tick_volume >= (long)(avgVolume * InpMinVolumeMultiplier)` | **Matched** |
| **Execution Trigger** | Bar close of breakout candle (`process_orders_on_close=true`) | On completed bar 1 (`rates[0]`) | **Matched (1:1)** |
| **Stop Loss** | Box midpoint with ATR buffer | `MathMax(boxMid, triggerBar.low) - (5.0 * point)` | **Matched (1:1)** |
| **Take Profit Target** | Full limit exit at `entry + (risk * 2.5)` | Single target at `entry + (slDistance * InpRewardToRiskRatio)` | **Matched (1:1 at 2.5R)** |
| **Position Sizing** | 1.0% equity via `strategy.percent_of_equity` | Dynamic lot sizing based on 0.5%–1.0% risk per stop distance | Both enforce 1.0% maximum risk guardrail |

---

## 3. TradingView Verification Checklist

1. Open `USTEC` or `US500` on the **15m** chart in TradingView.
2. Load [`src/strategies/HR_Volatility_Breakout_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Volatility_Breakout_Strategy.pine) into Pine Editor.
3. Confirm 0 errors and 0 warnings on compilation.
4. Verify entry markers coincide exactly with [`src/indicators/HR_Volatility_Breakout_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Volatility_Breakout_Indicator.pine).
