# ICT / SMC Market Structure Specification

## Core Definitions & Logic

### 1. Fair Value Gaps (FVG)
- **Bullish FVG**: Occurs when `low > high[2]`. The imbalance range between `high[2]` and `low` represents unfilled resting liquidity.
- **Bearish FVG**: Occurs when `high < low[2]`. The imbalance range between `low[2]` and `high` indicates aggressive downside displacement.

### 2. Order Blocks (OB)
- **Bullish Order Block**: Defined as the last bearish candle preceding an aggressive upward displacement that breaks prior minor highs and closes above the 9 EMA.
- **Bearish Order Block**: Defined as the last bullish candle preceding an aggressive downward displacement that breaks prior minor lows and closes below the 9 EMA.

### 3. Dealing Ranges & Premium / Discount
- **Swing Range**: Calculated over the trailing 20 confirmed bars (`highest(high, 20)` and `lowest(low, 20)`).
- **Equilibrium (EQ)**: Defined as `(Range High + Range Low) / 2`.
- **Discount Zone**: Price trading below Equilibrium. Favorable for long setups.
- **Premium Zone**: Price trading above Equilibrium. Favorable for short setups.
