# Python Market Candle Data Directory

This directory holds the raw closed candle data for the Python companion terminal.

### Expected Files
- `XAUUSD_M5.csv`
- `XAGUSD_M5.csv`
- `US500_M5.csv`
- `USTEC_M5.csv`
- `DXY_M5.csv`

### Format Specification
Standard comma-separated format with datetime and OHLCV:
```csv
time,open,high,low,close,volume
2026-11-05 10:00,2720.50,2723.10,2719.80,2722.40,1450
```

### Last Candle Snapshots
Machine-readable JSON snapshots of the last closed bar for each instrument are saved automatically to `last_candles/`.
