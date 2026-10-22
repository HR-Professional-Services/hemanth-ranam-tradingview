#!/usr/bin/env python3
"""
Unit Tests for Phase 11 — Forward Paper-Trading Protocol & Logger
Verifies:
1. Schema & Range validation on inbound TradingView alert payloads.
2. Duplicate alert prevention (idempotency via unique signal_id).
3. Fail-closed position sizing mechanics under stop distance and risk constraints.
4. Frozen configuration integrity (0.5% risk budget, review milestones).
"""

import unittest
import os
import json
import tempfile
import shutil
from research.forward_test.paper_trade_logger import PaperTradeLogger

class TestPhase11ForwardProtocol(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.logger = PaperTradeLogger(log_dir=self.test_dir)
        
        self.valid_payload = {
            "brand": "Hemanth Ranam",
            "candidate_id": "HR-PRD-03-CANDIDATE-EXPA2",
            "signal_id": "HR-PRD-03-XAUUSD-1730000000000-BUY",
            "symbol": "XAUUSD",
            "timeframe": "15",
            "bar_time": 1730000000000,
            "direction": "BUY",
            "entry_price": 2720.50,
            "stop_loss": 2710.50,
            "take_profit": 2745.50,
            "planned_risk_pct": 0.5,
            "planned_risk_usd": 50.0,
            "qty": 5.0,
            "exit_reason_planned": "R_MULTIPLE_2.5"
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_valid_payload_acceptance(self):
        res = self.logger.process_alert(self.valid_payload)
        self.assertEqual(res["status"], "LOGGED")
        self.assertEqual(res["record"]["simulated_fill"], 2720.52) # 2 ticks slippage ($0.02)
        self.assertEqual(res["record"]["signal_id"], "HR-PRD-03-XAUUSD-1730000000000-BUY")

    def test_duplicate_signal_rejection(self):
        # First emission must log
        res1 = self.logger.process_alert(self.valid_payload)
        self.assertEqual(res1["status"], "LOGGED")
        
        # Second emission with identical signal_id must be flagged as DUPLICATE
        res2 = self.logger.process_alert(self.valid_payload)
        self.assertEqual(res2["status"], "DUPLICATE")
        self.assertEqual(res2["signal_id"], self.valid_payload["signal_id"])

    def test_invalid_payload_field_rejection(self):
        # Missing brand
        bad_payload = dict(self.valid_payload)
        del bad_payload["brand"]
        res = self.logger.process_alert(bad_payload)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("Missing required field", res["reason"])

        # Unrecognized candidate
        bad_payload = dict(self.valid_payload)
        bad_payload["candidate_id"] = "HR-PRD-99-INVALID"
        res = self.logger.process_alert(bad_payload)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("Unrecognized candidate_id", res["reason"])

    def test_stop_loss_directional_alignment(self):
        # BUY with SL above Entry
        bad_buy = dict(self.valid_payload)
        bad_buy["stop_loss"] = 2730.0 # Above 2720.50
        res = self.logger.process_alert(bad_buy)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("must be below entry", res["reason"])

        # SELL with SL below Entry
        bad_sell = dict(self.valid_payload)
        bad_sell["direction"] = "SELL"
        bad_sell["signal_id"] = "HR-PRD-03-XAUUSD-1730000000000-SELL"
        bad_sell["stop_loss"] = 2710.0 # Below 2720.50
        res = self.logger.process_alert(bad_sell)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("must be above entry", res["reason"])

    def test_risk_budget_cap_guardrail(self):
        # Planned risk exceeds 0.75% hard ceiling
        high_risk = dict(self.valid_payload)
        high_risk["planned_risk_pct"] = 1.5
        res = self.logger.process_alert(high_risk)
        self.assertEqual(res["status"], "REJECTED")
        self.assertIn("exceeds hard cap", res["reason"])

    def test_frozen_configuration_integrity(self):
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "forward_test", "forward_test_config.json")
        self.assertTrue(os.path.exists(config_path), "Missing forward_test_config.json")
        
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            
        self.assertEqual(cfg["governance_rules"]["planned_risk_pct_target"], 0.5)
        self.assertTrue(cfg["governance_rules"]["strict_no_retuning_rule"])
        self.assertTrue(cfg["governance_rules"]["fail_closed_on_invalid_sizing"])
        
        candidates = [c["candidate_id"] for c in cfg["candidates"]]
        self.assertIn("HR-PRD-03-CANDIDATE-EXPA2", candidates)
        self.assertIn("HR-PRD-04-CANDIDATE-FORWARD", candidates)

if __name__ == '__main__':
    unittest.main()
