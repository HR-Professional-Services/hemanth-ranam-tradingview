# Hemanth Ranam — Breakout Retest Pro Manual

## 1. Overview
The **Breakout Retest Pro** strategy captures directional continuation trades by waiting for confirmed breaks of 20-period range extremes followed by a structural retest and hold of the broken level.

---

## 2. Core Method
1. **Range Definition**: Dynamic 20-period swing highs and lows.
2. **Breakout Trigger**: Price crosses and closes beyond range boundary with $\ge 1.2\times$ average volume.
3. **Retest Verification**: Price pulls back toward the broken support/resistance level within 10 bars without violating the boundary.
4. **Order Execution**: Order triggers when price resumes original breakout direction.

---

## 3. Webhook Alert Schema
```json
{
  "brand": "Hemanth Ranam",
  "system": "TradingView",
  "strategy": "Breakout Retest Pro",
  "signal": "BUY",
  "symbol": "EURUSD",
  "timeframe": "15",
  "entry": 1.0850,
  "stop_loss": 1.0820,
  "take_profit_1": 1.0910,
  "timestamp": 1724784000
}
```
