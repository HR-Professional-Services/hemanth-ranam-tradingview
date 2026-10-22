# HR TradingView — Installation & Usage Guide

**Domain**: Trading Systems (HR TradingView / ScaleNova / Hemanth Ranam)  
**Pine Script Version**: v6  
**Target Platform**: TradingView (Desktop App, Web Browser)  
**Last Updated**: 2026-10-22

---

## 1. Prerequisites

Before installing any HR TradingView script:
1. Ensure you have an active [TradingView account](https://www.tradingview.com/) (Essential, Plus, or Premium).
2. Set your chart timezone to **UTC** or **New York** according to your strategy rules.
3. Use high-liquidity symbols with reliable data feeds (e.g., OANDA, FOREX.com, Pepperstone, FXCM for FX/CFDs; TVC for commodities/indices).
4. Verify you are using **Pine Script v6** compatible syntax.

---

## 2. Installing Standalone Indicators

Indicators live in `src/indicators/` and are designed for chart markup, visual trade signals, trend dashboards, and webhook alerts without affecting trading orders.

### Step-by-Step Installation:
1. Open TradingView and navigate to your target chart (e.g., `XAUUSD`, `15m`).
2. Click on the **Pine Editor** tab located on the bottom toolbar.
3. Click **Open** > **New indicator** (or clear the current editor contents).
4. Copy the complete source code from the target indicator file:
   - `src/indicators/HR_EMA_Pullback_Indicator.pine`
   - `src/indicators/HR_Liquidity_Sweep_Indicator.pine`
   - `src/indicators/HR_Volatility_Breakout_Indicator.pine`
   - `src/indicators/HR_Market_Structure_Indicator.pine`
5. Paste the code into the Pine Editor.
6. Click **Save** (e.g. name it `HR - EMA Trend Pullback Indicator`).
7. Click **Add to chart**.
8. Click the gear icon on the indicator label on the top left of the chart to configure settings:
   - Toggle EMA ribbon visibility, cloud coloring, dashboard position, and alert conditions.

---

## 3. Installing & Backtesting Strategies

Strategies live in `src/strategies/` and use the Pine `strategy()` declaration. They execute simulated trades inside TradingView's native **Strategy Tester**.

### Step-by-Step Installation:
1. Open your target chart and timeframe (e.g., `XAUUSD`, `15m`).
2. Open **Pine Editor** on the bottom toolbar.
3. Clear the editor and paste the full code of the desired strategy file:
   - `src/strategies/HR_EMA_Pullback_Pro.pine`
   - `src/strategies/HR_Liquidity_Sweep_Strategy.pine`
   - `src/strategies/HR_Volatility_Breakout_Strategy.pine`
   - `src/strategies/HR_Market_Structure_Strategy.pine`
4. Click **Save** and then **Add to chart**.
5. Switch to the **Strategy Tester** tab at the bottom to inspect backtest performance.

---

## 4. Configuring Strategy Parameters for Backtesting

To ensure realistic, non-overfitted results, configure the strategy properties in the Strategy Settings dialog (`Gear Icon` -> `Properties` tab):

| Setting | Recommended Value | Rationale |
| :--- | :--- | :--- |
| **Initial Capital** | `$10,000` | Standard institutional retail account benchmark |
| **Default Order Size** | `1% of equity` | Controlled capital allocation |
| **Commission** | `0.02%` (Cash per order or %) | Models standard broker fee structures |
| **Slippage** | `2 ticks` | Models real-world latency and execution friction |
| **Order Fill Model** | `On Bar Close` / Next Bar Open | Matches `process_orders_on_close = true` |
| **Recalculate After Order Filled** | `Disabled` | Prevents intraday recalculation repainting |

---

## 5. Setting Up TradingView Webhook Alerts

Both indicators and strategies support TradingView alerts for manual trading or automated order execution engines (e.g., Chartora, Webhook listeners).

1. Right-click the chart and select **Add Alert** (or press `Alt + A`).
2. In the **Condition** dropdown, select the added indicator or strategy.
3. Select the alert condition (e.g., `Any alert() function call` or specific condition).
4. Under **Trigger**, select:
   - **Once Per Bar Close** (Mandatory for closed-bar anti-repainting).
5. Under **Notifications**:
   - Check **Webhook URL** and provide your automated receiver URL.
   - Or check **Send email** / **Push notifications** for manual execution.
6. In the **Message** box, if using dynamic alerts, leave default or input standard JSON:
   - For indicators using `alert()`, the script automatically dispatches a standardized JSON string payload containing ticker, signal, entry, stop loss, and target levels.

---

## 6. Troubleshooting Common Issues

- **Warning: `request.security` repainting**: All HR scripts use `lookahead = barmerge.lookahead_off` and historical `[1]` bar offsets. Ensure you do not remove the `[1]` index.
- **Order fills at unexpected prices**: Pine Script strategy emulator fills market orders on the next bar open when `process_orders_on_close = true` is enabled. Account for the opening gap.
- **Zero trades appearing**: Check your date range filter in the strategy settings. Ensure the chart timeframe matches the strategy design (e.g., 15M).
