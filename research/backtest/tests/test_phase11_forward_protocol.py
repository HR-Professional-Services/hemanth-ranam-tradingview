#!/usr/bin/env python3
"""
Unit Tests for Phase 11/13 — Forward Paper-Trading Protocol, Logger & Risk Engine
Verifies:
1. Schema & Range validation on inbound TradingView alert payloads.
2. Duplicate alert prevention (idempotency via unique signal_id).
3. Directional stop loss alignment.
4. Risk budget hard cap enforcement.
5. Frozen configuration integrity.
6. Exact mathematical behavior of calc_pine_sizing (rounding down, fail-closed).
7. Active circuit breaker triggering on consecutive losses (12) and drawdown (10%).
"""

import unittest
import os
import json
import tempfile
import shutil
from research.forward_test.paper_trade_logger import PaperTradeLogger, calc_pine_sizing

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

    def test_pine_sizing_step_rounding_and_fail_closed(self):
        # 1. Rounding DOWN test:
        # Equity = $10,000, risk = 0.5% ($50 budget).
        # Entry = 2700, SL = 2689.5 (dist = 10.5).
        # Raw qty = 50 / (10.5 * 1.0) = 4.761904...
        # With min_volume_step = 0.01: stepped qty must be 4.76 (NOT rounded up to 4.77)
        qty, budget = calc_pine_sizing(
            equity=10000.0, risk_pct=0.5, max_risk_usd=100.0,
            entry_price=2700.0, sl_price=2689.5, point_value=1.0, contract_mult=1.0, min_volume_step=0.01
        )
        self.assertEqual(qty, 4.76)
        self.assertEqual(budget, 50.0)
        # Verify realized risk at stop does not exceed planned budget
        self.assertLessEqual(qty * 10.5, budget)

        # 2. Fail closed on zero stop distance
        qty_zero, _ = calc_pine_sizing(
            equity=10000.0, risk_pct=0.5, max_risk_usd=100.0,
            entry_price=2700.0, sl_price=2700.0
        )
        self.assertEqual(qty_zero, 0.0)

        # 3. Fail closed on sub-minimum volume step
        # If stop distance is huge (e.g. 10,000 pts), raw qty = 50 / 10000 = 0.005
        # Below min_volume_step of 0.01 -> must fail closed to 0.0
        qty_sub, _ = calc_pine_sizing(
            equity=10000.0, risk_pct=0.5, max_risk_usd=100.0,
            entry_price=12000.0, sl_price=2000.0, point_value=1.0, contract_mult=1.0, min_volume_step=0.01
        )
        self.assertEqual(qty_sub, 0.0)

        # 4. Max risk cap clamping
        # On $100,000 equity, 0.5% would be $500, but max_risk_usd is capped at $100
        qty_cap, budget_cap = calc_pine_sizing(
            equity=100000.0, risk_pct=0.5, max_risk_usd=100.0,
            entry_price=2700.0, sl_price=2690.0, point_value=1.0, contract_mult=1.0, min_volume_step=0.01
        )
        self.assertEqual(budget_cap, 100.0) # Clamped to 100
        self.assertEqual(qty_cap, 10.0)    # 100 / 10 = 10.0 units

    def test_active_circuit_breaker_consecutive_losses(self):
        # Configure logger with 3 consecutive loss limit for testing
        self.logger.early_stop_consecutive_losses = 3

        for i in range(3):
            payload = dict(self.valid_payload)
            payload["signal_id"] = f"SIG-LOSS-{i}"
            payload["bar_time"] = 1730000000000 + (i * 900000)
            log_res = self.logger.process_alert(payload)
            self.assertEqual(log_res["status"], "LOGGED")

            # Close as loss
            exit_res = self.logger.record_trade_exit(
                signal_id=f"SIG-LOSS-{i}",
                exit_price=2710.50, # Hit stop
                exit_time=1730000000000 + (i * 900000) + 60000,
                exit_reason="STOP_LOSS"
            )
            self.assertEqual(exit_res["status"], "CLOSED")
            self.assertLess(exit_res["record"]["net_pnl_usd"], 0)

        # After 3 consecutive losses, circuit breaker must be tripped
        self.assertTrue(self.logger.circuit_breaker_tripped)
        self.assertEqual(self.logger.consecutive_losses, 3)

        # Next alert must be HALTED by circuit breaker
        next_payload = dict(self.valid_payload)
        next_payload["signal_id"] = "SIG-AFTER-BREAKER"
        halt_res = self.logger.process_alert(next_payload)
        self.assertEqual(halt_res["status"], "CIRCUIT_BREAKER_HALTED")
        self.assertIn("consecutive losses", halt_res["reason"])

    def test_active_circuit_breaker_drawdown(self):
        # Configure logger with 10% drawdown limit
        self.logger.early_stop_max_drawdown_pct = 10.0
        self.logger.initial_capital = 10000.0

        # Log a large loss that exceeds 10% ($1,000)
        payload = dict(self.valid_payload)
        payload["signal_id"] = "SIG-DD-TEST"
        payload["qty"] = 100.0 # 100 units
        self.logger.process_alert(payload)

        # Exit with a $15 loss per unit * 100 = $1,500 loss (15% drawdown)
        exit_res = self.logger.record_trade_exit(
            signal_id="SIG-DD-TEST",
            exit_price=2705.50,
            exit_time=1730000060000,
            exit_reason="STOP_LOSS"
        )
        self.assertTrue(self.logger.circuit_breaker_tripped)
        self.assertGreaterEqual(exit_res["record"]["drawdown_pct"], 10.0)

        # Subsequent alert rejected
        halt_res = self.logger.process_alert(self.valid_payload)
        self.assertEqual(halt_res["status"], "CIRCUIT_BREAKER_HALTED")
        self.assertIn("Drawdown", halt_res["reason"])

if __name__ == '__main__':
    unittest.main()
