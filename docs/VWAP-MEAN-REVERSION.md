# Hemanth Ranam — VWAP Mean Reversion Pro Manual

## 1. Overview
The **VWAP Mean Reversion Pro** strategy trades statistical exhaustion away from the volume-weighted average price (VWAP) back toward the mean.

---

## 2. Key Safeguard: Trend Protection Guard
Unlike naive mean-reversion systems that blow up during parabolic trends, VWAP Mean Reversion Pro includes an automated **Trend Protection Guard**:
* If ADX trend strength exceeds 35, all reversal entries are locked out.
* Trades only trigger when RSI is oversold/overbought ($\le 30$ / $\ge 70$) AND price exhibits candle rejection confirmation back inside the 2.0 standard deviation band.

---

## 3. Webhook Alert Schema
```json
{
  "brand": "Hemanth Ranam",
  "system": "TradingView",
  "strategy": "VWAP Mean Reversion Pro",
  "signal": "BUY",
  "symbol": "GBPUSD",
  "timeframe": "15",
  "entry": 1.3120,
  "stop_loss": 1.3090,
  "take_profit_1": 1.3150,
  "timestamp": 1724784000
}
```
