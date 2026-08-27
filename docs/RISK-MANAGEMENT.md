# Hemanth Ranam — Trading Risk Management Principles

## 1. Institutional 1% Capital Rule
* **Maximum Account Risk**: No single setup should ever risk more than **1.0%** of total account equity.
* **Stop Loss Sizing**: Dynamic stop losses are derived from market volatility ($1.5 \times \text{ATR}$) rather than arbitrary fixed pips/points.
* **Position Sizing Formula**:
  $$\text{Position Size (Lots)} = \frac{\text{Account Balance} \times 0.01}{\text{Stop Loss Distance} \times \text{Tick Value}}$$

---

## 2. Daily Drawdown Circuit Breaker
If cumulative intraday losses reach **3.0%** of starting balance, all trading execution is halted until the next daily session.
