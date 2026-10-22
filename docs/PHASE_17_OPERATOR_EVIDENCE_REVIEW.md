# Phase 17 — Operator Evidence Review & Paper-Test Gate Report

**Repository:** `HR-Professional-Services/hemanth-ranam-tradingview`  
**Branch:** `feat/commercial-indicators-phase2-4`  
**Baseline Commit:** `79767f2`  
**Authoritative Reference:** `HR-Professional-Services/HemanthRanam-MT5-EAs` (Strictly Read-Only — 100% Unmodified)  
**Lead Quantitative Systems Auditor:** Antigravity Quantitative Research Engine  
**Project Owner:** Hemanth Ranam  
**Audit Date:** 2026-10-22  
**Audit Focus:** Independent Evidence Inspection, Risk Sizing Audit, Gate Taxonomies, and Forward-Test Activation State

---

## 1. Executive Summary & Authoritative Gate Verdicts

In Phase 17, an audit was conducted on the operator evidence intake file ([`docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md)) and the local evidence directory (`docs/audit_evidence/`).

### Empirical Status Determination
- **Operator Intake Status:** The intake checklist exists at [`docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md), but remains in its **unfilled intake state**. All operational fields (symbol/feed, compiler outputs, trade sizing samples, and verification signature) are marked `[ PENDING ]`.
- **Evidence Artifacts:** The directory `docs/audit_evidence/` does not currently contain screenshots or exported compiler logs.
- **Strict Governance Adherence:** In accordance with Master Engine rules and Phase 17 instructions ("Do not assume the checks passed merely because the checklist exists or automated tests pass... If evidence is missing, inaccessible, ambiguous, or inconsistent, keep the corresponding gate PENDING or BLOCKED"), the compilation and empirical sizing gates remain **`PENDING`**, and forward paper-testing activation remains **`BLOCKED`**.

### Explicit Gate Decision Matrix

| Gate Category | Candidate / Target | Status | Authoritative Reason | Required Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **`CANDIDATE-INTEGRITY`** | HR-PRD-03 Exp A2 | **`PASS`** | Checksum matches Phase 14–16 records exactly (`57adb2...`); logic unchanged. | Maintain frozen candidate state. |
| **`CANDIDATE-INTEGRITY`** | HR-PRD-04 Forward | **`PASS`** | Checksum matches Phase 14–16 records exactly (`b32601...`); logic unchanged. | Maintain frozen candidate state. |
| **`NATIVE-COMPILATION`** | HR-PRD-03 Exp A2 | **`PENDING`** | No compiler console screenshot or log recorded in intake checklist. | Operator to paste script into Pine Editor and record result. |
| **`NATIVE-COMPILATION`** | HR-PRD-04 Forward | **`PENDING`** | No compiler console screenshot or log recorded in intake checklist. | Operator to paste script into Pine Editor and confirm resolution of baseline line 163 error. |
| **`RISK-SIZING-VALIDATION`** | HR-PRD-03 Exp A2 | **`PENDING`** | Mathematical formula verified in Pine/Python, but empirical live chart trade sample table is empty. | Operator to record 3 actual trades from Strategy Tester List of Trades. |
| **`RISK-SIZING-VALIDATION`** | HR-PRD-04 Forward | **`PENDING`** | Mathematical formula verified in Pine/Python, but empirical live chart trade sample table is empty. | Operator to record 3 actual trades from Strategy Tester List of Trades. |
| **`FORWARD-PAPER-TEST`** | Passive Logger Activation | **`BLOCKED`** | Forward paper evaluation is gated until native compilation and chart trade sizing are verified and approved. | Awaiting operator checklist completion and explicit authorization. |

---

## 2. Repository & Frozen Candidate Integrity Verification

### A. Candidate Checksum Ledger
Both research candidate source files were audited via SHA-256 hash checks and confirmed identical to Phase 14, 15, and 16 baselines:

```text
src/candidates/HR_Volatility_Breakout_Candidate_ExpA2.pine
SHA-256: 57adb2b59abe9df3bad3a3bb186d55f358f4318309e86d05c21a0960c6d25e86

src/candidates/HR_Market_Structure_Candidate_Forward.pine
SHA-256: b32601f3dde7f1ece313bc24d378289b226be69013a03d412d0aa1128705c5c8
```

### B. Commercial Baseline & Reference Preservation
- **Eight Original Commercial Scripts:** Audited via `git diff faee296 HEAD -- src/indicators/ src/strategies/`. Output is **0 bytes**. All original commercial indicators and strategies remain byte-for-byte identical to baseline commit `faee296`.
- **MT5 Reference Repository:** `HR-Professional-Services/HemanthRanam-MT5-EAs` was audited and is 100% untouched and strictly read-only.

---

## 3. Independent Sizing Formula & Feed Specification Audit

### A. Institutional Sizing Model
The Pine Script v6 position sizing engine (`calcSizing`) calculates contract order quantity as:

$$Q_{\text{raw}} = \frac{R}{D \times \text{PV}}$$

$$Q_{\text{stepped}} = \left\lfloor \frac{Q_{\text{raw}}}{S} \right\rfloor \times S$$

Where:
- $R = \min(\text{Equity} \times 0.005,\; 100.0)$ is the planned monetary risk budget ($50.00 USD on $10,000 equity).
- $D = |P_{\text{entry}} - P_{\text{stop}}|$ is the absolute stop distance in USD.
- $\text{PV} = \text{syminfo.pointvalue} > 0 \;?\; \text{syminfo.pointvalue} : \text{contractMult}$ is the contract point value factor.
- $S = 0.01$ is the minimum volume step increment (`minVolumeStep`).

### B. Mathematical Properties & Defensive Guardrails
1. **Floor Truncation:** Because the quantity is stepped using `math.floor(rawQty / minVolumeStep) * minVolumeStep`, fractional lot overage is discarded. Realized loss at the stop price under normal market conditions will always satisfy:
   $$\text{Realized Loss} = Q_{\text{stepped}} \times D \times \text{PV} \le R$$
2. **Defensive Fail-Closed Guards:**
   - If $D \le 0$ or $D$ is `na`, the sizing block exits with `validQty = 0.0`.
   - If $Q_{\text{stepped}} < S$ ($0.01$ units), `validQty` remains `0.0`.
   - In execution blocks: `if orderQty > 0 strategy.entry(...)`. Orders with zero quantity are suppressed.
3. **Symbol & Feed Specifications (Spot Gold CFD vs Futures):**
   - Spot Gold CFD (`XAUUSD`): 1 unit = 1 troy oz ($\text{pointvalue} = 1.0$). On $10,000 equity with a $10.00 stop, $Q = 5.00$ units.
   - Gold Futures (`GC1!`): 1 contract = 100 troy oz ($\text{pointvalue} = 100.0$). If run on futures without setting `contractMult = 100.0` (or if `syminfo.pointvalue` is unsupported), orders would be 100x oversized ($500 oz instead of $5 oz). The operator must run on spot `XAUUSD`.
4. **Account Base Currency:** The model calculates in USD. If the strategy is applied to an account denominated in GBP or EUR, TradingView does not automatically convert equity into quote currency; the operator must ensure the account currency is USD.
5. **Planned Risk vs. Realized Loss Boundary:** 0.5% ($50 on $10k equity) is an order-generation parameter assuming fill at the stop loss price. It does **NOT** guarantee protection against weekend price gaps, macroeconomic news slippage, or spread widening.

---

## 4. Inspection of Operator Evidence Intake

The intake file [`docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md) was inspected line-by-line:

- **Section 2.B (Chart & Feed Configuration - Exp A2):** All fields (`TradingView Symbol`, `Data Feed`, `Chart Timeframe`, `Account Base Currency`, `Initial Simulated Capital`) are marked `[ PENDING ]`.
- **Section 2.C (Pine Editor Compilation - Exp A2):** Compiler status and timestamp are marked `[ PENDING ]`.
- **Section 2.D (Strategy Tester Sizing Audit - Exp A2):** Trade sample table rows (Trade 1, Trade 2, Trade 3) are empty and marked `[ PENDING ]`.
- **Section 2.E (Evidence Artifacts - Exp A2):** Screenshot references are marked `[ PENDING ]`.
- **Section 3.B–E (Candidate Forward Intake):** All fields, compiler outputs, and trade sample rows are marked `[ PENDING ]`.
- **Section 4 (Operator Verification Sign-Off):** Signature and approval date are marked `[ PENDING ]`.

Because no empirical data or screenshots were supplied, native compilation and empirical sizing cannot be certified at this time.

---

## 5. Frozen Paper-Test Protocol (Gated & Awaiting Operator Approval)

The forward paper-test protocol remains frozen as configured in [`research/forward_test/forward_test_config.json`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/research/forward_test/forward_test_config.json):

- **Target Instrument:** `XAUUSD` (Spot Gold CFD, 15-Minute Chart).
- **Simulated Capital:** `$10,000.00 USD`.
- **Planned Risk Budget:** `0.5%` per trade ($50.00 USD), hard capped at `$100.00 USD`.
- **Primary Milestone / Stopping Rule:** **60 calendar days OR 50 confirmed closed trades** per candidate.
- **Idempotency Protection:** Rejection of duplicate alert signals based on unique `signal_id`.
- **Circuit Breaker 1:** Emergency suspension upon **12 consecutive losses**.
- **Circuit Breaker 2:** Emergency suspension upon **10.0% account equity drawdown**.
- **Execution Guardrail:** Passive telemetry logging only via [`paper_trade_logger.py`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/research/forward_test/paper_trade_logger.py). Zero broker API connections, zero real orders.

---

## 6. Automated Test Suite Record

```bash
python -m unittest discover tests ; python -m unittest discover research/backtest/tests
```
- **Tests Run:** 74 (55 core regression + 19 research harness tests)
- **Failures:** 0
- **Errors:** 0
- **Status:** **PASSED (100%)**

---

## 7. Actionable Next Steps for the Operator

To enable gate progression from `PENDING` to `PASS`:

1. Open your authenticated TradingView desktop or browser application.
2. Load a spot `XAUUSD` 15-minute chart with a USD account setting.
3. Open Pine Editor and compile both candidates:
   - [`HR_Volatility_Breakout_Candidate_ExpA2.pine`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/candidates/HR_Volatility_Breakout_Candidate_ExpA2.pine)
   - [`HR_Market_Structure_Candidate_Forward.pine`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/candidates/HR_Market_Structure_Candidate_Forward.pine)
4. Verify compiler output (0 errors, 0 warnings) and confirm line 163 duplicate error is resolved in Candidate Forward.
5. In the Strategy Tester **List of Trades** tab, record 3 trade examples for each candidate in [`docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md).
6. Save screenshots into `docs/audit_evidence/`.
7. Sign off in Section 4 of the checklist.
