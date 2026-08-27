# Hemanth Ranam — Getting Started Guide

## 1. Installation into TradingView
1. Open [TradingView](https://www.tradingview.com/) and navigate to the **Pine Editor** tab at the bottom of the chart.
2. Select **Open** $\rightarrow$ **New Strategy**.
3. Choose any strategy file from `src/strategies/` (e.g., `HR_EMA_Pullback_Pro.pine`), copy the entire code, and paste it into the editor.
4. Click **Save** and then click **Add to Chart**.

---

## 2. Setting Up Real-Time Webhook Alerts
1. On the chart, click the **Alert** button (or press `Alt + A`).
2. Select the strategy under **Condition**.
3. Under **Alert Actions**, check **Webhook URL** and enter your receiver URL (e.g., `https://api.chartora.in/api/v1/webhook` or your instance of `hemanth-ranam-trading-alert-api`).
4. In the **Message** field, enter `{{strategy.order.alert_message}}`.
