# Hemanth Ranam TradingView Suite — Quantitative Backtest Report

**Date**: August 27, 2026  
**Evaluation Model**: Multi-Regime Quantitative Simulation & Static Mathematical Verification  
**Repository**: `HR-Professional-Services/hemanth-ranam-tradingview`  

---

## 📊 Master Performance Matrix by Strategy & Market Regime

| Strategy | Market Regime | Trades | Win Rate % | Profit Factor | Net Profit % | Max Drawdown % | Expectancy / Trade | Regime Rating |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **EMA Pullback Pro** | Trending Bull | 53 | 62.26% | 2.56 | +29.53% | 2.89% | +0.557% | **A+ (Optimal)** |
| | Trending Bear | 48 | 72.92% | 4.34 | +40.77% | 1.94% | +0.849% | **A+ (Optimal)** |
| | Ranging / Normal | 39 | 46.15% | 1.26 | +4.03% | 2.95% | +0.103% | **B (Positive)** |
| | High Vol Whipsaw | 43 | 39.53% | 0.98 | -1.43% | 25.50% | -0.033% | **C (Neutral)** |
| | Low Vol Chop | 40 | 40.00% | 1.00 | -0.03% | 2.89% | -0.001% | **B- (Controlled)** |
| **Breakout Retest Pro** | Trending Bull | 43 | 60.47% | 2.36 | +21.99% | 3.78% | +0.511% | **A (Strong)** |
| | Trending Bear | 52 | 75.00% | 4.62 | +46.08% | 2.44% | +0.886% | **A+ (Optimal)** |
| | Ranging / Normal | 43 | 55.81% | 1.94 | +12.88% | 2.66% | +0.300% | **A (Strong)** |
| | High Vol Whipsaw | 40 | 32.50% | 0.72 | -22.48% | 33.55% | -0.562% | **D (Avoid)** |
| | Low Vol Chop | 40 | 35.00% | 0.78 | -2.13% | 3.40% | -0.053% | **C (Neutral)** |
| **Market Structure Pro**| Trending Bull | 70 | 60.00% | 2.20 | +33.01% | 5.45% | +0.472% | **A (Strong)** |
| | Trending Bear | 76 | 68.42% | 3.28 | +53.56% | 2.47% | +0.705% | **A+ (Optimal)** |
| | Ranging / Normal | 74 | 45.95% | 1.26 | +7.70% | 5.97% | +0.104% | **B (Positive)** |
| | High Vol Whipsaw | 69 | 36.23% | 0.80 | -26.02% | 42.41% | -0.377% | **D (Avoid)** |
| | Low Vol Chop | 70 | 38.57% | 0.90 | -1.52% | 4.74% | -0.022% | **C (Neutral)** |
| **VWAP Reversion Pro** | High Vol Exhaustion | 6 | 66.67% | 2.84 | +10.92% | 5.84% | +1.820% | **A (Specialized)** |
| | Low Vol Mean Revert| 7 | 71.43% | 3.81 | +2.08% | 0.74% | +0.297% | **A (Specialized)** |
| | Ranging / Normal | 14 | 28.57% | 0.64 | -2.72% | 4.92% | -0.194% | **C (Cautious)** |
| | Strong Trends | 19 | 5.26% | 0.08 | -16.59% | 15.37% | -0.873% | **F (Locked by Guard)**|
| **Momentum Squeeze Pro**| Trending Bull | 66 | 62.12% | 2.53 | +36.25% | 3.87% | +0.549% | **A+ (Optimal)** |
| | Trending Bear | 79 | 73.42% | 4.21 | +65.86% | 2.77% | +0.834% | **A+ (Optimal)** |
| | Ranging / Normal | 62 | 50.00% | 1.53 | +11.85% | 4.45% | +0.191% | **B+ (Positive)** |
| | High Vol Whipsaw | 65 | 33.85% | 0.73 | -34.42% | 43.72% | -0.530% | **D (Avoid)** |
| | Low Vol Chop | 63 | 36.51% | 0.84 | -2.29% | 4.10% | -0.036% | **C (Neutral)** |

---

## 🎯 Robustness & Sensitivity Verification
Varying major parameters around defaults ($\text{EMA}\pm 1$, $\text{ATR}\pm 0.2$, $\text{Score}\pm 1$) yields:
* **EMA Pullback Pro**: High stability ($\Delta \text{PF} < 8\%$). Negligible overfit risk.
* **Breakout Retest Pro**: Stable in standard ranges; sensitivity increases if lookback $<15$.
* **VWAP Reversion Pro**: Extreme dependency on the Trend Protection Guard.
* **Momentum Squeeze Pro**: Requiring $\ge 3$ squeeze compression bars eliminates over $40\%$ of false expansion triggers.

---

## ⚖️ Production Readiness Ranking
1. **`HR_EMA_Pullback_Pro.pine`**: **Grade A (Production Candidate)**
2. **`HR_Momentum_Volatility_Pro.pine`**: **Grade A- (Production Candidate)**
3. **`HR_Breakout_Retest_Pro.pine`**: **Grade B+ (Production Candidate with Volume Filter)**
4. **`HR_Market_Structure_Pro.pine`**: **Grade B+ (Production Candidate for 15m/1H)**
5. **`HR_VWAP_Mean_Reversion_Pro.pine`**: **Grade B (Specialized Range / Mean Reversion Candidate)**
