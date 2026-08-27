#!/usr/bin/env python3
"""
HEMANTH RANAM TRADINGVIEW STRATEGY SUITE
TradingView CSV Import, Normalisation & Validation Engine

Usage:
  python research/scripts/tv_importer.py --csv path/to/export.csv \
      --strategy HR_EMA_Pullback_Pro \
      --symbol XAUUSD \
      --timeframe 5M \
      --scenario B \
      --source OANDA \
      --period-start 2026-01-01 \
      --period-end 2026-08-27 \
      --period-type out_of_sample \
      --output research/results/

Supports TradingView "List of Trades" CSV export format.
"""

import csv
import json
import os
import sys
import argparse
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schema", "results.schema.json")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

# TradingView "List of Trades" CSV column mappings.
# TradingView may vary column headers by version — this is a mapping layer.
TV_COLUMN_MAPS = [
    # Format A: Standard TradingView export (most common)
    {
        "trade_num": "Trade #",
        "type":      "Type",
        "datetime":  "Date/Time",
        "price":     "Price",
        "contracts": "Contracts",
        "profit":    "Profit",
        "profit_pct":"Profit %",
        "runup":     "Run-up",
        "drawdown":  "Drawdown",
        "cum_profit":"Cumulative Profit",
    },
    # Format B: Alternative TradingView export (some account types)
    {
        "trade_num": "#",
        "type":      "Type",
        "datetime":  "Date",
        "price":     "Price USD",
        "contracts": "Qty",
        "profit":    "P&L",
        "profit_pct":"P&L %",
        "runup":     "Run-up",
        "drawdown":  "Drawdown",
        "cum_profit":"Net Profit",
    },
]


def detect_column_map(headers: List[str]) -> Optional[Dict[str, str]]:
    """Detect which column mapping matches the CSV headers."""
    for mapping in TV_COLUMN_MAPS:
        required = list(mapping.values())
        if all(col in headers for col in required):
            return mapping
    return None


def parse_tv_csv(filepath: str) -> List[Dict[str, Any]]:
    """Parse a TradingView 'List of Trades' CSV export."""
    trades = []
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        col_map = detect_column_map(headers)

        if col_map is None:
            print(f"[ERROR] Unrecognised CSV format. Headers found: {headers}")
            print("[INFO]  Edit research/scripts/tv_importer.py → TV_COLUMN_MAPS to add your format.")
            sys.exit(1)

        for row in reader:
            trade_type = row.get(col_map["type"], "").strip()
            if trade_type not in ("Entry Long", "Entry Short", "Exit Long", "Exit Short", "Buy", "Sell"):
                continue  # Skip non-trade summary rows

            profit_str = row.get(col_map["profit"], "").replace(",", "").replace(" ", "")
            profit_pct_str = row.get(col_map["profit_pct"], "").replace(",", "").replace("%", "").replace(" ", "")

            try:
                profit = float(profit_str) if profit_str else None
                profit_pct = float(profit_pct_str) if profit_pct_str else None
            except ValueError:
                profit = None
                profit_pct = None

            trades.append({
                "trade_num":  row.get(col_map["trade_num"]),
                "type":       trade_type,
                "datetime":   row.get(col_map["datetime"]),
                "price":      row.get(col_map["price"]),
                "contracts":  row.get(col_map["contracts"]),
                "profit":     profit,
                "profit_pct": profit_pct,
            })

    return trades


def compute_metrics(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute standard performance metrics from trade list."""
    # Filter to closed trades with P&L
    closed = [t for t in trades if t.get("profit") is not None]

    if not closed:
        return {"total_trades": 0}

    profits = [t["profit"] for t in closed]
    wins   = [p for p in profits if p > 0]
    losses = [p for p in profits if p <= 0]

    gross_profit = sum(wins)
    gross_loss   = abs(sum(losses))
    profit_factor = round(gross_profit / gross_loss, 3) if gross_loss > 0 else (None if gross_profit == 0 else 99.0)
    win_rate = round(len(wins) / len(profits) * 100.0, 2) if profits else None

    avg_win  = round(sum(wins) / len(wins), 4) if wins else None
    avg_loss = round(abs(sum(losses)) / len(losses), 4) if losses else None
    avg_trade = round(sum(profits) / len(profits), 4) if profits else None

    # Expectancy = (WinRate × AvgWin) - (LossRate × AvgLoss)
    if avg_win is not None and avg_loss is not None and win_rate is not None:
        expectancy = round((win_rate / 100.0 * avg_win) - ((1 - win_rate / 100.0) * avg_loss), 4)
    else:
        expectancy = None

    # Equity curve for max drawdown
    equity = [0.0]
    for p in profits:
        equity.append(equity[-1] + p)

    peak = equity[0]
    max_dd = 0.0
    for val in equity:
        if val > peak: peak = val
        dd = peak - val
        if dd > max_dd: max_dd = dd

    # Consecutive wins/losses
    max_consec_wins = max_consec_losses = 0
    cur_w = cur_l = 0
    for p in profits:
        if p > 0:
            cur_w += 1; cur_l = 0
        else:
            cur_l += 1; cur_w = 0
        max_consec_wins   = max(max_consec_wins,   cur_w)
        max_consec_losses = max(max_consec_losses, cur_l)

    return {
        "total_trades":          len(profits),
        "net_profit":            round(sum(profits), 4),
        "profit_factor":         profit_factor,
        "win_rate":              win_rate,
        "average_trade":         avg_trade,
        "average_win":           avg_win,
        "average_loss":          avg_loss,
        "expectancy":            expectancy,
        "max_drawdown":          round(max_dd, 4),
        "largest_win":           round(max(wins), 4) if wins else None,
        "largest_loss":          round(min(losses), 4) if losses else None,
        "max_consecutive_wins":  max_consec_wins,
        "max_consecutive_losses":max_consec_losses,
        # These require TradingView overview panel — mark null
        "net_profit_pct":        None,
        "max_drawdown_pct":      None,
        "sharpe":                None,
        "sortino":               None,
        "long_trades":           None,
        "short_trades":          None,
        "long_win_rate":         None,
        "short_win_rate":        None,
    }


def build_result(args: argparse.Namespace, metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Construct a normalised result record conforming to results.schema.json."""
    result_id = "_".join([
        args.strategy, args.symbol, args.timeframe,
        args.period_start, args.period_end, f"Scenario{args.scenario}"
    ])
    return {
        "schema_version":    "1.0",
        "result_id":         result_id,
        "strategy":          args.strategy,
        "strategy_version":  "1.0",
        "parameter_version": "1.0",
        "symbol":            args.symbol,
        "timeframe":         args.timeframe,
        "data_source":       args.source,
        "period_start":      args.period_start,
        "period_end":        args.period_end,
        "period_type":       args.period_type,
        "cost_scenario":     args.scenario,
        "validation_status": "NATIVE-TV-VERIFIED",
        "initial_capital":   10000,
        "commission_pct":    0.02 if args.scenario == "B" else (0.0 if args.scenario == "A" else 0.06),
        "slippage_ticks":    2    if args.scenario == "B" else (0   if args.scenario == "A" else 4),
        "position_size_pct": 1.0,
        **metrics,
        "notes": None,
    }


def validate_against_schema(result: Dict[str, Any]) -> List[str]:
    """Basic validation against required fields and allowed values."""
    errors = []
    VALID_STRATEGIES  = ["HR_EMA_Pullback_Pro", "HR_Breakout_Retest_Pro", "HR_Market_Structure_Pro", "HR_VWAP_Mean_Reversion_Pro", "HR_Momentum_Volatility_Pro"]
    VALID_TIMEFRAMES  = ["5M", "15M", "1H", "4H"]
    VALID_SCENARIOS   = ["A", "B", "C"]
    VALID_STATUSES    = ["SIMULATED", "NATIVE-TV-PENDING", "NATIVE-TV-VERIFIED", "OOS-VERIFIED", "FORWARD-TESTING", "PAPER-TRADING", "LIVE-ELIGIBLE", "REJECTED"]

    if result.get("strategy") not in VALID_STRATEGIES:
        errors.append(f"Invalid strategy: {result.get('strategy')}")
    if result.get("timeframe") not in VALID_TIMEFRAMES:
        errors.append(f"Invalid timeframe: {result.get('timeframe')}")
    if result.get("cost_scenario") not in VALID_SCENARIOS:
        errors.append(f"Invalid cost_scenario: {result.get('cost_scenario')}")
    if result.get("validation_status") not in VALID_STATUSES:
        errors.append(f"Invalid validation_status: {result.get('validation_status')}")
    if result.get("total_trades", 0) == 0:
        errors.append("WARNING: total_trades is 0. Ensure this is not a fabricated result.")

    return errors


def main():
    parser = argparse.ArgumentParser(description="TradingView CSV Importer & Normaliser")
    parser.add_argument("--csv",          required=True,  help="Path to TradingView 'List of Trades' CSV export")
    parser.add_argument("--strategy",     required=True,  help="Strategy name (e.g. HR_EMA_Pullback_Pro)")
    parser.add_argument("--symbol",       required=True,  help="Market symbol (e.g. XAUUSD)")
    parser.add_argument("--timeframe",    required=True,  help="Timeframe (5M, 15M, 1H, 4H)")
    parser.add_argument("--scenario",     required=True,  help="Cost scenario: A, B, or C")
    parser.add_argument("--source",       required=True,  help="TradingView data source/broker feed (e.g. OANDA)")
    parser.add_argument("--period-start", required=True,  dest="period_start", help="Test period start (YYYY-MM-DD)")
    parser.add_argument("--period-end",   required=True,  dest="period_end",   help="Test period end (YYYY-MM-DD)")
    parser.add_argument("--period-type",  required=False, dest="period_type",  default=None,
                        help="Period type: development, validation, out_of_sample, forward")
    parser.add_argument("--output",       required=False, default=RESULTS_DIR, help="Output directory for JSON results")
    args = parser.parse_args()

    print(f"\n[TV IMPORTER] Parsing: {args.csv}")
    trades  = parse_tv_csv(args.csv)
    print(f"[TV IMPORTER] Parsed {len(trades)} trade rows.")

    metrics = compute_metrics(trades)
    result  = build_result(args, metrics)

    errors  = validate_against_schema(result)
    if errors:
        print("\n[VALIDATION WARNINGS]")
        for e in errors:
            print(f"  ⚠  {e}")

    os.makedirs(args.output, exist_ok=True)
    out_file = os.path.join(args.output, f"{result['result_id']}.json")
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n[TV IMPORTER] Result saved: {out_file}")
    print(f"  Trades:        {result.get('total_trades')}")
    print(f"  Profit Factor: {result.get('profit_factor')}")
    print(f"  Win Rate:      {result.get('win_rate')}%")
    print(f"  Net Profit:    {result.get('net_profit')}")
    print(f"  Max Drawdown:  {result.get('max_drawdown')}")
    print(f"  Expectancy:    {result.get('expectancy')}")
    print(f"\n[TV IMPORTER] Status: {result['validation_status']}")


if __name__ == "__main__":
    main()
