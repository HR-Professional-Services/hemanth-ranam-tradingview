#!/usr/bin/env python3
"""
HEMANTH RANAM — TRADINGVIEW PINE SCRIPT V6 COMPREHENSIVE VALIDATION SUITE
Verifies:
1. Presence of all 5 independent strategy files.
2. Compliance with Pine Script v6 (//@version=6).
3. Backtestable strategy() declaration with risk & capital properties.
4. Non-repainting request.security parameters.
5. Standardized Webhook Alert JSON schema.
6. Full documentation integrity.
"""

import unittest
import os
import json
import glob

class TestTradingViewSuiteV6(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.strat_dir = os.path.join(self.root_dir, "src", "strategies")
        self.docs_dir = os.path.join(self.root_dir, "docs")
        
        self.expected_strategies = [
            "HR_EMA_Pullback_Pro.pine",
            "HR_Breakout_Retest_Pro.pine",
            "HR_Market_Structure_Pro.pine",
            "HR_VWAP_Mean_Reversion_Pro.pine",
            "HR_Momentum_Volatility_Pro.pine"
        ]

    def test_all_five_strategies_exist(self):
        """All 5 primary strategy files must exist in src/strategies/."""
        for strat in self.expected_strategies:
            strat_path = os.path.join(self.strat_dir, strat)
            self.assertTrue(os.path.exists(strat_path), f"Missing strategy file: {strat}")

    def test_pine_script_v6_version_declaration(self):
        """Every strategy file must strictly declare //@version=6."""
        for strat in self.expected_strategies:
            strat_path = os.path.join(self.strat_dir, strat)
            with open(strat_path, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                self.assertEqual(first_line, "//@version=6", f"{strat} must start with //@version=6")

    def test_strategy_declaration_present(self):
        """Every strategy file must use strategy(...) for native backtesting."""
        for strat in self.expected_strategies:
            strat_path = os.path.join(self.strat_dir, strat)
            with open(strat_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("strategy(", content, f"{strat} must declare strategy()")
                self.assertIn("strategy.entry(", content, f"{strat} must implement strategy.entry()")
                self.assertIn("strategy.exit(", content, f"{strat} must implement strategy.exit()")

    def test_non_repainting_security_calls(self):
        """If request.security is called, it must enforce barmerge.lookahead_off."""
        for strat in self.expected_strategies:
            strat_path = os.path.join(self.strat_dir, strat)
            with open(strat_path, "r", encoding="utf-8") as f:
                content = f.read()
                if "request.security(" in content:
                    self.assertIn("barmerge.lookahead_off", content, f"{strat} request.security must enforce lookahead_off")

    def test_webhook_alert_json_contract(self):
        """Every strategy must emit standardized JSON alerts."""
        for strat in self.expected_strategies:
            strat_path = os.path.join(self.strat_dir, strat)
            with open(strat_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("alert(", content, f"{strat} must contain alert() function calls")
                self.assertIn('"brand":"Hemanth Ranam"', content, f"{strat} alert payload must include brand")
                self.assertIn('"stop_loss":', content, f"{strat} alert payload must include stop_loss")
                self.assertIn('"take_profit_1":', content, f"{strat} alert payload must include take_profit_1")

    def test_documentation_files_exist(self):
        """All expected documentation manuals must exist."""
        required_docs = [
            "EMA-PULLBACK.md",
            "BREAKOUT-RETEST.md",
            "MARKET-STRUCTURE.md",
            "VWAP-MEAN-REVERSION.md",
            "MOMENTUM-VOLATILITY.md",
            "GETTING-STARTED.md",
            "STRATEGY-COMPARISON.md",
            "ALERTS.md",
            "BACKTESTING.md",
            "RISK-MANAGEMENT.md",
            "TROUBLESHOOTING.md"
        ]
        for doc in required_docs:
            doc_path = os.path.join(self.docs_dir, doc)
            self.assertTrue(os.path.exists(doc_path), f"Missing documentation file: {doc}")

    def test_audit_and_readme_exist(self):
        """AUDIT.md, BACKTEST-REPORT.md, and README.md must exist."""
        self.assertTrue(os.path.exists(os.path.join(self.root_dir, "AUDIT.md")))
        self.assertTrue(os.path.exists(os.path.join(self.root_dir, "BACKTEST-REPORT.md")))
        self.assertTrue(os.path.exists(os.path.join(self.root_dir, "PERFORMANCE-AUDIT.md")))
        self.assertTrue(os.path.exists(os.path.join(self.root_dir, "README.md")))
        self.assertTrue(os.path.exists(os.path.join(self.root_dir, "CHANGELOG.md")))

    def test_backtest_simulation_engine(self):
        """Validates quantitative backtest simulation engine runs cleanly."""
        from tests.backtest_engine import MarketDataGenerator, StrategyEvaluator
        candles = MarketDataGenerator.generate_candles("trending_bull", length=100)
        res = StrategyEvaluator.run_strategy_backtest(candles, "EMA_Pullback", {"atr_len": 14, "sl_atr_mult": 1.5, "tp_rr_mult": 1.5})
        self.assertIn("win_rate_pct", res)
        self.assertIn("profit_factor", res)

if __name__ == "__main__":
    unittest.main()

