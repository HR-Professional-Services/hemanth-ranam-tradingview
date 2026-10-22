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
├── src/                       # Production & Candidate Pine Script v6 files
│   ├── indicators/            # 4 Standalone Commercial Indicators (Commit faee296)
│   ├── strategies/            # 4 Standalone Commercial Strategies (Commit faee296)
│   ├── candidates/            # Isolated Research Candidates (0.5% Dynamic Risk Sizing)
│   │   ├── HR_Volatility_Breakout_Candidate_ExpA2.pine
│   │   └── HR_Market_Structure_Candidate_Forward.pine
│   └── legacy/                # Preserved historical scripts and prototypes (Read-Only)
│
├── docs/                      # Canonical technical & research documentation
│   ├── PHASE_8_AUDIT_REPORT.md      # Local backtest baseline report (4 products)
│   ├── PHASE_9_DEVELOPMENT_REPORT.md# Remediation experiments & Exp A2 derivation
│   ├── PHASE_10_INDEPENDENT_AUDIT_REPORT.md # Independent verification & PF reconciliation
│   ├── PHASE_11_COMPILATION_READINESS.md    # Static audit & manual compiler steps
│   ├── PHASE_11_FORWARD_TEST_PROTOCOL.md    # Blind forward testing protocol & rules
│   ├── PHASE_12_FINAL_HANDOVER.md   # Master consolidation & handover report
│   ├── PRODUCT_CATALOG.md     # Detailed product specifications
│   ├── INSTALLATION_AND_USAGE.md # Step-by-step TradingView setup guide
│   ├── STRATEGY_REFERENCE.md  # Mathematical formulas and signal rules
│   ├── ALERTS_AND_INTEGRATION.md # Standardized JSON webhook schemas
│   ├── VERIFICATION_STATUS.md # Master evidence ledger and verification status
│   ├── MT5_PARITY_MATRIX.md   # MQL5 vs Pine Script parity breakdown
│   ├── BACKTEST_PROTOCOL.md   # Empirical backtest methodology & split-testing
│   └── RELEASE_CHECKLIST.md   # 5-gate commercial release criteria
│
├── tests/                     # Automated Python testing and validation engine
│   ├── test_commercial_products.py # Structural syntax, v6 declaration, security checks
│   ├── test_pine_syntax.py    # AST and regex structural validation
│   └── test_strategies_v6.py  # Pine Script v6 compliance verification
│
├── research/                  # Quantitative research, datasets, and configurations
│   ├── backtest/              # Modular Python backtesting engine & research tests
│   ├── experiments/           # Reproducible experiment runners (Phase 9/10)
│   ├── forward_test/          # Passive forward paper-trading logger & JSON schema
│   └── results/               # Baseline/experiment matrices & trade logs
└── recovered/                 # Recovered prototypes and historical snapshots (Preserved)
```

---

## 5. Quick Start: Local Testing

To run the full automated validation test suite (71 deterministic tests):

```bash
# Run Core Commercial Regression Suite (55 tests)
python -m unittest discover tests

# Run Research Backtest & Protocol Suite (16 tests)
python -m unittest discover research/backtest/tests
```

Current test baseline: **71 tests passed (100% pass rate, 0 failures, 0 errors)**.

---

## 6. How to Use in TradingView

### Adding an Indicator:
1. Open [TradingView](https://www.tradingview.com/) and load your target chart (e.g. `XAUUSD`, `15m`).
2. Open **Pine Editor** at the bottom of the screen.
3. Paste the contents of any script from `src/indicators/`.
4. Click **Add to chart**.
5. Configure visual styles, EMA periods, and dashboard displays in the settings menu.

### Running a Strategy Backtest:
1. Open **Pine Editor** and paste the contents of any script from `src/strategies/` or `src/candidates/`.
2. Click **Add to chart**.
3. Open the **Strategy Tester** tab.
4. Verify properties: Initial capital `$10,000`, Commission `0.02%`, Slippage `2 ticks`, Order fill `On Bar Close`.
5. For full protocol details, see [`docs/BACKTEST_PROTOCOL.md`](docs/BACKTEST_PROTOCOL.md) and [`docs/PHASE_11_COMPILATION_READINESS.md`](docs/PHASE_11_COMPILATION_READINESS.md).

---

## 7. Webhook & JSON Alert Integration

All scripts emit structured JSON alerts compatible with external trade automation gateways and the Phase 11 passive paper-trading logger:

```json
{
  "brand": "Hemanth Ranam",
  "candidate_id": "HR-PRD-03-CANDIDATE-EXPA2",
  "signal_id": "HR-PRD-03-XAUUSD-1730000000000-BUY",
  "symbol": "XAUUSD",
  "timeframe": "15",
  "bar_time": 1730000000000,
  "direction": "BUY",
  "entry_price": 2720.50,
  "stop_loss": 2710.50,
  "take_profit": 2745.50,
  "planned_risk_pct": 0.5,
  "planned_risk_usd": 50.0,
  "qty": 5.0,
  "exit_reason_planned": "R_MULTIPLE_2.5"
}
```
Detailed payload definitions and forward logging schemas are documented in [`docs/PHASE_11_FORWARD_TEST_PROTOCOL.md`](docs/PHASE_11_FORWARD_TEST_PROTOCOL.md) and [`research/forward_test/forward_test_schema.json`](research/forward_test/forward_test_schema.json).

---

## 8. Current Verification & Quality Gate Status

All scripts and strategies operate under strict, evidence-based status labels:
- **Python Static Validation**: `LOCAL-VALIDATION-PASSED` (71/71 tests passed).
- **Native TradingView Compilation**: `NATIVE-COMPILATION-PENDING` (manual verification in Pine Editor required).
- **Forward Paper Testing**: `FORWARD-PROTOCOL-READY` (configurations frozen; evaluation starts post-compilation).
- **Commercial Release Gate**: `ZERO-COMMERCIAL-RELEASES` (Candidates remain research-only; HR-PRD-01 and HR-PRD-02 require structural rework).

See [`docs/VERIFICATION_STATUS.md`](docs/VERIFICATION_STATUS.md) and [`docs/PHASE_12_FINAL_HANDOVER.md`](docs/PHASE_12_FINAL_HANDOVER.md) for full audit tracking.
