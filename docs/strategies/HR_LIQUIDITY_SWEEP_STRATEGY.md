# HR Liquidity Sweep Reversal Pro Strategy Manual

**Product ID**: `HR-PRD-02`  
**Version**: 1.0 (Pine Script v6)  
**File**: [`src/strategies/HR_Liquidity_Sweep_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Liquidity_Sweep_Strategy.pine)  
**Corresponding Indicator**: [`src/indicators/HR_Liquidity_Sweep_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Liquidity_Sweep_Indicator.pine)  
**Corresponding MT5 EA**: `01_LIQUIDITY_SWEEP/LIQUIDITY_SWEEP_REVERSAL_EA.mq5`  
**Last Updated**: 2026-10-22

---

## 1. Overview & Strategy Purpose

The **HR Liquidity Sweep Reversal Pro Strategy** is an institutional mean-reversion system designed for TradingView's native Strategy Tester. It models the behavioral tendency of markets to sweep key structural liquidity pools (swing highs/lows) before snapping back aggressively in the opposite direction.

The strategy translates the core rules from `LIQUIDITY_SWEEP_REVERSAL_EA.mq5` into Pine Script v6, modeling capital allocation, commission friction, slippage, and stop-loss boundaries.

---

## 2. Cross-Platform Parity: TradingView Strategy vs MT5 EA

| Component | TradingView Strategy (`HR_Liquidity_Sweep_Strategy.pine`) | MT5 EA (`LIQUIDITY_SWEEP_REVERSAL_EA.mq5`) | Parity Classification |
| :--- | :--- | :--- | :--- |
| **Reference Levels** | Rolling `highest(high[1], 24)` and `lowest(low[1], 24)` | Iterative loop scanning prior 24 bars excluding bar 0 | **Matched (1:1)** |
| **Execution Trigger** | Bar close of reversal candle (`process_orders_on_close=true`) | On completed bar 1 (`CopyRates(..., 1, lookback+2)`) | **Matched (1:1)** |
| **Rejection Ratio** | Bullish: `(close - low) / range >= 0.50` | `bodyReversal = (close - low) / barRange >= InpMinDisplacementR` | **Matched (1:1)** |
| **Stop Loss** | Structural wick extreme minus ATR buffer: `low - (atr * 0.2)` | Structural wick extreme minus buffer: `triggerBar.low - (5.0 * point)` | **Functionally Equivalent** (ATR-normalized in TV) |
| **Take Profit Target** | Full limit exit at `entry + (risk * 2.5)` | Single target at `entry + (slDistance * InpRewardToRiskRatio)` | **Matched (1:1 at 2.5R)** |
| **Position Sizing** | 1.0% equity via `strategy.percent_of_equity` | Dynamic lot sizing based on 0.5%–1.0% equity risk per stop distance | Both enforce 1.0% maximum risk guardrail |
| **Costs & Slippage** | 0.02% commission, 2 ticks slippage configured explicitly | Broker spread, commission ($7/lot round-turn), tick slippage | Simulated in TV |

---

## 3. TradingView Verification Checklist

1. Open `XAUUSD` or `EURUSD` on the **15m** chart in TradingView.
2. Load [`src/strategies/HR_Liquidity_Sweep_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Liquidity_Sweep_Strategy.pine) into Pine Editor.
3. Confirm 0 errors and 0 warnings on compilation.
4. Verify entry markers coincide exactly with [`src/indicators/HR_Liquidity_Sweep_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Liquidity_Sweep_Indicator.pine).
