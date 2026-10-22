"""
HR TradingView — Experimental Candidates Engine (Phase 9)
Implements isolated candidate logic for:
- HR-PRD-01 Candidates: ADX Chop Filter (thresholds 18, 20, 22, 25) + ATR Stop Sensitivity (1.5, 1.75, 2.0 ATR)
- HR-PRD-02 Candidates: Directional Alignment with H1 200 EMA + Sweep Quality Filtering
- HR-PRD-03 Candidates: Controlled Squeeze Relaxation (1.8, 2.0, 2.2 ATR; 12, 16, 20 lookbacks)
- HR-PRD-04 Benchmark: Dynamic Stop-Based Position Sizing Validation
"""
from typing import List, Dict, Any, Optional
from research.backtest.indicators import (
     calc_ema, calc_sma, calc_atr, calc_rsi, calc_adx, calc_highest, calc_lowest, calc_pivots
)
from research.backtest.strategies.pine_reproductions import build_htf_alignment

class CandidateSimulator:
    @staticmethod
    def simulate_ema_pullback_candidate(candles: List[Dict[str, Any]], h1_candles: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        HR-PRD-01 Candidate with ADX Chop Filter and Configurable ATR Stop Multiplier.
        """
        n = len(candles)
        closes = [c['close'] for c in candles]
        opens = [c['open'] for c in candles]
        highs = [c['high'] for c in candles]
        lows = [c['low'] for c in candles]
        
        fast_len = params.get('fast_len', 9)
        mid_len = params.get('mid_len', 21)
        slow_len = params.get('slow_len', 200)
        atr_len = params.get('atr_len', 14)
        sl_atr_mult = params.get('sl_atr_mult', 1.5)
        tp_rr_mult = params.get('tp1_rr_mult', 1.5)
        cooldown_bars = params.get('cooldown_bars', 5)
        min_score = params.get('min_score', 70)
        use_adx = params.get('use_adx', False)
        adx_threshold = params.get('adx_threshold', 20.0)
        
        ema9 = calc_ema(closes, fast_len)
        ema21 = calc_ema(closes, mid_len)
        ema200 = calc_ema(closes, slow_len)
        atr = calc_atr(highs, lows, closes, atr_len)
        htf_ema200 = build_htf_alignment(candles, h1_candles, 200)
        adx = calc_adx(highs, lows, closes, 14, 14) if use_adx else None
        
        signals = [{'buy': False, 'sell': False, 'sl': 0.0, 'tp': 0.0, 'score': 0.0, 'grade': 'C'} for _ in range(n)]
        last_trade_bar = -100
        
        for i in range(slow_len + 1, n):
            c = closes[i]
            o = opens[i]
            h = highs[i]
            l = lows[i]
            cur_atr = max(atr[i], 0.001)
            
            can_trade = (i - last_trade_bar) >= cooldown_bars
            
            bull_stack = (ema9[i] > ema21[i]) and (ema21[i] > ema200[i]) and (c > ema200[i])
            bear_stack = (ema9[i] < ema21[i]) and (ema21[i] < ema200[i]) and (c < ema200[i])
            
            htf_bull = c > htf_ema200[i]
            htf_bear = c < htf_ema200[i]
            
            adx_ok = True if not use_adx else (adx[i] >= adx_threshold)
            
            pull_buy = (l <= ema9[i] or l <= ema21[i]) and (c >= ema21[i])
            pull_sell = (h >= ema9[i] or h >= ema21[i]) and (c <= ema21[i])
            
            conf_buy = (c > o) and (c > highs[i - 1]) and (c > ema9[i])
            conf_sell = (c < o) and (c < lows[i - 1]) and (c < ema9[i])
            
            score_buy = 50.0 + (25.0 if bull_stack else 0.0) + (25.0 if htf_bull else 0.0)
            score_sell = 50.0 + (25.0 if bear_stack else 0.0) + (25.0 if htf_bear else 0.0)
            
            if bull_stack and htf_bull and pull_buy and conf_buy and adx_ok and can_trade and score_buy >= min_score:
                entry = c
                sl = entry - (cur_atr * sl_atr_mult)
                risk = entry - sl
                tp = entry + (risk * tp_rr_mult)
                signals[i] = {'buy': True, 'sell': False, 'sl': sl, 'tp': tp, 'score': score_buy, 'grade': 'A'}
                last_trade_bar = i
            elif bear_stack and htf_bear and pull_sell and conf_sell and adx_ok and can_trade and score_sell >= min_score:
                entry = c
                sl = entry + (cur_atr * sl_atr_mult)
                risk = sl - entry
                tp = entry - (risk * tp_rr_mult)
                signals[i] = {'buy': False, 'sell': True, 'sl': sl, 'tp': tp, 'score': score_sell, 'grade': 'A'}
                last_trade_bar = i
                
        return signals

    @staticmethod
    def simulate_liquidity_sweep_candidate(candles: List[Dict[str, Any]], h1_candles: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        HR-PRD-02 Candidate with Pro-Trend Directional Alignment (H1 200 EMA).
        Bullish sweep only taken if HTF Trend is Bullish (close > htf_ema200).
        Bearish sweep only taken if HTF Trend is Bearish (close < htf_ema200).
        """
        n = len(candles)
        closes = [c['close'] for c in candles]
        opens = [c['open'] for c in candles]
        highs = [c['high'] for c in candles]
        lows = [c['low'] for c in candles]
        
        lookback = params.get('lookback_bars', 24)
        atr_len = params.get('atr_len', 14)
        min_sweep_atr = params.get('min_sweep_atr', 0.20)
        rr_multiplier = params.get('rr_multiplier', 2.5)
        sl_buffer_atr = params.get('sl_buffer_atr', 0.20)
        cooldown_bars = params.get('cooldown_bars', 5)
        enforce_htf_trend = params.get('enforce_htf_trend', True)
        
        atr = calc_atr(highs, lows, closes, atr_len)
        htf_ema200 = build_htf_alignment(candles, h1_candles, 200)
        
        signals = [{'buy': False, 'sell': False, 'sl': 0.0, 'tp': 0.0, 'score': 0.0, 'grade': 'C'} for _ in range(n)]
        last_trade_bar = -100
        
        for i in range(lookback + 1, n):
            c = closes[i]
            o = opens[i]
            h = highs[i]
            l = lows[i]
            cur_atr = max(atr[i], 0.001)
            rng = max(h - l, 0.0001)
            
            can_trade = (i - last_trade_bar) >= cooldown_bars
            
            swing_high = max(highs[i - lookback:i])
            swing_low = min(lows[i - lookback:i])
            
            # Directional HTF Trend condition
            htf_bull_ok = not enforce_htf_trend or (c > htf_ema200[i])
            htf_bear_ok = not enforce_htf_trend or (c < htf_ema200[i])
            
            sweep_low_depth = swing_low - l
            valid_bull_depth = (sweep_low_depth / cur_atr) >= min_sweep_atr
            bull_reclaim = c > swing_low
            bull_wick_ratio = (min(o, c) - l) / rng
            bull_displace = bull_wick_ratio >= 0.40
            
            sweep_high_depth = h - swing_high
            valid_bear_depth = (sweep_high_depth / cur_atr) >= min_sweep_atr
            bear_reclaim = c < swing_high
            bear_wick_ratio = (h - max(o, c)) / rng
            bear_displace = bear_wick_ratio >= 0.40
            
            if (l < swing_low) and bull_reclaim and valid_bull_depth and bull_displace and htf_bull_ok and can_trade:
                entry = c
                sl = l - (cur_atr * sl_buffer_atr)
                risk = entry - sl
                tp = entry + (risk * rr_multiplier)
                signals[i] = {'buy': True, 'sell': False, 'sl': sl, 'tp': tp, 'score': 85.0, 'grade': 'A'}
                last_trade_bar = i
            elif (h > swing_high) and bear_reclaim and valid_bear_depth and bear_displace and htf_bear_ok and can_trade:
                entry = c
                sl = h + (cur_atr * sl_buffer_atr)
                risk = sl - entry
                tp = entry - (risk * rr_multiplier)
                signals[i] = {'buy': False, 'sell': True, 'sl': sl, 'tp': tp, 'score': 85.0, 'grade': 'A'}
                last_trade_bar = i
                
        return signals

    @staticmethod
    def simulate_volatility_breakout_candidate(candles: List[Dict[str, Any]], h1_candles: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        HR-PRD-03 Candidate with Controlled Squeeze Relaxation.
        """
        n = len(candles)
        closes = [c['close'] for c in candles]
        opens = [c['open'] for c in candles]
        highs = [c['high'] for c in candles]
        lows = [c['low'] for c in candles]
        vols = [c.get('vol', 1.0) for c in candles]
        
        box_lookback = params.get('box_lookback', 20)
        atr_len = params.get('atr_len', 14)
        squeeze_threshold = params.get('squeeze_threshold', 1.80)
        require_volume = params.get('require_volume', True)
        volume_mult = params.get('volume_mult', 1.1)
        rr_multiplier = params.get('rr_multiplier', 2.5)
        sl_buffer_atr = params.get('sl_buffer_atr', 0.20)
        cooldown_bars = params.get('cooldown_bars', 5)
        
        atr = calc_atr(highs, lows, closes, atr_len)
        avg_vol = calc_sma(vols, box_lookback)
        htf_ema200 = build_htf_alignment(candles, h1_candles, 200)
        
        signals = [{'buy': False, 'sell': False, 'sl': 0.0, 'tp': 0.0, 'score': 0.0, 'grade': 'C'} for _ in range(n)]
        last_trade_bar = -100
        
        for i in range(box_lookback + 1, n):
            c = closes[i]
            o = opens[i]
            h = highs[i]
            l = lows[i]
            cur_atr = max(atr[i], 0.001)
            
            can_trade = (i - last_trade_bar) >= cooldown_bars
            
            box_high = max(highs[i - box_lookback:i])
            box_low = min(lows[i - box_lookback:i])
            box_range = box_high - box_low
            box_mid = (box_high + box_low) / 2.0
            
            is_compressed = (box_range / cur_atr) <= squeeze_threshold
            vol_expanded = not require_volume or (vols[i] >= (avg_vol[i] * volume_mult))
            
            bull_breakout = (c > box_high) and (c > o) and is_compressed and vol_expanded and (c > htf_ema200[i])
            bear_breakout = (c < box_low) and (c < o) and is_compressed and vol_expanded and (c < htf_ema200[i])
            
            if bull_breakout and can_trade:
                entry = c
                sl = box_mid - (cur_atr * sl_buffer_atr)
                risk = entry - sl
                tp = entry + (risk * rr_multiplier)
                signals[i] = {'buy': True, 'sell': False, 'sl': sl, 'tp': tp, 'score': 80.0, 'grade': 'A'}
                last_trade_bar = i
            elif bear_breakout and can_trade:
                entry = c
                sl = box_mid + (cur_atr * sl_buffer_atr)
                risk = sl - entry
                tp = entry - (risk * rr_multiplier)
                signals[i] = {'buy': False, 'sell': True, 'sl': sl, 'tp': tp, 'score': 80.0, 'grade': 'A'}
                last_trade_bar = i
                
        return signals
