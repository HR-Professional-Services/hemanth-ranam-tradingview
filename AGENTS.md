# AGENTS.md — Permanent Operational Instructions for Future AI Agents

**Domain**: Quantitative Trading Systems (HR TradingView / ScaleNova / Hemanth Ranam)  
**Governance**: Master Engine Protocol (Dual AI Model, Zero Blind Trust, Evidence-First)  
**Authority**: Execution Authority: Antigravity | Analytical Review: Gemini CLI  
**Last Updated**: 2026-10-22

---

## 1. Prime Directives & Anti-Hallucination Guardrails

Future AI agents operating in this repository MUST strictly follow these rules:

1. **Verify Code Reality Before Asserting Facts**:
   - Always inspect the actual source code, Git working tree, and test outputs before claiming a feature exists, compiles, or performs well.
   - Do not invent file paths, functions, parameters, broker specifications, alerts, or performance numbers.

2. **Strict Status Taxonomy**:
   - **`LOCAL-VALIDATION-PASSED`**: Only when local Python/static tests pass.
   - **`NATIVE-COMPILATION-PENDING`**: Never claim a Pine script compiles natively in TradingView unless an actual compilation was observed in the TradingView Pine Editor and recorded with real output.
   - **`BACKTEST-PENDING`**: Never claim a strategy is profitable, passed, or has an institutional edge without empirical CSV trade records exported from TradingView Strategy Tester.
   - **`MT5-PARITY-REVIEW-PENDING`** or **`PARTIAL`**: Never claim 100% parity with MT5 without comprehensive source line comparison and execution alignment.
   - **`DEFERRED-RESEARCH-CANDIDATE`**: Assigned to HR-PRD-05 (Adaptive Market Regime).

3. **Read-Only Preservation of Historical Work**:
   - Preserved directories (`src/legacy/`, `recovered/`) must NEVER be deleted, overwritten, or renamed. They serve as an immutable historical record and audit trail.
   - Never present an old prototype as current commercial code.

4. **MT5 Reference Repository Isolation**:
   - `HR-Professional-Services/HemanthRanam-MT5-EAs` is the authoritative reference for MT5 logic.
   - It is strictly **READ-ONLY** during TradingView tasks. Never edit, commit, or push changes to the MT5 repository from this workspace.

5. **Secrets & Privacy Hygiene**:
   - Zero live API tokens, passwords, broker logins, or personal credentials may ever be committed, staged, or written to documentation or code.

---

## 2. Directory Layout & Canonical Paths

- **Commercial Indicators**: `src/indicators/` (4 files: `HR_EMA_Pullback_Indicator.pine`, `HR_Liquidity_Sweep_Indicator.pine`, `HR_Volatility_Breakout_Indicator.pine`, `HR_Market_Structure_Indicator.pine`).
- **Commercial Strategies**: `src/strategies/` (4 files: `HR_EMA_Pullback_Pro.pine`, `HR_Liquidity_Sweep_Strategy.pine`, `HR_Volatility_Breakout_Strategy.pine`, `HR_Market_Structure_Strategy.pine`).
- **Technical Documentation**: `docs/` (Canonical documents: `PRODUCT_CATALOG.md`, `INSTALLATION_AND_USAGE.md`, `STRATEGY_REFERENCE.md`, `ALERTS_AND_INTEGRATION.md`, `ARCHITECTURE.md`, `VERIFICATION_STATUS.md`, `MT5_PARITY_MATRIX.md`, `BACKTEST_PROTOCOL.md`, `RELEASE_CHECKLIST.md`).
- **Automated Validation Suite**: `tests/` (Executed via `python -m unittest discover tests`).

---

## 3. Git & Publication Workflows

- **Target Repository**: `https://github.com/HR-Professional-Services/hemanth-ranam-tradingview`
- **Active Working Branch**: `feat/commercial-indicators-phase2-4`
- **Zero Force-Pushes**: Never run `git push --force` or rewrite Git commit history.
- **Stage Exclusively Relevant Files**: Never run blanket `git add .` without reviewing untracked files and ensuring build caches (`__pycache__`, `.pyc`) are excluded via `.gitignore`.
