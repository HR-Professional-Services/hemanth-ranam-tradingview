# HR TradingView & MT5 Parity Matrix

**Domain**: Cross-Platform Quantitative Engineering  
**Primary Repository**: `HR-Professional-Services/hemanth-ranam-tradingview`  
**Authoritative Reference Repository**: `HR-Professional-Services/HemanthRanam-MT5-EAs` (Read-Only)  
**Last Updated**: 2026-10-22  
**Status Taxonomies**: `MATCHED` | `PARTIAL` | `DIFFERENT` | `UNVERIFIED` | `NOT-APPLICABLE`

---

## 1. Cross-Platform Architecture Comparison

| Dimension | TradingView Implementation (`Pine Script v6`) | MetaTrader 5 Reference (`MQL5`) | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Execution Model** | Bar Close (`barstate.isconfirmed`, `process_orders_on_close = true`) | Real-time tick evaluation on bar open/tick events | `MATCHED` | Both execute on completed bar signals to prevent repainting. |
| **Multi-Timeframe Handling** | `request.security(..., [1], lookahead=barmerge.lookahead_off)` | `iTime()`, `CopyBuffer()`, `iClose()` with bar index `1` | `MATCHED` | Zero forward-looking bias on both platforms. |
| **Account Risk Cap** | `default_qty_type = percent_of_equity`, value = 1.0 | Fixed 1.0% equity risk per trade via dynamic lot sizing function | `PARTIAL` | Pine uses percent of equity for quantity; MT5 calculates exact stop monetary loss. |
| **Slippage & Costs** | Explicit 0.02% commission + 2 ticks slippage in `strategy()` | Real broker spread & commission applied dynamically | `MATCHED` | Modeled explicitly in both environments. |
| **Alert Infrastructure** | Standardized JSON payload via `alert()` | Print logs, Push notifications, and DLL webhook sockets | `PARTIAL` | TradingView provides native webhook emission; MT5 requires WebRequest or DLL. |

---

## 2. Product-by-Product Parity Breakdown

### HR-PRD-01: EMA Trend Pullback Pro
- **TradingView**: `src/indicators/HR_EMA_Pullback_Indicator.pine` / `src/strategies/HR_EMA_Pullback_Pro.pine`
- **MT5 Reference**: `02_TREND_PULLBACK/TREND_PULLBACK_CONTINUATION_EA.mq5`

| Feature | TradingView Logic | MT5 Logic | Parity Status | Divergence / Implementation Details |
| :--- | :--- | :--- | :--- | :--- |
| **Trend Alignment** | EMA 9 > 21 > 200 | EMA 9 > 21 > 200 | `MATCHED` | Exact identical exponential moving average calculation. |
| **HTF Filter** | 1H 200 EMA (`[1]`, `lookahead_off`) | 1H 200 EMA (`CopyBuffer(hEMA_HTF, 0, 1, 1, buf)`) | `MATCHED` | Both sample the closed 1H bar. |
| **Pullback Zone** | Low touches 21 EMA; closes above 50 EMA | Low touches 21 EMA; closes above 50 EMA | `MATCHED` | Structural pullback logic matched. |
| **Stop Loss** | Fixed 1.5 × ATR(14) | Swing low or 1.5 × ATR(14) | `PARTIAL` | MT5 allows structural swing stop with ATR fallback; TV uses pure ATR. |
| **Target** | Single 1.5R target (`strategy.exit`) | Split targets: TP1 (1.0R, 50%), TP2 (2.0R, 50%) + trailing stop | `DIFFERENT` | TV uses single target for deterministic backtesting; MT5 supports partial scaling. |

---

### HR-PRD-02: Liquidity Sweep Reversal Pro
- **TradingView**: `src/indicators/HR_Liquidity_Sweep_Indicator.pine` / `src/strategies/HR_Liquidity_Sweep_Strategy.pine`
- **MT5 Reference**: `01_LIQUIDITY_SWEEP/LIQUIDITY_SWEEP_REVERSAL_EA.mq5`

| Feature | TradingView Logic | MT5 Logic | Parity Status | Divergence / Implementation Details |
| :--- | :--- | :--- | :--- | :--- |
| **Swing Lookback** | 24-bar rolling high/low (`highest(high[1], 24)`) | 24-bar rolling swing or session High/Low | `PARTIAL` | MT5 supports London/NY session high/low modes; TV implements 24-bar rolling swing. |
| **Displacement** | Minimum 0.20 × ATR penetration | Fixed pip or 0.20 × ATR displacement | `MATCHED` | Both require minimum clearance beyond level to trigger liquidity. |
| **Rejection Candle** | Rejection wick >= 40% of candle; close back inside | Rejection wick >= 40% of candle; close back inside | `MATCHED` | Candle anatomy filter identical. |
| **Stop Loss** | Placed beyond sweep wick + 0.2 ATR | Placed beyond sweep wick + broker spread buffer | `MATCHED` | Structural stop placement matched. |
| **Target** | Fixed 2.5R target | 2.5R target with breakeven at 1.0R | `PARTIAL` | Breakeven move is an optional setting in MT5 EA. |

---

### HR-PRD-03: Volatility Expansion Breakout Pro
- **TradingView**: `src/indicators/HR_Volatility_Breakout_Indicator.pine` / `src/strategies/HR_Volatility_Breakout_Strategy.pine`
- **MT5 Reference**: `03_VOLATILITY_BREAKOUT/VOLATILITY_EXPANSION_BREAKOUT_EA.mq5`

| Feature | TradingView Logic | MT5 Logic | Parity Status | Divergence / Implementation Details |
| :--- | :--- | :--- | :--- | :--- |
| **Consolidation Box** | 20-bar highest high & lowest low | 20-bar consolidation channel | `MATCHED` | Channel calculation identical. |
| **Squeeze Condition** | Box range <= 1.8 × ATR(14) | Box range <= 1.8 × ATR(14) | `MATCHED` | Volatility compression criteria identical. |
| **Volume Filter** | Volume > 1.2 × SMA(Volume, 20) | Tick Volume > 1.2 × SMA(Tick Volume, 20) | `PARTIAL` | TV uses exchange volume or tick proxy; MT5 uses broker tick volume. |
| **Stop Loss** | Consolidation box midpoint | Box midpoint or opposite edge | `MATCHED` | Box midpoint stop implemented. |
| **Target** | Fixed 2.5R target | 2.5R target with ATR trailing stop | `PARTIAL` | TV uses fixed target; MT5 supports trailing expansion. |

---

### HR-PRD-04: Market Structure Momentum Pro
- **TradingView**: `src/indicators/HR_Market_Structure_Indicator.pine` / `src/strategies/HR_Market_Structure_Strategy.pine`
- **MT5 Reference**: `04_STRUCTURE_MOMENTUM/MARKET_STRUCTURE_MOMENTUM_EA.mq5`

| Feature | TradingView Logic | MT5 Logic | Parity Status | Divergence / Implementation Details |
| :--- | :--- | :--- | :--- | :--- |
| **Fractal Swings** | 3-bar left, 3-bar right (`pivothigh/low`) | 3-bar fractal definition | `MATCHED` | Exact 3-bar confirmation delay on both platforms. |
| **BOS Confirmation** | Closed bar beyond prior pivot | Closed bar beyond prior pivot | `MATCHED` | No intrabar execution; strictly confirmed closes. |
| **Momentum Filter** | RSI(14) > 53.0 (Long), < 47.0 (Short) | RSI(14) > 53.0 (Long), < 47.0 (Short) | `MATCHED` | Identical momentum threshold checks. |
| **Macro Trend** | Price relative to 200 EMA | Price relative to 200 EMA | `MATCHED` | Baseline trend filter matched. |
| **Stop Loss** | Opposing structural pivot + 0.3 ATR | Opposing structural pivot + spread buffer | `MATCHED` | Structural pivot stop matched. |
| **Target** | Fixed 2.4R target | 2.4R target | `MATCHED` | Reward-to-risk ratio matched. |

---

## 3. Discrepancy Governance & Maintenance

- **MT5 Repository Policy**: The authoritative MT5 repository (`HemanthRanam-MT5-EAs`) is strictly **read-only** during TradingView development cycles. Any MT5 modifications must be performed in an authorized, dedicated MT5 task.
- **Intentional Divergences**: Strategy Tester simplicity requires deterministic single-target exits (`take_profit_1`) to ensure reliable historical reporting. Partial exits and complex trailing logic can be enabled as advanced user parameters once native compilation is signed off.
