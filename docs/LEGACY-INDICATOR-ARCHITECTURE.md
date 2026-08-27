# Legacy Indicator Architecture — Hemanth Ranam Trading System

**Source File**: `ORIGINAL_HemanthRanamTradingSystem_RECOVERED.pine`  
**Original Git Path**: `src/HemanthRanamTradingSystem.pine`  
**Pine Version**: v5  
**Commit Added**: `f391583`  
**Commit Deleted**: `a3afe4b`  
**SHA256**: `f58b7b7c2f28d9f1dfe5124b19f9307881dd4a7b478619222ee10926967ee5ea`  

> This document describes the architecture **actually found in the recovered source**.  
> Nothing has been added or assumed. All descriptions map to specific line numbers.

---

## Indicator Declaration (Line 2)

```pine
indicator("Hemanth Ranam — Multi-Strategy Trading Engine", 
          shorttitle="HR Trading Engine", 
          overlay=true, 
          max_labels_count=500, 
          max_lines_count=500)
```

**Type**: `indicator()` — overlay indicator (NOT a `strategy()`).  
**Labels limit**: 500  
**Lines limit**: 500

---

## Strategy Modes (Lines 15–16)

The indicator is a **single-file multi-strategy engine** with 5 selectable modes via one input dropdown:

| Mode | Description |
| :--- | :--- |
| `EMA Pullback` | Default. 9/21/200 EMA alignment + pullback zone + confirmation |
| `Breakout + Retest` | 20-period range breakout + retest via EMA 21 |
| `Market Structure` | Pivot high/low break (HH/HL/LH/LL) + EMA 200 filter |
| `VWAP Mean Reversion` | 2σ VWAP bands + RSI |
| `Momentum Expansion` | Bollinger/Keltner squeeze compression + release |

---

## EMA Configuration (Lines 22–28)

| Variable | Input | Default | Description |
| :--- | :--- | :---: | :--- |
| `fast_len` | `input.int` | 9 | Fast EMA length |
| `mid_len` | `input.int` | 21 | Pullback EMA length |
| `slow_len` | `input.int` | 200 | Trend baseline EMA |
| `htf_trend_filter` | `input.bool` | `true` | Enable 1H HTF filter |
| `htf_timeframe` | `input.timeframe` | `"60"` | HTF resolution |

**Calculations (Lines 45–48)**:
```pine
ema9   = ta.ema(close, fast_len)
ema21  = ta.ema(close, mid_len)
ema200 = ta.ema(close, slow_len)
atr    = ta.atr(atr_len)
```

---

## Sessions (Lines 37–41, 57)

**Single configurable session** (not multi-session):

| Input | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `use_session_filter` | `input.bool` | `false` | OFF by default |
| `session_hours` | `input.session` | `"0700-1700:23456"` | Mon–Fri, UTC 07:00–17:00 |

**Session check (Line 57)**:
```pine
in_session = not use_session_filter or not na(time(timeframe.period, session_hours))
```

Sessions are used as **a gate** — all 5 strategy modes share this single session filter.

---

## Higher Timeframe (HTF) Trend Filter (Lines 50–54)

```pine
htf_close  = request.security(syminfo.tickerid, htf_timeframe, close, 
                               barmerge.gaps_off, barmerge.lookahead_off)
htf_ema200 = request.security(syminfo.tickerid, htf_timeframe, ta.ema(close, slow_len), 
                               barmerge.gaps_off, barmerge.lookahead_off)
htf_bullish = not htf_trend_filter or (htf_close > htf_ema200)
htf_bearish = not htf_trend_filter or (htf_close < htf_ema200)
```

**Uses `lookahead_off`** — HTF filter is non-repainting at the bar level.

---

## Risk Management Inputs (Lines 30–35)

| Input | Type | Default | Description |
| :--- | :--- | :---: | :--- |
| `atr_len` | `input.int` | 14 | ATR length |
| `sl_atr_mult` | `input.float` | 1.5 | SL = entry ± (ATR × 1.5) |
| `tp1_rr_mult` | `input.float` | 1.5 | TP1 = entry ± (risk × 1.5) |
| `tp2_rr_mult` | `input.float` | 2.5 | TP2 = entry ± (risk × 2.5) |

---

## SMC-Equivalent Logic

> ⚠️ **Important**: The recovered indicator does **not use the terms BOS, CHoCH, Order Block, FVG, or Liquidity** anywhere in the code.  
> It uses **pivot-based market structure continuation** (Strategy 3) which is logically equivalent to parts of SMC, but is not labelled as SMC.

### Market Structure / Structure Break Logic (Lines 92–105)

```pine
swing_high = ta.pivothigh(high, 5, 2)
swing_low  = ta.pivotlow(low, 5, 2)
var float last_sh = na
var float last_sl = na
if not na(swing_high)
    last_sh := swing_high
if not na(swing_low)
    last_sl := swing_low

struct_buy  = ta.crossover(close, last_sh) and (close > ema200) and in_session
struct_sell = ta.crossunder(close, last_sl) and (close < ema200) and in_session
```

**This is the equivalent of BOS** — price crossing a recent swing high/low in direction of the trend — but the code does not draw or label it as "BOS" or "CHoCH".

**Pivot settings**: `left=5`, `right=2` bars  
**Repainting**: `ta.pivotlow/pivothigh` with `right=2` confirms 2 bars after the pivot forms. No future peeking.

---

## Strategy 1: EMA Pullback (Lines 65–79) — PRIMARY

```pine
ema_bull_align = (ema9 > ema21) and (ema21 > ema200) and (close > ema200)
ema_bear_align = (ema9 < ema21) and (ema21 < ema200) and (close < ema200)

pullback_buy_zone  = (low <= ema9 or low <= ema21) and (close >= ema21)
pullback_sell_zone = (high >= ema9 or high >= ema21) and (close <= ema21)

bull_trigger = close > open and close > high[1]
bear_trigger = close < open and close < low[1]

sig_ema_buy  = ema_bull_align and pullback_buy_zone and bull_trigger and htf_bullish and in_session
sig_ema_sell = ema_bear_align and pullback_sell_zone and bear_trigger and htf_bearish and in_session
```

**BUY requires ALL of**:
1. `ema9 > ema21 > ema200 and close > ema200` — full bull alignment
2. `low <= ema9 or low <= ema21` — price pulled back to value zone
3. `close >= ema21` — closed back above pullback level
4. `close > open` — bullish candle
5. `close > high[1]` — broke previous high
6. HTF 1H close > 1H EMA 200
7. In active session

**SELL**: Mirror conditions.

---

## Visual Elements

### EMA Plots (Lines 60–62)
```pine
plot(ema9,   "EMA 9 (Fast)",           color=color.new(#60a5fa, 20), linewidth=1)
plot(ema21,  "EMA 21 (Mid)",           color=color.new(#2563eb, 0),  linewidth=2)
plot(ema200, "EMA 200 (Trend Baseline)", color=color.new(#f59e0b, 0),  linewidth=2)
```

| EMA | Colour | Linewidth |
| :-- | :--- | :-- |
| 9 (Fast) | `#60a5fa` (light blue, 20% transparent) | 1 |
| 21 (Mid) | `#2563eb` (blue, solid) | 2 |
| 200 (Trend) | `#f59e0b` (amber, solid) | 2 |

### Buy/Sell Labels (Lines 191–195)
```pine
label.new(bar_index, low - (atr * 0.5),  "BUY\n"  + strat_mode, color=#2563eb, 
          textcolor=color.white, style=label.style_label_up,   size=size.small)
label.new(bar_index, high + (atr * 0.5), "SELL\n" + strat_mode, color=#dc2626, 
          textcolor=color.white, style=label.style_label_down, size=size.small)
```

- BUY label: Blue `#2563eb`, upward arrow style, placed `ATR × 0.5` below bar low
- SELL label: Red `#dc2626`, downward arrow style, placed `ATR × 0.5` above bar high
- Label text includes active strategy mode name

### HUD Dashboard (Lines 198–231)
6-row table, 2 columns, top-right (configurable):

| Row | Left Cell | Right Cell |
| :-: | :--- | :--- |
| 0 | "HEMANTH RANAM" (header) | "TRADING SYSTEM" |
| 1 | "Strategy" | Active strategy mode |
| 2 | "1H Trend" | BULLISH / BEARISH |
| 3 | "EMA Structure" | ALIGNED UP / ALIGNED DOWN / NEUTRAL |
| 4 | "ATR (14)" | ATR value |
| 5 | "Status" | LONG / SHORT / SEARCHING |

Dashboard background: `#0f172a` (dark navy, 15% transparency)  
Border: `#334155` (slate, 30% transparency)

---

## Alert Logic (Lines 233–243)

**Trigger**: `alert.freq_once_per_bar_close` — alerts fire on bar close only (non-intrabar).

**Alert payload format** (JSON string):
```json
{
  "brand": "Hemanth Ranam",
  "system": "TradingEngine",
  "strategy": "<active_strategy_mode>",
  "symbol": "<syminfo.ticker>",
  "timeframe": "<timeframe.period>",
  "signal": "BUY",
  "entry": <close>,
  "stop_loss": <active_sl>,
  "take_profit_1": <active_tp1>,
  "timestamp": <time>
}
```

**Two `alert()` calls**: one for BUY, one for SELL.  
No `alertcondition()` is used — uses the direct `alert()` function.

---

## Duplicate Signal Prevention (Lines 158–166)

```pine
var int last_signal_dir = 0 // 1: Buy, -1: Sell
buy_trigger  = final_buy and (last_signal_dir != 1)
sell_trigger = final_sell and (last_signal_dir != -1)
```

Prevents consecutive same-direction signals.

---

## Repainting Audit

| Component | Method | Repainting? |
| :--- | :--- | :---: |
| EMA 9/21/200 | `ta.ema(close, ...)` | ❌ Non-repainting (recalculate on each close) |
| HTF Close | `request.security(..., lookahead_off)` | ❌ Non-repainting |
| HTF EMA200 | `request.security(..., lookahead_off)` | ❌ Non-repainting |
| Pivot High | `ta.pivothigh(high, 5, 2)` | ⚠️ 2-bar delay — confirms 2 bars after pivot. Historical pivots do NOT repaint. |
| Pivot Low | `ta.pivotlow(low, 5, 2)` | ⚠️ Same 2-bar delay. |
| `last_sh` / `last_sl` | `var float` persisted | ❌ Non-repainting |
| Session filter | `time(timeframe.period, session_hours)` | ❌ Non-repainting |

**Overall verdict**: **NON-REPAINTING** (with the understood 2-bar pivot confirmation delay on the Market Structure strategy mode).

---

## Comparison with Current Five Strategies

| Feature | Original Monolith | Current Suite |
| :--- | :--- | :--- |
| File structure | Single `indicator()` file | 5 separate `strategy()` files |
| Pine version | v5 | v6 |
| EMA Pullback | ✅ (Mode 1) | ✅ `HR_EMA_Pullback_Pro.pine` (extended with score engine) |
| Breakout + Retest | ✅ (Mode 2) | ✅ `HR_Breakout_Retest_Pro.pine` |
| Market Structure | ✅ (Mode 3) | ✅ `HR_Market_Structure_Pro.pine` |
| VWAP Reversion | ✅ (Mode 4) | ✅ `HR_VWAP_Mean_Reversion_Pro.pine` |
| Momentum Squeeze | ✅ (Mode 5) | ✅ `HR_Momentum_Volatility_Pro.pine` |
| HTF Filter | ✅ `lookahead_off` | ✅ `lookahead_off` + `close[1]` shift |
| Sessions | Single configurable session | Session filter per strategy |
| Signal scoring | ❌ | ✅ Score engine in EMA Pullback Pro |
| process_orders_on_close | N/A (indicator) | ✅ |

**Conclusion**: The original monolith was **split into 5 independent strategies** during the upgrade from Pine v5 → v6. All original logic is preserved and extended in the current suite. No logic was lost — the original was the architectural ancestor.
