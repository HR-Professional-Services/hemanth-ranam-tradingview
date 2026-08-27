#!/usr/bin/env python3
"""
Test suite validating Pine Script v5 syntax patterns, alert contracts, and strategy definitions.
"""

import unittest
import re
import os

class TestPineScriptIntegrity(unittest.TestCase):
    def setUp(self):
        self.pine_file = os.path.join(os.path.dirname(__file__), "..", "src", "HemanthRanamTradingSystem.pine")
        with open(self.pine_file, "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_pine_version_is_v5(self):
        """Must use modern Pine Script version 5."""
        self.assertTrue(self.content.startswith("//@version=5"), "Pine Script must specify //@version=5")

    def test_all_five_strategies_present(self):
        """Verifies presence of all 5 strategy frameworks."""
        strategies = [
            "EMA Pullback",
            "Breakout + Retest",
            "Market Structure",
            "VWAP Mean Reversion",
            "Momentum Expansion"
        ]
        for s in strategies:
            self.assertIn(s, self.content, f"Strategy {s} missing from Pine script")

    def test_webhook_alert_json_structure(self):
        """Verifies standardized JSON alert payload format."""
        self.assertIn('"brand":"Hemanth Ranam"', self.content)
        self.assertIn('"strategy":', self.content)
        self.assertIn('"symbol":', self.content)
        self.assertIn('"signal":', self.content)
        self.assertIn('"stop_loss":', self.content)
        self.assertIn('"take_profit_1":', self.content)

if __name__ == "__main__":
    unittest.main()
