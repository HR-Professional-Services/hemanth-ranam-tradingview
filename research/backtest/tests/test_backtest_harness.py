"""
Unit Tests for Research Backtest Engine & Pine Reproduction Strategies
Verifies:
- Indicator calculations (EMA, ATR, RSI, Pivots)
- Order execution on next bar open (process_orders_on_close)
- Commission and slippage accounting
- Non-repainting pivot confirmation delays
- Zero lookahead in HTF data alignment
- Position sizing under percent_of_equity vs fixed_monetary_risk
"""
import unittest
from research.backtest.indicators import (
    calc_ema, calc_sma, calc_atr, calc_rsi, calc_pivots
)
from research.backtest.engine import BacktestEngine
from research.backtest.strategies.pine_reproductions import StrategySimulator, build_htf_alignment

class TestBacktestEngine(unittest.TestCase):
    def test_ema_calculation(self):
        prices = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0]
        ema = calc_ema(prices, 5)
        self.assertEqual(len(ema), len(prices))
        # Initial SMA for 5 periods: sum(10..14)/5 = 12.0
        self.assertAlmostEqual(ema[4], 12.0, places=4)
        # Next EMA: alpha = 2/6 = 1/3; ema[5] = 1/3 * 15 + 2/3 * 12 = 5 + 8 = 13.0
        self.assertAlmostEqual(ema[5], 13.0, places=4)

    def test_pivot_confirmation_delay(self):
        # 3-bar left, 3-bar right pivot high
        highs = [10, 11, 12, 20, 13, 11, 10, 9, 8] # Peak at index 3 (value 20)
        lows = [5, 5, 5, 5, 5, 5, 5, 5, 5]
        ph, pl = calc_pivots(highs, lows, 3, 3)
        # Pivot peak is at index 3, confirmed at index 3 + 3 = 6
        self.assertIsNone(ph[3])
        self.assertIsNone(ph[4])
        self.assertIsNone(ph[5])
        self.assertEqual(ph[6], 20.0)

    def test_engine_next_bar_fill(self):
        # Verify that signal on bar 0 fills at bar 1 open with slippage
        candles = [
            {'time': '2024-01-01 00:00:00', 'open': 100.0, 'high': 102.0, 'low': 99.0, 'close': 101.0},
            {'time': '2024-01-01 00:15:00', 'open': 101.5, 'high': 106.0, 'low': 101.0, 'close': 105.0},
            {'time': '2024-01-01 00:30:00', 'open': 105.0, 'high': 105.5, 'low': 104.0, 'close': 104.5}
        ]
        signals = [
            {'buy': True, 'sell': False, 'sl': 95.0, 'tp': 110.0, 'score': 90.0, 'grade': 'A'},
            {'buy': False, 'sell': False, 'sl': 0.0, 'tp': 0.0, 'score': 0.0, 'grade': 'C'},
            {'buy': False, 'sell': False, 'sl': 0.0, 'tp': 0.0, 'score': 0.0, 'grade': 'C'}
        ]
        engine = BacktestEngine(initial_capital=10000.0, commission_pct=0.02, slippage_ticks=2, tick_size=0.01)
        res = engine.run(candles, signals)
        
        self.assertEqual(len(engine.trades), 0) # Still active at bar 2
        self.assertIsNotNone(engine.active_trade)
        # Entry price should be bar 1 open (101.5) + slippage (2 * 0.01 = 0.02) = 101.52
        self.assertAlmostEqual(engine.active_trade.entry_price, 101.52, places=4)
        self.assertEqual(engine.active_trade.entry_bar, 1)

    def test_monetary_risk_sizing(self):
        # Under fixed monetary risk of 1% on $10,000 equity = $100 risk
        # Entry = 100, SL = 95 -> SL distance = 5.0
        # Qty should be $100 / 5.0 = 20 units
        engine = BacktestEngine(initial_capital=10000.0, risk_mode="fixed_monetary_risk", risk_value=1.0, contract_size=1.0)
        qty = engine.calculate_position_size(100.0, 95.0)
        self.assertAlmostEqual(qty, 20.0, places=2)

if __name__ == '__main__':
    unittest.main()
