# HR EMA Pullback Pro — Indicator Documentation

**Version**: 1.0  
**File**: `src/indicators/HR_EMA_Pullback_Indicator.pine`  
**Type**: `indicator()` — overlay, non-backtestable  
**Pine Version**: 6  
**Status**: `NATIVE-TV-COMPILATION-PENDING` — must be verified in TradingView Pine Editor

---

## Overview

HR EMA Pullback Pro identifies high-probability pullback entries within an established EMA trend. The core logic requires:

1. **Full EMA alignment** — EMA 9 > 21 > 200 (bull) or 9 < 21 < 200 (bear)
2. **Higher-timeframe agreement** — HTF close vs HTF EMA 200
3. **Price pullback into the EMA zone** — wick touches between EMA 9 and EMA 21
4. **Candle confirmation** — engulfing, wick rejection, or momentum body
5. **Market regime clear** — not choppy, not overextended
6. **Quality gate** — minimum score and grade threshold

Signals fire **only on confirmed closed bars** and emit once per trend phase via the crossover state machine.

---

## Recommended Instruments

Works across: **Forex majors/minors**, **Gold/Silver (XAUUSD/XAGUSD)**, **Indices (US30, NAS100, SPX)**, **Crypto (BTC, ETH)**, **Commodities**, **Equities**.

---

## Recommended Timeframes

| Timeframe | Notes |
|:---|:---|
| **5M** | Primary scalping timeframe. HTF default (1H) is appropriate. |
| **15M** | Swing scalp. Consider changing HTF to 4H. |
| **1H** | Intraday swing. Change HTF to Daily. |
| **4H / Daily** | Position trading. Change HTF to Weekly. |

> Always adjust the HTF input to be at least 4× your chart timeframe.

---

## Input Reference

### General
| Input | Default | Description |
|:---|:---:|:---|
| Enable BUY Signals | ✓ | Disable to suppress all long signals |
| Enable SELL Signals | ✓ | Disable to suppress all short signals |

### EMA Configuration
| Input | Default | Description |
|:---|:---:|:---|
| Fast EMA Length | 9 | Short-term momentum |
| Mid EMA Length | 21 | Pullback target |
| Trend Baseline EMA | 200 | Long-term trend direction |

### Higher-Timeframe Filter
| Input | Default | Description |
|:---|:---:|:---|
| Enable HTF Filter | ✓ | Requires HTF agreement. Disable for counter-trend modes. |
| Higher Timeframe | 60 | 60 = 1-hour. Adjust per chart timeframe. |
| HTF EMA Period | 200 | EMA applied on higher timeframe |

### Pullback & Candle Confirmation
| Input | Default | Description |
|:---|:---:|:---|
| Pullback Target Zone | EMA 9-21 Zone | Zone price must touch for pullback |
| Require Close Beyond EMA 9 | ✓ | Candle must close above/below EMA 9 |
| Require Engulfing Candle | ✓ | Engulfing body confirmation |
| Require Rejection Wick | ✗ | Optional wick rejection filter |
| Min Rejection Wick | 35% | Minimum wick size as % of bar range |
| Require Strong Momentum Body | ✗ | Optional body strength filter |
| Min Candle Body | 55% | Minimum body size as % of bar range |

### Market Regime Filters
| Input | Default | Description |
|:---|:---:|:---|
| Enable Chop Filter | ✓ | Blocks signals in sideways/compressed markets |
| Min EMA Gap (× ATR) | 0.06 | EMA 9/21 separation threshold relative to ATR |
| Enable Overextension Filter | ✓ | Blocks late-entry signals far from EMA 9 |
| Max Price Distance to EMA 9 | 2.5× ATR | Maximum allowed price-to-EMA 9 distance |
| EMA Slope Lookback | 3 bars | Bars used for slope calculation |
| Enable Market Structure Filter | ✗ | Optional pivot-based structure gate |
| Market Structure Pivot Lookback | 5 | Pivot detection left/right bars (adds N-bar lag) |

### Signal Quality & Scoring
| Input | Default | Description |
|:---|:---:|:---|
| Minimum Entry Score | 70 | Signals below this score are suppressed |
| Minimum Signal Grade | A and Above | Grade gate: A+, A, B, or All |
| Show Score on Label | ✓ | Display quality score on chart label |
| Show Grade on Label | ✓ | Display grade letter on chart label |

### Risk Reference Levels
| Input | Default | Description |
|:---|:---:|:---|
| Show SL/TP Reference Lines | ✓ | Toggle ATR-based level lines |
| ATR Period | 14 | ATR calculation length |
| Stop-Loss ATR Multiplier | 1.5 | SL = entry ± (ATR × 1.5) |
| Take-Profit 1 R:R Ratio | 1.5 | TP1 = entry ± (risk × 1.5) |
| Take-Profit 2 R:R Ratio | 2.5 | TP2 = entry ± (risk × 2.5) |

> **Important**: SL/TP lines are reference guides only. They are not automatically placed as broker orders.

### Session Filter (Optional)
| Input | Default | Description |
|:---|:---:|:---|
| Enable Session Filter | ✗ | OFF by default. Works on all markets without enabling. |
| Preferred Session Window | London + NY | Filter preset when enabled |
| Custom Session | 0700-1700 UTC | Used with "Off — Use Custom" mode |
| UTC Offset | 0 | Adjust for broker timezone offset |

---

## Signal Quality Score

Each signal is scored 0–100 from six weighted components:

| Component | Max Points | Condition |
|:---|:---:|:---|
| EMA Health Score | 25 | Composite of slope, stacking, gap, and position |
| EMA Structure | 20 | Full stack (9>21>200) vs partial alignment |
| HTF Confirmation | 20 | HTF close vs HTF EMA 200 direction match |
| Candle Pattern | 15 | Engulfing (15) vs other (8) |
| Market Structure | 10 | Pivot confirmation when filter enabled |
| Session Window | 10 | Signal within preferred session hours |

**Grade thresholds**: A+ ≥ 90 | A ≥ 75 | B ≥ 60 | C < 60

---

## Alert Setup (TradingView)

### Step-by-step
1. Load the indicator on a chart
2. Right-click the chart → **Add alert**
3. Under **Condition**, select `HR EMA Pullback Pro`
4. Choose one of four conditions:
   - `HR EMA Pullback — BUY Signal`
   - `HR EMA Pullback — SELL Signal`
   - `HR EMA Pullback — A+ BUY`
   - `HR EMA Pullback — A+ SELL`
5. Set **Trigger**: `Once Per Bar Close` (enforced by the indicator)
6. Set **Alert actions**: notification, email, or webhook

### Dynamic Alert Payload
Alerts fire with a structured message:
```
SYMBOL | TF | DIRECTION | Grade: X | Score: NN | Health: NN | Trend: STATE | HTF: STATE | Session: NAME | Entry: PRICE | SL: PRICE | TP1: PRICE
```

Example:
```
XAUUSD | 5 | BUY | Grade: A+ | Score: 87 | Health: 92 | Trend: STRONG BULL | HTF: BULL | Session: London | Entry: 2415.50 | SL: 2409.20 | TP1: 2424.90
```

For webhook JSON payloads (planned v2.0), see `research/schema/alert-payload.schema.json`.

---

## Dashboard Guide

| Row | Content |
|:---|:---|
| Header | HR EMA PULLBACK PRO v1.0 |
| Signal | Current signal state with grade |
| Trend / HTF | Chart-timeframe trend + higher-timeframe trend |
| Market / Session | Regime state (Trending/Choppy/Extended) + session name |
| EMA Health / Quality | Health score/100 + active quality score/100 |
| **Advanced (optional)** | |
| Risk Levels | Entry, SL, TP1 reference prices from last signal |
| Active Filters | Which filters are currently enabled |
| EMA Values | Current EMA 9, 21, 200 prices |
| ATR & Gap | ATR value, gap ratio, current timeframe |

---

## Non-Repainting Declaration

This indicator is designed to be non-repainting for **historical** signal markers:

| Mechanism | Implementation | Risk |
|:---|:---|:---|
| Bar confirmation | `barstate.isconfirmed` required | None — signals only fire at bar close |
| HTF security | `close[1]`, `ema[1]`, `lookahead_off` | None — previous closed HTF bar only |
| Pivot lag | `msPivotLen`-bar delay (default 5 bars) | Inherent, documented |
| Live bar dashboard | Updates intrabar | Dashboard updates but no signal fires |

**Native TradingView validation status**: `PENDING` — must be verified in TradingView Pine Editor by loading the script and checking the Pine Editor console for errors.

---

## Known Limitations

- Strategies using this indicator's signals cannot be automatically backtested via TradingView Strategy Tester (indicator mode). Use the corresponding `src/strategies/HR_EMA_Pullback_Pro.pine` for Strategy Tester backtesting once complete.
- Volume data may not be available on all forex feeds.
- Session filter uses UTC; broker feeds with non-UTC server time may require UTC offset adjustment.
- On very low-liquidity instruments, ATR-based SL/TP references may be wider than desired.

---

## Version History

| Version | Date | Changes |
|:---|:---:|:---|
| 1.0 | 2026-10-22 | Initial commercial release. Full signal engine, dashboard, alerts, ATR risk references. Derived from recovered/SCRATCH_ema_921_200_scalper_indicator.pine. |
