"""
HR TradingView Backtesting Framework — Core Math & Indicators
Reproduces Pine Script v6 technical indicators with exact numerical parity.
"""
import math
from typing import List, Dict, Any, Tuple

def calc_ema(series: List[float], length: int) -> List[float]:
    """
    Pine Script ta.ema(source, length)
    First value is SMA(length), or simple recurrence with alpha = 2 / (length + 1)
    In Pine Script:
    alpha = 2 / (length + 1)
    ema := na(ema[1]) ? sma(source, length) : alpha * source + (1 - alpha) * ema[1]
    """
    n = len(series)
    ema = [0.0] * n
    alpha = 2.0 / (length + 1.0)
    
    if n == 0:
        return ema
    
    # Calculate initial SMA for first value
    if n >= length:
        sma_init = sum(series[:length]) / length
        for i in range(length - 1):
            ema[i] = series[i]
        ema[length - 1] = sma_init
        for i in range(length, n):
            ema[i] = alpha * series[i] + (1.0 - alpha) * ema[i - 1]
    else:
        ema[0] = series[0]
        for i in range(1, n):
            ema[i] = alpha * series[i] + (1.0 - alpha) * ema[i - 1]
            
    return ema

def calc_sma(series: List[float], length: int) -> List[float]:
    """Pine Script ta.sma(source, length)"""
    n = len(series)
    sma = [0.0] * n
    current_sum = 0.0
    for i in range(n):
        current_sum += series[i]
        if i >= length:
            current_sum -= series[i - length]
            sma[i] = current_sum / length
        elif i == length - 1:
            sma[i] = current_sum / length
        else:
            sma[i] = current_sum / (i + 1)
    return sma

def calc_atr(highs: List[float], lows: List[float], closes: List[float], length: int = 14) -> List[float]:
    """
    Pine Script ta.atr(length)
    RMA of True Range:
    tr = max(high - low, abs(high - close[1]), abs(low - close[1]))
    rma(tr, length): alpha = 1 / length
    """
    n = len(closes)
    trs = [0.0] * n
    if n == 0:
        return trs
    
    trs[0] = highs[0] - lows[0]
    for i in range(1, n):
        h = highs[i]
        l = lows[i]
        cp = closes[i - 1]
        trs[i] = max(h - l, abs(h - cp), abs(l - cp))
        
    atr = [0.0] * n
    alpha = 1.0 / length
    
    if n >= length:
        atr[length - 1] = sum(trs[:length]) / length
        for i in range(length):
            if i < length - 1:
                atr[i] = trs[i]
        for i in range(length, n):
            atr[i] = alpha * trs[i] + (1.0 - alpha) * atr[i - 1]
    else:
        atr[0] = trs[0]
        for i in range(1, n):
            atr[i] = alpha * trs[i] + (1.0 - alpha) * atr[i - 1]
            
    return atr

def calc_rsi(closes: List[float], length: int = 14) -> List[float]:
    """
    Pine Script ta.rsi(source, length)
    Uses RMA of gains and losses.
    """
    n = len(closes)
    rsi = [50.0] * n
    if n <= length:
        return rsi
        
    gains = [0.0] * n
    losses = [0.0] * n
    for i in range(1, n):
        diff = closes[i] - closes[i - 1]
        if diff > 0:
            gains[i] = diff
        else:
            losses[i] = -diff
            
    alpha = 1.0 / length
    avg_gain = sum(gains[1:length + 1]) / length
    avg_loss = sum(losses[1:length + 1]) / length
    
    if avg_loss == 0.0:
        rsi[length] = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi[length] = 100.0 - (100.0 / (1.0 + rs))
        
    for i in range(length + 1, n):
        avg_gain = alpha * gains[i] + (1.0 - alpha) * avg_gain
        avg_loss = alpha * losses[i] + (1.0 - alpha) * avg_loss
        if avg_loss == 0.0:
            rsi[i] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi[i] = 100.0 - (100.0 / (1.0 + rs))
            
    return rsi

def calc_adx(highs: List[float], lows: List[float], closes: List[float], di_len: int = 14, adx_len: int = 14) -> List[float]:
    """
    Pine Script ta.dmi(di_len, adx_len) -> [plus_di, minus_di, adx]
    Calculates ADX using RMA of True Range and Directional Movements.
    """
    n = len(closes)
    adx = [0.0] * n
    if n <= di_len + adx_len:
        return adx
        
    plus_dm = [0.0] * n
    minus_dm = [0.0] * n
    tr = [0.0] * n
    
    tr[0] = highs[0] - lows[0]
    for i in range(1, n):
        h = highs[i]
        l = lows[i]
        cp = closes[i - 1]
        tr[i] = max(h - l, abs(h - cp), abs(l - cp))
        
        up = h - highs[i - 1]
        down = lows[i - 1] - l
        
        if up > down and up > 0:
            plus_dm[i] = up
        else:
            plus_dm[i] = 0.0
            
        if down > up and down > 0:
            minus_dm[i] = down
        else:
            minus_dm[i] = 0.0
            
    # RMA function for series
    def rma(series, length):
        out = [0.0] * len(series)
        alpha = 1.0 / length
        if len(series) >= length:
            out[length - 1] = sum(series[:length]) / length
            for k in range(length):
                if k < length - 1:
                    out[k] = series[k]
            for k in range(length, len(series)):
                out[k] = alpha * series[k] + (1.0 - alpha) * out[k - 1]
        return out
        
    smooth_tr = rma(tr, di_len)
    smooth_pdm = rma(plus_dm, di_len)
    smooth_mdm = rma(minus_dm, di_len)
    
    dx = [0.0] * n
    for i in range(di_len, n):
        str_val = smooth_tr[i]
        if str_val > 0:
            p_di = 100.0 * (smooth_pdm[i] / str_val)
            m_di = 100.0 * (smooth_mdm[i] / str_val)
            di_sum = p_di + m_di
            if di_sum > 0:
                dx[i] = 100.0 * (abs(p_di - m_di) / di_sum)
                
    smooth_adx = rma(dx, adx_len)
    return smooth_adx

def calc_highest(series: List[float], length: int) -> List[float]:
    """Pine Script ta.highest(source, length)"""
    n = len(series)
    res = [0.0] * n
    for i in range(n):
        start = max(0, i - length + 1)
        res[i] = max(series[start:i + 1])
    return res

def calc_lowest(series: List[float], length: int) -> List[float]:
    """Pine Script ta.lowest(source, length)"""
    n = len(series)
    res = [0.0] * n
    for i in range(n):
        start = max(0, i - length + 1)
        res[i] = min(series[start:i + 1])
    return res

def calc_pivots(highs: List[float], lows: List[float], left: int = 3, right: int = 3) -> Tuple[List[float], List[float]]:
    """
    Pine Script ta.pivothigh(high, left, right) and ta.pivotlow(low, left, right)
    Returns list where value is populated on bar index when confirmed (i.e. at index pivot_bar + right).
    Value is na (None) otherwise.
    """
    n = len(highs)
    p_highs = [None] * n
    p_lows = [None] * n
    
    span = left + right + 1
    for i in range(left + right, n):
        pivot_idx = i - right
        val_h = highs[pivot_idx]
        val_l = lows[pivot_idx]
        
        # Check high
        is_high = True
        for k in range(i - span + 1, i + 1):
            if k != pivot_idx and highs[k] >= val_h:
                is_high = False
                break
        if is_high:
            p_highs[i] = val_h
            
        # Check low
        is_low = True
        for k in range(i - span + 1, i + 1):
            if k != pivot_idx and lows[k] <= val_l:
                is_low = False
                break
        if is_low:
            p_lows[i] = val_l
            
    return p_highs, p_lows
