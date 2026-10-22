# HR TradingView — Product Registry

**Version**: 2.0  
**Domain**: Trading Systems (ScaleNova / HR TradingView / Hemanth Ranam)  
**Last Updated**: 2026-10-22  
**Governance**: Master Engine Protocol (Dual AI Model, Zero Blind Trust, Closed-Bar Execution)

---

## 1. Overview

The **HR TradingView Product Registry** maps each approved institutional trading strategy family to its standalone TradingView Indicator (`src/indicators/`), backtestable TradingView Strategy (`src/strategies/`), and authoritative MT5 Expert Advisor (`HemanthRanam-MT5-EAs`).

Every product family adheres to the **Signal Contract** (`docs/architecture/SIGNAL-CONTRACT.md`) and undergoes rigorous cross-platform alignment, non-repainting verification, and execution gap analysis.

---

## 2. Product Registry Master Table

| Product ID | Strategy Family | Standalone Indicator (`src/indicators/`) | Dedicated Strategy (`src/strategies/`) | Authoritative MT5 EA | Documentation | Status | Release Readiness |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **HR-PRD-01** | **EMA Trend Pullback Pro** | [`HR_EMA_Pullback_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_EMA_Pullback_Indicator.pine) | [`HR_EMA_Pullback_Pro.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_EMA_Pullback_Pro.pine) | `02_TREND_PULLBACK/TREND_PULLBACK_CONTINUATION_EA.mq5` | [`HR_EMA_PULLBACK_INDICATOR.md`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/indicators/HR_EMA_PULLBACK_INDICATOR.md), [`EMA-PULLBACK.md`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/EMA-PULLBACK.md) | **Implemented & Automated Tests Passed** | Native TV Compilation Pending |
| **HR-PRD-02** | **Liquidity Sweep Reversal Pro** | [`HR_Liquidity_Sweep_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Liquidity_Sweep_Indicator.pine) | [`HR_Liquidity_Sweep_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Liquidity_Sweep_Strategy.pine) | `01_LIQUIDITY_SWEEP/LIQUIDITY_SWEEP_REVERSAL_EA.mq5` | [`HR_LIQUIDITY_SWEEP_INDICATOR.md`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/indicators/HR_LIQUIDITY_SWEEP_INDICATOR.md), [`HR_LIQUIDITY_SWEEP_STRATEGY.md`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/strategies/HR_LIQUIDITY_SWEEP_STRATEGY.md) | **Implemented & Automated Tests Passed** | Native TV Compilation Pending |
| **HR-PRD-03** | **Volatility Expansion Breakout Pro** | [`HR_Volatility_Breakout_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Volatility_Breakout_Indicator.pine) | [`HR_Volatility_Breakout_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Volatility_Breakout_Strategy.pine) | `03_VOLATILITY_BREAKOUT/VOLATILITY_EXPANSION_BREAKOUT_EA.mq5` | [`HR_VOLATILITY_BREAKOUT_INDICATOR.md`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/indicators/HR_VOLATILITY_BREAKOUT_INDICATOR.md), [`HR_VOLATILITY_BREAKOUT_STRATEGY.md`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/strategies/HR_VOLATILITY_BREAKOUT_STRATEGY.md) | **Implemented & Automated Tests Passed** | Native TV Compilation Pending |
| **HR-PRD-04** | **Market Structure Momentum Pro** | [`HR_Market_Structure_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Market_Structure_Indicator.pine) | [`HR_Market_Structure_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Market_Structure_Strategy.pine) | `04_STRUCTURE_MOMENTUM/MARKET_STRUCTURE_MOMENTUM_EA.mq5` | [`HR_MARKET_STRUCTURE_INDICATOR.md`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/indicators/HR_MARKET_STRUCTURE_INDICATOR.md), [`HR_MARKET_STRUCTURE_STRATEGY.md`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/strategies/HR_MARKET_STRUCTURE_STRATEGY.md) | **Implemented & Automated Tests Passed** | Native TV Compilation Pending |
| **HR-PRD-05** | **Adaptive Market Regime** | `src/indicators/HR_Adaptive_Regime_Indicator.pine` *(Research)* | `src/strategies/HR_Adaptive_Regime_Strategy.pine` *(Research)* | `05_ADAPTIVE_REGIME/ADAPTIVE_MARKET_REGIME_EA.mq5` | `docs/STRATEGY-COMPARISON.md` | **Research Lab Candidate (Deferred)** | Forward Testing In Progress |

---

## 3. Cross-Platform Parity Summary Matrix

| Strategy Element | Platform Parity Baseline | MT5 EA Alignment | Pine Script Implementation | Documented Deviations |
| :--- | :--- | :--- | :--- | :--- |
| **Bar Execution Timing** | Closed-Bar Standard | Completed bar 1 (`rates[0]`) | `barstate.isconfirmed`, `process_orders_on_close = true` | **1:1 Matched**: Orders fill on next bar open. |
| **HTF Anti-Repainting** | Zero Lookahead | Multi-timeframe bar checks | `lookahead_off` and `[1]` indexing on `request.security` | **1:1 Matched**: Zero future-data leakage. |
| **Risk Cap** | Maximum 1.0% Equity | Dynamic lot sizing per equity risk | `default_qty_type = percent_of_equity, default_qty_value = 1.0` | **1:1 Matched**: Strict 1% risk guardrail enforced. |
| **Friction Modeling** | Explicit Costs | Live broker spread & commission | 0.02% commission, 2 ticks slippage configured explicitly | Realistic simulation in Strategy Tester. |
| **Alert Schema** | Standardized JSON | Text / Push notification logging | Standardized JSON webhook with brand, signal, levels, and grade | Compatible with automated webhooks. |
