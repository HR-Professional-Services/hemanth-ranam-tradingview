# TakeProfit Chart UI & Visual Design Verification

## Visual Identity Standards
The Indie v5 indicator suite adheres to the institutional HR Trading visual design tokens:
- **Bullish Signals / Markers**: Lime Green (`color.GREEN`, `color.LIME`).
- **Bearish Signals / Markers**: Vivid Red / Crimson (`color.RED`, `color.MAGENTA`).
- **EMA 9**: Green (`line_width=2`).
- **EMA 21**: Orange (`line_width=1`).
- **EMA 200**: Dodger Blue (`line_width=3`).
- **Cloud Fill**: 12% Opacity (`color.GREEN(0.12)`, `color.RED(0.12)`).
- **Compression Boxes**: Aqua with 8% Opacity fill (`color.AQUA(0.08)`).
- **Markers**: Circular nodes positioned above high / below low with `display_options=plot.MarkerDisplayOptions(pane=True, status_line=False, price_label=False)`.

## Chart Readability & Clutter Control
1. **Zero Text Flooding**: Eliminates bulky floating labels that obscure candlesticks; signals are designated with clean circular dots.
2. **Hidden Value Clutter**: Marker price coordinates are hidden from the chart title status line, preserving uncluttered OHLC inspection.
3. **Multi-Timeframe Scaling**: Lines and bands automatically adapt whether viewed on M5, M15, M30, or H1 charts.
4. **Symbol Agnostic**: Tested across Gold (`XAUUSD`/`XAUUSDm`), Silver (`XAGUSD`/`XAGUSDm`), S&P 500 (`US500`/`US500m`), and Nasdaq (`USTEC`/`USTECm`).
