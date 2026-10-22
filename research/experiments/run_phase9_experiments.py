"""
HR TradingView — Phase 9 Quantitative Experiment Runner
Runs all controlled experiments across:
1. Phase 9B: HR-PRD-01 EMA Pullback:
   - Control (No ADX, 1.5 ATR SL)
   - Experiment A: ADX thresholds (18, 20, 22, 25)
   - Experiment B: ATR Stop Sensitivity (1.5, 1.75, 2.0 ATR)
   - Experiment C: Best combined candidates
2. Phase 9C: HR-PRD-02 Liquidity Sweep:
   - Control (Unrestricted Sweeps)
   - Experiment A: Pro-Trend Sweeps (H1 200 EMA alignment)
   - Experiment B: Sweep Quality depth variations
3. Phase 9D: HR-PRD-03 Volatility Breakout:
   - Control (20-bar, 1.8 ATR squeeze, volume filter)
   - Experiment A: Squeeze threshold relaxation (1.8, 2.0, 2.2 ATR; 12, 16, 20 lookbacks)
   - Experiment B: Volume filter on vs off
4. Phase 9E: HR-PRD-04 Market Structure:
   - Benchmark validation under TV sizing vs True 1% monetary risk
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any
from research.backtest.engine import BacktestEngine
from research.backtest.run_matrix import load_candles, INSTRUMENT_FILES
from research.backtest.strategies.pine_reproductions import StrategySimulator
from research.backtest.candidates.candidate_simulators import CandidateSimulator

def run_phase9_experiments():
    print("=" * 90)
    print("STARTING PHASE 9 CONTROLLED STRATEGY REMEDIATION & OPTIMIZATION")
    print("=" * 90)
    
    # Load primary assets
    xau = {
        "m15": load_candles(INSTRUMENT_FILES["XAUUSD"]["m15"]),
        "h1": load_candles(INSTRUMENT_FILES["XAUUSD"]["h1"]),
        "spec": INSTRUMENT_FILES["XAUUSD"]
    }
    xag = {
        "m15": load_candles(INSTRUMENT_FILES["XAGUSD"]["m15"]),
        "h1": load_candles(INSTRUMENT_FILES["XAGUSD"]["h1"]),
        "spec": INSTRUMENT_FILES["XAGUSD"]
    }
    us500 = {
        "m15": load_candles(INSTRUMENT_FILES["US500"]["m15"]),
        "h1": load_candles(INSTRUMENT_FILES["US500"]["h1"]),
        "spec": INSTRUMENT_FILES["US500"]
    }
    ustec = {
        "m15": load_candles(INSTRUMENT_FILES["USTEC"]["m15"]),
        "h1": load_candles(INSTRUMENT_FILES["USTEC"]["h1"]),
        "spec": INSTRUMENT_FILES["USTEC"]
    }
    
    assets = {"XAUUSD": xau, "XAGUSD": xag, "US500": us500, "USTEC": ustec}
    
    # Date Windows
    IS_START, IS_END = "2024-01-01 00:00:00", "2025-06-30 23:59:59"
    OOS_START, OOS_END = "2025-07-01 00:00:00", "2026-10-22 23:59:59"
    FULL_START, FULL_END = "2023-12-15 00:00:00", "2026-10-22 23:59:59"
    
    results = {}

    def eval_candidate(name, sim_func, params, asset_key):
        asset = assets[asset_key]
        candles = asset["m15"]
        h1 = asset["h1"]
        spec = asset["spec"]
        
        all_signals = sim_func(candles, h1, params)
        
        # In-sample
        is_candles, is_signals = [], []
        oos_candles, oos_signals = [], []
        full_candles, full_signals = [], []
        
        for idx, c in enumerate(candles):
            t = c['time']
            if IS_START <= t <= IS_END:
                is_candles.append(c)
                is_signals.append(all_signals[idx])
            if OOS_START <= t <= OOS_END:
                oos_candles.append(c)
                oos_signals.append(all_signals[idx])
            if FULL_START <= t <= FULL_END:
                full_candles.append(c)
                full_signals.append(all_signals[idx])
                
        # Run standard TV sizing
        engine_is = BacktestEngine(10000.0, 0.02, 2, spec["tick_size"], contract_size=spec["contract_size"], risk_mode="percent_of_equity")
        m_is = engine_is.run(is_candles, is_signals)
        
        engine_oos = BacktestEngine(10000.0, 0.02, 2, spec["tick_size"], contract_size=spec["contract_size"], risk_mode="percent_of_equity")
        m_oos = engine_oos.run(oos_candles, oos_signals)
        
        engine_full = BacktestEngine(10000.0, 0.02, 2, spec["tick_size"], contract_size=spec["contract_size"], risk_mode="percent_of_equity")
        m_full = engine_full.run(full_candles, full_signals)
        
        return {
            "name": name,
            "asset": asset_key,
            "params": params,
            "in_sample": m_is,
            "out_of_sample": m_oos,
            "full": m_full
        }

    # =========================================================================
    # 1. PHASE 9B: HR-PRD-01 EMA PULLBACK EXPERIMENTS
    # =========================================================================
    print("\n--- [Phase 9B] HR-PRD-01 EMA Trend Pullback Pro Experiments ---")
    results["HR-PRD-01"] = []
    
    # Controls & ADX Variations on XAUUSD
    adx_variations = [
        ("Control (No ADX, 1.5 ATR SL)", {"use_adx": False, "sl_atr_mult": 1.5}),
        ("ADX >= 18 (1.5 ATR SL)", {"use_adx": True, "adx_threshold": 18.0, "sl_atr_mult": 1.5}),
        ("ADX >= 20 (1.5 ATR SL)", {"use_adx": True, "adx_threshold": 20.0, "sl_atr_mult": 1.5}),
        ("ADX >= 22 (1.5 ATR SL)", {"use_adx": True, "adx_threshold": 22.0, "sl_atr_mult": 1.5}),
        ("ADX >= 25 (1.5 ATR SL)", {"use_adx": True, "adx_threshold": 25.0, "sl_atr_mult": 1.5}),
        ("Stop Sensitivity: 1.75 ATR (No ADX)", {"use_adx": False, "sl_atr_mult": 1.75}),
        ("Stop Sensitivity: 2.0 ATR (No ADX)", {"use_adx": False, "sl_atr_mult": 2.0}),
        ("Combined: ADX >= 20 + 2.0 ATR SL", {"use_adx": True, "adx_threshold": 20.0, "sl_atr_mult": 2.0}),
        ("Combined: ADX >= 22 + 2.0 ATR SL", {"use_adx": True, "adx_threshold": 22.0, "sl_atr_mult": 2.0})
    ]
    
    for name, p in adx_variations:
        res = eval_candidate(name, CandidateSimulator.simulate_ema_pullback_candidate, p, "XAUUSD")
        results["HR-PRD-01"].append(res)
        is_m, oos_m, f_m = res["in_sample"], res["out_of_sample"], res["full"]
        print(f"XAUUSD | {name:36s} | Full: PF {f_m['profit_factor']:4.2f} (${f_m['net_profit']:7.2f}, {f_m['total_trades']:4d} tr) | IS: PF {is_m['profit_factor']:4.2f} | OOS: PF {oos_m['profit_factor']:4.2f}")

    # =========================================================================
    # 2. PHASE 9C: HR-PRD-02 LIQUIDITY SWEEP REVERSAL EXPERIMENTS
    # =========================================================================
    print("\n--- [Phase 9C] HR-PRD-02 Liquidity Sweep Reversal Experiments ---")
    results["HR-PRD-02"] = []
    
    sweep_variations = [
        ("Control (No HTF Alignment)", {"enforce_htf_trend": False, "min_sweep_atr": 0.20}),
        ("Experiment A: Pro-Trend Sweeps (H1 200 EMA)", {"enforce_htf_trend": True, "min_sweep_atr": 0.20}),
        ("Experiment B: Deep Sweeps (min 0.35 ATR)", {"enforce_htf_trend": False, "min_sweep_atr": 0.35}),
        ("Combined: Pro-Trend + Deep Sweep (0.35 ATR)", {"enforce_htf_trend": True, "min_sweep_atr": 0.35})
    ]
    
    for name, p in sweep_variations:
        for sym in ["XAUUSD", "US500"]:
            res = eval_candidate(name, CandidateSimulator.simulate_liquidity_sweep_candidate, p, sym)
            results["HR-PRD-02"].append(res)
            is_m, oos_m, f_m = res["in_sample"], res["out_of_sample"], res["full"]
            print(f"{sym:6s} | {name:40s} | Full: PF {f_m['profit_factor']:4.2f} (${f_m['net_profit']:8.2f}, {f_m['total_trades']:4d} tr) | IS: PF {is_m['profit_factor']:4.2f} | OOS: PF {oos_m['profit_factor']:4.2f}")

    # =========================================================================
    # 3. PHASE 9D: HR-PRD-03 VOLATILITY EXPANSION BREAKOUT EXPERIMENTS
    # =========================================================================
    print("\n--- [Phase 9D] HR-PRD-03 Volatility Expansion Breakout Experiments ---")
    results["HR-PRD-03"] = []
    
    breakout_variations = [
        ("Control (Lookback 20, Squeeze 1.8 ATR, Vol On)", {"box_lookback": 20, "squeeze_threshold": 1.80, "require_volume": True}),
        ("Exp A1: Squeeze 2.0 ATR (Lookback 20, Vol On)", {"box_lookback": 20, "squeeze_threshold": 2.00, "require_volume": True}),
        ("Exp A2: Squeeze 2.2 ATR (Lookback 20, Vol On)", {"box_lookback": 20, "squeeze_threshold": 2.20, "require_volume": True}),
        ("Exp A3: Lookback 16, Squeeze 1.8 ATR (Vol On)", {"box_lookback": 16, "squeeze_threshold": 1.80, "require_volume": True}),
        ("Exp A4: Lookback 12, Squeeze 2.2 ATR (Vol On)", {"box_lookback": 12, "squeeze_threshold": 2.20, "require_volume": True}),
        ("Exp B1: Lookback 20, Squeeze 2.0 ATR (Vol Off)", {"box_lookback": 20, "squeeze_threshold": 2.00, "require_volume": False}),
        ("Exp B2: Lookback 12, Squeeze 2.2 ATR (Vol Off)", {"box_lookback": 12, "squeeze_threshold": 2.20, "require_volume": False})
    ]
    
    for name, p in breakout_variations:
        for sym in ["XAUUSD", "US500", "USTEC"]:
            res = eval_candidate(name, CandidateSimulator.simulate_volatility_breakout_candidate, p, sym)
            results["HR-PRD-03"].append(res)
            is_m, oos_m, f_m = res["in_sample"], res["out_of_sample"], res["full"]
            print(f"{sym:6s} | {name:46s} | Full: PF {f_m['profit_factor']:4.2f} (${f_m['net_profit']:7.2f}, {f_m['total_trades']:3d} tr) | IS: PF {is_m['profit_factor']:4.2f} | OOS: PF {oos_m['profit_factor']:4.2f}")

    # Save Phase 9 experiment matrix to JSON
    out_file = "research/results/phase9_experiments_matrix.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[OK] Phase 9 experiment results saved to {out_file}")

if __name__ == '__main__':
    run_phase9_experiments()
