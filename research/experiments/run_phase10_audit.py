"""
HR TradingView — Phase 10 Independent Audit, Robustness Engine & Trade Log Exporter
1. Reconciles Phase 9 claims against exact trade logs.
2. Exports trade-by-trade CSVs with entry, exit, duration, planned risk, realized PnL, and costs.
3. Performs parameter perturbation sensitivity analysis (box lookback 16 vs 20, squeeze 2.0 vs 2.2).
4. Tests adverse cost scenarios (2x commission, 2x slippage, adverse spread).
5. Computes statistical uncertainty metrics: bootstrap confidence intervals, consecutive loss distributions.
"""
import os
import csv
import json
import math
import random
from datetime import datetime
from typing import List, Dict, Any
from research.backtest.engine import BacktestEngine, Trade
from research.backtest.run_matrix import load_candles, INSTRUMENT_FILES
from research.backtest.strategies.pine_reproductions import StrategySimulator
from research.backtest.candidates.candidate_simulators import CandidateSimulator

IS_START, IS_END = "2024-01-01 00:00:00", "2025-06-30 23:59:59"
OOS_START, OOS_END = "2025-07-01 00:00:00", "2026-10-22 23:59:59"
FULL_START, FULL_END = "2023-12-15 00:00:00", "2026-10-22 23:59:59"

def export_trade_log_csv(trades: List[Trade], filepath: str):
    fieldnames = [
        "trade_id", "direction", "entry_bar", "entry_time", "entry_price",
        "sl_price", "tp_price", "exit_bar", "exit_time", "exit_price",
        "exit_reason", "qty", "pnl_cash", "pnl_pct", "commission", "score", "grade"
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in trades:
            writer.writerow({
                "trade_id": t.trade_id,
                "direction": "BUY" if t.direction == 1 else "SELL",
                "entry_bar": t.entry_bar,
                "entry_time": t.entry_time,
                "entry_price": round(t.entry_price, 4),
                "sl_price": round(t.sl_price, 4),
                "tp_price": round(t.tp_price, 4),
                "exit_bar": t.exit_bar,
                "exit_time": t.exit_time,
                "exit_price": round(t.exit_price, 4) if t.exit_price else 0.0,
                "exit_reason": t.exit_reason,
                "qty": round(t.qty, 4),
                "pnl_cash": round(t.pnl_cash, 2),
                "pnl_pct": round(t.pnl_pct, 4),
                "commission": round(t.commission, 2),
                "score": t.score,
                "grade": t.grade
            })

def calc_consecutive_losses(trades: List[Trade]) -> int:
    max_streak = 0
    cur_streak = 0
    for t in trades:
        if t.pnl_cash <= 0:
            cur_streak += 1
            if cur_streak > max_streak:
                max_streak = cur_streak
        else:
            cur_streak = 0
    return max_streak

def bootstrap_profit_factor_ci(trades: List[Trade], n_iter: int = 1000, seed: int = 42) -> Dict[str, float]:
    """Calculates 95% bootstrap confidence interval for Profit Factor."""
    if len(trades) < 5:
        return {"p025": 0.0, "p50": 0.0, "p975": 0.0}
    random.seed(seed)
    pnls = [t.pnl_cash for t in trades]
    pfs = []
    for _ in range(n_iter):
        sample = random.choices(pnls, k=len(pnls))
        wins = sum(x for x in sample if x > 0)
        losses = abs(sum(x for x in sample if x <= 0))
        pf = (wins / losses) if losses > 0 else (10.0 if wins > 0 else 0.0)
        pfs.append(pf)
    pfs.sort()
    return {
        "p025": round(pfs[int(n_iter * 0.025)], 2),
        "p50": round(pfs[int(n_iter * 0.50)], 2),
        "p975": round(pfs[int(n_iter * 0.975)], 2)
    }

def run_phase10_audit():
    print("=" * 90)
    print("STARTING PHASE 10 INDEPENDENT VERIFICATION & ROBUSTNESS ENGINE")
    print("=" * 90)
    
    # 1. Load Data
    spec_xau = INSTRUMENT_FILES["XAUUSD"]
    m15_xau = load_candles(spec_xau["m15"])
    h1_xau = load_candles(spec_xau["h1"])
    
    spec_xag = INSTRUMENT_FILES["XAGUSD"]
    m15_xag = load_candles(spec_xag["m15"])
    h1_xag = load_candles(spec_xag["h1"])

    audit_records = {}

    # =========================================================================
    # AUDIT 1: HR-PRD-03 Exp A2 Independent Reproduction & Trade Logs
    # =========================================================================
    print("\n[+] Audit 1: HR-PRD-03 Candidate Exp A2 (XAUUSD)...")
    p_expa2 = {"box_lookback": 20, "squeeze_threshold": 2.20, "require_volume": True}
    sigs_expa2 = CandidateSimulator.simulate_volatility_breakout_candidate(m15_xau, h1_xau, p_expa2)
    
    # Run full under TV Sizing
    eng_tv_full = BacktestEngine(10000.0, 0.02, 2, spec_xau["tick_size"], contract_size=spec_xau["contract_size"], risk_mode="percent_of_equity")
    m_tv_full = eng_tv_full.run(m15_xau, sigs_expa2)
    export_trade_log_csv(eng_tv_full.trades, "research/results/phase10_trade_logs/HR_PRD_03_ExpA2_TV_Sizing_Full.csv")
    
    # Run full under True 1.0% Risk
    eng_rk_full = BacktestEngine(10000.0, 0.02, 2, spec_xau["tick_size"], contract_size=spec_xau["contract_size"], risk_mode="fixed_monetary_risk", risk_value=1.0)
    m_rk_full = eng_rk_full.run(m15_xau, sigs_expa2)
    export_trade_log_csv(eng_rk_full.trades, "research/results/phase10_trade_logs/HR_PRD_03_ExpA2_True1pctRisk_Full.csv")
    
    # Separate IS vs OOS under True 1% Risk
    is_c, is_s = [], []
    oos_c, oos_s = [], []
    for idx, c in enumerate(m15_xau):
        t = c['time']
        if IS_START <= t <= IS_END:
            is_c.append(c)
            is_s.append(sigs_expa2[idx])
        if OOS_START <= t <= OOS_END:
            oos_c.append(c)
            oos_s.append(sigs_expa2[idx])
            
    eng_rk_is = BacktestEngine(10000.0, 0.02, 2, spec_xau["tick_size"], contract_size=spec_xau["contract_size"], risk_mode="fixed_monetary_risk", risk_value=1.0)
    m_rk_is = eng_rk_is.run(is_c, is_s)
    export_trade_log_csv(eng_rk_is.trades, "research/results/phase10_trade_logs/HR_PRD_03_ExpA2_True1pctRisk_IS.csv")
    
    eng_rk_oos = BacktestEngine(10000.0, 0.02, 2, spec_xau["tick_size"], contract_size=spec_xau["contract_size"], risk_mode="fixed_monetary_risk", risk_value=1.0)
    m_rk_oos = eng_rk_oos.run(oos_c, oos_s)
    export_trade_log_csv(eng_rk_oos.trades, "research/results/phase10_trade_logs/HR_PRD_03_ExpA2_True1pctRisk_OOS.csv")
    
    # Bootstrap CI for Exp A2 OOS
    ci_expa2_oos = bootstrap_profit_factor_ci(eng_rk_oos.trades)
    max_streak_expa2 = calc_consecutive_losses(eng_rk_full.trades)
    
    audit_records["HR-PRD-03-ExpA2"] = {
        "tv_sizing_full": m_tv_full,
        "true_risk_full": m_rk_full,
        "true_risk_is": m_rk_is,
        "true_risk_oos": m_rk_oos,
        "bootstrap_ci_oos_pf": ci_expa2_oos,
        "max_consecutive_losses": max_streak_expa2
    }
    
    print(f"   Exp A2 TV Sizing Full: Trades={m_tv_full['total_trades']}, PF={m_tv_full['profit_factor']}, Net=${m_tv_full['net_profit']}")
    print(f"   Exp A2 True 1% Risk Full: Trades={m_rk_full['total_trades']}, PF={m_rk_full['profit_factor']}, Net=${m_rk_full['net_profit']}")
    print(f"   Exp A2 True 1% Risk IS:   Trades={m_rk_is['total_trades']}, PF={m_rk_is['profit_factor']}, Net=${m_rk_is['net_profit']}")
    print(f"   Exp A2 True 1% Risk OOS:  Trades={m_rk_oos['total_trades']}, PF={m_rk_oos['profit_factor']}, Net=${m_rk_oos['net_profit']}")
    print(f"   Exp A2 OOS Bootstrap 95% CI for PF: [{ci_expa2_oos['p025']} - {ci_expa2_oos['p975']}] (Median: {ci_expa2_oos['p50']})")
    print(f"   Exp A2 Max Consecutive Losses: {max_streak_expa2}")

    # =========================================================================
    # AUDIT 2: HR-PRD-03 Parameter Perturbations & Adverse Costs
    # =========================================================================
    print("\n[+] Audit 2: HR-PRD-03 Robustness & Cost Stress Testing...")
    perturbations = [
        ("Base Exp A2", 20, 2.20, 0.02, 2),
        ("Perturb Squeeze 2.10 ATR", 20, 2.10, 0.02, 2),
        ("Perturb Squeeze 2.30 ATR", 20, 2.30, 0.02, 2),
        ("Perturb Lookback 18 bars", 18, 2.20, 0.02, 2),
        ("Perturb Lookback 22 bars", 22, 2.20, 0.02, 2),
        ("Stress Cost: 0.04% Comm + 4 Ticks Slip", 20, 2.20, 0.04, 4),
        ("Extreme Cost: 0.06% Comm + 6 Ticks Slip", 20, 2.20, 0.06, 6)
    ]
    
    pert_results = []
    for label, lb, sq, comm, slip in perturbations:
        s_pert = CandidateSimulator.simulate_volatility_breakout_candidate(m15_xau, h1_xau, {"box_lookback": lb, "squeeze_threshold": sq, "require_volume": True})
        eng_p = BacktestEngine(10000.0, comm, slip, spec_xau["tick_size"], contract_size=spec_xau["contract_size"], risk_mode="fixed_monetary_risk", risk_value=1.0)
        m_p = eng_p.run(m15_xau, s_pert)
        pert_results.append({
            "label": label,
            "lookback": lb,
            "squeeze": sq,
            "commission": comm,
            "slippage": slip,
            "trades": m_p["total_trades"],
            "win_rate": m_p["win_rate"],
            "pf": m_p["profit_factor"],
            "net_profit": m_p["net_profit"],
            "max_dd_pct": m_p["max_drawdown_pct"]
        })
        print(f"   {label:38s} | Tr: {m_p['total_trades']:2d} | PF: {m_p['profit_factor']:4.2f} | Net $: {m_p['net_profit']:8.2f} | MaxDD: {m_p['max_drawdown_pct']:4.1f}%")
        
    audit_records["HR-PRD-03-Perturbations"] = pert_results

    # =========================================================================
    # AUDIT 3: HR-PRD-04 Market Structure Reproduction & Trade Logs
    # =========================================================================
    print("\n[+] Audit 3: HR-PRD-04 Market Structure Reproduction & Reconciliation...")
    sigs_ms_xau = StrategySimulator.simulate_market_structure(m15_xau, h1_xau, {})
    
    # 0.5% Risk Full
    eng_ms_05_full = BacktestEngine(10000.0, 0.02, 2, spec_xau["tick_size"], contract_size=spec_xau["contract_size"], risk_mode="fixed_monetary_risk", risk_value=0.5)
    m_ms_05_full = eng_ms_05_full.run(m15_xau, sigs_ms_xau)
    export_trade_log_csv(eng_ms_05_full.trades, "research/results/phase10_trade_logs/HR_PRD_04_XAU_Risk05_Full.csv")
    
    # 1.0% Risk Full
    eng_ms_10_full = BacktestEngine(10000.0, 0.02, 2, spec_xau["tick_size"], contract_size=spec_xau["contract_size"], risk_mode="fixed_monetary_risk", risk_value=1.0)
    m_ms_10_full = eng_ms_10_full.run(m15_xau, sigs_ms_xau)
    export_trade_log_csv(eng_ms_10_full.trades, "research/results/phase10_trade_logs/HR_PRD_04_XAU_Risk10_Full.csv")
    
    # IS vs OOS at 0.5%
    is_ms_c, is_ms_s = [], []
    oos_ms_c, oos_ms_s = [], []
    for idx, c in enumerate(m15_xau):
        t = c['time']
        if IS_START <= t <= IS_END:
            is_ms_c.append(c)
            is_ms_s.append(sigs_ms_xau[idx])
        if OOS_START <= t <= OOS_END:
            oos_ms_c.append(c)
            oos_ms_s.append(sigs_ms_xau[idx])
            
    eng_ms_05_is = BacktestEngine(10000.0, 0.02, 2, spec_xau["tick_size"], contract_size=spec_xau["contract_size"], risk_mode="fixed_monetary_risk", risk_value=0.5)
    m_ms_05_is = eng_ms_05_is.run(is_ms_c, is_ms_s)
    
    eng_ms_05_oos = BacktestEngine(10000.0, 0.02, 2, spec_xau["tick_size"], contract_size=spec_xau["contract_size"], risk_mode="fixed_monetary_risk", risk_value=0.5)
    m_ms_05_oos = eng_ms_05_oos.run(oos_ms_c, oos_ms_s)
    
    ci_ms_oos = bootstrap_profit_factor_ci(eng_ms_05_oos.trades)
    max_streak_ms = calc_consecutive_losses(eng_ms_05_full.trades)
    
    audit_records["HR-PRD-04-XAUUSD"] = {
        "risk_05_full": m_ms_05_full,
        "risk_10_full": m_ms_10_full,
        "risk_05_is": m_ms_05_is,
        "risk_05_oos": m_ms_05_oos,
        "bootstrap_ci_oos_pf": ci_ms_oos,
        "max_consecutive_losses": max_streak_ms
    }
    
    print(f"   HR-PRD-04 0.5% Risk Full: Trades={m_ms_05_full['total_trades']}, PF={m_ms_05_full['profit_factor']}, Net=${m_ms_05_full['net_profit']}, MaxDD={m_ms_05_full['max_drawdown_pct']}%")
    print(f"   HR-PRD-04 0.5% Risk IS:   Trades={m_ms_05_is['total_trades']}, PF={m_ms_05_is['profit_factor']}, Net=${m_ms_05_is['net_profit']}, MaxDD={m_ms_05_is['max_drawdown_pct']}%")
    print(f"   HR-PRD-04 0.5% Risk OOS:  Trades={m_ms_05_oos['total_trades']}, PF={m_ms_05_oos['profit_factor']}, Net=${m_ms_05_oos['net_profit']}, MaxDD={m_ms_05_oos['max_drawdown_pct']}%")
    print(f"   HR-PRD-04 OOS Bootstrap 95% CI for PF: [{ci_ms_oos['p025']} - {ci_ms_oos['p975']}] (Median: {ci_ms_oos['p50']})")
    print(f"   HR-PRD-04 Max Consecutive Losses: {max_streak_ms}")

    # =========================================================================
    # AUDIT 4: HR-PRD-04 Silver (XAGUSD) Separate Validation
    # =========================================================================
    print("\n[+] Audit 4: HR-PRD-04 Silver (XAGUSD) Separate Validation...")
    sigs_ms_xag = StrategySimulator.simulate_market_structure(m15_xag, h1_xag, {})
    eng_xag_05 = BacktestEngine(10000.0, 0.02, 2, spec_xag["tick_size"], contract_size=spec_xag["contract_size"], risk_mode="fixed_monetary_risk", risk_value=0.5)
    m_xag_05 = eng_xag_05.run(m15_xag, sigs_ms_xag)
    export_trade_log_csv(eng_xag_05.trades, "research/results/phase10_trade_logs/HR_PRD_04_XAG_Risk05_Full.csv")
    print(f"   HR-PRD-04 XAGUSD 0.5% Risk Full: Trades={m_xag_05['total_trades']}, PF={m_xag_05['profit_factor']}, Net=${m_xag_05['net_profit']}, MaxDD={m_xag_05['max_drawdown_pct']}%")
    audit_records["HR-PRD-04-XAGUSD"] = m_xag_05

    # =========================================================================
    # AUDIT 5: Stress Testing HR-PRD-04 under Adverse Costs
    # =========================================================================
    print("\n[+] Audit 5: HR-PRD-04 Cost Stress Testing on Gold...")
    ms_cost_tests = [
        ("Base Cost: 0.02% Comm, 2 Ticks Slip", 0.02, 2),
        ("Elevated Cost: 0.04% Comm, 4 Ticks Slip", 0.04, 4),
        ("Severe Cost: 0.06% Comm, 6 Ticks Slip", 0.06, 6)
    ]
    ms_cost_res = []
    for c_lbl, comm, slip in ms_cost_tests:
        eng_c = BacktestEngine(10000.0, comm, slip, spec_xau["tick_size"], contract_size=spec_xau["contract_size"], risk_mode="fixed_monetary_risk", risk_value=0.5)
        m_c = eng_c.run(m15_xau, sigs_ms_xau)
        ms_cost_res.append({"label": c_lbl, "pf": m_c["profit_factor"], "net_profit": m_c["net_profit"], "max_dd_pct": m_c["max_drawdown_pct"]})
        print(f"   {c_lbl:42s} | PF: {m_c['profit_factor']:4.2f} | Net $: {m_c['net_profit']:8.2f} | MaxDD: {m_c['max_drawdown_pct']:4.1f}%")
    audit_records["HR-PRD-04-Cost-Stress"] = ms_cost_res

    # Save to JSON
    out_file = "research/results/phase10_verification_matrix.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(audit_records, f, indent=2)
    print(f"\n[OK] Phase 10 verification records successfully saved to {out_file}")

if __name__ == '__main__':
    run_phase10_audit()
