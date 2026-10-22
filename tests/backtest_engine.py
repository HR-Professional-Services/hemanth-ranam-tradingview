#!/usr/bin/env python3
"""
HEMANTH RANAM — QUANTITATIVE STRATEGY SIMULATION & ROBUSTNESS ENGINE
Executes multi-regime backtests for all 5 Pine Script v6 strategies:
1. EMA Pullback Pro
2. Breakout Retest Pro
3. Market Structure Pro
4. VWAP Mean Reversion Pro
5. Momentum Volatility Pro
"""

import math
import random
try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    np = None
    _HAS_NUMPY = False
from typing import Dict, List, Any, Tuple

class MarketDataGenerator:
    @staticmethod
    def generate_candles(regime: str = "trending_bull", length: int = 1000, seed: int = 42) -> List[Dict[str, float]]:
        if _HAS_NUMPY:
            np.random.seed(seed)
        else:
            random.seed(seed)
        candles = []
        price = 100.0 if "forex" in regime else 2000.0 # e.g. Gold/Index level
        
        for i in range(length):
            if regime == "trending_bull":
                drift = 0.0008
                volatility = 0.004
            elif regime == "trending_bear":
                drift = -0.0008
                volatility = 0.004
            elif regime == "ranging":
                drift = 0.001 * math.sin(i / 15.0)
                volatility = 0.003
            elif regime == "high_volatility":
                drift = 0.0002
                volatility = 0.012
            elif regime == "low_vol_chop":
                drift = 0.00005
                volatility = 0.0015
            else:
                drift = 0.0002
                volatility = 0.005

            if _HAS_NUMPY:
                norm1 = np.random.normal(0, volatility)
                norm2 = abs(np.random.normal(0, volatility * 0.5))
                norm3 = abs(np.random.normal(0, volatility * 0.5))
                vol = float(np.random.gamma(shape=2.0, scale=1000.0))
            else:
                norm1 = random.gauss(0, volatility)
                norm2 = abs(random.gauss(0, volatility * 0.5))
                norm3 = abs(random.gauss(0, volatility * 0.5))
                vol = float(random.gammavariate(2.0, 1000.0))

            ret = drift + norm1
            open_p = price
            close_p = price * (1.0 + ret)
            high_p = max(open_p, close_p) * (1.0 + norm2)
            low_p = min(open_p, close_p) * (1.0 - norm3)
            
            candles.append({
                "open": open_p,
                "high": high_p,
                "low": low_p,
                "close": close_p,
                "volume": vol
            })
            price = close_p
            
        return candles

class StrategyEvaluator:
    @staticmethod
    def calculate_ema(prices: List[float], length: int) -> List[float]:
        ema = []
        alpha = 2.0 / (length + 1)
        for i, p in enumerate(prices):
            if i == 0:
                ema.append(p)
            else:
                ema.append((p * alpha) + (ema[-1] * (1 - alpha)))
        return ema

    @staticmethod
    def calculate_atr(candles: List[Dict[str, float]], length: int = 14) -> List[float]:
        trs = []
        for i in range(len(candles)):
            if i == 0:
                trs.append(candles[i]["high"] - candles[i]["low"])
            else:
                h = candles[i]["high"]
                l = candles[i]["low"]
                c_prev = candles[i-1]["close"]
                tr = max(h - l, abs(h - c_prev), abs(l - c_prev))
                trs.append(tr)
        
        atr = []
        for i in range(len(trs)):
            if i < length:
                atr.append(sum(trs[:i+1]) / (i + 1))
            else:
                atr.append((atr[-1] * (length - 1) + trs[i]) / length)
        return atr

    @staticmethod
    def calculate_rsi(prices: List[float], length: int = 14) -> List[float]:
        gains, losses = [], []
        for i in range(1, len(prices)):
            chg = prices[i] - prices[i-1]
            gains.append(max(0.0, chg))
            losses.append(max(0.0, -chg))
        
        rsi = [50.0]
        avg_gain = sum(gains[:length]) / length if len(gains) >= length else 0.0
        avg_loss = sum(losses[:length]) / length if len(losses) >= length else 0.0
        
        for i in range(length, len(gains)):
            avg_gain = ((avg_gain * (length - 1)) + gains[i]) / length
            avg_loss = ((avg_loss * (length - 1)) + losses[i]) / length
            if avg_loss == 0:
                rsi.append(100.0)
            else:
                rs = avg_gain / avg_loss
                rsi.append(100.0 - (100.0 / (1.0 + rs)))
                
        while len(rsi) < len(prices):
            rsi.insert(0, 50.0)
        return rsi

    @staticmethod
    def run_strategy_backtest(candles: List[Dict[str, float]], strategy_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        closes = [c["close"] for c in candles]
        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]
        atr = StrategyEvaluator.calculate_atr(candles, params.get("atr_len", 14))
        
        trades = []
        position = None # {"dir": 1 or -1, "entry": float, "sl": float, "tp": float, "bar": int}
        last_trade_bar = -100
        cooldown = params.get("cooldown_bars", 5)
        
        # Precompute indicators
        ema9 = StrategyEvaluator.calculate_ema(closes, params.get("fast_len", 9))
        ema21 = StrategyEvaluator.calculate_ema(closes, params.get("mid_len", 21))
        ema200 = StrategyEvaluator.calculate_ema(closes, params.get("slow_len", 200))
        rsi = StrategyEvaluator.calculate_rsi(closes, params.get("rsi_len", 14))
        
        for i in range(50, len(candles)):
            c = candles[i]
            
            # 1. Manage Active Position Exits
            if position is not None:
                p_dir = position["dir"]
                p_entry = position["entry"]
                p_sl = position["sl"]
                p_tp = position["tp"]
                
                # Check for exit hit on high/low of current bar
                if p_dir == 1:
                    if c["low"] <= p_sl:
                        # SL hit
                        pnl_pct = (p_sl - p_entry) / p_entry
                        trades.append({"pnl_pct": pnl_pct, "win": False, "bars": i - position["bar"]})
                        position = None
                        last_trade_bar = i
                    elif c["high"] >= p_tp:
                        # TP hit
                        pnl_pct = (p_tp - p_entry) / p_entry
                        trades.append({"pnl_pct": pnl_pct, "win": True, "bars": i - position["bar"]})
                        position = None
                        last_trade_bar = i
                elif p_dir == -1:
                    if c["high"] >= p_sl:
                        # SL hit
                        pnl_pct = (p_entry - p_sl) / p_entry
                        trades.append({"pnl_pct": pnl_pct, "win": False, "bars": i - position["bar"]})
                        position = None
                        last_trade_bar = i
                    elif c["low"] <= p_tp:
                        # TP hit
                        pnl_pct = (p_entry - p_tp) / p_entry
                        trades.append({"pnl_pct": pnl_pct, "win": True, "bars": i - position["bar"]})
                        position = None
                        last_trade_bar = i
                continue

            # 2. Check New Entry Signals if No Position
            if (i - last_trade_bar) < cooldown:
                continue

            sig_dir = 0 # 1=Buy, -1=Sell
            
            if strategy_name == "EMA_Pullback":
                ema_bull = (ema9[i] > ema21[i]) and (ema21[i] > ema200[i]) and (closes[i] > ema200[i])
                ema_bear = (ema9[i] < ema21[i]) and (ema21[i] < ema200[i]) and (closes[i] < ema200[i])
                pullback_buy = (lows[i] <= ema9[i] or lows[i] <= ema21[i]) and (closes[i] >= ema21[i])
                pullback_sell = (highs[i] >= ema9[i] or highs[i] >= ema21[i]) and (closes[i] <= ema21[i])
                confirm_bull = (closes[i] > candles[i]["open"]) and (closes[i] > highs[i-1])
                confirm_bear = (closes[i] < candles[i]["open"]) and (closes[i] < lows[i-1])
                
                if ema_bull and pullback_buy and confirm_bull:
                    sig_dir = 1
                elif ema_bear and pullback_sell and confirm_bear:
                    sig_dir = -1

            elif strategy_name == "Breakout_Retest":
                lookback = params.get("range_len", 20)
                r_high = max(highs[i-lookback:i])
                r_low = min(lows[i-lookback:i])
                if closes[i] > r_high and closes[i] > ema200[i]:
                    sig_dir = 1
                elif closes[i] < r_low and closes[i] < ema200[i]:
                    sig_dir = -1

            elif strategy_name == "VWAP_Reversion":
                # Simulated VWAP using 20 SMA mean
                mean = sum(closes[i-20:i]) / 20.0
                stdev = float(np.std(closes[i-20:i]))
                upper = mean + (2.0 * stdev)
                lower = mean - (2.0 * stdev)
                
                if lows[i] <= lower and rsi[i] <= 30 and closes[i] > candles[i]["open"]:
                    sig_dir = 1
                elif highs[i] >= upper and rsi[i] >= 70 and closes[i] < candles[i]["open"]:
                    sig_dir = -1

            elif strategy_name == "Momentum_Squeeze":
                # Bollinger inside Keltner
                bb_std = float(np.std(closes[i-20:i]))
                bb_width = 4.0 * bb_std
                kc_width = 3.0 * atr[i]
                if (bb_width > kc_width) and ema9[i] > ema21[i] and closes[i] > ema200[i]:
                    sig_dir = 1
                elif (bb_width > kc_width) and ema9[i] < ema21[i] and closes[i] < ema200[i]:
                    sig_dir = -1

            elif strategy_name == "Market_Structure":
                if closes[i] > highs[i-5] and closes[i] > ema200[i]:
                    sig_dir = 1
                elif closes[i] < lows[i-5] and closes[i] < ema200[i]:
                    sig_dir = -1

            # Execute entry if signal triggered
            if sig_dir != 0:
                cur_atr = max(atr[i], 0.001)
                sl_mult = params.get("sl_atr_mult", 1.5)
                tp_mult = params.get("tp_rr_mult", 1.5)
                
                if sig_dir == 1:
                    entry = closes[i]
                    sl = entry - (cur_atr * sl_mult)
                    risk = entry - sl
                    tp = entry + (risk * tp_mult)
                    position = {"dir": 1, "entry": entry, "sl": sl, "tp": tp, "bar": i}
                else:
                    entry = closes[i]
                    sl = entry + (cur_atr * sl_mult)
                    risk = sl - entry
                    tp = entry - (risk * tp_mult)
                    position = {"dir": -1, "entry": entry, "sl": sl, "tp": tp, "bar": i}

        # Calculate Performance Metrics
        if not trades:
            return {
                "trades_count": 0,
                "win_rate_pct": 0.0,
                "profit_factor": 0.0,
                "net_profit_pct": 0.0,
                "max_drawdown_pct": 0.0,
                "expectancy_pct": 0.0,
                "avg_win_pct": 0.0,
                "avg_loss_pct": 0.0,
                "max_consecutive_losses": 0
            }

        wins = [t["pnl_pct"] for t in trades if t["win"]]
        losses = [abs(t["pnl_pct"]) for t in trades if not t["win"]]
        
        gross_profit = sum(wins)
        gross_loss = sum(losses)
        pf = (gross_profit / gross_loss) if gross_loss > 0 else (99.0 if gross_profit > 0 else 0.0)
        win_rate = (len(wins) / len(trades)) * 100.0
        net_profit = (gross_profit - gross_loss) * 100.0
        
        # Max Drawdown & Consecutive Losses
        equity_curve = [100.0]
        consec_losses, max_consec = 0, 0
        for t in trades:
            equity_curve.append(equity_curve[-1] * (1.0 + t["pnl_pct"]))
            if not t["win"]:
                consec_losses += 1
                max_consec = max(max_consec, consec_losses)
            else:
                consec_losses = 0
                
        peak = equity_curve[0]
        max_dd = 0.0
        for eq in equity_curve:
            if eq > peak: peak = eq
            dd = (peak - eq) / peak
            if dd > max_dd: max_dd = dd

        avg_win = (sum(wins) / len(wins) * 100.0) if wins else 0.0
        avg_loss = (sum(losses) / len(losses) * 100.0) if losses else 0.0
        expectancy = ((win_rate / 100.0) * avg_win) - (((100.0 - win_rate) / 100.0) * avg_loss)

        return {
            "trades_count": len(trades),
            "win_rate_pct": round(win_rate, 2),
            "profit_factor": round(pf, 2),
            "net_profit_pct": round(net_profit, 2),
            "max_drawdown_pct": round(max_dd * 100.0, 2),
            "expectancy_pct": round(expectancy, 3),
            "avg_win_pct": round(avg_win, 2),
            "avg_loss_pct": round(avg_loss, 2),
            "max_consecutive_losses": max_consec
        }

if __name__ == "__main__":
    strategies = [
        "EMA_Pullback",
        "Breakout_Retest",
        "Market_Structure",
        "VWAP_Reversion",
        "Momentum_Squeeze"
    ]
    regimes = ["trending_bull", "trending_bear", "ranging", "high_volatility", "low_vol_chop"]
    
    print("=" * 80)
    print("HEMANTH RANAM — QUANTITATIVE SIMULATION & MULTI-REGIME PERFORMANCE MATRIX")
    print("=" * 80)
    
    for strat in strategies:
        print(f"\n📊 Strategy: {strat}")
        print("-" * 75)
        print(f"{'Market Regime':<20} | {'Trades':<7} | {'Win %':<7} | {'PF':<6} | {'Net %':<8} | {'Max DD %':<9} | {'Expectancy'}")
        print("-" * 75)
        
        for regime in regimes:
            candles = MarketDataGenerator.generate_candles(regime, length=1200)
            res = StrategyEvaluator.run_strategy_backtest(candles, strat, {"atr_len": 14, "sl_atr_mult": 1.5, "tp_rr_mult": 1.5})
            print(f"{regime:<20} | {res['trades_count']:<7} | {res['win_rate_pct']:<6}% | {res['profit_factor']:<6} | {res['net_profit_pct']:<7}% | {res['max_drawdown_pct']:<8}% | {res['expectancy_pct']:+.3f}%")
