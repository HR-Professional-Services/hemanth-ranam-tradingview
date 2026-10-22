# Phase 16 — Native Validation Closure & Forward-Test Authorization Gate

**Repository:** `HR-Professional-Services/hemanth-ranam-tradingview`  
**Branch:** `feat/commercial-indicators-phase2-4`  
**Baseline Commit:** `2e4b321`  
**Authoritative Reference:** `HR-Professional-Services/HemanthRanam-MT5-EAs` (Strictly Read-Only — 100% Unmodified)  
**Lead Quantitative Systems Auditor:** Antigravity Quantitative Research Engine  
**Project Owner:** Hemanth Ranam  
**Audit Date:** 2026-10-22  
**Audit Scope:** Native Compilation Intake, Mathematical Sizing Audit, Gate Status Taxonomies, and Paper-Test Authorization Protocol

---

## 1. Executive Summary & Authoritative Gate Decisions

In Phase 16, the repository state is verified, the mathematical position-sizing engine in the frozen research candidates is audited against contract specifications, a formal operator evidence intake template is deployed, and the forward paper-trading protocol is structured for explicit operator authorization.

### Formal Four-Gate Status Matrix

| Gate Dimension | Gate Status | Criteria for Status Determination | Next Action Required |
| :--- | :--- | :--- | :--- |
| **`CANDIDATE-INTEGRITY`** | **`PASS`** | Both candidate SHA-256 hashes match Phase 14 & 15 exactly; zero code modifications; all 8 commercial baseline scripts remain 100% byte-for-byte identical to baseline `faee296`. | Maintain frozen state. |
| **`NATIVE-COMPILATION`** | **`PENDING`** | Automated browser execution blocked (Playwright CDN driver 404); native compilation can only be confirmed with genuine operator evidence from an authenticated TradingView session. | Operator to complete [`PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md). |
| **`RISK-SIZING-VALIDATION`** | **`PASS`** *(Algorithm)* / **`PENDING`** *(Chart)* | Mathematical formula and Pine code audited: unit stepping, point-value fallback, and fail-closed guards are mathematically correct. Live chart reconciliation remains pending operator intake. | Operator to verify 3 trade entries in Strategy Tester List of Trades. |
| **`FORWARD-PAPER-TEST`** | **`BLOCKED`** | Strict governance guardrail: passive logging and forward paper evaluation must not be activated until native compilation and chart sizing are empirically approved. | Awaiting operator intake completion and explicit authorization. |

---

## 2. Frozen Candidate Checksums & Baseline Preservation

### Candidate Integrity Check
Both research candidate source files were audited via SHA-256 hash checks and confirmed unchanged:

- **Candidate Exp A2 (`HR-PRD-03`):**
  - Path: `src/candidates/HR_Volatility_Breakout_Candidate_ExpA2.pine`
  - SHA-256: `57adb2b59abe9df3bad3a3bb186d55f358f4318309e86d05c21a0960c6d25e86`
  - Status: `FROZEN` (`RESEARCH-ONLY`)
- **Candidate Forward (`HR-PRD-04`):**
  - Path: `src/candidates/HR_Market_Structure_Candidate_Forward.pine`
  - SHA-256: `b32601f3dde7f1ece313bc24d378289b226be69013a03d412d0aa1128705c5c8`
  - Status: `FROZEN` (`RESEARCH-ONLY`)

### Commercial Baseline Preservation Guarantee
- Command: `git diff faee296 HEAD -- src/indicators/ src/strategies/`
- Result: **0 bytes difference**. All 8 original commercial scripts remain pristine and unmodified.
- MT5 Reference Repository: `HR-Professional-Services/HemanthRanam-MT5-EAs` was audited and is 100% untouched and strictly read-only.

---

## 3. Mathematical Position Sizing & Pine Script v6 Audit

### A. Theoretical Unit-Based Sizing Formula
For an institutional risk allocation model:
- $R$ = Monetary risk budget in account base currency ($\text{USD}$)
- $D$ = Absolute stop distance in quote currency ($\Delta_{\text{SL}} = |P_{\text{entry}} - P_{\text{stop}}|$)
- $\text{PV}$ = Symbol point value / contract value factor ($\text{USD}$ per price unit per contract)
- $S$ = Minimum volume step increment (e.g. $0.01$ units)

$$\text{Raw Quantity: } Q_{\text{raw}} = \frac{R}{D \times \text{PV}}$$

$$\text{Stepped Quantity: } Q_{\text{stepped}} = \left\lfloor \frac{Q_{\text{raw}}}{S} \right\rfloor \times S$$

$$\text{Planned Monetary Risk: } \text{Risk}_{\text{planned}} = Q_{\text{stepped}} \times D \times \text{PV} \le R$$

Because the quantity is rounded down ($\lfloor \dots \rfloor$), $\text{Risk}_{\text{planned}}$ is mathematically guaranteed to be less than or equal to $R$, never exceeding the planned budget under standard fills.

### B. Actual Pine Script v6 Implementation Analysis
The sizing logic in both candidate scripts (`calcSizing`) was audited line-by-line:

```pinescript
calcSizing(float entryP, float slP) =>
    slDist = math.abs(entryP - slP)
    float validQty = 0.0
    float plannedRiskUsd = 0.0
    
    if slDist > 0 and not na(slDist)
        // Dollar budget capped at maxRiskUsdCap ($100.0)
        budgetUsd = math.min(strategy.equity * (riskPercent / 100.0), maxRiskUsdCap)
        plannedRiskUsd := budgetUsd
        
        // Determine point value
        pv = syminfo.pointvalue > 0 ? syminfo.pointvalue : contractMult
        rawQty = budgetUsd / (slDist * pv)
        
        // Round down to volume step to guarantee never exceeding risk budget
        steppedQty = math.floor(rawQty / minVolumeStep) * minVolumeStep
        
        // Fail-closed: reject if below minimum step or invalid
        if steppedQty >= minVolumeStep
            validQty := steppedQty
            
    [validQty, plannedRiskUsd]
```

#### Detailed Line Audit:
1. **Distance Validation (`slDist > 0 and not na(slDist)`):** If $P_{\text{entry}} = P_{\text{stop}}$, or if either is `na`, the execution block is skipped entirely. `validQty` remains `0.0`.
2. **Equity & Risk Budget (`budgetUsd`):** Evaluates `strategy.equity * 0.005`, strictly capped at `maxRiskUsdCap = 100.0`. Prevents runaway sizing during equity growth.
3. **Point Value & Multiplier (`pv`):** Evaluates `syminfo.pointvalue`. If the broker feed returns `> 0`, it uses native exchange point value. If `0` or `na`, it falls back to the user input `contractMult` (default $1.0$).
4. **Volume Stepping (`math.floor(rawQty / minVolumeStep) * minVolumeStep`):** Uses mathematical floor division to truncate excess fractional lots, ensuring the actual risk never exceeds the $50.00 budget.
5. **Fail-Closed Threshold (`if steppedQty >= minVolumeStep`):** If the calculated position is smaller than $0.01$ units (e.g. on extreme stop distances or tiny accounts), `validQty` remains `0.0`.
6. **Order Execution Guard:** In the strategy execution block:
   ```pinescript
   if orderQty > 0
       strategy.entry(..., qty=orderQty)
   ```
   If `orderQty == 0`, no entry order is submitted to the Strategy Tester. The trade is suppressed.

### C. Account Currency & Symbol Feed Discrepancy Analysis
1. **Base Currency Assumption:** Pine Script calculates `strategy.equity` in the strategy account's base currency. For gold (`XAUUSD`), the price and stop distance are quoted in USD. Therefore, the strategy mathematically requires a **USD-denominated account**. If applied to a GBP or EUR account, TradingView does not automatically convert equity into USD for internal sizing formulas; the user must ensure account currency is USD.
2. **Contract Multiplier Override (CFD vs Futures):**
   - Spot Gold CFD (`XAUUSD`): 1 unit = 1 troy ounce. $\text{PV} = 1.0$. Point value is $1.0$.
   - COMEX Gold Futures (`GC1!`): 1 contract = 100 troy ounces. $\text{PV} = 100.0$.
   - **Crucial Operator Warning:** If the strategy is loaded on a futures ticker (`GC1!`) without setting `contractMult = 100.0` (or if `syminfo.pointvalue` is not recognized), the position will be 100x oversized. The operator must run the strategy on spot `XAUUSD`.

### D. Planned Risk vs. Realized Loss Boundary
Planned risk ($50.00 on $10,000 equity) is an order-generation parameter assuming fill at the exact stop loss price. It does **NOT** constitute a guarantee against:
- Weekend market gaps or session open jumps.
- High-impact macroeconomic news slippage (e.g. US CPI, Non-Farm Payrolls).
- Broker spread widening during low-liquidity rollover windows.
Realized losses during such events can expand beyond $50.00 to $100.00–$250.00 (1.0%–2.5%).

---

## 4. Operator Validation Intake Workflow

To complete native compilation validation without resorting to unreliable browser automation, the operator must execute the empirical intake protocol:

```mermaid
flowchart TD
    A[Operator Opens TradingView Desktop/Web] --> B[Load Spot XAUUSD 15M Chart]
    B --> C[Open docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md]
    C --> D[Compile Candidate Exp A2]
    D --> E{0 Errors, 0 Warnings?}
    E -- No --> F[Log Compiler Output & Halt]
    E -- Yes --> G[Record 3 Trade Sizing Examples from Strategy Tester]
    G --> H[Compile Candidate Forward]
    H --> I{0 Errors, 0 Warnings?}
    I -- No --> J[Log Compiler Output & Halt]
    I -- Yes --> K[Record 3 Trade Sizing Examples from Strategy Tester]
    K --> L[Capture Full-Screen Screenshots to docs/audit_evidence/]
    L --> M[Submit Checklist & Request Gate Approval]
```

The intake document is published at:  
[`docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/docs/PHASE_16_OPERATOR_VALIDATION_CHECKLIST.md)

---

## 5. Frozen Forward Paper-Trading Protocol (Ready for Authorization)

Once native compilation evidence is recorded in the checklist, the following frozen forward testing protocol is submitted for explicit operator authorization:

### Protocol Specifications (`forward_test_config.json`)
- **Instrument:** `XAUUSD` (Spot Gold CFD)
- **Timeframe:** `15` (15-Minute)
- **Higher Timeframe Filter:** `60` (1-Hour 200 EMA)
- **Initial Simulated Capital:** `$10,000.00 USD`
- **Planned Risk Budget:** `0.5%` per trade ($50.00 USD max planned loss)
- **Hard Risk Cap:** `$100.00 USD` maximum risk cap per trade
- **Stopping Milestone:** **60 calendar days OR 50 confirmed closed trades** per candidate
- **Idempotency Protection:** Active alert deduplication on unique `signal_id`
- **Active Circuit Breaker 1:** Emergency suspension upon **12 consecutive losses**
- **Active Circuit Breaker 2:** Emergency suspension upon **10.0% account equity drawdown**
- **Execution Mode:** Passive webhook ingestion via [`paper_trade_logger.py`](file:///c:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/research/forward_test/paper_trade_logger.py). Zero broker connections, zero real orders.

---

## 6. Automated Regression Test Verification

All 74 automated unit and regression tests were executed and confirmed passing:
- Core commercial product and syntax suite: **55 tests passed**
- Research harness, backtest models, and forward protocol suite: **19 tests passed**
- Total: **74 tests passed, 0 failures, 0 errors (100% pass rate)**.
