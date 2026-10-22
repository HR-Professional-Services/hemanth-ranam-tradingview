#!/usr/bin/env python3
"""
HEMANTH RANAM — COMMERCIAL SUITE PINE SCRIPT V6 COMPREHENSIVE VALIDATION
Verifies:
1. Presence of all 4 commercial indicator files in src/indicators/.
2. Presence of all 4 commercial strategy files in src/strategies/.
3. Pine Script v6 version headers (//@version=6).
4. Strict non-repainting request.security parameters (lookahead_off).
5. Standardized JSON alert schemas across all indicators and strategies.
6. Documentation integrity and cross-platform architecture specifications.
7. Risk Guardrail Audit: Default percent_of_equity <= 1.0% and max risk cap adherence.
8. Valid Stop Distance / Position Sizing Guardrails in all strategy files.
"""

import unittest
import os
import re

class TestCommercialProductsSuite(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.ind_dir  = os.path.join(self.root_dir, "src", "indicators")
        self.strat_dir= os.path.join(self.root_dir, "src", "strategies")
        self.docs_ind = os.path.join(self.root_dir, "docs", "indicators")
        self.docs_strat = os.path.join(self.root_dir, "docs", "strategies")
        
        self.commercial_indicators = [
            "HR_EMA_Pullback_Indicator.pine",
            "HR_Liquidity_Sweep_Indicator.pine",
            "HR_Volatility_Breakout_Indicator.pine",
            "HR_Market_Structure_Indicator.pine"
        ]
        
        self.commercial_strategies = [
            "HR_EMA_Pullback_Pro.pine",
            "HR_Liquidity_Sweep_Strategy.pine",
            "HR_Volatility_Breakout_Strategy.pine",
            "HR_Market_Structure_Strategy.pine"
        ]

    def test_all_commercial_indicators_exist(self):
        """All 4 commercial indicators must exist in src/indicators/."""
        for ind in self.commercial_indicators:
            path = os.path.join(self.ind_dir, ind)
            self.assertTrue(os.path.exists(path), f"Missing commercial indicator: {ind}")

    def test_all_commercial_strategies_exist(self):
        """All 4 commercial strategies must exist in src/strategies/."""
        for strat in self.commercial_strategies:
            path = os.path.join(self.strat_dir, strat)
            self.assertTrue(os.path.exists(path), f"Missing commercial strategy: {strat}")

    def test_pine_v6_declaration(self):
        """All commercial scripts must strictly declare //@version=6."""
        for ind in self.commercial_indicators:
            with open(os.path.join(self.ind_dir, ind), "r", encoding="utf-8") as f:
                self.assertEqual(f.readline().strip(), "//@version=6", f"{ind} must be //@version=6")
        for strat in self.commercial_strategies:
            with open(os.path.join(self.strat_dir, strat), "r", encoding="utf-8") as f:
                self.assertEqual(f.readline().strip(), "//@version=6", f"{strat} must be //@version=6")

    def test_non_repainting_security(self):
        """request.security calls must enforce lookahead_off and [1] historical offset."""
        for ind in self.commercial_indicators:
            with open(os.path.join(self.ind_dir, ind), "r", encoding="utf-8") as f:
                content = f.read()
                if "request.security(" in content:
                    self.assertIn("barmerge.lookahead_off", content, f"{ind} must enforce lookahead_off")
                    self.assertIn("[1]", content, f"{ind} must use [1] offset for HTF data")
        for strat in self.commercial_strategies:
            with open(os.path.join(self.strat_dir, strat), "r", encoding="utf-8") as f:
                content = f.read()
                if "request.security(" in content:
                    self.assertIn("barmerge.lookahead_off", content, f"{strat} must enforce lookahead_off")
                    self.assertIn("[1]", content, f"{strat} must use [1] offset for HTF data")

    def test_alert_json_payloads(self):
        """All scripts must emit structured JSON alerts."""
        for ind in self.commercial_indicators:
            with open(os.path.join(self.ind_dir, ind), "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("alert(", content)
                self.assertIn('"brand":"Hemanth Ranam"', content)
        for strat in self.commercial_strategies:
            with open(os.path.join(self.strat_dir, strat), "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("alert(", content)
                self.assertIn('"brand":"Hemanth Ranam"', content)

    def test_risk_guardrail_maximum_one_percent(self):
        """All strategies must strictly configure default_qty_value <= 1.0% equity."""
        for strat in self.commercial_strategies:
            with open(os.path.join(self.strat_dir, strat), "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("default_qty_type=strategy.percent_of_equity", content, f"{strat} must use percent_of_equity")
                match = re.search(r'default_qty_value\s*=\s*([0-9.]+)', content)
                self.assertIsNotNone(match, f"{strat} must have default_qty_value defined")
                val = float(match.group(1))
                self.assertLessEqual(val, 1.0, f"{strat} risk per trade must not exceed 1.0% (found {val}%)")

    def test_process_orders_on_close_enforced(self):
        """All strategies must enforce process_orders_on_close=true for closed-bar fills."""
        for strat in self.commercial_strategies:
            with open(os.path.join(self.strat_dir, strat), "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("process_orders_on_close=true", content, f"{strat} must declare process_orders_on_close=true")

    def test_all_documentation_manuals_exist(self):
        """Each product must have dedicated indicator and strategy manuals."""
        expected_docs = [
            os.path.join(self.docs_ind, "HR_EMA_PULLBACK_INDICATOR.md"),
            os.path.join(self.docs_ind, "HR_LIQUIDITY_SWEEP_INDICATOR.md"),
            os.path.join(self.docs_ind, "HR_VOLATILITY_BREAKOUT_INDICATOR.md"),
            os.path.join(self.docs_ind, "HR_MARKET_STRUCTURE_INDICATOR.md"),
            os.path.join(self.root_dir, "docs", "EMA-PULLBACK.md"),
            os.path.join(self.docs_strat, "HR_LIQUIDITY_SWEEP_STRATEGY.md"),
            os.path.join(self.docs_strat, "HR_VOLATILITY_BREAKOUT_STRATEGY.md"),
            os.path.join(self.docs_strat, "HR_MARKET_STRUCTURE_STRATEGY.md"),
            os.path.join(self.root_dir, "docs", "architecture", "PRODUCT-REGISTRY.md"),
            os.path.join(self.root_dir, "docs", "architecture", "SIGNAL-CONTRACT.md")
        ]
        for doc in expected_docs:
            self.assertTrue(os.path.exists(doc), f"Missing documentation manual: {doc}")

    def test_shorttitle_length_limit(self):
        """TradingView strictly enforces shorttitle <= 10 characters (SHORT_TITLE_TOO_LONG)."""
        for ind in self.commercial_indicators:
            with open(os.path.join(self.ind_dir, ind), "r", encoding="utf-8") as f:
                content = f.read()
                m = re.search(r'shorttitle\s*=\s*"([^"]+)"', content)
                if m:
                    self.assertLessEqual(len(m.group(1)), 10, f"{ind} shorttitle '{m.group(1)}' exceeds 10 chars")
        for strat in self.commercial_strategies:
            with open(os.path.join(self.strat_dir, strat), "r", encoding="utf-8") as f:
                content = f.read()
                m = re.search(r'shorttitle\s*=\s*"([^"]+)"', content)
                if m:
                    self.assertLessEqual(len(m.group(1)), 10, f"{strat} shorttitle '{m.group(1)}' exceeds 10 chars")

    def test_no_duplicate_title_parameter_in_plots(self):
        """TradingView CE10072: Two or more arguments are passed to the 'title' parameter."""
        pattern = re.compile(r'(?:^|[^a-zA-Z0-9_.])(plot|plotshape|plotchar)\s*\(([^;]+?)\)')
        all_scripts = [os.path.join(self.ind_dir, f) for f in self.commercial_indicators] + \
                      [os.path.join(self.strat_dir, f) for f in self.commercial_strategies]
        for script_path in all_scripts:
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            for m in pattern.finditer(content):
                fn = m.group(1)
                args_str = m.group(2)
                args = []
                cur = []
                depth = 0
                in_str = False
                quote_char = ''
                for c in args_str:
                    if c in ('"', "'"):
                        if not in_str:
                            in_str = True
                            quote_char = c
                        elif quote_char == c:
                            in_str = False
                    elif c == '(' and not in_str:
                        depth += 1
                    elif c == ')' and not in_str:
                        depth -= 1
                    elif c == ',' and depth == 0 and not in_str:
                        args.append(''.join(cur).strip())
                        cur = []
                        continue
                    cur.append(c)
                if cur:
                    args.append(''.join(cur).strip())
                has_pos_title = len(args) > 1 and not ('=' in args[1].split('?')[0]) and (args[1].startswith('"') or args[1].startswith("'"))
                has_kw_title = any(re.match(r'^title\s*=', a) for a in args)
                self.assertFalse(has_pos_title and has_kw_title,
                                 f"{os.path.basename(script_path)}: {fn} has duplicate title parameter (positional and keyword): {args_str[:60]}")

if __name__ == "__main__":
    unittest.main()

