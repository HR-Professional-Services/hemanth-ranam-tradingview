# TakeProfit Installation & Quick-Start Guide

## Prerequisites
- A TakeProfit account ([takeprofit.com](https://takeprofit.com)).
- An active Exness account (Live or Demo) connected via API Key (for order execution) or viewed directly on TakeProfit charts.

---

## Step-by-Step Installation

### Method 1: Direct Paste in TakeProfit IDE
1. On your TakeProfit workspace, click **Add Widget** $\rightarrow$ **Code Editor (IDE)**.
2. Click the **+** (New File) button in the IDE header.
3. Choose **New Indicator**.
4. Clear any template code and paste the exact code from your desired `.indie` file:
   - `01_EMA_INDICATORS/HR_9_EMA_BUY_SELL.indie`
   - `01_EMA_INDICATORS/HR_9_21_200_EMA_PULLBACK.indie`
   - `02_LIQUIDITY/HR_LIQUIDITY_SWEEP.indie`
   - `03_MARKET_STRUCTURE/HR_MARKET_STRUCTURE_BOS_CHOCH.indie`
   - `04_VOLATILITY/HR_VOLATILITY_EXPANSION_BREAKOUT.indie`
5. Press `Ctrl + S` (or `Cmd + S` on Mac) to compile and save.
6. Click **Add to Chart** in the top right of the editor.

### Method 2: Via TakeProfit AI Assistant & MCP Server
If you have connected your AI assistant (Claude, Cursor, Codex) to the TakeProfit MCP Server:
```text
Load my "HR 9 EMA Buy/Sell Pro" script and validate it using TakeProfit MCP.
```
