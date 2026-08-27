# Hemanth Ranam — TradingView Suite Troubleshooting Guide

### 1. "Study/Strategy cannot be added to chart"
* Ensure you are pasting into the **Pine Editor** and clicking **Add to Chart** while logged in to TradingView.
* Confirm that your TradingView compiler is set to Pine Script v6 (`//@version=6`).

### 2. "Why am I not seeing signals on the chart?"
* Verify the **Setup Score** on the on-chart HUD table. If the default required score is 6/8, lower the threshold in Settings $\rightarrow$ Signal Quality Scoring Engine to 5/8 or 4/8 to evaluate less strict market conditions.
* Check if the **Active Session Filter** is enabled and outside your current local market hours.
