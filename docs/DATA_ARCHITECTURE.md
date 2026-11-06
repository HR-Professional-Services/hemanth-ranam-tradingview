# Data Architecture & Broker Parity Specification

## 1. Multi-Feed Symbols
The system defaults to institutional reference data feeds:
- `OANDA:XAUUSD` (Spot Gold / USD)
- `OANDA:XAGUSD` (Spot Silver / USD)
- `SP:SPX` (S&P 500 Index)
- `NASDAQ:NDX` (Nasdaq 100 Index)
- `TVC:DXY` (US Dollar Index)

Inputs remain fully customizable within TradingView and Python settings to accommodate specific broker prefixes (e.g. `XAUUSDm`, `US500.cash`).

## 2. Zero-Hallucination Data Flow
- Live data feeds directly from TradingView `request.security()`.
- Python companion processes standard CSV time series exported from MT5 or historical repositories.
