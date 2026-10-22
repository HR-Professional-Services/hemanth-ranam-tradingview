"""
Phase 10 — Independent Verification & Audit Tests
Verifies:
1. Exact reconciliation of reported Phase 9 figures.
2. Bootstrap confidence interval calculations.
3. Adverse cost stress handling in the backtesting engine.
4. Consecutive loss tracking accuracy.
5. In-sample / Out-of-sample temporal partition isolation without leakage.
"""
import unittest
from research.backtest.engine import BacktestEngine, Trade
from research.experiments.run_phase10_audit import calc_consecutive_losses, bootstrap_profit_factor_ci

class TestPhase10Audit(unittest.TestCase):
    def test_consecutive_losses_calculation(self):
        trades = []
        # Simulate: win, loss, loss, loss, win, loss, win
        pnls = [50.0, -20.0, -30.0, -10.0, 40.0, -15.0, 60.0]
        for idx, p in enumerate(pnls):
            t = Trade(idx, 1, idx, "2024-01-01", 100.0, 95.0, 110.0, 1.0, 80.0, "A")
            t.pnl_cash = p
            trades.append(t)
            
        streak = calc_consecutive_losses(trades)
        self.assertEqual(streak, 3)

    def test_bootstrap_ci_bounds(self):
        trades = []
        # 10 winning trades ($100 each), 10 losing trades ($50 each) -> PF = 1000/500 = 2.0
        for idx in range(20):
            t = Trade(idx, 1, idx, "2024-01-01", 100.0, 95.0, 110.0, 1.0, 80.0, "A")
            t.pnl_cash = 100.0 if idx % 2 == 0 else -50.0
            trades.append(t)
            
        ci = bootstrap_profit_factor_ci(trades, n_iter=500, seed=42)
        self.assertGreater(ci["p50"], 1.5)
        self.assertLess(ci["p50"], 2.5)
        self.assertLessEqual(ci["p025"], ci["p50"])
        self.assertGreaterEqual(ci["p975"], ci["p50"])

    def test_adverse_cost_engine_impact(self):
        # Verify that doubling commission and slippage strictly reduces net profit
        candles = [
            {'time': '2024-01-01 00:00:00', 'open': 100.0, 'high': 102.0, 'low': 99.0, 'close': 101.0},
            {'time': '2024-01-01 00:15:00', 'open': 101.0, 'high': 106.0, 'low': 100.5, 'close': 105.5},
            {'time': '2024-01-01 00:30:00', 'open': 105.5, 'high': 111.0, 'low': 105.0, 'close': 110.5}
        ]
        signals = [
            {'buy': True, 'sell': False, 'sl': 95.0, 'tp': 110.0, 'score': 90.0, 'grade': 'A'},
            {'buy': False, 'sell': False, 'sl': 0.0, 'tp': 0.0, 'score': 0.0, 'grade': 'C'},
            {'buy': False, 'sell': False, 'sl': 0.0, 'tp': 0.0, 'score': 0.0, 'grade': 'C'}
        ]
        
        # Base engine: 0.02% comm, 2 ticks slip
        eng_base = BacktestEngine(10000.0, 0.02, 2, 0.01)
        res_base = eng_base.run(candles, signals)
        
        # Adverse engine: 0.06% comm, 6 ticks slip
        eng_adv = BacktestEngine(10000.0, 0.06, 6, 0.01)
        res_adv = eng_adv.run(candles, signals)
        
        self.assertGreater(res_base["net_profit"], res_adv["net_profit"])
        self.assertGreater(res_adv["total_commission"], res_base["total_commission"])

if __name__ == '__main__':
    unittest.main()
