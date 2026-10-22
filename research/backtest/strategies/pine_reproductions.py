"""
HR TradingView Backtesting Framework — Faithful Reproduction of Commercial Strategies
Replicates exact signal logic from:
- HR_EMA_Pullback_Pro.pine
- HR_Liquidity_Sweep_Strategy.pine
- HR_Volatility_Breakout_Strategy.pine
- HR_Market_Structure_Strategy.pine
"""
from typing import List, Dict, Any, Optional
from research.backtest.indicators import (
    calc_ema, calc_sma, calc_atr, calc_rsi, calc_highest, calc_lowest, calc_pivots
)

def build_htf_alignment(m15_candles: List[Dict[str, Any]], h1_candles: List[Dict[str, Any]], htf_ema_len: int = 200) -> List[float]:
    """
    Implements Pine Script's request.security(syminfo.tickerid, "60", ta.ema(close, 200)[1], lookahead = barmerge.lookahead_off).
    Each M15 bar receives the 200 EMA of the CLOSED 1-hour bar prior to current bar.
    """
    h1_closes = [c['close'] for c in h1_candles]
    h1_emas = calc_ema(h1_closes, htf_ema_len)
    
    # Map H1 timestamps to closed EMA
    # An H1 bar at 10:00 closes at 11:00. So M15 bars between 11:00 and 11:45 see the 10:00 H1 EMA.
    h1_map = {}
    for i in range(len(h1_candles)):
        t_str = h1_candles[i]['time'] # "YYYY-MM-DD HH:MM:00"
        h1_map[t_str] = h1_emas[i]
        
    m15_htf_ema = [0.0] * len(m15_candles)
    last_known_ema = h1_emas[0] if h1_emas else 0.0
    
    for i, c in enumerate(m15_candles):
        # Look back for latest completed H1
        # In our data, H1 timestamps are HH:00:00.
        # An M15 bar at 14:15:00 has completed H1 at 13:00:00.
        cur_time = c['time']
        date_part, time_part = cur_time.split(' ')
        h, m, _ = time_part.split(':')
        
        # Closed H1 is hour - 1
        h_int = int(h)
        # Find the latest H1 bar strictly before current hour
        h1_target_hour = h_int if int(m) > 0 else (h_int - 1)
        target_str = f"{date_part} {h1_target_hour:02d}:00:00"
        
        if target_str in h1_map:
            last_known_ema = h1_map[target_str]
            
        m15_htf_ema[i] = last_known_ema
        
    return m15_htf_ema

class StrategySimulator:
    @staticmethod
    def simulate_ema_pullback(candles: List[Dict[str, Any]], h1_candles: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Reproduces HR_EMA_Pullback_Pro.pine
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
        
        ema9 = calc_ema(closes, fast_len)
        ema21 = calc_ema(closes, mid_len)
        ema200 = calc_ema(closes, slow_len)
        atr = calc_atr(highs, lows, closes, atr_len)
        htf_ema200 = build_htf_alignment(candles, h1_candles, 200)
        
        signals = [{'buy': False, 'sell': False, 'sl': 0.0, 'tp': 0.0, 'score': 0.0, 'grade': 'C'} for _ in range(n)]
        
        last_trade_bar = -100
        
        for i in range(slow_len + 1, n):
            c = closes[i]
            o = opens[i]
            h = highs[i]
            l = lows[i]
            cur_atr = max(atr[i], 0.001)
            
            can_trade = (i - last_trade_bar) >= cooldown_bars
            
            # Trend stacking
            bull_stack = (ema9[i] > ema21[i]) and (ema21[i] > ema200[i]) and (c > ema200[i])
            bear_stack = (ema9[i] < ema21[i]) and (ema21[i] < ema200[i]) and (c < ema200[i])
            
            # HTF filter
            htf_bull = c > htf_ema200[i]
            htf_bear = c < htf_ema200[i]
            
            # Pullback condition
            pull_buy = (l <= ema9[i] or l <= ema21[i]) and (c >= ema21[i])
            pull_sell = (h >= ema9[i] or h >= ema21[i]) and (c <= ema21[i])
            
            # Resumption candle confirmation: close in trend direction and close beyond previous bar extreme
            conf_buy = (c > o) and (c > highs[i - 1]) and (c > ema9[i])
            conf_sell = (c < o) and (c < lows[i - 1]) and (c < ema9[i])
            
            # Scoring
            score_buy = 50.0
            if bull_stack: score_buy += 25.0
            if htf_bull: score_buy += 25.0
            
            score_sell = 50.0
            if bear_stack: score_sell += 25.0
            if htf_bear: score_sell += 25.0
            
            if bull_stack and htf_bull and pull_buy and conf_buy and can_trade and score_buy >= min_score:
                entry = c
                sl = entry - (cur_atr * sl_atr_mult)
                risk = entry - sl
                tp = entry + (risk * tp_rr_mult)
                signals[i] = {'buy': True, 'sell': False, 'sl': sl, 'tp': tp, 'score': score_buy, 'grade': 'A'}
                last_trade_bar = i
            elif bear_stack and htf_bear and pull_sell and conf_sell and can_trade and score_sell >= min_score:
                entry = c
                sl = entry + (cur_atr * sl_atr_mult)
                risk = sl - entry
                tp = entry - (risk * tp_rr_mult)
                signals[i] = {'buy': False, 'sell': True, 'sl': sl, 'tp': tp, 'score': score_sell, 'grade': 'A'}
                last_trade_bar = i
                
        return signals

    @staticmethod
    def simulate_liquidity_sweep(candles: List[Dict[str, Any]], h1_candles: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Reproduces HR_Liquidity_Sweep_Strategy.pine
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
            
            # Bullish sweep of swing low
            sweep_low_depth = swing_low - l
            valid_bull_depth = (sweep_low_depth / cur_atr) >= min_sweep_atr
            bull_reclaim = c > swing_low
            bull_wick_ratio = (min(o, c) - l) / rng
            bull_displace = bull_wick_ratio >= 0.40
            
            # Bearish sweep of swing high
            sweep_high_depth = h - swing_high
            valid_bear_depth = (sweep_high_depth / cur_atr) >= min_sweep_atr
            bear_reclaim = c < swing_high
            bear_wick_ratio = (h - max(o, c)) / rng
            bear_displace = bear_wick_ratio >= 0.40
            
            if (l < swing_low) and bull_reclaim and valid_bull_depth and bull_displace and can_trade:
                entry = c
                sl = l - (cur_atr * sl_buffer_atr)
                risk = entry - sl
                tp = entry + (risk * rr_multiplier)
                signals[i] = {'buy': True, 'sell': False, 'sl': sl, 'tp': tp, 'score': 85.0, 'grade': 'A'}
                last_trade_bar = i
            elif (h > swing_high) and bear_reclaim and valid_bear_depth and bear_displace and can_trade:
                entry = c
                sl = h + (cur_atr * sl_buffer_atr)
                risk = sl - entry
                tp = entry - (risk * rr_multiplier)
                signals[i] = {'buy': False, 'sell': True, 'sl': sl, 'tp': tp, 'score': 85.0, 'grade': 'A'}
                last_trade_bar = i
                
        return signals

    @staticmethod
    def simulate_volatility_breakout(candles: List[Dict[str, Any]], h1_candles: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Reproduces HR_Volatility_Breakout_Strategy.pine
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
            vol_expanded = vols[i] >= (avg_vol[i] * 1.1)
            
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

    @staticmethod
    def simulate_market_structure(candles: List[Dict[str, Any]], h1_candles: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Reproduces HR_Market_Structure_Strategy.pine
        """
        n = len(candles)
        closes = [c['close'] for c in candles]
        opens = [c['open'] for c in candles]
        highs = [c['high'] for c in candles]
        lows = [c['low'] for c in candles]
        
        pivot_strength = params.get('pivot_strength', 3)
        lookback_window = params.get('lookback_window', 50)
        atr_len = params.get('atr_len', 14)
        bullish_rsi_min = params.get('bullish_rsi_min', 53.0)
        bearish_rsi_max = params.get('bearish_rsi_max', 47.0)
        rr_multiplier = params.get('rr_multiplier', 2.4)
        sl_buffer_atr = params.get('sl_buffer_atr', 0.30)
        cooldown_bars = params.get('cooldown_bars', 5)
        
        atr = calc_atr(highs, lows, closes, atr_len)
        rsi = calc_rsi(closes, 14)
        p_highs, p_lows = calc_pivots(highs, lows, pivot_strength, pivot_strength)
        htf_ema200 = build_htf_alignment(candles, h1_candles, 200)
        
        signals = [{'buy': False, 'sell': False, 'sl': 0.0, 'tp': 0.0, 'score': 0.0, 'grade': 'C'} for _ in range(n)]
        
        last_ph = None
        last_ph_bar = 0
        last_pl = None
        last_pl_bar = 0
        last_trade_bar = -100
        
        for i in range(50, n):
            c = closes[i]
            cur_atr = max(atr[i], 0.001)
            can_trade = (i - last_trade_bar) >= cooldown_bars
            
            if p_highs[i] is not None:
                last_ph = p_highs[i]
                last_ph_bar = i - pivot_strength
                
            if p_lows[i] is not None:
                last_pl = p_lows[i]
                last_pl_bar = i - pivot_strength
                
            ph_valid = (last_ph is not None) and (i - last_ph_bar <= lookback_window)
            pl_valid = (last_pl is not None) and (i - last_pl_bar <= lookback_window)
            
            bull_bos = ph_valid and (closes[i - 1] <= last_ph) and (c > last_ph) and (rsi[i] >= bullish_rsi_min) and (c > htf_ema200[i])
            bear_bos = pl_valid and (closes[i - 1] >= last_pl) and (c < last_pl) and (rsi[i] <= bearish_rsi_max) and (c < htf_ema200[i])
            
            if bull_bos and can_trade:
                entry = c
                sl = (last_pl if last_pl is not None else entry - cur_atr * 2.0) - (cur_atr * sl_buffer_atr)
                risk = entry - sl
                if risk > 0:
                    tp = entry + (risk * rr_multiplier)
                    signals[i] = {'buy': True, 'sell': False, 'sl': sl, 'tp': tp, 'score': 85.0, 'grade': 'A'}
                    last_trade_bar = i
            elif bear_bos and can_trade:
                entry = c
                sl = (last_ph if last_ph is not None else entry + cur_atr * 2.0) + (cur_atr * sl_buffer_atr)
                risk = sl - entry
                if risk > 0:
                    tp = entry - (risk * rr_multiplier)
                    signals[i] = {'buy': False, 'sell': True, 'sl': sl, 'tp': tp, 'score': 85.0, 'grade': 'A'}
                    last_trade_bar = i
                    
        return signals
