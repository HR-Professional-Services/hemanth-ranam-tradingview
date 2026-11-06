# Exness CFD Compatibility & Symbol Calibration Reference

## 1. Supported Exness Instrument Families

| Asset Class | Standard Account Symbol | Pro / Raw / Zero Account Symbol | Contract Multiplier | Minimum Pip/Tick Precision |
| :--- | :--- | :--- | :--- | :--- |
| **Gold** | `XAUUSD` | `XAUUSDm` | 100 oz | 0.01 / 0.001 |
| **Silver** | `XAGUSD` | `XAGUSDm` | 5,000 oz | 0.001 |
| **S&P 500 Index** | `US500` | `US500m` | 1 index point | 0.01 / 0.1 |
| **Nasdaq 100 Index** | `USTEC` | `USTECm` | 1 index point | 0.01 / 0.1 |
| **Major FX Pairs** | `EURUSD`, `GBPUSD` | `EURUSDm`, `GBPUSDm` | 100,000 units | 0.00001 (5-digit) |

---

## 2. Dynamic Point & Volatility Handling

TakeProfit Indie indicators run directly against the active chart feed. Unlike MetaTrader 5 scripts that require manual `_Point` or `Digits` handling:
- **Price Streams**: `self.close`, `self.high`, `self.low`, `self.open` return the exact asset price without needing hardcoded multiplier transformations.
- **Normalization with ATR**: All buffer offsets, stop loss guide levels, and squeeze boundaries use `Atr.new(length)` rather than fixed pips.
  - This allows the same script to run on `XAUUSD` ($2,700 price level), `US500` ($5,900 price level), and `EURUSD` ($1.0800 level) without reconfiguring parameters.
- **Floating Spread Independence**: Signals calculate exclusively on closed-candle mid/last feeds, avoiding false triggers from Exness floating spread spikes during rollover.
