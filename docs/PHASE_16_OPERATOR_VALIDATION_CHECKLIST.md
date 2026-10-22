# Phase 16 — Operator Native Validation Checklist & Evidence Intake

**Repository:** `HR-Professional-Services/hemanth-ranam-tradingview`  
**Branch:** `feat/commercial-indicators-phase2-4`  
**Commit:** `2e4b321`  
**Authoritative Reference:** `HR-Professional-Services/HemanthRanam-MT5-EAs` (Strictly Read-Only)  
**Lead Quantitative Systems Auditor:** Antigravity Quantitative Research Engine  
**Project Owner:** Hemanth Ranam  
**Audit Date:** 2026-10-22  
**Purpose:** Intake template for genuine operator evidence from an authenticated TradingView session.

---

## 1. Operating Instructions for the Operator

> [!IMPORTANT]
> **Zero Guessing / Zero Hallucination Standard:**
> Automated browser subagent attempts failed due to CDN driver download issues (404 Not Found), and guest browser sessions cannot save private scripts. Genuine native TradingView compilation evidence must be recorded directly by the human operator in an authenticated TradingView desktop or browser application.
> Do NOT alter candidate source files. All operator intake fields below are initialized to `PENDING`. Fill them with empirical observations from your TradingView chart.

---

## 2. Candidate 1 Validation Intake: Volatility Breakout Pro [Exp A2]

### A. Candidate Metadata & Checksum
- **Candidate ID:** `HR-PRD-03-CANDIDATE-EXPA2`
- **File Path:** `src/candidates/HR_Volatility_Breakout_Candidate_ExpA2.pine`
- **Frozen SHA-256 Checksum:** `57adb2b59abe9df3bad3a3bb186d55f358f4318309e86d05c21a0960c6d25e86`
- **Candidate Integrity Status:** `PASSED` (Preserved byte-for-byte)

### B. Chart & Feed Configuration (Operator Intake)
| Configuration Parameter | Required Specification | Operator Observed Value | Verification Status |
| :--- | :--- | :--- | :--- |
| **TradingView Symbol** | `XAUUSD` (Spot Gold CFD) | `[ PENDING: Operator to enter, e.g. XAUUSD ]` | `PENDING` |
| **Data Feed / Exchange** | Spot CFD (e.g. OANDA / FOREX.com / FXCM) | `[ PENDING: Operator to enter feed provider ]` | `PENDING` |
| **Chart Timeframe** | `15` (15-Minute) | `[ PENDING: Operator to confirm 15m ]` | `PENDING` |
| **Account Base Currency** | `USD` (Required by sizing model) | `[ PENDING: Operator to confirm USD ]` | `PENDING` |
| **Initial Simulated Capital**| `$10,000.00 USD` | `[ PENDING: Operator to confirm $10k ]` | `PENDING` |

### C. Pine Editor Compilation Results (Operator Intake)
- **Compilation Timestamp (UTC):** `[ PENDING: Operator to enter timestamp ]`
- **Compiler Status:** `[ PENDING: e.g. 0 errors, 0 warnings ]`
- **Compiler Warnings (if any):** `[ PENDING: None / List warning text ]`
- **Add to Chart Successful:** `[ PENDING: YES / NO ]`

### D. Strategy Tester Sizing & Execution Audit (Operator Intake)
Inspect the **Strategy Tester** -> **List of Trades** tab. Select 3 representative trades across recent historical bars:

| Trade # | Direction | Entry Price | Stop Loss Price | Stop Distance ($\Delta_{\text{SL}}$) | Actual Qty (Units) | Expected Qty ($50 / \Delta_{\text{SL}}$) | Planned Risk ($) | Discrepancy? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Trade 1** | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` |
| **Trade 2** | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` |
| **Trade 3** | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` |

### E. Evidence Artifacts (Operator Intake)
- **Compiler Console Screenshot:** `[ PENDING: e.g. docs/audit_evidence/expa2_compiler_console.png ]`
- **Strategy Tester Summary Screenshot:** `[ PENDING: e.g. docs/audit_evidence/expa2_strategy_tester.png ]`
- **List of Trades Screenshot:** `[ PENDING: e.g. docs/audit_evidence/expa2_trades_list.png ]`
- **Unresolved Issues / Notes:** `[ PENDING: Operator notes ]`

---

## 3. Candidate 2 Validation Intake: Market Structure Momentum Pro [Forward]

### A. Candidate Metadata & Checksum
- **Candidate ID:** `HR-PRD-04-CANDIDATE-FORWARD`
- **File Path:** `src/candidates/HR_Market_Structure_Candidate_Forward.pine`
- **Frozen SHA-256 Checksum:** `b32601f3dde7f1ece313bc24d378289b226be69013a03d412d0aa1128705c5c8`
- **Candidate Integrity Status:** `PASSED` (Preserved byte-for-byte)

### B. Chart & Feed Configuration (Operator Intake)
| Configuration Parameter | Required Specification | Operator Observed Value | Verification Status |
| :--- | :--- | :--- | :--- |
| **TradingView Symbol** | `XAUUSD` (Spot Gold CFD) | `[ PENDING: Operator to enter, e.g. XAUUSD ]` | `PENDING` |
| **Data Feed / Exchange** | Spot CFD (e.g. OANDA / FOREX.com / FXCM) | `[ PENDING: Operator to enter feed provider ]` | `PENDING` |
| **Chart Timeframe** | `15` (15-Minute) | `[ PENDING: Operator to confirm 15m ]` | `PENDING` |
| **Account Base Currency** | `USD` (Required by sizing model) | `[ PENDING: Operator to confirm USD ]` | `PENDING` |
| **Initial Simulated Capital**| `$10,000.00 USD` | `[ PENDING: Operator to confirm $10k ]` | `PENDING` |

### C. Pine Editor Compilation Results (Operator Intake)
- **Compilation Timestamp (UTC):** `[ PENDING: Operator to enter timestamp ]`
- **Compiler Status:** `[ PENDING: e.g. 0 errors, 0 warnings ]`
- **Line 163 Baseline Error Check:** `[ PENDING: Confirm duplicate variable 'lastBullBar' is resolved ]`
- **Compiler Warnings (if any):** `[ PENDING: None / List warning text ]`
- **Add to Chart Successful:** `[ PENDING: YES / NO ]`

### D. Strategy Tester Sizing & Execution Audit (Operator Intake)
Inspect the **Strategy Tester** -> **List of Trades** tab. Select 3 representative trades across recent historical bars:

| Trade # | Direction | Entry Price | Stop Loss Price | Stop Distance ($\Delta_{\text{SL}}$) | Actual Qty (Units) | Expected Qty ($50 / \Delta_{\text{SL}}$) | Planned Risk ($) | Discrepancy? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Trade 1** | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` |
| **Trade 2** | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` |
| **Trade 3** | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` | `[ PENDING ]` |

### E. Evidence Artifacts (Operator Intake)
- **Compiler Console Screenshot:** `[ PENDING: e.g. docs/audit_evidence/forward_compiler_console.png ]`
- **Strategy Tester Summary Screenshot:** `[ PENDING: e.g. docs/audit_evidence/forward_strategy_tester.png ]`
- **List of Trades Screenshot:** `[ PENDING: e.g. docs/audit_evidence/forward_trades_list.png ]`
- **Unresolved Issues / Notes:** `[ PENDING: Operator notes ]`

---

## 4. Operator Verification Sign-Off Protocol

Once the above fields are populated with genuine empirical data and screenshots are placed in `docs/audit_evidence/`:

1. Sign and date below:
   - **Operator Name:** `Hemanth Ranam`
   - **Signature Date:** `[ PENDING ]`
   - **Operator Verdict:** `[ PENDING: APPROVED / REJECTED ]`
2. Update gate statuses in `docs/PHASE_16_VALIDATION_GATE.md` from `PENDING` to `PASS`.
3. Proceed to the explicit authorization step for forward paper testing.
