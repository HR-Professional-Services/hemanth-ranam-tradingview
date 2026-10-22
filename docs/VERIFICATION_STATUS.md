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

| Product ID | Product Name | Script Path | Script Type | Local Python Tests | Native TV Compilation | Local Backtest Status | Forward Validation Status | Release Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **HR-PRD-01** | EMA Trend Pullback Pro | `src/indicators/HR_EMA_Pullback_Indicator.pine` | Indicator | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | N/A | N/A | `REQUIRES-REWORK` |
| **HR-PRD-01** | EMA Trend Pullback Pro | `src/strategies/HR_EMA_Pullback_Pro.pine` | Strategy | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | Full Sample PF 0.74 (Losses -$1,411) | N/A | `REQUIRES-REWORK` (Chop Whipsaws) |
| **HR-PRD-02** | Liquidity Sweep Reversal Pro | `src/indicators/HR_Liquidity_Sweep_Indicator.pine` | Indicator | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | N/A | N/A | `REQUIRES-REWORK` |
| **HR-PRD-02** | Liquidity Sweep Reversal Pro | `src/strategies/HR_Liquidity_Sweep_Strategy.pine` | Strategy | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | Full Sample PF 0.65 (Losses -$2,374) | N/A | `REQUIRES-REWORK` (Trend Whipsaws) |
| **HR-PRD-03** | Volatility Expansion Breakout | `src/indicators/HR_Volatility_Breakout_Indicator.pine` | Indicator | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | N/A | N/A | `REQUIRES-REWORK` |
| **HR-PRD-03** | Volatility Expansion Breakout | `src/strategies/HR_Volatility_Breakout_Strategy.pine` | Strategy | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | Baseline PF 1.14 (N=9 trades) | N/A | `REQUIRES-REWORK` (Signal Starvation) |
| **HR-PRD-03** | Volatility Breakout [Exp A2] | `src/candidates/HR_Volatility_Breakout_Candidate_ExpA2.pine` | Research | **PASSED** (All Suite Checks) | `NATIVE-COMPILATION-PENDING` | Full PF 1.53 (N=59), OOS PF 2.22 (N=18) | `FORWARD-PROTOCOL-READY` (0.5% Risk) | `CANDIDATE-REMAINS-RESEARCH-ONLY` |
| **HR-PRD-04** | Market Structure Momentum | `src/indicators/HR_Market_Structure_Indicator.pine` | Indicator | **PASSED** (14 checks) | `NATIVE-COMPILATION-PENDING` | N/A | N/A | `REQUIRES-REWORK` |
| **HR-PRD-04** | Market Structure Momentum | `src/strategies/HR_Market_Structure_Strategy.pine` | Strategy | **PASSED** (Local Regressions) | `NATIVE-COMPILATION-BLOCKED` (Line 163) | In-Sample PF 0.88, OOS PF 1.33 | Blocked (Requires Candidate) | `REQUIRES-REWORK` |
| **HR-PRD-04** | Market Structure [Forward] | `src/candidates/HR_Market_Structure_Candidate_Forward.pine` | Research | **PASSED** (All Suite Checks) | `NATIVE-COMPILATION-PENDING` | Line 163 Fixed, Dynamic 0.5% Risk | `FORWARD-PROTOCOL-READY` (0.5% Risk) | `CANDIDATE-REMAINS-RESEARCH-ONLY` |

---

## 3. Automated Test Execution Record

- **Test Runner**: Python 3.12 `unittest`
- **Execution Command**: `python -m unittest discover tests; python -m unittest discover research/backtest/tests`
- **Date Executed**: 2026-10-22
- **Test Modules Run**:
  1. `tests/test_commercial_products.py`: Verifies existence of all 8 commercial files, `@version=6` declaration, `lookahead = barmerge.lookahead_off`, historical `[1]` indexing on `request.security`, JSON alert payload construction, and max 1% equity risk settings.
  2. `tests/test_pine_syntax.py`: Verifies balanced syntax, absence of illegal identifiers, and required imports.
  3. `tests/test_strategies_v6.py`: Verifies compliance of strategy parameters and backtest friction configuration.
  4. `research/backtest/tests/test_backtest_harness.py`: Deterministic tests verifying EMA math, non-repainting pivot confirmation lag (3 bars), next-bar execution, and monetary risk calculations.
  5. `research/backtest/tests/test_phase9_risk_and_candidates.py`: Verifies ADX range boundaries, fixed monetary risk position sizing derivation, and zero-SL defensive fallbacks.
  6. `research/backtest/tests/test_phase10_audit.py`: Reconciles Phase 9 figures, bootstrap profit factor bounds, consecutive loss tracking, and adverse cost stress degradation.
  7. `research/backtest/tests/test_phase11_forward_protocol.py`: Verifies alert payload schema validation, duplicate alert rejection (idempotency via unique signal_id), directional SL alignment, risk budget hard caps, frozen configuration integrity, exact volume step rounding down and fail-closed behavior, and active circuit breaker tripping on 12 consecutive losses and 10% drawdown.
- **Results**:
  - **Tests Run**: 74 (55 main regression + 19 research test cases)
  - **Failures**: 0
  - **Errors**: 0
  - **Status**: **PASSED (100%)**

---

## 4. Known Platform Differences & Limitations

1. **Intraday Bar Filling vs. Tick Execution**:
   - TradingView strategies execute using `process_orders_on_close = true`, filling market orders at the open of the following bar. MT5 EAs evaluate tick-by-tick and may execute immediately during high volatility.
2. **Equity Notional vs. Stop-Loss Monetary Position Sizing**:
   - `strategy.percent_of_equity = 1.0` allocates 1% notional trade value, which does NOT risk 1% of equity at the stop loss. Genuine monetary risk sizing requires dynamic lot derivation (`riskCash / (slDistance * pointValue)`).
3. **Volume Feed Discrepancies**:
   - Breakout volume filters on CFDs/Forex rely on broker tick volume, which varies between data providers (e.g., OANDA vs FOREX.com vs FXCM).

---

## 5. Phase 16 & 17 Native Validation & Forward-Test Gate Matrix

As established in [`docs/PHASE_16_VALIDATION_GATE.md`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/PHASE_16_VALIDATION_GATE.md), [`docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md), and audited in [`docs/PHASE_17_OPERATOR_EVIDENCE_REVIEW.md`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/PHASE_17_OPERATOR_EVIDENCE_REVIEW.md):

| Gate Taxonomy | Status | Verification Evidence / Condition |
| :--- | :--- | :--- |
| **`CANDIDATE-INTEGRITY`** | **`PASS`** | Checksums verified for `HR_Volatility_Breakout_Candidate_ExpA2.pine` (`57adb2...`) and `HR_Market_Structure_Candidate_Forward.pine` (`b32601...`). All 8 commercial baselines match `faee296` (0 byte diff). |
| **`NATIVE-COMPILATION`** | **`PENDING`** | Automated browser execution blocked (Playwright CDN 404); requires manual operator confirmation in authenticated TradingView session. Intake checklist currently unfilled (`PENDING`). |
| **`RISK-SIZING-VALIDATION`** | **`PASS`** *(Algorithm)* / **`PENDING`** *(Chart)* | Unit formula `rawQty = R / (D * PV)` and floor volume step rounding audited in Pine Script v6. Empirical Strategy Tester trade entry audit pending operator intake. |
| **`FORWARD-PAPER-TEST`** | **`BLOCKED`** | Forward paper evaluation is gated. Logger activation requires completed operator compilation checklist and explicit operator authorization. |

