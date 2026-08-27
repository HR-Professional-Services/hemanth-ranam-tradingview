# Hemanth Ranam — Market Structure Pro Manual

## 1. Overview
The **Market Structure Pro** strategy identifies structural shifts (Break of Structure — BOS and Change of Character — CHoCH) based on algorithmic swing pivot tracking (HH/HL and LH/LL).

---

## 2. Core Method
* **Swing Pivots**: 5-bar left, 2-bar right fractal pivot algorithm.
* **Break of Structure (BOS)**: Price crossing prior validated swing high/low.
* **Trend Alignment**: 200 EMA macro trend directional filter.
* **Scoring Engine**: Evaluates pivot freshness, candle body momentum, and session filters.

---

## 3. Webhook Alert Schema
```json
{
  "brand": "Hemanth Ranam",
  "system": "TradingView",
  "strategy": "Market Structure Pro",
  "signal": "BUY",
  "symbol": "US500",
  "timeframe": "5",
  "entry": 5620.50,
  "stop_loss": 5605.00,
  "take_profit_1": 5651.50,
  "timestamp": 1724784000
}
```
