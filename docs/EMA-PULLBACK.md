# Hemanth Ranam — EMA Pullback Pro Manual

## 1. Overview
The **EMA Pullback Pro** is the flagship trend-following strategy of the Hemanth Ranam TradingView Suite. It identifies high-probability continuation entries in established trends by requiring multi-moving average alignment, higher timeframe confirmation, and dynamic value-zone pullbacks.

---

## 2. Core Method & Strategy Engine
* **Moving Average Baseline**: 9 EMA (Fast), 21 EMA (Pullback Target), 200 EMA (Long-term Trend Baseline).
* **Higher Timeframe Filter**: 1H (60m) trend baseline alignment to ensure trades align with macro directional momentum.
* **Pullback Value Zone**: Price penetrates or tests the area between the 9 EMA and 21 EMA without closing beyond the 21 EMA.
* **Candlestick Confirmation**: Bullish/bearish engulfing or high/low breakout trigger.
* **Setup Quality Scoring**: 8-factor score engine (requires $\ge 6/8$ score to execute).

---

## 3. Recommended Starting Settings
| Parameter | Conservative (Swing) | Moderate (Intraday) | Aggressive (Scalp) |
| :--- | :--- | :--- | :--- |
| **Timeframe** | 1H / 4H | 15m / 30m | 5m |
| **HTF Filter** | Daily | 1H (60m) | 15m |
| **ADX Minimum** | 25 | 20 | 18 |
| **SL Multiplier**| 2.0 ATR | 1.5 ATR | 1.2 ATR |
| **Take Profit 1**| 2.0 R:R | 1.5 R:R | 1.5 R:R |

---

## 4. Webhook Alert Schema
```json
{
  "brand": "Hemanth Ranam",
  "system": "TradingView",
  "strategy": "EMA Pullback Pro",
  "signal": "BUY",
  "symbol": "XAUUSD",
  "timeframe": "5",
  "entry": 3342.50,
  "stop_loss": 3336.10,
  "take_profit_1": 3351.50,
  "score": 7,
  "timestamp": 1724784000
}
```

---

## 5. Non-Repainting & Real-Time Considerations
* HTF security requests utilize `barmerge.lookahead_off` and `close[1]` offsets.
* Orders and alerts fire strictly on the close of the confirmation candle.
