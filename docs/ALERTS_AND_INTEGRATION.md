# HR TradingView — Alerts & Webhook Integration Standard

**Domain**: Systems Integration (HR TradingView / ScaleNova / Chartora)  
**Standard**: Signal Contract v2.0  
**Transport**: HTTP POST JSON Webhook  
**Last Updated**: 2026-10-22

---

## 1. Webhook Architecture Overview

All HR TradingView indicators and strategies emit structured JSON payloads via the native Pine Script `alert()` function. These payloads are designed for direct ingestion by webhook listeners, trade execution gateways, Telegram/Discord bots, and internal trade loggers.

```
┌─────────────────────────────────┐
│ TradingView Bar Close Event     │
│ (barstate.isconfirmed == true)  │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Script Evaluates Signal Rules   │
│ Computes Stop, TP, Grade, ATR   │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ alert(payload, alert.freq_once_ │
│       per_bar_close)            │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ TradingView Webhook Engine      │
│ POST https://api.yourdomain.com │
└─────────────────────────────────┘
```

---

## 2. Standardized JSON Schema

Every generated alert payload conforms strictly to the following JSON structure:

```json
{
  "brand": "HR TradingView",
  "strategy": "HR_EMA_Pullback_Pro",
  "product_id": "HR-PRD-01",
  "signal": "BUY",
  "symbol": "XAUUSD",
  "timeframe": "15",
  "entry": 2735.40,
  "stop_loss": 2728.15,
  "take_profit_1": 2746.28,
  "take_profit_2": 2757.15,
  "risk_r": 1.5,
  "score": 85,
  "grade": "A",
  "timestamp": 1729614000000
}
```

### Field Definitions

| Field | Type | Description |
| :--- | :--- | :--- |
| `brand` | `string` | Always `"HR TradingView"` |
| `strategy` | `string` | Script identifier (e.g. `"HR_Liquidity_Sweep_Strategy"`) |
| `product_id` | `string` | Canonical product code (`HR-PRD-01` through `HR-PRD-04`) |
| `signal` | `string` | Directional action: `"BUY"`, `"SELL"`, `"CLOSE_LONG"`, `"CLOSE_SHORT"` |
| `symbol` | `string` | TradingView ticker symbol (`syminfo.ticker`) |
| `timeframe` | `string` | Chart interval resolution (`timeframe.period`) |
| `entry` | `number` | Closing price of the signal bar (intended entry fill price) |
| `stop_loss` | `number` | Exact structural or ATR stop price |
| `take_profit_1` | `number` | Primary target level (1.5R to 2.5R depending on strategy) |
| `take_profit_2` | `number` | Secondary target level or runner target (if enabled) |
| `risk_r` | `number` | Target reward-to-risk ratio |
| `score` | `number` | Quantitative setup score (0–100) based on alignment metrics |
| `grade` | `string` | Setup quality grade: `"A+"`, `"A"`, `"B"`, `"C"` |
| `timestamp` | `number` | Bar closing UNIX timestamp in milliseconds (`time_close`) |

---

## 3. Real Example Payloads per Product

### Product 1: HR EMA Trend Pullback Pro
```json
{
  "brand": "HR TradingView",
  "strategy": "HR_EMA_Pullback_Pro",
  "product_id": "HR-PRD-01",
  "signal": "BUY",
  "symbol": "XAUUSD",
  "timeframe": "15",
  "entry": 2742.10,
  "stop_loss": 2734.60,
  "take_profit_1": 2753.35,
  "risk_r": 1.5,
  "score": 90,
  "grade": "A+",
  "timestamp": 1729614900000
}
```

### Product 2: HR Liquidity Sweep Reversal Pro
```json
{
  "brand": "HR TradingView",
  "strategy": "HR_Liquidity_Sweep_Strategy",
  "product_id": "HR-PRD-02",
  "signal": "SELL",
  "symbol": "EURUSD",
  "timeframe": "15",
  "entry": 1.08450,
  "stop_loss": 1.08620,
  "take_profit_1": 1.08025,
  "risk_r": 2.5,
  "score": 85,
  "grade": "A",
  "timestamp": 1729615800000
}
```

### Product 3: HR Volatility Expansion Breakout Pro
```json
{
  "brand": "HR TradingView",
  "strategy": "HR_Volatility_Breakout_Strategy",
  "product_id": "HR-PRD-03",
  "signal": "BUY",
  "symbol": "USTEC",
  "timeframe": "15",
  "entry": 20450.0,
  "stop_loss": 20380.0,
  "take_profit_1": 20625.0,
  "risk_r": 2.5,
  "score": 80,
  "grade": "A",
  "timestamp": 1729616700000
}
```

### Product 4: HR Market Structure Momentum Pro
```json
{
  "brand": "HR TradingView",
  "strategy": "HR_Market_Structure_Strategy",
  "product_id": "HR-PRD-04",
  "signal": "BUY",
  "symbol": "US500",
  "timeframe": "15",
  "entry": 5860.25,
  "stop_loss": 5845.00,
  "take_profit_1": 5896.85,
  "risk_r": 2.4,
  "score": 88,
  "grade": "A",
  "timestamp": 1729617600000
}
```

---

## 4. Webhook Setup Instructions

1. Configure your receiving server with an SSL/TLS endpoint (TradingView requires HTTPS).
2. Create an alert on the chart selecting **Any alert() function call**.
3. Under **Notification**, enable **Webhook URL** and paste your endpoint:
   `https://api.yourdomain.com/v1/tradingview-webhook`
4. Set the message box to `{{strategy.order.alert_message}}` (for strategies using strategy alerts) or leave default if using indicator `alert()` calls.
5. In your server handler, validate the incoming payload against the schema and authenticate using an authorization header or URL token.
