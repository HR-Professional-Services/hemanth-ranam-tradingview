"""
HR TradingView — Full Historical Backtesting Matrix Runner
Executes local historical backtests for all 4 commercial products on Exness-MT5Trial8 data:
- Instruments: XAUUSD, XAGUSD, US500, USTEC
- Timeframes: Primary M15, Higher-Timeframe H1
- Periods: In-Sample (2024-01-01 to 2025-06-30), Out-of-Sample (2025-07-01 to 2026-10-22), Full (2023-12 to 2026-10)
- Execution: 0.02% commission, 2 ticks slippage, On-bar-close fill
- Risk Modes: percent_of_equity (TV Strategy default) AND fixed_monetary_risk (true 1% equity risk)
"""
import os
import csv
import json
from datetime import datetime
from typing import List, Dict, Any
from research.backtest.engine import BacktestEngine
from research.backtest.strategies.pine_reproductions import StrategySimulator

DATA_BASE = "C:/MT5_Research_Lab/Historical_Data/Exness_Demo"

INSTRUMENT_FILES = {
    "XAUUSD": {
        "m15": f"{DATA_BASE}/XAUUSD/M15/XAUUSD_M15_202312211939_202610220033.csv",
        "h1": f"{DATA_BASE}/XAUUSD/H1/XAUUSD_H1_202312211939_202610220033.csv",
        "tick_size": 0.001,
        "contract_size": 100.0
    },
    "XAGUSD": {
        "m15": f"{DATA_BASE}/XAGUSD/M15/XAGUSD_M15_202312202322_202610220034.csv",
        "h1": f"{DATA_BASE}/XAGUSD/H1/XAGUSD_H1_202312202322_202610220034.csv",
        "tick_size": 0.001,
        "contract_size": 5000.0
    },
    "US500": {
        "m15": f"{DATA_BASE}/US500/M15/US500_M15_202312150800_202610220029.csv",
        "h1": f"{DATA_BASE}/US500/H1/US500_H1_202312150800_202610220029.csv",
        "tick_size": 0.01,
        "contract_size": 1.0
    },
    "USTEC": {
        "m15": f"{DATA_BASE}/USTEC/M15/USTEC_M15_202312190307_202610220038.csv",
        "h1": f"{DATA_BASE}/USTEC/H1/USTEC_H1_202312190307_202610220038.csv",
        "tick_size": 0.01,
        "contract_size": 1.0
    }
}

def load_candles(csv_path: str, start_dt: str = None, end_dt: str = None) -> List[Dict[str, Any]]:
    candles = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            t = r['datetime_utc']
            if start_dt and t < start_dt:
                continue
            if end_dt and t > end_dt:
                continue
            candles.append({
                'time': t,
                'open': float(r['open']),
                'high': float(r['high']),
                'low': float(r['low']),
                'close': float(r['close']),
                'vol': float(r.get('tick_volume', 1.0))
            })
    return candles

def run_matrix():
    strategies = [
        ("HR-PRD-01", "EMA_Pullback", StrategySimulator.simulate_ema_pullback, {}),
        ("HR-PRD-02", "Liquidity_Sweep", StrategySimulator.simulate_liquidity_sweep, {}),
        ("HR-PRD-03", "Volatility_Breakout", StrategySimulator.simulate_volatility_breakout, {}),
        ("HR-PRD-04", "Market_Structure", StrategySimulator.simulate_market_structure, {})
    ]
    
    target_instruments = ["XAUUSD", "US500", "USTEC", "XAGUSD"]
    
    periods = [
        ("In-Sample", "2024-01-01 00:00:00", "2025-06-30 23:59:59"),
        ("Out-of-Sample", "2025-07-01 00:00:00", "2026-10-22 23:59:59"),
        ("Full-Historical", "2023-12-15 00:00:00", "2026-10-22 23:59:59")
    ]
    
    matrix_results = []
    
    print("=" * 90)
    print("STARTING HR TRADINGVIEW QUANTITATIVE BACKTEST MATRIX EXECUTION")
    print("=" * 90)
    
    for prd_id, strat_name, sim_func, params in strategies:
        for sym in target_instruments:
            spec = INSTRUMENT_FILES[sym]
            print(f"\n[+] Processing {prd_id} ({strat_name}) on {sym}...")
            
            # Load full candles first to avoid warm-up distortions
            all_m15 = load_candles(spec["m15"])
            all_h1 = load_candles(spec["h1"])
            
            # Generate signals on full sequence
            all_signals = sim_func(all_m15, all_h1, params)
            
            for p_name, p_start, p_end in periods:
                # Filter candles and signals for window
                window_candles = []
                window_signals = []
                for idx, c in enumerate(all_m15):
                    if p_start <= c['time'] <= p_end:
                        window_candles.append(c)
                        window_signals.append(all_signals[idx])
                        
                if not window_candles:
                    continue
                    
                # Run engine in standard TV mode (percent_of_equity = 1.0)
                engine_tv = BacktestEngine(
                    initial_capital=10000.0,
                    commission_pct=0.02,
                    slippage_ticks=2,
                    tick_size=spec["tick_size"],
                    contract_size=spec["contract_size"],
                    risk_mode="percent_of_equity",
                    risk_value=1.0
                )
                metrics_tv = engine_tv.run(window_candles, window_signals)
                
                # Also run engine in true 1% monetary risk mode for audit comparison
                engine_risk = BacktestEngine(
                    initial_capital=10000.0,
                    commission_pct=0.02,
                    slippage_ticks=2,
                    tick_size=spec["tick_size"],
                    contract_size=spec["contract_size"],
                    risk_mode="fixed_monetary_risk",
                    risk_value=1.0
                )
                metrics_risk = engine_risk.run(window_candles, window_signals)
                
                res_record = {
                    "product_id": prd_id,
                    "strategy_name": strat_name,
                    "symbol": sym,
                    "period": p_name,
                    "start": p_start,
                    "end": p_end,
                    "bars": len(window_candles),
                    "tv_sizing": metrics_tv,
                    "true_1pct_risk": metrics_risk
                }
                matrix_results.append(res_record)
                
                print(f"   [{p_name:15s}] Trades: {metrics_tv['total_trades']:3d} | WinRate: {metrics_tv['win_rate']:5.1f}% | PF: {metrics_tv['profit_factor']:4.2f} | Net $: {metrics_tv['net_profit']:8.2f} | MaxDD: {metrics_tv['max_drawdown_pct']:4.1f}%")

    # Save results to json
    out_file = "research/results/phase8_baseline_matrix.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(matrix_results, f, indent=2)
    print(f"\n[OK] Full backtest matrix results successfully saved to {out_file}")

if __name__ == '__main__':
    run_matrix()
