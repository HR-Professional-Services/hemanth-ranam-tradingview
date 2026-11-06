# HR Bloomberg Quant Terminal — Python Desktop Official Technical Specification

## 1. System Architecture
The Python Desktop Companion provides an institutional-grade multi-market analytics dashboard mirroring the **HR Unified Master OS** methodology:
- Multi-instrument support: `XAUUSD`, `XAGUSD`, `US500`, `USTEC`, `DXY`
- Multi-timeframe execution model: `M5` primary execution + `H1` directional trend filter
- Quantitative analytics: EMA 9 / 21 / 200, RSI 14, MACD 12/26/9, ATR 14, Relative Volume (RVOL), and Candle Buying Pressure Proxy
- ICT / SMC elements: Dynamic 20-bar Dealing Range (Premium vs Discount vs Equilibrium), Swings, and confirmed structural alignment

## 2. Live-Data vs Analytical Boundary
- The Python terminal acts strictly as an analytical visualization interface.
- Execution constraints, position sizing, margin, order routing, and broker guardrails remain the sole responsibility of the broker-connected MetaTrader 5 Expert Advisor suite (`HR-Professional-Services/HemanthRanam-MT5-EAs`).
