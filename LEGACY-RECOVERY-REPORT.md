# Legacy TradingView Indicator Recovery Report

---

## Summary

```
Original Indicator:  Hemanth Ranam Multi-Strategy Trading Engine
Description:         9/21/200 EMA + Session Filter + Market Structure (pivot-based)
                     + Breakout/Retest + VWAP Reversion + Momentum Squeeze
Recovery Status:     RECOVERED — EXACT SOURCE FOUND
```

---

## Primary Recovered File

| Field | Value |
| :--- | :--- |
| **Recovery Status** | ✅ RECOVERED — EXACT SOURCE |
| **Source Location** | `recovered/ORIGINAL_HemanthRanamTradingSystem_RECOVERED.pine` |
| **Original Repository** | `HR-Professional-Services/hemanth-ranam-tradingview` |
| **Original Path** | `src/HemanthRanamTradingSystem.pine` |
| **Original Commit** | `f391583` — "feat: initialize Hemanth Ranam multi-strategy Pine Script v5 trading engine suite" |
| **Original Branch** | `main` |
| **Deleted By Commit** | `a3afe4b` — "feat: upgrade trading engine to pine v6 and add five backtestable strategies" |
| **Pine Version** | **v5** |
| **File Size** | 12 KB / 243 lines |
| **SHA256** | `f58b7b7c2f28d9f1dfe5124b19f9307881dd4a7b478619222ee10926967ee5ea` |
| **Exact Source** | YES — extracted verbatim via `git show f391583:src/HemanthRanamTradingSystem.pine` |
| **Modified** | NO |

---

## Component Audit

```
9 EMA:         FOUND
               Line 45: ema9 = ta.ema(close, fast_len)   default = 9
               Line 60: plot(ema9, "EMA 9 (Fast)", color=#60a5fa)

21 EMA:        FOUND
               Line 46: ema21 = ta.ema(close, mid_len)   default = 21
               Line 61: plot(ema21, "EMA 21 (Mid)", color=#2563eb)

200 EMA:       FOUND
               Line 47: ema200 = ta.ema(close, slow_len)  default = 200
               Line 62: plot(ema200, "EMA 200 (Trend Baseline)", color=#f59e0b)

Sessions:      FOUND — PARTIAL
               Single configurable session via input.session("0700-1700:23456")
               Session filter is OFF by default
               Three-session engine (London/NY/Tokyo) NOT present in original
               See CANDIDATE 3 for three-session evolved version

SMC:           NOT FOUND AS EXPLICIT LABELS
               Market structure logic IS present (pivot-based HH/HL/LH/LL via ta.pivothigh/pivotlow)
               No BOS labels, no CHoCH labels, no Order Block boxes, no FVG zones
               No "Smart Money Concepts" terminology in code
               The pivot break logic (struct_buy/struct_sell) is the structural equivalent

BOS:           NOT FOUND AS LABEL — EQUIVALENT LOGIC FOUND
               struct_buy  = ta.crossover(close, last_sh) and (close > ema200) and in_session
               struct_sell = ta.crossunder(close, last_sl) and (close < ema200) and in_session

CHoCH:         NOT FOUND

Order Blocks:  NOT FOUND

FVG:           NOT FOUND

Liquidity:     NOT FOUND

Buy Signals:   FOUND
               label.new(bar_index, low - (atr*0.5), "BUY\n" + strat_mode, ...)
               Colour: #2563eb (blue), style: label_up

Sell Signals:  FOUND
               label.new(bar_index, high + (atr*0.5), "SELL\n" + strat_mode, ...)
               Colour: #dc2626 (red), style: label_down

Alerts:        FOUND
               alert() with JSON payload on alert.freq_once_per_bar_close
               Fields: brand, system, strategy, symbol, timeframe, signal, entry,
                       stop_loss, take_profit_1, timestamp

Dashboard:     FOUND
               6-row 2-column HUD table
               Shows: Active Strategy / 1H Trend / EMA Structure / ATR / Status

HTF Filter:    FOUND
               1H Higher Timeframe via request.security(... barmerge.lookahead_off)
               Uses htf_timeframe = input.timeframe("60", ...)

Repainting:    NON-REPAINTING
               - HTF: lookahead_off confirmed
               - Pivots: right=2 bars delay — no future data used
               - All EMAs: standard close-based calculation
```

---

## Confidence

```
Exact Source Confidence: EXACT
Reason: File extracted verbatim from git object store.
        Git commit hash f391583 is immutable.
        SHA256 confirmed: f58b7b7c...
```

---

## Recovery Method

```
Method:  git show <commit>:<path>
Command: git show f391583:src/HemanthRanamTradingSystem.pine > recovered/ORIGINAL_...pine
```

The file was deleted in commit `a3afe4b` during the Pine v5 → v6 upgrade. The git object store preserves all historical content even after deletion.

---

## Relationship to Current Five Strategies

```
The original indicator is the DIRECT ANCESTOR of the current strategy suite.

The original was:
  - A single indicator() file (not a strategy())
  - Pine v5
  - 5 selectable modes via dropdown input

The current suite is:
  - Five separate strategy() files
  - Pine v6
  - Each strategy extended with score engines, better filters,
    process_orders_on_close, and improved commission declarations

NO LOGIC WAS LOST in the upgrade.
All 5 original modes are preserved and extended in the current suite.
```

---

## Additional Candidates Found

| File | Type | Confidence | Notes |
| :--- | :--- | :--- | :--- |
| `SCRATCH_EMA_921_Pullback_Strategy.pine` | v5 strategy | POSSIBLE | Simple 9/21/200 pullback strategy. Has `lookahead_on` bug. Earlier prototype. |
| `SCRATCH_ema_921_200_scalper_indicator.pine` | v6 indicator (32K) | VERY LIKELY | Evolved PRO indicator with 3-session engine, market structure, signal scoring. |
| `SCRATCH_ema_921_200_scalper_strategy.pine` | v6 strategy (19K) | VERY LIKELY | Strategy companion to the 32K indicator above. |

See [`RECOVERY-CANDIDATES.md`](../RECOVERY-CANDIDATES.md) for full candidate ranking and SHA256 hashes.

---

## Modernisation

```
Status:  NOT STARTED
```

The original source has been preserved unmodified in `recovered/`. No modernisation has been applied to the recovery copy.

A separate legacy copy has been placed in `src/legacy/` for future modernisation reference.

---

## TradingView Compilation

```
TradingView compilation: NOT EXECUTED
Static checks performed:
  - Pine version: v5 ✅
  - indicator() declaration: ✅
  - No syntax-level errors visible from static inspection ✅
  - request.security() lookahead_off: ✅
  - alert() on bar close: ✅
  - Inputs all use valid v5 functions: ✅
```

---

## Git Record

```
Recovery commit: pending (files staged — see below)
Files added:
  recovered/ORIGINAL_HemanthRanamTradingSystem_RECOVERED.pine
  recovered/SCRATCH_EMA_921_Pullback_Strategy.pine
  recovered/SCRATCH_ema_921_200_scalper_indicator.pine
  recovered/SCRATCH_ema_921_200_scalper_strategy.pine
  src/legacy/HR_9_21_EMA_Sessions_SMC_LEGACY.pine
  RECOVERY-CANDIDATES.md
  LEGACY-RECOVERY-REPORT.md
  docs/LEGACY-INDICATOR-ARCHITECTURE.md
```
