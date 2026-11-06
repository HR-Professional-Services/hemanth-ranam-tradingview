# HR Bloomberg Quant Terminal — Python Desktop Companion

## Overview
This is the official desktop companion terminal for the **HR Unified Master OS** suite. It connects directly with exported candle files (M5) or live bridge feeds to calculate institutional quantitative metrics, ICT/SMC dealing ranges, multi-timeframe trend alignment, and real-time market ribbons.

## Installation & Running

```bash
cd python
pip install -r requirements.txt
python app.py
```

## Data Input Format
Place market data CSVs in `python/data/`:
- `XAUUSD_M5.csv`
- `XAGUSD_M5.csv`
- `US500_M5.csv`
- `USTEC_M5.csv`
- `DXY_M5.csv`

Expected columns:
```csv
time,open,high,low,close,volume
2026-11-05 10:00,2720.50,2723.10,2719.80,2722.40,1450
```

## Last Candle Snapshots
Whenever candle data is processed, the latest closed bar is automatically recorded into:
`python/data/last_candles/{SYMBOL}_last_candle.json`
