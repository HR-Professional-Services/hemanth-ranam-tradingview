# HR Liquidity Sweep Reversal Pro — Commercial Indicator Manual

**Product ID**: `HR-PRD-02`  
**Version**: 1.0 (Pine Script v6)  
**File**: [`src/indicators/HR_Liquidity_Sweep_Indicator.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/indicators/HR_Liquidity_Sweep_Indicator.pine)  
**Strategy Counterpart**: [`src/strategies/HR_Liquidity_Sweep_Strategy.pine`](file:///C:/Users/vaibh/.gemini/antigravity-ide/scratch/hemanth-ranam-tradingview/src/strategies/HR_Liquidity_Sweep_Strategy.pine)  
**Authoritative MT5 EA**: `01_LIQUIDITY_SWEEP/LIQUIDITY_SWEEP_REVERSAL_EA.mq5`  
**Last Updated**: 2026-10-22

---

## 1. Overview & Strategy Concept

**HR Liquidity Sweep Reversal Pro** is a Smart Money Concepts (SMC) quantitative reversal system. It detects institutional liquidity purges occurring when price temporarily pierces prominent swing extremes (stop-run zones) and rapidly reclaims the level with aggressive rejection displacement.

### Key Capabilities
- **Dynamic Liquidity Pool Detection**: Tracks the highest high and lowest low over an adjustable lookback window (default 24 bars, matching MT5 EA `InpSwingLookbackBars`).
- **Displacement Engine**: Rejects weak wicks by verifying that the closing price finishes in the upper 50% (Bullish) or lower 50% (Bearish) of the candle range.
- **Normalized Sweep Depth**: Normalizes penetration distance via ATR to operate consistently across Gold (`XAUUSD`), Silver (`XAGUSD`), S&P 500 (`US500`), Nasdaq (`USTEC`), and Forex majors.
- **Session Focus**: Optional filters for high-liquidity London (07:00–16:00 UTC) and New York (13:00–22:00 UTC) windows.
- **Non-Repainting Guarantee**: All alerts and markers fire strictly on confirmed closed bars (`barstate.isconfirmed`).

---

## 2. Trading Rules

### A. Bullish Liquidity Sweep (BUY)
1. **Sweep**: Candle `low` penetrates below `swingLow` (identifying trapped breakout sellers and triggered long stop-losses).
2. **Reclaim**: Candle `close` finishes back firmly above `swingLow`.
3. **Displacement Ratio**: Reversal displacement ratio `(close - low) / (high - low) >= 0.50` (strong buying rejection).
4. **Depth Bounds**: Penetration depth is within `0.10 × ATR` to `2.50 × ATR` (avoids runaway continuation trends).
5. **Session Filter**: Signal bar falls within allowed session window (if enabled).

### B. Bearish Liquidity Sweep (SELL)
1. **Sweep**: Candle `high` penetrates above `swingHigh` (purging buy-stop liquidity).
2. **Reclaim**: Candle `close` finishes back firmly below `swingHigh`.
3. **Displacement Ratio**: Reversal displacement ratio `(high - close) / (high - low) >= 0.50` (strong selling rejection).
4. **Depth Bounds**: Penetration depth is within `0.10 × ATR` to `2.50 × ATR`.
5. **Session Filter**: Signal bar falls within allowed session window (if enabled).

---

## 3. Configuration & Inputs

| Input Group | Parameter | Default | Description |
| :--- | :--- | :--- | :--- |
| **Liquidity Sweep** | `lookbackBars` | 24 | Rolling bar window for swing high/low tracking. |
| **Liquidity Sweep** | `minSweepAtr` | 0.1 | Minimum penetration beyond level in ATR multiples. |
| **Liquidity Sweep** | `maxSweepAtr` | 2.5 | Maximum permitted penetration before classifying as breakout. |
| **Displacement** | `minDisplacementR` | 0.50 | Minimum candle displacement ratio (0.50 = upper/lower half). |
| **Displacement** | `requireCloseInside` | True | Demands close inside the structural level. |
| **Risk References** | `slBufferAtr` | 0.2 | Protective stop buffer beyond sweep wick. |
| **Risk References** | `rrMultiplier` | 2.5 | Indicative target R:R multiplier (matching MT5 1:2.5). |

---

## 4. Webhook Alert Schema

Alert payloads follow standard JSON syntax:

```json
{
  "brand": "Hemanth Ranam",
  "system": "TradingView",
  "strategy": "Liquidity Sweep Reversal Pro",
  "signal": "BUY",
  "symbol": "XAUUSD",
  "timeframe": "15",
  "entry": 2735.50,
  "stop_loss": 2728.10,
  "take_profit_1": 2754.00,
  "score": "85",
  "grade": "A",
  "timestamp": 1729612800000
}
```
