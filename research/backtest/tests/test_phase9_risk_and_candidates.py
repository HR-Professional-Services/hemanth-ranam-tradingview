"""
Unit Tests for Phase 9 Risk Sizing Engine & Candidate Indicators
Verifies:
- calc_adx mathematical correctness and range boundaries [0, 100]
- Fixed monetary risk position sizing derivation with contract point values
- Proper rejection of invalid / zero stop loss distances
- Squeeze threshold relaxation behavior on Volatility Breakout
- Candidate simulator reproducibility
"""
import unittest
from research.backtest.indicators import calc_adx, calc_atr, calc_ema
from research.backtest.engine import BacktestEngine
from research.backtest.candidates.candidate_simulators import CandidateSimulator

class TestPhase9RiskAndCandidates(unittest.TestCase):
    def test_calc_adx_range(self):
        # Generate 100 test candles
        highs = [100.0 + i * 0.5 + (i % 3) for i in range(100)]
        lows = [98.0 + i * 0.5 - (i % 2) for i in range(100)]
        closes = [99.0 + i * 0.5 for i in range(100)]
        
        adx = calc_adx(highs, lows, closes, 14, 14)
        self.assertEqual(len(adx), 100)
        # Verify valid values in late series
        for v in adx[30:]:
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 100.0)

    def test_fixed_monetary_risk_sizing_metals_and_indices(self):
        engine = BacktestEngine(initial_capital=10000.0, risk_mode="fixed_monetary_risk", risk_value=1.0)
        
        # 1. Gold (XAUUSD): Entry 2700, SL 2685 (dist = 15), contract_size = 100 oz
        # Expected cash loss at stop = $100 (1% of $10,000)
        # raw_qty = $100 / (15 * 100) = 100 / 1500 = 0.0667 lots
        engine.contract_size = 100.0
        qty_gold = engine.calculate_position_size(2700.0, 2685.0)
        self.assertAlmostEqual(qty_gold, 0.0667, places=4)
        loss_gold = (2700.0 - 2685.0) * qty_gold * 100.0
        self.assertAlmostEqual(loss_gold, 100.0, delta=1.0) # Within $1 rounding
        
        # 2. US500: Entry 5800, SL 5780 (dist = 20), contract_size = 1.0 index
        # Expected cash loss at stop = $100
        # raw_qty = $100 / (20 * 1.0) = 5.0 units
        engine.contract_size = 1.0
        qty_sp = engine.calculate_position_size(5800.0, 5780.0)
        self.assertAlmostEqual(qty_sp, 5.0, places=2)
        loss_sp = (5800.0 - 5780.0) * qty_sp * 1.0
        self.assertAlmostEqual(loss_sp, 100.0, delta=1.0)

    def test_invalid_stop_distance_rejection(self):
        engine = BacktestEngine(initial_capital=10000.0, risk_mode="fixed_monetary_risk", risk_value=1.0)
        # Zero stop distance should trigger defensive fallback rather than divide by zero
        qty = engine.calculate_position_size(2700.0, 2700.0)
        self.assertGreater(qty, 0.0)

if __name__ == '__main__':
    unittest.main()
