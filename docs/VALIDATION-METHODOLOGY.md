# Hemanth Ranam — Strategy Validation & Testing Methodology

## 1. Multi-Tier Validation Hierarchy
To prevent over-reliance on simulated assumptions, all strategies in the Hemanth Ranam TradingView Suite are subjected to a rigorous 3-tier validation framework:

```
Tier 1: Custom Python Simulation (Research & Mathematical Logic Verification)
       ↓
Tier 2: TradingView Strategy Tester (Native Pine Script Execution on Live Broker Feeds)
       ↓
Tier 3: Forward Testing & Paper Trading (Real-Time Order Routing & Slippage Validation)
```

---

## 2. Friction & Execution Cost Scenarios
Short-term intraday strategies (5m/15m) are heavily impacted by real-world execution friction. We evaluate three standardized cost tiers:

| Scenario | Commission (Per Side) | Slippage Assumption | Round-Trip Friction Impact | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Scenario A (Reference)** | $0.00\%$ | $0$ Ticks | $0.00\%$ | Theoretical zero-friction baseline |
| **Scenario B (Realistic)** | $0.02\%$ | $2$ Ticks | $\approx 0.05\%$ | Standard broker execution profile |
| **Scenario C (Stress)** | $0.06\%$ | $4$ Ticks | $\approx 0.15\%$ | High-spread news & illiquid session stress test |

---

## 3. In-Sample vs Out-of-Sample Discipline
* **In-Sample (60%)**: Used exclusively for structural formulation and baseline parameter selection.
* **Validation (20%)**: Used for parameter neighborhood stability verification.
* **Out-of-Sample (20%)**: Parameters are strictly **LOCKED**. If out-of-sample performance degrades excessively ($\Delta \text{PF} > 40\%$), the strategy is marked as `OOS FAILURE` rather than re-optimized.
