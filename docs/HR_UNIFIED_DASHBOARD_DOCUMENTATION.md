# HR UNIFIED DASHBOARD — TECHNICAL DOCUMENTATION
## HR Bloomberg Quant Terminal — Master OS (TradingView + Python)

### 1. Architectural Overview
The **HR Unified Dashboard** represents the definitive TradingView Pine Script v6 institutional analytics environment. Engineered by Hemanth Ranam, it synthesizes multi-market telemetry across Gold (`XAUUSD`), Silver (`XAGUSD`), S&P 500 (`US500`), Nasdaq 100 (`USTEC`), and the US Dollar Index (`DXY`).

### 2. Analytical Engine Components
- **Trend Matrix**: EMA 9, 21, and 200 calculated across execution (`M5`) and macro filter (`H1`) timeframes.
- **Oscillators & Volatility**: Standard 14-period RSI, 12/26/9 MACD histogram, and 14-period normalized ATR.
- **Order Flow Proxies**: Relative Volume (RVOL) benchmarked over 20 periods; Candle Buying Pressure proxy evaluated as `(close - low) / (high - low) * 100`.
- **ICT / SMC Mechanics**: Fair Value Gaps (3-bar imbalances), Order Blocks (displacement origins), and 20-bar Dealing Ranges (Premium / Discount / Equilibrium).
- **Macro Anchor**: Dedicated DXY strip providing macro currency bias.

### 3. Non-Repainting & Data Integrity Standards
- HTF calculations strictly implement `barmerge.lookahead_off` and closed historical bar indexing (`[1]`).
- Visual chart overlays (FVG, OB) persist based on closed bar confirmation.
