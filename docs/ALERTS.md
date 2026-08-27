# Hemanth Ranam — TradingView Webhook Alerts Architecture

## 1. End-to-End Alert Relay Flow
```
TradingView Alert (JSON Payload)
       ↓
Webhook Ingestion API (hemanth-ranam-trading-alert-api)
       ↓
Signal Deduplication & Risk Sizing Engine
       ↓
Telegram Broadcaster (hemanth-ranam-trading-telegram) & MT5 Bridge (hemanth-ranam-mt5)
```

---

## 2. Standardized JSON Contract
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
