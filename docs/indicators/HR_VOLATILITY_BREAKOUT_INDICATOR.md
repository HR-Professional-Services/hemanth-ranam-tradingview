# HR Volatility Expansion Breakout Pro — Commercial Indicator Manual

**Product ID**: `HR-PRD-03`  
**Version**: 1.0 (Pine Script v6)  
**File**: [`src/indicators/HR_Volatility_Breakout_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Volatility_Breakout_Indicator.pine)  
**Strategy Counterpart**: [`src/strategies/HR_Volatility_Breakout_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Volatility_Breakout_Strategy.pine)  
**Authoritative MT5 EA**: `03_VOLATILITY_BREAKOUT/VOLATILITY_EXPANSION_BREAKOUT_EA.mq5`  
**Last Updated**: 2026-10-22

---

## 1. Overview & Strategy Concept

The **HR Volatility Expansion Breakout Pro** system captures aggressive explosive momentum moves emerging from low-volatility consolidation ranges (squeezes). By identifying periods where price compression reaches extreme thresholds relative to the Average True Range (ATR), the system positions for volatility expansion on confirmed directional bar breakouts.

### Core Architecture
- **Consolidation Box**: Evaluates the highest high and lowest low across a 20-bar window (`compressionBars = 20`).
- **Squeeze Threshold**: Qualifies a squeeze when `Box Height <= ATR × 1.8` (`maxCompressionAtr = 1.8`, matching MT5 EA `InpMaxCompressionATR`).
- **Breakout Trigger**: Enforces that the trigger candle closes outside the box boundaries (`Close > boxHigh` for Bullish, `Close < boxLow` for Bearish).
- **Volume Expansion**: Optional filter requiring volume >= 1.25x the 20-period volume moving average.
- **Protective Stops**: Dynamically anchors stop-loss to the box midpoint or candle extreme with configurable ATR buffer.

---

## 2. Webhook Alert Payload

```json
{
  "brand": "Hemanth Ranam",
  "system": "TradingView",
  "strategy": "Volatility Expansion Breakout Pro",
  "signal": "BUY",
  "symbol": "USTEC",
  "timeframe": "15",
  "entry": 20450.25,
  "stop_loss": 20380.00,
  "take_profit_1": 20625.85,
  "score": "88",
  "grade": "A",
  "timestamp": 1729612800000
}
```
