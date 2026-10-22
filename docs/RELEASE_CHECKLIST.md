# HR TradingView — Commercial Release Checklist & Quality Gates

**Domain**: Release Engineering & Governance (HR TradingView / ScaleNova / Hemanth Ranam)  
**Release Target**: Commercial Suite v2.0 (4 Product Families)  
**Last Updated**: 2026-10-22

---

## 1. Multi-Stage Quality Gates

To achieve full commercial release readiness, each product family must clear five progressive quality gates. No product may be distributed or promoted without documented clearance across all gates.

```
┌─────────────────────────┐
│ GATE 1: Local Integrity │ ◄── [CURRENT STATE: PASSED 55/55]
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ GATE 2: Native TV Comp. │ ◄── [PENDING MANUAL TV VERIFICATION]
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ GATE 3: Empirical BT    │ ◄── [PENDING STRATEGY TESTER EXPORTS]
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ GATE 4: MT5 Parity Sync │ ◄── [PARTIALLY MATCHED / AUDITED]
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ GATE 5: Release Sign-Off│ ◄── [BLOCKED UNTIL GATES 2-4 COMPLETE]
└─────────────────────────┘
```

---

## 2. Release Gate Specifications

### Gate 1: Local Code Integrity & Automated Validation
- [x] All 8 canonical Pine Script v6 files exist in `src/indicators/` and `src/strategies/`.
- [x] All scripts declare `//@version=6`.
- [x] Closed-bar execution (`process_orders_on_close = true`, `barstate.isconfirmed`) enforced.
- [x] Multi-timeframe requests protected against lookahead (`lookahead_off` and `[1]` historical offset).
- [x] 1.0% maximum equity risk sizing baseline configured.
- [x] Python regression suite passing 100% (`55/55` tests passed).
- [x] Zero credentials, secrets, or API keys in tracked files.

### Gate 2: Native TradingView Compilation
- [ ] `HR_EMA_Pullback_Indicator.pine` compiled in Pine Editor without warnings or errors.
- [ ] `HR_EMA_Pullback_Pro.pine` compiled in Pine Editor without warnings or errors.
- [ ] `HR_Liquidity_Sweep_Indicator.pine` compiled in Pine Editor without warnings or errors.
- [ ] `HR_Liquidity_Sweep_Strategy.pine` compiled in Pine Editor without warnings or errors.
- [ ] `HR_Volatility_Breakout_Indicator.pine` compiled in Pine Editor without warnings or errors.
- [ ] `HR_Volatility_Breakout_Strategy.pine` compiled in Pine Editor without warnings or errors.
- [ ] `HR_Market_Structure_Indicator.pine` compiled in Pine Editor without warnings or errors.
- [ ] `HR_Market_Structure_Strategy.pine` compiled in Pine Editor without warnings or errors.

### Gate 3: Empirical Strategy Tester Validation
- [ ] Backtests configured with $10,000 initial capital, 0.02% commission, 2 ticks slippage.
- [ ] Minimum 100 executed trades across evaluation period.
- [ ] Out-of-sample profit factor >= 1.30 on primary instruments.
- [ ] Maximum equity drawdown strictly < 15.0%.
- [ ] Trade logs exported as CSV and cataloged in `research/data/`.

### Gate 4: Cross-Platform MT5 Parity Reconciliation
- [x] Core entry/exit logic mapped to authoritative MT5 EAs in `HemanthRanam-MT5-EAs`.
- [x] Documented structural differences (single TV target vs MT5 partial scaling).
- [ ] Verification of broker feed alignment (OANDA/FXCM vs MT5 broker feed).

### Gate 5: Commercial Packaging & Legal Sign-Off
- [x] Technical manuals created for all 4 indicator products (`docs/indicators/`).
- [x] Technical manuals created for all 4 strategy products (`docs/strategies/`).
- [x] Prominent financial and risk disclaimers included in `README.md` and documentation.
- [x] Repository clean of cache artifacts, temp files, and non-whitelisted assets.
- [ ] Project Owner (Hemanth Ranam) commercial distribution sign-off.
