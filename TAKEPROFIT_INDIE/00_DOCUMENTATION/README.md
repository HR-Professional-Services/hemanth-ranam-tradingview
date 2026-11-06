# HR Trading Indie v5 Indicator Suite for TakeProfit & Exness

Comprehensive collection of institutional technical indicators engineered in native **Indie® v5** for the **TakeProfit** charting platform, calibrated for **Exness** CFD instruments.

---

## 1. Indicator Catalog

| Folder / Script | Indicator Name | Strategy Class | Primary Signals |
| :--- | :--- | :--- | :--- |
| `01_EMA_INDICATORS/HR_9_EMA_BUY_SELL.indie` | **HR 9 EMA Buy/Sell Pro** | Fast Execution / Scalping | Crossovers, Pullbacks, Rejections |
| `01_EMA_INDICATORS/HR_9_21_200_EMA_PULLBACK.indie` | **HR EMA Pullback Pro** | Trend Continuation | 9-21 Zone Pullbacks + 1H 200 EMA Filter |
| `02_LIQUIDITY/HR_LIQUIDITY_SWEEP.indie` | **HR Liquidity Sweep Pro** | SMC / Liquidity Reversals | BSL & SSL false breakout sweeps |
| `03_MARKET_STRUCTURE/HR_MARKET_STRUCTURE_BOS_CHOCH.indie` | **HR Market Structure BOS/CHOCH** | SMC Trend Breaks | Confirmed BOS with RSI(14) momentum gate |
| `04_VOLATILITY/HR_VOLATILITY_EXPANSION_BREAKOUT.indie` | **HR Volatility Breakout Pro** | Volatility Expansion | Squeeze box breakouts with 1H trend alignment |

---

## 2. Key Technical Invariants

* **Language Version**: Native `# indie:lang_version = 5`.
* **Zero Repainting**: All signal triggers, filters, and pivot calculations evaluate strictly on completed closed bars (`index [1]`).
* **State Management**: Uses `MutSeriesF.new(init=...)` to manage state transitions, suppressing duplicate buy/sell tags.
* **Exness Compatibility**: Works dynamically on `XAUUSD`, `XAUUSDm`, `XAGUSD`, `XAGUSDm`, `US500`, `US500m`, `USTEC`, and `USTECm`. Does not hardcode symbol names or assume fixed pip multipliers.
* **Multi-Timeframe Integration**: Uses native `@sec_context` and `calc_on()` to incorporate higher-timeframe (1H) 200 EMA trend filtering.

---

## 3. Installation Guide

1. Open **TakeProfit** ([takeprofit.com](https://takeprofit.com)).
2. Open the **Indicator Code Editor (IDE)** widget.
3. Click **New Script** and select **Indicator**.
4. Copy and paste the contents of any `.indie` file from this repository.
5. Click **Save** and **Add to Chart**.
