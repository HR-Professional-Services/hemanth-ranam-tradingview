# Hemanth Ranam — Strategy Optimization & Parameter Tuning

## 1. Proven Parameter Ranges
* **EMA Pullback Pro**:
  * Fast EMA: `8–10` (Default: `9`)
  * Pullback EMA: `20–22` (Default: `21`)
  * Minimum Setup Score: `5–7` (Default: `6/8`)
  * Stop Loss ATR Multiplier: `1.3–1.8` (Default: `1.5`)
* **Momentum Squeeze Pro**:
  * Squeeze Compression Bars: `3–5` (Default: `3`)
  * Bollinger StDev Multiplier: `1.8–2.2` (Default: `2.0`)
* **VWAP Mean Reversion Pro**:
  * Trend Guard ADX Threshold: `30–35` (Default: `35`)
  * RSI Oversold/Overbought: `25–30` / `70–75` (Default: `30/70`)

---

## 2. Preventing Curve-Fitting (Overfit Protection)
1. Never calibrate parameters to a single historical spike.
2. Ensure parameter variation of $\pm 10\%$ does not cause performance degradation $>15\%$.
3. Run out-of-sample forward testing across at least 3 uncorrelated instruments (e.g. `XAUUSD`, `US500`, `EURUSD`).
