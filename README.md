# HR TradingView Strategy & Commercial Indicator Suite

> **Regulatory & Risk Disclaimer**: All trading strategies, indicators, backtests, and quantitative simulations in this repository are for research, educational, and software demonstration purposes only. They do not constitute financial advice or investment recommendations. Past performance in simulation or backtesting does not guarantee future results. Trading foreign exchange, commodities, indices, and derivatives carries substantial risk of loss. Always validate on paper trading accounts before deploying capital.

---

## 1. Overview

The **HR TradingView Commercial Suite** is an institutional-grade algorithmic trading software suite developed for TradingView (Pine Script v6). It provides four independent commercial strategy families, each engineered with a dedicated pair of scripts:
1. **Commercial Indicator** (`src/indicators/`): Real-time chart visualization, trend ribbons, diagnostic HUD tables, and standardized JSON webhook alert generation.
2. **Commercial Strategy** (`src/strategies/`): Fully autonomous TradingView Strategy Tester implementation featuring realistic friction modeling (0.02% commission, 2 ticks slippage), closed-bar order execution, and ATR-derived risk management.

This repository serves as a **controlled quantitative research and engineering system**, maintaining complete traceability to our authoritative MetaTrader 5 (MT5) Expert Advisors in `HR-Professional-Services/HemanthRanam-MT5-EAs`.

---

## 2. Four Commercial Product Families

| Product ID | Product Name | Primary Timeframe | Recommended Markets | Core Analytical Edge | Indicator Script | Strategy Script | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **HR-PRD-01** | **EMA Trend Pullback Pro** | 15M (1H HTF) | `XAUUSD`, `US500`, `EURUSD` | EMA 9/21/200 alignment + HTF trend filter + pullback resumption | [`HR_EMA_Pullback_Indicator.pine`](src/indicators/HR_EMA_Pullback_Indicator.pine) | [`HR_EMA_Pullback_Pro.pine`](src/strategies/HR_EMA_Pullback_Pro.pine) | `LOCAL-VALIDATION-PASSED` |
| **HR-PRD-02** | **Liquidity Sweep Reversal Pro** | 15M | `XAUUSD`, `EURUSD` | 24-bar swing liquidity sweeps + rejection candle structure (40% wick) | [`HR_Liquidity_Sweep_Indicator.pine`](src/indicators/HR_Liquidity_Sweep_Indicator.pine) | [`HR_Liquidity_Sweep_Strategy.pine`](src/strategies/HR_Liquidity_Sweep_Strategy.pine) | `LOCAL-VALIDATION-PASSED` |
| **HR-PRD-03** | **Volatility Expansion Breakout Pro** | 15M | `USTEC` (`US100`), `XAUUSD` | 20-bar consolidation box (<= 1.8 ATR squeeze) + volume surge breakout | [`HR_Volatility_Breakout_Indicator.pine`](src/indicators/HR_Volatility_Breakout_Indicator.pine) | [`HR_Volatility_Breakout_Strategy.pine`](src/strategies/HR_Volatility_Breakout_Strategy.pine) | `LOCAL-VALIDATION-PASSED` |
| **HR-PRD-04** | **Market Structure Momentum Pro** | 15M, 1H | `US500`, `XAUUSD` | 3-bar fractal pivot BOS/CHoCH confirmation + RSI momentum thresholds | [`HR_Market_Structure_Indicator.pine`](src/indicators/HR_Market_Structure_Indicator.pine) | [`HR_Market_Structure_Strategy.pine`](src/strategies/HR_Market_Structure_Strategy.pine) | `LOCAL-VALIDATION-PASSED` |
| **HR-PRD-05** | **Adaptive Market Regime Pro** | Multi-TF | Cross-Asset | Adaptive regime filter (ADX + ATR + KAMA) | *Research Candidate* | *Research Candidate* | `DEFERRED-RESEARCH-CANDIDATE` |

---

## 3. Indicators vs. Strategies vs. MT5 EAs

Understanding the architectural distinction between product types:

| Component | Platform | Execution Mechanism | Primary Purpose |
| :--- | :--- | :--- | :--- |
| **Commercial Indicator** | TradingView (Pine v6) | Chart overlays, shapes, dashboard tables, alerts | Real-time market analysis, visual discretionary signals, webhook alerting |
| **Commercial Strategy** | TradingView (Pine v6) | Native `strategy.entry()` / `exit()` in Strategy Tester | Historical backtesting, equity curve analysis, parameter sensitivity |
| **Expert Advisor (EA)** | MetaTrader 5 (MQL5) | Native broker tick execution engine | Autonomous broker-side execution, live order routing, dynamic trade management |

---

## 4. Repository Structure

```
hemanth-ranam-tradingview/
├── .github/                   # GitHub Action workflows
├── .gitignore                 # Cache and OS file exclusions
├── AGENTS.md                  # Permanent agent instructions & anti-hallucination rules
├── README.md                  # Main repository overview and guide
│
├── src/                       # Production Pine Script v6 source files
│   ├── indicators/            # 4 Standalone Commercial Indicators
│   ├── strategies/            # 4 Standalone Commercial Strategies
│   └── legacy/                # Preserved historical scripts and prototypes (Read-Only)
│
├── docs/                      # Canonical technical documentation
│   ├── PRODUCT_CATALOG.md     # Detailed product specifications
│   ├── INSTALLATION_AND_USAGE.md # Step-by-step TradingView setup guide
│   ├── STRATEGY_REFERENCE.md  # Mathematical formulas and signal rules
│   ├── ALERTS_AND_INTEGRATION.md # Standardized JSON webhook schemas
│   ├── ARCHITECTURE.md        # Code separation and layout standards
│   ├── VERIFICATION_STATUS.md # Evidence ledger and verification status
│   ├── MT5_PARITY_MATRIX.md   # MQL5 vs Pine Script parity breakdown
│   ├── BACKTEST_PROTOCOL.md   # Empirical backtest methodology & split-testing
│   ├── RELEASE_CHECKLIST.md   # 5-gate commercial release criteria
│   ├── indicators/            # Individual indicator user manuals
│   └── strategies/            # Individual strategy user manuals
│
├── tests/                     # Automated Python testing and validation engine
│   ├── test_commercial_products.py # Structural syntax, v6 declaration, security checks
│   ├── test_pine_syntax.py    # AST and regex structural validation
│   └── test_strategies_v6.py  # Pine Script v6 compliance verification
│
├── research/                  # Quantitative research, datasets, and configurations
└── recovered/                 # Recovered prototypes and historical snapshots (Preserved)
```

---

## 5. Quick Start: Local Testing

To run the automated validation test suite:

```bash
# Ensure Python 3.10+ is installed
python -m unittest discover tests
```

Current test baseline: **55 tests passed (100% pass rate, 0 failures, 0 errors)**.

---

## 6. How to Use in TradingView

### Adding an Indicator:
1. Open [TradingView](https://www.tradingview.com/) and load your target chart (e.g. `XAUUSD`, `15m`).
2. Open **Pine Editor** at the bottom of the screen.
3. Paste the contents of any script from `src/indicators/`.
4. Click **Add to chart**.
5. Configure visual styles, EMA periods, and dashboard displays in the settings menu.

### Running a Strategy Backtest:
1. Open **Pine Editor** and paste the contents of any script from `src/strategies/`.
2. Click **Add to chart**.
3. Open the **Strategy Tester** tab.
4. Verify properties: Initial capital `$10,000`, Commission `0.02%`, Slippage `2 ticks`, Order fill `On Bar Close`.
5. For full protocol details, see [`docs/BACKTEST_PROTOCOL.md`](docs/BACKTEST_PROTOCOL.md) and [`docs/INSTALLATION_AND_USAGE.md`](docs/INSTALLATION_AND_USAGE.md).

---

## 7. Webhook & JSON Alert Integration

All scripts emit structured JSON alerts compatible with external trade automation gateways:

```json
{
  "brand": "HR TradingView",
  "strategy": "HR_EMA_Pullback_Pro",
  "product_id": "HR-PRD-01",
  "signal": "BUY",
  "symbol": "XAUUSD",
  "timeframe": "15",
  "entry": 2742.10,
  "stop_loss": 2734.60,
  "take_profit_1": 2753.35,
  "risk_r": 1.5,
  "score": 90,
  "grade": "A+",
  "timestamp": 1729614900000
}
```
Detailed payload definitions and webhook setup instructions are documented in [`docs/ALERTS_AND_INTEGRATION.md`](docs/ALERTS_AND_INTEGRATION.md).

---

## 8. Current Verification & Quality Gate Status

All scripts and strategies operate under strict evidence-based status labels:
- **Python Static Validation**: `LOCAL-VALIDATION-PASSED` (55/55 tests passed).
- **Native TradingView Compilation**: `NATIVE-COMPILATION-PENDING` (manual verification in Pine Editor required).
- **Strategy Tester Backtesting**: `BACKTEST-PENDING` (empirical trade exports required before commercial claims).
- **MT5 Source Parity**: `PARTIAL` (structural comparison documented in [`docs/MT5_PARITY_MATRIX.md`](docs/MT5_PARITY_MATRIX.md)).

See [`docs/VERIFICATION_STATUS.md`](docs/VERIFICATION_STATUS.md) and [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md) for full release gate tracking.
