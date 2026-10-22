# HR Market Structure Momentum Pro — Commercial Indicator Manual

**Product ID**: `HR-PRD-04`  
**Version**: 1.0 (Pine Script v6)  
**File**: [`src/indicators/HR_Market_Structure_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Market_Structure_Indicator.pine)  
**Strategy Counterpart**: [`src/strategies/HR_Market_Structure_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Market_Structure_Strategy.pine)  
**Authoritative MT5 EA**: `04_STRUCTURE_MOMENTUM/MARKET_STRUCTURE_MOMENTUM_EA.mq5`  
**Last Updated**: 2026-10-22

---

## 1. Overview & Strategy Concept

The **HR Market Structure Momentum Pro** system identifies institutional trend transitions and continuations via algorithmic Break of Structure (BOS) detection. By mapping confirmed fractal swing highs and lows, the system fires signals when price pierces and closes beyond a validated structural pivot with confirmed RSI momentum acceleration.

### Core Architecture
- **Fractal Pivots**: Calculated using `pivotStrength = 3` (3 bars left, 3 bars right), matching MT5 EA `InpPivotStrength=3`.
- **Pivot Confirmation Delay**: Acknowledges that swing fractals require 3 right-side bars before confirmation. Signals fire strictly on the subsequent break bar close.
- **Momentum Filter**: Requires RSI(14) >= 53.0 for Bullish BOS and <= 47.0 for Bearish BOS, filtering out false structural breaks with decaying momentum.
- **Macro Alignment**: Requires 1H Close > 200 EMA for Longs, < 200 EMA for Shorts.

---

## 2. Webhook Alert Payload

```json
{
  "brand": "Hemanth Ranam",
  "system": "TradingView",
  "strategy": "Market Structure Momentum Pro",
  "signal": "BUY",
  "symbol": "XAUUSD",
  "timeframe": "15",
  "entry": 2748.20,
  "stop_loss": 2736.50,
  "take_profit_1": 2776.28,
  "score": "84",
  "grade": "A",
  "timestamp": 1729612800000
}
```
