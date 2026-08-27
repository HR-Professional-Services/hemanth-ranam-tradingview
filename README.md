# Hemanth Ranam — Multi-Strategy Trading Engine (TradingView / Pine Script v5)

Institutional-grade, modular TradingView Pine Script v5 indicator suite featuring five robust strategy frameworks, dynamic risk management calculations, a compact on-chart HUD dashboard, and standardized webhook alert JSON payloads.

---

## 🎯 Five Strategy Frameworks Included

1. **EMA Pullback & Trend Continuation**: 9/21/200 EMA structure + 1H higher timeframe trend filter + pullback value zone confirmation.
2. **Breakout + Retest**: 20-period range boundary detection + structural retest hold.
3. **Market Structure Continuation**: Swing pivot highs/lows (HH/HL/LH/LL) trend tracking.
4. **VWAP Mean Reversion**: 2.0 Standard Deviation bands + RSI exhaustion confirmation.
5. **Momentum Volatility Expansion**: Bollinger & Keltner squeeze release breakout detection.

---

## 📊 Features & Technical Architecture
* **Pine Script Version**: `v5`
* **On-Chart Telemetry HUD**: Displays real-time Trend, EMA Structure, ATR Volatility, and active setup direction.
* **Dynamic Targets**: Auto-calculates Entry, Stop Loss (1.5 ATR), TP1 (1:1.5 R:R), and TP2 (1:2.5 R:R).
* **Webhook Automation Ready**: Emits structured JSON alerts compatible with `hemanth-ranam-trading-alert-api`.

---

## 📡 Webhook Alert Payload Schema
```json
{
  "brand": "Hemanth Ranam",
  "system": "TradingEngine",
  "strategy": "EMA Pullback",
  "symbol": "XAUUSD",
  "timeframe": "5",
  "signal": "BUY",
  "entry": 3342.50,
  "stop_loss": 3336.10,
  "take_profit_1": 3351.50,
  "timestamp": 1724784000
}
```

---

## 🧪 Testing & Validation
```bash
python3 -m unittest tests/test_pine_syntax.py
```

---

## ⚖️ Disclaimer
*For educational and software development purposes only. Past performance does not guarantee future results. Always plan and manage your trading risk.*

**Author**: Hemanth Ranam  
**Website**: [https://app.hemanth-ranam.workers.dev/](https://app.hemanth-ranam.workers.dev/)
