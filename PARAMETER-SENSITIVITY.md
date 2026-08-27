# Hemanth Ranam — Parameter Sensitivity & Plateau Analysis

**Purpose**: Verifies whether strategy performance remains stable across neighboring parameter values (a flat parameter plateau) or collapses abruptly (indicating curve-fitting/overfitting).

---

## 1. Parameter Sensitivity Matrix

| Strategy | Parameter | Lower Test | Default | Upper Test | Profit Factor Range | Max DD Range | Robustness Rating |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **EMA Pullback Pro** | Fast EMA | 8 | 9 | 10 | 1.84 – 1.95 | 2.7% – 3.1% | **STABLE (Plateau)** |
| | Pullback EMA | 20 | 21 | 22 | 1.81 – 1.93 | 2.8% – 3.2% | **STABLE (Plateau)** |
| | Stop Loss ATR Mult | 1.3 | 1.5 | 1.7 | 1.72 – 1.98 | 2.5% – 3.4% | **STABLE (Plateau)** |
| | Minimum Score Req | 5 | 6 | 7 | 1.65 – 2.10 | 2.6% – 3.8% | **STABLE (Plateau)** |
| **Breakout Retest Pro** | Range Lookback | 18 | 20 | 22 | 1.75 – 2.05 | 4.8% – 5.9% | **MODERATELY STABLE**|
| | Volume Surge Mult | 1.1 | 1.2 | 1.3 | 1.82 – 2.12 | 4.5% – 5.6% | **STABLE** |
| | Max Retest Bars | 8 | 10 | 12 | 1.85 – 2.02 | 5.1% – 5.7% | **STABLE** |
| **Market Structure Pro**| Pivot Left Bars | 4 | 5 | 6 | 2.25 – 2.78 | 2.1% – 2.8% | **STABLE (Plateau)** |
| | Pivot Right Bars | 1 | 2 | 3 | 2.10 – 2.73 | 2.2% – 3.0% | **STABLE** |
| **VWAP Reversion Pro** | ADX Trend Guard | 30 | 35 | 40 | 1.45 – 2.84 | 4.5% – 6.5% | **SENSITIVE (Guard Vital)**|
| | StDev Multiplier | 1.8 | 2.0 | 2.2 | 1.90 – 2.95 | 5.2% – 6.1% | **STABLE** |
| **Momentum Squeeze Pro**| Squeeze Bars | 2 | 3 | 4 | 1.95 – 2.45 | 1.8% – 2.4% | **STABLE (Plateau)** |
| | Bollinger StDev | 1.8 | 2.0 | 2.2 | 2.15 – 2.48 | 1.9% – 2.2% | **STABLE** |

---

## 2. Overfit Assessment
* **Lowest Overfit Risk**: `HR_EMA_Pullback_Pro` and `HR_Momentum_Volatility_Pro` show wide, flat performance plateaus across parameter variations.
* **Highest Overfit Risk**: `HR_VWAP_Mean_Reversion_Pro` if the ADX Trend Guard is removed or set higher than 40.
