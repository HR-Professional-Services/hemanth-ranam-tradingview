# Hemanth Ranam TradingView Strategy Suite

> **Disclaimer**: Historical backtests and simulations are research tools only. They do not guarantee future performance. Native TradingView validation is required before production use.

---

## Overview

Five independent Pine Script v6 trading strategies for TradingView, built for intraday and swing trading on liquid instruments including `XAUUSD`, `US100`, `US500`, and Forex majors.

This repository is a **controlled professional trading strategy research and validation system**, not simply a collection of Pine scripts.

---

## Five Strategies

| Strategy | Primary Edge | Recommended Markets | Timeframes |
| :--- | :--- | :--- | :--- |
| **EMA Pullback Pro** | 9/21/200 EMA alignment + 1H HTF filter + score engine | XAUUSD, US100, EURUSD | 5M, 15M, 1H |
| **Breakout Retest Pro** | 20-period range breakout + volume filter + retest hold | EURUSD, GBPUSD, US500 | 15M, 1H |
| **Market Structure Pro** | Fractal pivot BOS/CHoCH + 200 EMA direction | XAUUSD, US500 | 15M, 1H, 4H |
| **VWAP Mean Reversion Pro** | 2σ VWAP exhaustion + RSI + ADX trend guard | EURUSD, GBPUSD, USDJPY | 5M, 15M |
| **Momentum Volatility Pro** | Bollinger/Keltner squeeze compression + release | US100, XAUUSD | 5M, 15M |

---

## Installation

1. Open [TradingView](https://www.tradingview.com/).
2. Open your preferred chart (e.g. `XAUUSD`, `5M`).
3. Open **Pine Editor** (bottom toolbar).
4. Paste the contents of any `.pine` file from `src/strategies/`.
5. Click **Add to chart**.
6. Open **Strategy Tester** to run backtests.

---

## TradingView Usage

See [`docs/TRADINGVIEW-NATIVE-TEST-PROTOCOL.md`](docs/TRADINGVIEW-NATIVE-TEST-PROTOCOL.md) for exact step-by-step instructions including:
- Recommended symbols and broker feeds
- Commission and slippage settings
- Date ranges for in-sample vs out-of-sample testing
- CSV export format for result import

---

## Backtesting

This repository contains two backtesting layers:

1. **Python Simulation** (`tests/backtest_engine.py`): Mathematical simulation of strategy logic across synthetic market regimes. Research evidence only — not equivalent to TradingView.
2. **Native TradingView Strategy Tester**: Required for production assessment. Follow `docs/TRADINGVIEW-NATIVE-TEST-PROTOCOL.md`.

The distinction is explained in [`docs/VALIDATION-METHODOLOGY.md`](docs/VALIDATION-METHODOLOGY.md).

---

## Native Validation

Current validation status: **NATIVE-TV-PENDING** for all five strategies.

See [`VALIDATION-STATUS.md`](VALIDATION-STATUS.md) for the current gate status of each strategy.

To import TradingView results:
```bash
python research/scripts/tv_importer.py --csv <export.csv> --strategy HR_EMA_Pullback_Pro \
  --symbol XAUUSD --timeframe 5M --scenario B --source OANDA \
  --period-start 2026-01-01 --period-end 2026-08-27 --period-type out_of_sample
```

---

## Risk Management

- All strategies use **1% equity position sizing** and **ATR-based stop losses**.
- No strategy implies fixed returns or guaranteed profitability.
- See [`docs/RISK-MANAGEMENT.md`](docs/RISK-MANAGEMENT.md).

---

## Alerts & Webhook Integration

Strategies emit structured JSON alerts compatible with webhook endpoints (e.g. Chartora).

Alert payload standard: [`research/schema/alert-payload.schema.json`](research/schema/alert-payload.schema.json).

Do not connect live MT5 execution until the paper trading gate has been passed.

---

## Research Methodology

Full validation framework documented in [`docs/VALIDATION-METHODOLOGY.md`](docs/VALIDATION-METHODOLOGY.md).

Research configs (markets, timeframes, cost scenarios, locked parameters): `research/configs/`.

---

## Forward Testing

Forward test journal template: [`research/forward/forward-test-template.csv`](research/forward/forward-test-template.csv).

Forward testing uses **locked parameters only**. No mid-test optimisation permitted.

---

## Known Limitations

- Python simulation results are research evidence only — not native TradingView results.
- VWAP Mean Reversion Pro has low trade frequency in trending markets by design (Trend Protection Guard).
- Breakout Retest Pro has higher sensitivity to volume filter parameters than other strategies.
- All results require native TradingView verification before production deployment.

---

## Disclaimer

> **Past performance is not indicative of future results.**
> 
> These strategies are research and educational tools. They do not guarantee profitable trading.
> Native TradingView validation, realistic cost testing, out-of-sample verification, and forward testing are required before any live deployment.
> 
> All risk management decisions remain the sole responsibility of the trader.
