#!/usr/bin/env python3
"""
HEMANTH RANAM TRADINGVIEW STRATEGY SUITE — PHASE 3 VALIDATION INTEGRITY TESTS

Tests the research framework, schema, CSV importer, Pine code properties,
alert payload structure, and research integrity guards.

Run:  python3 -m pytest tests/test_validation_integrity.py -v
  or: python3 -m unittest tests.test_validation_integrity
"""

import os
import json
import csv
import io
import sys
import glob
import unittest
import tempfile

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR   = os.path.join(REPO_ROOT, "src", "strategies")
RES_DIR   = os.path.join(REPO_ROOT, "research")
SCHEMA_DIR = os.path.join(RES_DIR, "schema")
CFG_DIR    = os.path.join(RES_DIR, "configs")
DOCS_DIR   = os.path.join(REPO_ROOT, "docs")


class TestPineCodeAudit(unittest.TestCase):
    """Code-level static audit of all 5 Pine Script v6 strategies."""

    STRATEGIES = [
        "HR_EMA_Pullback_Pro.pine",
        "HR_Breakout_Retest_Pro.pine",
        "HR_Market_Structure_Pro.pine",
        "HR_VWAP_Mean_Reversion_Pro.pine",
        "HR_Momentum_Volatility_Pro.pine",
    ]

    def _read(self, fname: str) -> str:
        with open(os.path.join(SRC_DIR, fname), encoding="utf-8") as f:
            return f.read()

    def test_all_pine_files_exist(self):
        for strat in self.STRATEGIES:
            self.assertTrue(os.path.exists(os.path.join(SRC_DIR, strat)),
                            f"Missing: {strat}")

    def test_all_pine_v6(self):
        for strat in self.STRATEGIES:
            content = self._read(strat)
            self.assertTrue(content.startswith("//@version=6"),
                            f"{strat} must start with //@version=6")

    def test_strategy_declaration_present(self):
        for strat in self.STRATEGIES:
            self.assertIn("strategy(", self._read(strat),
                          f"{strat} must contain strategy() declaration")

    def test_process_orders_on_close(self):
        """All strategies must declare process_orders_on_close=true to prevent intrabar fill anomalies."""
        for strat in self.STRATEGIES:
            self.assertIn("process_orders_on_close=true", self._read(strat),
                          f"{strat} must include process_orders_on_close=true")

    def test_no_lookahead_on(self):
        """lookahead_on is prohibited — causes future data leakage."""
        for strat in self.STRATEGIES:
            self.assertNotIn("lookahead_on", self._read(strat),
                             f"{strat} must not use barmerge.lookahead_on")

    def test_htf_uses_lookahead_off(self):
        """Any request.security() call must use barmerge.lookahead_off."""
        for strat in self.STRATEGIES:
            content = self._read(strat)
            if "request.security" in content:
                self.assertIn("lookahead_off", content,
                              f"{strat}: request.security() must use barmerge.lookahead_off")

    def test_htf_uses_historical_bar_shift(self):
        """HTF security requests must use close[1] not close to prevent future-bar peeking."""
        htf_strategies = ["HR_EMA_Pullback_Pro.pine"]
        for strat in htf_strategies:
            content = self._read(strat)
            self.assertIn("close[1]", content,
                          f"{strat}: HTF request must use close[1] (historical bar shift)")

    def test_commission_in_declaration(self):
        for strat in self.STRATEGIES:
            self.assertIn("commission_type", self._read(strat),
                          f"{strat} must declare commission_type")

    def test_alert_has_brand(self):
        for strat in self.STRATEGIES:
            self.assertIn('"brand":"Hemanth Ranam"', self._read(strat),
                          f"{strat} alert payload must include brand field")

    def test_alert_has_stop_loss(self):
        for strat in self.STRATEGIES:
            content = self._read(strat)
            self.assertIn('"stop_loss":', content,
                          f"{strat} alert payload must include stop_loss")

    def test_alert_has_take_profit(self):
        for strat in self.STRATEGIES:
            content = self._read(strat)
            self.assertIn('"take_profit_1":', content,
                          f"{strat} alert payload must include take_profit_1")

    def test_alert_fired_on_bar_close(self):
        """Alerts must fire once per bar close, not on every tick."""
        for strat in self.STRATEGIES:
            content = self._read(strat)
            self.assertIn("alert.freq_once_per_bar_close", content,
                          f"{strat} alerts must use alert.freq_once_per_bar_close")


class TestResearchArchitecture(unittest.TestCase):
    """Validate the research directory structure and config files exist."""

    def test_research_dirs_exist(self):
        for subdir in ["configs", "data", "exports", "results", "reports", "schema", "forward", "scripts"]:
            self.assertTrue(os.path.isdir(os.path.join(RES_DIR, subdir)),
                            f"Missing research/{subdir}/ directory")

    def test_config_files_exist(self):
        configs = ["markets.json", "timeframes.json", "cost-scenarios.json",
                   "validation-periods.json", "locked-parameters.json"]
        for cfg in configs:
            self.assertTrue(os.path.exists(os.path.join(CFG_DIR, cfg)),
                            f"Missing research/configs/{cfg}")

    def test_schema_files_exist(self):
        schemas = ["results.schema.json", "alert-payload.schema.json"]
        for s in schemas:
            self.assertTrue(os.path.exists(os.path.join(SCHEMA_DIR, s)),
                            f"Missing research/schema/{s}")

    def test_importer_script_exists(self):
        self.assertTrue(os.path.exists(os.path.join(RES_DIR, "scripts", "tv_importer.py")))

    def test_report_generator_exists(self):
        self.assertTrue(os.path.exists(os.path.join(RES_DIR, "report_generator.py")))


class TestResultSchema(unittest.TestCase):
    """Validate the result JSON schema structure."""

    def _load_schema(self) -> dict:
        with open(os.path.join(SCHEMA_DIR, "results.schema.json")) as f:
            return json.load(f)

    def test_schema_is_valid_json(self):
        schema = self._load_schema()
        self.assertIsInstance(schema, dict)

    def test_schema_has_required_fields(self):
        schema = self._load_schema()
        required = schema.get("required", [])
        expected = ["schema_version", "result_id", "strategy", "symbol", "timeframe",
                    "data_source", "period_start", "period_end", "cost_scenario",
                    "validation_status", "total_trades"]
        for field in expected:
            self.assertIn(field, required, f"Schema must require field: {field}")

    def test_schema_prohibits_fabrication(self):
        """Unknown values must be null in the schema — not zero or estimated."""
        schema = self._load_schema()
        props = schema.get("properties", {})
        nullable_fields = ["sharpe", "sortino", "net_profit_pct", "max_drawdown_pct",
                           "long_win_rate", "short_win_rate"]
        for field in nullable_fields:
            if field in props:
                field_type = props[field].get("type", [])
                self.assertIn("null", field_type if isinstance(field_type, list) else [field_type],
                              f"Schema field '{field}' must allow null (not fabricate missing values)")


class TestCostScenariosConfig(unittest.TestCase):
    """Validate cost scenarios configuration."""

    def _load(self) -> dict:
        with open(os.path.join(CFG_DIR, "cost-scenarios.json")) as f:
            return json.load(f)

    def test_three_scenarios_present(self):
        cfg = self._load()
        for sc in ["A", "B", "C"]:
            self.assertIn(sc, cfg["scenarios"])

    def test_scenario_A_is_zero_cost(self):
        cfg = self._load()
        self.assertEqual(cfg["scenarios"]["A"]["commission_pct_per_side"], 0.0)
        self.assertEqual(cfg["scenarios"]["A"]["slippage_ticks"], 0)

    def test_scenario_B_is_realistic(self):
        cfg = self._load()
        sc_b = cfg["scenarios"]["B"]
        self.assertGreater(sc_b["commission_pct_per_side"], 0.0)
        self.assertGreater(sc_b["slippage_ticks"], 0)

    def test_required_for_production_is_B(self):
        cfg = self._load()
        self.assertEqual(cfg.get("required_for_production"), "B")


class TestLockedParameters(unittest.TestCase):
    """Verify locked parameters cover all 5 strategies."""

    STRATEGY_KEYS = [
        "HR_EMA_Pullback_Pro", "HR_Breakout_Retest_Pro",
        "HR_Market_Structure_Pro", "HR_VWAP_Mean_Reversion_Pro",
        "HR_Momentum_Volatility_Pro"
    ]

    def _load(self) -> dict:
        with open(os.path.join(CFG_DIR, "locked-parameters.json")) as f:
            return json.load(f)

    def test_all_strategies_present(self):
        cfg = self._load()
        for key in self.STRATEGY_KEYS:
            self.assertIn(key, cfg["strategies"], f"Locked params missing: {key}")

    def test_each_strategy_has_versioning(self):
        cfg = self._load()
        for key in self.STRATEGY_KEYS:
            strat = cfg["strategies"][key]
            self.assertIn("strategy_version", strat)
            self.assertIn("parameter_version", strat)

    def test_vwap_guard_is_locked_on(self):
        """VWAP Trend Protection Guard must be locked ON — disabling it causes catastrophic failure."""
        cfg = self._load()
        vwap = cfg["strategies"]["HR_VWAP_Mean_Reversion_Pro"]
        guard = vwap["parameters"].get("enable_trend_guard", {})
        self.assertTrue(guard.get("value"), "VWAP Trend Guard must be locked ON")


class TestAlertSchema(unittest.TestCase):
    """Validate alert payload schema."""

    def _load(self) -> dict:
        with open(os.path.join(SCHEMA_DIR, "alert-payload.schema.json")) as f:
            return json.load(f)

    def test_schema_is_valid_json(self):
        self.assertIsInstance(self._load(), dict)

    def test_required_alert_fields(self):
        schema = self._load()
        required = schema.get("required", [])
        for field in ["brand", "strategy", "symbol", "signal", "stop_loss", "take_profit_1", "timestamp"]:
            self.assertIn(field, required, f"Alert schema must require: {field}")

    def test_signal_enum_correct(self):
        schema = self._load()
        signal_prop = schema["properties"].get("signal", {})
        self.assertIn("BUY",  signal_prop.get("enum", []))
        self.assertIn("SELL", signal_prop.get("enum", []))


class TestCSVImporter(unittest.TestCase):
    """Test TradingView CSV import logic end-to-end with a synthetic export."""

    def _make_temp_csv(self) -> str:
        content = (
            "Trade #,Type,Date/Time,Price,Contracts,Profit,Profit %,Run-up,Drawdown,Cumulative Profit\n"
            "1,Entry Long,2026-01-05 09:30,2480.5,1,,,,,\n"
            "1,Exit Long,2026-01-05 11:00,2495.0,1,14.5,0.58,18.2,2.1,14.5\n"
            "2,Entry Short,2026-01-06 14:00,2492.0,1,,,,,\n"
            "2,Exit Short,2026-01-06 16:30,2485.0,1,7.0,0.28,9.1,1.2,21.5\n"
            "3,Entry Long,2026-01-07 09:45,2488.0,1,,,,,\n"
            "3,Exit Long,2026-01-07 12:00,2481.0,1,-7.0,-0.28,2.0,8.5,14.5\n"
        )
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_csv_parses_without_error(self):
        sys.path.insert(0, os.path.join(RES_DIR, "scripts"))
        from tv_importer import parse_tv_csv
        csv_path = self._make_temp_csv()
        try:
            trades = parse_tv_csv(csv_path)
            self.assertIsInstance(trades, list)
        finally:
            os.unlink(csv_path)

    def test_metrics_computed_correctly(self):
        sys.path.insert(0, os.path.join(RES_DIR, "scripts"))
        from tv_importer import compute_metrics
        trades = [
            {"profit": 14.5, "profit_pct": 0.58},
            {"profit":  7.0, "profit_pct": 0.28},
            {"profit": -7.0, "profit_pct": -0.28},
        ]
        m = compute_metrics(trades)
        self.assertEqual(m["total_trades"], 3)
        self.assertAlmostEqual(m["win_rate"], 66.67, places=0)
        self.assertGreater(m["profit_factor"], 1.0)

    def test_null_values_not_fabricated(self):
        """Fields that TradingView doesn't expose in CSV must be null, never zero."""
        sys.path.insert(0, os.path.join(RES_DIR, "scripts"))
        from tv_importer import compute_metrics
        trades = [{"profit": 10.0, "profit_pct": 0.5}]
        m = compute_metrics(trades)
        self.assertIsNone(m.get("sharpe"),         "sharpe must be null — not fabricated")
        self.assertIsNone(m.get("sortino"),        "sortino must be null — not fabricated")
        self.assertIsNone(m.get("net_profit_pct"), "net_profit_pct must be null — not fabricated from trade CSV")


class TestValidationDocumentation(unittest.TestCase):
    """Ensure key validation framework documents exist."""

    ROOT = REPO_ROOT

    def test_validation_status_exists(self):
        self.assertTrue(os.path.exists(os.path.join(self.ROOT, "VALIDATION-STATUS.md")))

    def test_change_control_exists(self):
        self.assertTrue(os.path.exists(os.path.join(self.ROOT, "CHANGE-CONTROL.md")))

    def test_htf_validation_doc_exists(self):
        self.assertTrue(os.path.exists(os.path.join(DOCS_DIR, "NON-REPAINTING-AUDIT.md")))

    def test_tradingview_protocol_exists(self):
        # Accept either the old or new filename
        old = os.path.exists(os.path.join(DOCS_DIR, "TRADINGVIEW-NATIVE-TEST-PROTOCOL.md"))
        new = os.path.exists(os.path.join(DOCS_DIR, "TRADINGVIEW-TEST-PROTOCOL.md"))
        self.assertTrue(old or new, "TradingView test protocol doc must exist")

    def test_validation_methodology_exists(self):
        self.assertTrue(os.path.exists(os.path.join(DOCS_DIR, "VALIDATION-METHODOLOGY.md")))

    def test_readme_contains_disclaimer(self):
        readme = os.path.join(self.ROOT, "README.md")
        with open(readme) as f:
            content = f.read().lower()
        self.assertIn("not guarantee", content,
                      "README must contain performance disclaimer")


if __name__ == "__main__":
    unittest.main()
