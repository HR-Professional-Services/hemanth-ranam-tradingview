# Hemanth Ranam — Strategy Backtesting & Robustness Guide

## 1. Multi-Asset Evaluation Matrix
Never optimize parameters against a single historical asset curve. Test each strategy across diverse asset classes:
* **Precious Metals**: XAUUSD, XAGUSD
* **Equity Indices**: US500, US100
* **Forex Majors**: EURUSD, GBPUSD, USDJPY

---

## 2. Key Performance Indicators (KPIs)
* **Profit Factor**: Aim for $\ge 1.50$ across $>100$ trades.
* **Win Rate vs Reward/Risk**: A 45% win rate with a 1:2.0 average R:R produces strong positive expectancy.
* **Max Historical Drawdown**: Must remain strictly below 10% on simulated equity.
