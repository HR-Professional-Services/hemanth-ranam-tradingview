# HR TradingView — Verification Status & Evidence Ledger

**Domain**: Quantitative Systems Audit (HR TradingView / ScaleNova / Hemanth Ranam)  
**Governance**: Master Engine Protocol (Dual AI Model, Zero Blind Trust, Evidence-First)  
**Audit Date**: 2026-10-22  
**Current Branch**: `feat/commercial-indicators-phase2-4`

---

## 1. Evidence-Based Status Taxonomies

To prevent AI hallucination, marketing exaggeration, and unverified performance claims, every script and feature is categorized using strict evidence labels:

- **`LOCAL-VALIDATION-PASSED`**: Verified via local automated static tests and Python regression suites (e.g. syntax, lookahead prevention, risk caps).
- **`NATIVE-COMPILATION-PENDING`**: Script syntax is written for Pine Script v6, but has not yet been compiled and confirmed inside the native TradingView Pine Editor engine.
- **`BACKTEST-PENDING`**: Strategy code is complete with backtest properties, but empirical trades have not yet been generated and exported from TradingView Strategy Tester.
- **`MT5-PARITY-REVIEW-PENDING`**: Source code parity comparison has been partially documented, but full execution matching under live tick data is unverified.
- **`DEFERRED-RESEARCH-CANDIDATE`**: Excluded from commercial distribution pending multi-regime research (HR-PRD-05).

---

## 2. Product Verification Status Ledger

| Product ID | Product Name | Script Path | Script Type | Local Python Tests | Native TV Compilation | Strategy Backtest | MT5 Parity Audit | Current Stage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **HR-PRD-01** | EMA Trend Pullback Pro | `src/indicators/HR_EMA_Pullback_Indicator.pine` | Indicator | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | N/A | `PARTIAL` | Ready for Native TV Test |
| **HR-PRD-01** | EMA Trend Pullback Pro | `src/strategies/HR_EMA_Pullback_Pro.pine` | Strategy | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | `BACKTEST-PENDING` | `PARTIAL` | Ready for Native TV Test |
| **HR-PRD-02** | Liquidity Sweep Reversal Pro | `src/indicators/HR_Liquidity_Sweep_Indicator.pine` | Indicator | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | N/A | `PARTIAL` | Ready for Native TV Test |
| **HR-PRD-02** | Liquidity Sweep Reversal Pro | `src/strategies/HR_Liquidity_Sweep_Strategy.pine` | Strategy | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | `BACKTEST-PENDING` | `PARTIAL` | Ready for Native TV Test |
| **HR-PRD-03** | Volatility Expansion Breakout | `src/indicators/HR_Volatility_Breakout_Indicator.pine` | Indicator | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | N/A | `PARTIAL` | Ready for Native TV Test |
| **HR-PRD-03** | Volatility Expansion Breakout | `src/strategies/HR_Volatility_Breakout_Strategy.pine` | Strategy | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | `BACKTEST-PENDING` | `PARTIAL` | Ready for Native TV Test |
| **HR-PRD-04** | Market Structure Momentum | `src/indicators/HR_Market_Structure_Indicator.pine` | Indicator | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | N/A | `PARTIAL` | Ready for Native TV Test |
| **HR-PRD-04** | Market Structure Momentum | `src/strategies/HR_Market_Structure_Strategy.pine` | Strategy | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | `BACKTEST-PENDING` | `PARTIAL` | Ready for Native TV Test |
| **HR-PRD-05** | Adaptive Market Regime Pro | `src/indicators/HR_Adaptive_Regime_Indicator.pine` | Research | N/A | N/A | N/A | `UNVERIFIED` | `DEFERRED-RESEARCH-CANDIDATE` |

---

## 3. Automated Test Execution Record

- **Test Runner**: Python 3.12 `unittest`
- **Execution Command**: `python -m unittest discover tests`
- **Date Executed**: 2026-10-22 16:41:06
- **Test Modules Run**:
  1. `tests/test_commercial_products.py`: Verifies existence of all 8 files, `@version=6` declaration, `lookahead = barmerge.lookahead_off`, historical `[1]` indexing on `request.security`, JSON alert payload construction, and max 1% equity risk settings.
  2. `tests/test_pine_syntax.py`: Verifies balanced syntax, absence of illegal identifiers, and required imports.
  3. `tests/test_strategies_v6.py`: Verifies compliance of strategy parameters and backtest friction configuration.
- **Results**:
  - **Tests Run**: 55
  - **Failures**: 0
  - **Errors**: 0
  - **Execution Time**: 0.195s
  - **Status**: **PASSED (100%)**

---

## 4. Known Platform Differences & Limitations

1. **Intraday Bar Filling vs. Tick Execution**:
   - TradingView strategies execute using `process_orders_on_close = true`, filling market orders at the open of the following bar. MT5 EAs evaluate tick-by-tick and may execute immediately during high volatility.
2. **Equity-Based vs. Monetary Position Sizing**:
   - `strategy.percent_of_equity` allocates order volume equal to 1% of account equity. In instruments with wide stops, actual monetary risk at the stop may differ from 1% of cash equity unless dynamically normalized by point value and lot size.
3. **Volume Feed Discrepancies**:
   - Breakout volume filters on CFDs/Forex rely on broker tick volume, which varies between data providers (e.g., OANDA vs FOREX.com vs FXCM).
