# Dataset Inventory & Provenance Report

**Environment**: Local Quantitative Research Lab  
**Reported Data Location**: `C:\MT5_Research_Lab\Historical_Data`  
**Broker Environment**: Exness Demo (`Exness-MT5Trial8`)  
**Data Extraction Mechanism**: MetaTrader 5 Python Client API  
**Inspection Date**: 2026-10-22  
**Validation Status**: Verified & Cataloged

---

## 1. Directory Structure & Layout

The historical data repository is partitioned into broker environments, validation manifests, and instrument subdirectories:

```
C:\MT5_Research_Lab\Historical_Data\
├── manifests/                 # JSON validation manifests with SHA-256 hashes
├── validation/                # Automated audit logs and integrity checks
└── Exness_Demo/               # Verified Exness Demo dataset
    ├── US500/                 # S&P 500 Index CFD
    │   ├── H1/                # 1-Hour Bar Data
    │   ├── M1/                # 1-Minute Base Bar Data
    │   ├── M15/               # 15-Minute Derived Bar Data
    │   ├── M5/                # 5-Minute Derived Bar Data
    │   └── Ticks/             # Sample Tick Stream Data (Recent 24h)
    ├── USTEC/                 # Nasdaq 100 Index CFD
    │   ├── H1/, M1/, M15/, M5/, Ticks/
    ├── XAGUSD/                # Spot Silver / US Dollar
    │   ├── H1/, M1/, M15/, M5/, Ticks/
    └── XAUUSD/                # Spot Gold / US Dollar
        ├── H1/, M1/, M15/, M5/, Ticks/
```

---

## 2. Complete File Inventory

| Symbol | Timeframe | File Name | Size (MB) | Total Rows | Earliest Timestamp (UTC) | Latest Timestamp (UTC) | SHA-256 Checksum (Prefix) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **XAUUSD** | **M15** | `XAUUSD_M15_202312211939_202610220033.csv` | 4.32 MB | 66,868 | 2023-12-21 19:30:00 | 2026-10-22 00:30:00 | `ae343a72a5...` |
| **XAUUSD** | **H1** | `XAUUSD_H1_202312211939_202610220033.csv` | 1.09 MB | 16,733 | 2023-12-21 19:00:00 | 2026-10-22 00:00:00 | `2d517ffb74...` |
| **XAUUSD** | **M1** | `XAUUSD_M1_202312211939_202610220033.csv` | 61.54 MB | 1,000,000 | 2023-12-21 19:39:00 | 2026-10-22 00:33:00 | `c61798dd2c...` |
| **XAUUSD** | **M5** | `XAUUSD_M5_202312211939_202610220033.csv` | 12.84 MB | 200,457 | 2023-12-21 19:35:00 | 2026-10-22 00:30:00 | `879ecca80e...` |
| **XAUUSD** | **Ticks** | `XAUUSD_Ticks_20261021_20261022.csv` | 10.89 MB | 234,689 | 2026-10-21 00:00:00 | 2026-10-22 00:33:00 | `6c1651af9a...` |
| **US500** | **M15** | `US500_M15_202312150800_202610220029.csv` | 4.01 MB | 66,884 | 2023-12-15 08:00:00 | 2026-10-22 00:15:00 | `b99677ee7d...` |
| **US500** | **H1** | `US500_H1_202312150800_202610220029.csv` | 1.02 MB | 16,729 | 2023-12-15 08:00:00 | 2026-10-22 00:00:00 | `fa05cd61e3...` |
| **USTEC** | **M15** | `USTEC_M15_202312190307_202610220038.csv` | 4.31 MB | 66,725 | 2023-12-19 03:00:00 | 2026-10-22 00:30:00 | `d552e67a0a...` |
| **USTEC** | **H1** | `USTEC_H1_202312190307_202610220038.csv` | 1.09 MB | 16,689 | 2023-12-19 03:00:00 | 2026-10-22 00:00:00 | `d637c3da49...` |
| **XAGUSD** | **M15** | `XAGUSD_M15_202312202322_202610220034.csv` | 3.78 MB | 66,915 | 2023-12-20 23:15:00 | 2026-10-22 00:30:00 | `9a05ba3017...` |
| **XAGUSD** | **H1** | `XAGUSD_H1_202312202322_202610220034.csv` | 0.96 MB | 16,746 | 2023-12-20 23:00:00 | 2026-10-22 00:00:00 | `553bcbc0eb...` |

---

## 3. Data Schema & Field Formatting

Every CSV file follows a standardized comma-separated layout:
```csv
datetime_utc,open,high,low,close,tick_volume,avg_spread,real_volume
2023-12-21 19:30:00,2044.171,2045.187,2044.168,2044.718,410,0.0,0
```

- **`datetime_utc`**: ISO-8601 UTC timestamp (`YYYY-MM-DD HH:MM:SS`). Strictly sorted chronologically.
- **`open`, `high`, `low`, `close`**: High-precision floating-point quotes (3 decimal digits for metals, 2 decimal digits for indices).
- **`tick_volume`**: Number of price updates registered during the candle window.
- **`avg_spread`**: Zero in standard historical exports; spread is modeled explicitly in the backtest engine.
- **`real_volume`**: Zero (typical for OTC CFD and Spot FX/Commodity broker feeds).

---

## 4. Instrument Specifications & Point Values

Extracted directly from verified instrument configuration profiles (`C:\MT5_Research_Lab\Instrument_Profiles\`):

| Instrument | Digits | Point Size | Tick Size | Tick Value (USD) | Contract Size | Min Volume | Volume Step | Typical Broker Spread |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **XAUUSD** | 3 | `0.001` | `0.001` | `$0.10` | 100.0 oz | 0.01 lot | 0.01 | 40 points ($0.04) |
| **XAGUSD** | 3 | `0.001` | `0.001` | `$5.00` | 5000.0 oz | 0.01 lot | 0.01 | 35 points ($0.035) |
| **US500** | 2 | `0.010` | `0.010` | `$0.01` | 1.0 index | 0.14 lot | 0.01 | 15 points ($0.15) |
| **USTEC** | 2 | `0.010` | `0.010` | `$0.01` | 1.0 index | 0.05 lot | 0.01 | 20 points ($0.20) |

---

## 5. Feasibility Assessment & Coverage Boundaries

1. **Available Data Horizon**: December 2023 through October 2026 (approx. 34 continuous months).
2. **Missing Pre-2024 Data**: The requested 2021–2023 history was not retained by Exness Demo servers due to the 1,000,000 M1 bar platform extraction limit.
3. **In-Sample Feasibility**: The designated In-Sample period (`2024-01-01` to `2025-06-30`, 18 months) has **100% complete bar coverage** across all four instruments.
4. **Out-of-Sample Feasibility**: The designated Out-of-Sample period (`2025-07-01` to `2026-10-22`, approx. 16 months) has **100% complete bar coverage**.
5. **EURUSD Status**: EURUSD is currently **NOT** present in the local `Exness_Demo` folder. Testing on EURUSD is temporarily blocked until the dataset is downloaded. `XAGUSD` (Spot Silver) was utilized as the fourth liquid instrument.
