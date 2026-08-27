# Hemanth Ranam — Momentum Volatility Pro Manual

## 1. Overview
The **Momentum Volatility Pro** strategy detects institutional volatility compression (Bollinger Bands narrowing completely inside Keltner Channels) and enters on the explosive directional expansion release.

---

## 2. Core Method
* **Squeeze Detection**: Bollinger Band (20, 2.0 StDev) inside Keltner Channel (20, 1.5 ATR).
* **Compression Threshold**: Requires minimum 3 consecutive bars in squeeze before qualification.
* **Directional Trigger**: Fast EMA 9 / Slow EMA 21 momentum alignment + close beyond outer band.

---

## 3. Webhook Alert Schema
```json
{
  "brand": "Hemanth Ranam",
  "system": "TradingView",
  "strategy": "Momentum Volatility Pro",
  "signal": "BUY",
  "symbol": "US100",
  "timeframe": "5",
  "entry": 19850.00,
  "stop_loss": 19780.00,
  "take_profit_1": 19990.00,
  "timestamp": 1724784000
}
```
