# HR TradingView — Backtest Protocol & Quantitative Validation Standard

**Domain**: Quantitative Research & Validation (HR TradingView / ScaleNova / Hemanth Ranam)  
**Governance**: Master Engine Protocol (Anti-Overfitting, Zero Blind Trust, Empirical Rigor)  
**Last Updated**: 2026-10-22

---

## 1. Principles of Empirical Backtesting

A profitable backtest in a single historical window is **never** proof of strategy robustness. Overfitting, survivorship bias, execution latency, and unrealistic friction often create illusions of profitability.

To establish authentic commercial readiness, all four HR TradingView strategies must undergo controlled native testing in TradingView's **Strategy Tester** under strict, reproducible standards.

---

## 2. Testing Environment & Cost Configuration

All native backtests must be executed with identical properties:

| Property | Standard Value | Rationale |
| :--- | :--- | :--- |
| **Initial Capital** | `$10,000 USD` | Standard retail/prop capital benchmark |
| **Position Sizing** | `1.0% of Equity` | Caps single-trade exposure strictly |
| **Commission** | `0.02%` (Cash/Percentage) | Models institutional ECN fees |
| **Slippage** | `2 Ticks` | Accounts for queue position and latency |
| **Bar Execution Model** | `On Bar Close` / Next Bar Open | Reflects `process_orders_on_close = true` |
| **Recalculate On Fill** | `False` | Prevents intrabar repainting during simulation |

---

## 3. Sample Split & Testing Windows

Strategies must be tested across two distinct temporal regimes:

```
┌─────────────────────────────────────────────────────────────┬────────────────────────────────┐
│ In-Sample (Optimization & Parameter Locking)               │ Out-of-Sample (Blind Forward)  │
│ 2024-01-01 to 2025-06-30 (18 Months)                       │ 2025-07-01 to 2026-10-22       │
└─────────────────────────────────────────────────────────────┴────────────────────────────────┘
```

1. **In-Sample Period (IS)**: 2024-01-01 to 2025-06-30 (18 months). Used to confirm baseline edge, verify trade frequency, and validate stop/target symmetry.
2. **Out-of-Sample Period (OOS)**: 2025-07-01 to 2026-10-22 (approx. 16 months). Blind validation test. Strategy parameters must remain frozen during OOS evaluation.

---

## 4. Product Test Matrix & Target Instruments

| Product ID | Product Name | Primary Timeframe | HTF Filter | Primary Instruments | Data Feed / Provider |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **HR-PRD-01** | EMA Trend Pullback Pro | 15M | 1H (200 EMA) | `XAUUSD`, `US500`, `EURUSD` | OANDA / TVC / Capital.com |
| **HR-PRD-02** | Liquidity Sweep Reversal Pro | 15M | None | `XAUUSD`, `EURUSD` | OANDA / FXCM |
| **HR-PRD-03** | Volatility Expansion Breakout | 15M | None | `USTEC` (`US100`), `XAUUSD` | TVC / OANDA |
| **HR-PRD-04** | Market Structure Momentum | 15M | None (200 EMA Macro) | `US500`, `XAUUSD` | TVC / OANDA |

---

## 5. Quantitative Acceptance Criteria (Release Gates)

For a strategy to pass the empirical validation gate and advance to paper trading, the out-of-sample backtest must meet all of the following benchmarks:

1. **Trade Sample Size**: Minimum of **100 executed trades** across the evaluation window (ensures statistical relevance).
2. **Profit Factor (PF)**: Strictly **>= 1.30** after factoring in commission and slippage.
3. **Maximum Drawdown (Max DD)**: Under **15.0%** of peak equity.
4. **Win Rate vs. Risk-Reward Consistency**:
   - For 1.5R systems: Win rate >= 42%.
   - For 2.5R systems: Win rate >= 32%.
5. **No Parameter Curve-Fitting**: Edge must persist across neighboring parameter values (±20% variation in lookbacks and ATR multipliers).

---

## 6. Backtest Recording & Export Workflow

1. Configure Strategy Tester in TradingView.
2. Select target symbol, timeframe, and date range.
3. Generate the backtest report.
4. Export the Trade List via **Download CSV**.
5. Save the CSV in `research/data/` or import using the quantitative importer:
   ```bash
   python research/scripts/tv_importer.py --csv <path-to-export.csv> --strategy <strategy-name> --symbol <symbol> --period-type out_of_sample
   ```
6. Update `docs/VERIFICATION_STATUS.md` with the observed empirical metrics.
