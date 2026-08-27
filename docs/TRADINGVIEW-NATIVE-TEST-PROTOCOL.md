# Hemanth Ranam — Native TradingView Backtesting Protocol

**Document Purpose**: Standardized testing instructions and export schemas for conducting native Pine Script v6 backtests inside the TradingView Strategy Tester on live broker feeds.

---

## 1. Environment & Feed Setup
To ensure clean and reproducible Strategy Tester reports:
1. **Instrument Selection**:
   * Precious Metals: `XAUUSD`, `XAGUSD` (OANDA / Forex.com / TVC feed)
   * Indices: `US100`, `US500` (CME / FXCM / TVC feed)
   * Forex: `EURUSD`, `GBPUSD`, `USDJPY` (OANDA / FXCM feed)
2. **Chart Resolution**: `5m` (Primary Intraday), `15m` (Structural), `1H` (Macro Swing).
3. **Strategy Properties Configuration**:
   * **Initial Capital**: `$10,000`
   * **Order Size**: `1.0% of equity` (or `1 Contract`)
   * **Commission**: `0.02%` (under Strategy Properties $\rightarrow$ Commission)
   * **Slippage**: `2 ticks`
   * **Process Orders on Close**: `Enabled (Checked)`

---

## 2. Standardized Export CSV Schema
When exporting Strategy Tester performance metrics back to the repository, adhere to the following schema:

```csv
Strategy,Symbol,Timeframe,Period,Trades,NetProfitPct,ProfitFactor,WinRatePct,AvgTradePct,MaxDrawdownPct,SharpeRatio,SortinoRatio,LongPF,ShortPF
HR_EMA_Pullback_Pro,XAUUSD,5m,2024-2026,142,28.4,1.82,58.4,0.20,4.12,1.65,2.10,1.94,1.68
```

---

## 3. Step-by-Step Native Execution
1. Open chart on specified ticker and resolution.
2. Open Pine Editor, paste the strategy from `src/strategies/`, and click **Add to Chart**.
3. In the **Strategy Tester** panel:
   * Record **Overview**: Net Profit %, Total Closed Trades, Percent Profitable, Profit Factor, Max Drawdown %.
   * Record **Performance Summary**: Average Win, Average Loss, Average Trade, Max Consecutive Losses.
   * Record **List of Trades**: Validate that entries occur strictly on the bar close following confirmed signals.
