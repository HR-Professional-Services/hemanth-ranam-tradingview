# Hemanth Ranam — TradingView Strategy Suite (Pine Script v6)

Professional, modular, and fully backtestable TradingView Strategy Suite engineered under Pine Script v6. Contains five independent trading strategies equipped with multi-factor Setup Quality scoring, dynamic ATR risk management, real-time on-chart HUD telemetry, and structured webhook alert emission.

---

## 🏛️ The Five Strategy Frameworks

| Strategy | Primary Market Environment | Core Method | Risk Model | Pine File |
| :--- | :--- | :--- | :--- | :--- |
| **EMA Pullback Pro** | Strong Trending | 9/21/200 EMA + 1H HTF Filter | Dynamic ATR SL / TP | [`HR_EMA_Pullback_Pro.pine`](src/strategies/HR_EMA_Pullback_Pro.pine) |
| **Breakout Retest Pro**| Volatility Expansion | 20-Period Range Break + Retest Hold | Dynamic ATR SL / TP | [`HR_Breakout_Retest_Pro.pine`](src/strategies/HR_Breakout_Retest_Pro.pine) |
| **Market Structure Pro**| Structural Swings | Fractal Pivots (HH/HL) + BOS | Dynamic ATR SL / TP | [`HR_Market_Structure_Pro.pine`](src/strategies/HR_Market_Structure_Pro.pine) |
| **VWAP Reversion Pro** | Statistical Reversals | 2.0 StDev + Trend Protection Guard | Mean Target (VWAP) | [`HR_VWAP_Mean_Reversion_Pro.pine`](src/strategies/HR_VWAP_Mean_Reversion_Pro.pine) |
| **Momentum Squeeze Pro**| Volatility Compression| Bollinger inside Keltner Release | Dynamic ATR SL / TP | [`HR_Momentum_Volatility_Pro.pine`](src/strategies/HR_Momentum_Volatility_Pro.pine) |

---

## 📁 Repository Directory
```
hemanth-ranam-tradingview/
├── AUDIT.md
├── CHANGELOG.md
├── README.md
│
├── src/
│   └── strategies/
│       ├── HR_EMA_Pullback_Pro.pine
│       ├── HR_Breakout_Retest_Pro.pine
│       ├── HR_Market_Structure_Pro.pine
│       ├── HR_VWAP_Mean_Reversion_Pro.pine
│       └── HR_Momentum_Volatility_Pro.pine
│
├── docs/
│   ├── GETTING-STARTED.md
│   ├── STRATEGY-COMPARISON.md
│   ├── ALERTS.md
│   ├── BACKTESTING.md
│   ├── RISK-MANAGEMENT.md
│   ├── TROUBLESHOOTING.md
│   ├── EMA-PULLBACK.md
│   ├── BREAKOUT-RETEST.md
│   ├── MARKET-STRUCTURE.md
│   ├── VWAP-MEAN-REVERSION.md
│   └── MOMENTUM-VOLATILITY.md
│
└── tests/
    └── test_strategies_v6.py
```

---

## 📡 Webhook Alert JSON Payload Schema
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

---

## 🧪 Testing & Static Validation
```bash
python3 -m unittest discover tests/
```

---

## ⚖️ Disclaimer
*For educational and software development purposes only. Past performance does not guarantee future results. Manage risk responsibly.*

**Author**: Hemanth Ranam  
**Website**: [https://app.hemanth-ranam.workers.dev/](https://app.hemanth-ranam.workers.dev/)
