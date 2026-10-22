# HR TradingView — System Architecture

**Domain**: Quantitative Systems Architecture (ScaleNova / HR TradingView / Hemanth Ranam)  
**Governance**: Master Engine Protocol (Dual AI Model, Zero Blind Trust, Closed-Bar Integrity)  
**Last Updated**: 2026-10-22

---

## 1. Repository Layout & Logical Separation

The repository is structured to cleanly separate production commercial indicators, Strategy Tester strategies, Python validation test suites, research lab tools, and historical legacy artifacts.

```
hemanth-ranam-tradingview/
├── .github/                   # CI/CD workflows and actions
├── .gitignore                 # Python cache, OS artifacts, and build exclusions
├── AGENTS.md                  # Permanent instructions and guardrails for future AI agents
├── README.md                  # Public master documentation & usage overview
│
├── src/                       # Production Pine Script v6 source files
│   ├── indicators/            # 4 Standalone Commercial Indicators (Visualization & Alerts)
│   │   ├── HR_EMA_Pullback_Indicator.pine
│   │   ├── HR_Liquidity_Sweep_Indicator.pine
│   │   ├── HR_Volatility_Breakout_Indicator.pine
│   │   └── HR_Market_Structure_Indicator.pine
│   ├── strategies/            # 4 Standalone Commercial Strategies (Strategy Tester Backtesting)
│   │   ├── HR_EMA_Pullback_Pro.pine
│   │   ├── HR_Liquidity_Sweep_Strategy.pine
│   │   ├── HR_Volatility_Breakout_Strategy.pine
│   │   └── HR_Market_Structure_Strategy.pine
│   └── legacy/                # Preserved historical scripts and prototypes (Read-Only)
│       └── HemanthRanamTradingSystem.pine
│
├── docs/                      # Comprehensive technical documentation & references
│   ├── PRODUCT_CATALOG.md     # Product inventory, specs, and status definitions
│   ├── INSTALLATION_AND_USAGE.md # Practical setup guide for TradingView users
│   ├── STRATEGY_REFERENCE.md  # Detailed mathematical signal logic and equations
│   ├── ALERTS_AND_INTEGRATION.md # Standardized JSON webhook schema and payloads
│   ├── ARCHITECTURE.md        # System architecture, file layout, and conventions
│   ├── VERIFICATION_STATUS.md # Evidence-based verification and audit ledger
│   ├── MT5_PARITY_MATRIX.md   # Feature-by-feature comparison with authoritative MT5 EAs
│   ├── BACKTEST_PROTOCOL.md   # Rigorous empirical testing protocol & cost modeling
│   ├── RELEASE_CHECKLIST.md   # Explicit release gates for production sign-off
│   ├── indicators/            # Dedicated product manuals for indicators
│   └── strategies/            # Dedicated product manuals for strategies
│
├── tests/                     # Automated Python testing and validation engine
│   ├── test_commercial_products.py # Structural syntax, v6 declaration, security checks
│   ├── test_pine_syntax.py    # AST and regex structural validation
│   ├── test_strategies_v6.py  # Pine Script v6 compliance verification
│   └── backtest_engine.py     # Python simulation engine for synthetic regimes
│
├── research/                  # Quantitative research, historical datasets & configurations
│   ├── configs/               # Market, timeframe, and cost configuration files
│   ├── scripts/               # Quantitative analysis, TV CSV importer, sensitivity tools
│   └── schema/                # Alert payload JSON schemas
│
└── recovered/                 # Recovered prototypes and historical snapshots (Preserved)
```

---

## 2. Code Responsibilities & Boundaries

### Commercial Indicators (`src/indicators/`)
- Declared with `@version=6` and `indicator(..., overlay = true)`.
- Responsible for real-time visual chart feedback: EMA ribbons, consolidation boxes, fractal swing points, and signal markers.
- Render compact on-chart diagnostic tables displaying trend state, setup grade, and volatility.
- Emit structured JSON alerts using `alert(payload, alert.freq_once_per_bar_close)`.
- Never execute orders directly; zero side-effects on broker accounts.

### Commercial Strategies (`src/strategies/`)
- Declared with `@version=6` and `strategy(..., overlay = true)`.
- Responsible for historical simulation inside TradingView's native **Strategy Tester**.
- Configure explicit execution parameters: `process_orders_on_close = true`, `default_qty_type = strategy.percent_of_equity`, `default_qty_value = 1.0`, `commission_type = strategy.commission.percent`, `commission_value = 0.02`, `slippage = 2`.
- Enforce strict closed-bar entries and exact structural stop and profit target orders (`strategy.entry()`, `strategy.exit()`).

### Test & Validation Infrastructure (`tests/`)
- Pure Python 3 test suites verifying file existence, syntax validity, lookahead prevention, risk parameter constraints, and alert schema integrity.
- Executed via standard discovery: `python -m unittest discover tests`.
- Must pass 100% prior to any repository release or commit.

---

## 3. Engineering Conventions & Guardrails

1. **Closed-Bar Execution**: All indicators and strategies require completed bar closes (`barstate.isconfirmed`) before finalizing signals to prevent intrabar repainting.
2. **Anti-Repainting Multi-Timeframe Indexing**: Every `request.security()` call MUST use `lookahead = barmerge.lookahead_off` and historical `[1]` indexing on the requested series.
3. **Strict 1.0% Capital Risk Guardrail**: Default capital risk per trade is strictly capped at 1.0% of account equity.
4. **Historical Preservation**: Legacy and recovered files are permanently preserved as historical context and audit trail; they are never deleted or rewritten.
