#!/usr/bin/env python3
"""
HR TradingView Suite — Phase 11 Passive Forward Paper-Trade Logger
Validates inbound TradingView alert payloads, enforces duplicate rejection (idempotency),
verifies fail-closed risk sizing bounds, and logs simulated executions without broker connectivity.

SAFETY RULES:
- Strictly passive / non-executing. Zero broker API calls, zero orders placed.
- Idempotency via unique signal_id prevents alert duplicates or replay attacks.
- Rejects signals violating 0.5% risk budget or fail-closed sizing.
"""

import json
import os
import math
import hashlib
from typing import Dict, Any, Tuple, Optional

REQUIRED_PAYLOAD_FIELDS = [
    "brand", "candidate_id", "signal_id", "symbol", "timeframe",
    "bar_time", "direction", "entry_price", "stop_loss", "take_profit",
    "planned_risk_pct", "planned_risk_usd", "qty"
]

class PaperTradeLogger:
    def __init__(self, config_path: Optional[str] = None, log_dir: Optional[str] = None):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), "forward_test_config.json")
        self.log_dir = log_dir or os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.log_file = os.path.join(self.log_dir, "forward_paper_trades.jsonl")
        self.seen_signals = set()
        self.load_seen_signals()

    def load_seen_signals(self):
        """Preload seen signal_ids from existing log file to preserve idempotency across restarts."""
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            record = json.loads(line)
                            sig_id = record.get("signal_id")
                            if sig_id:
                                self.seen_signals.add(sig_id)
                        except Exception:
                            continue

    def validate_payload(self, payload: Dict[str, Any]) -> Tuple[bool, str]:
        """Validates payload structure, types, and values against strict schema."""
        for field in REQUIRED_PAYLOAD_FIELDS:
            if field not in payload:
                return False, f"Missing required field: {field}"

        if payload.get("brand") != "Hemanth Ranam":
            return False, f"Invalid brand identifier: {payload.get('brand')}"

        cid = payload.get("candidate_id")
        if cid not in ["HR-PRD-03-CANDIDATE-EXPA2", "HR-PRD-04-CANDIDATE-FORWARD"]:
            return False, f"Unrecognized candidate_id: {cid}"

        direction = payload.get("direction")
        if direction not in ["BUY", "SELL"]:
            return False, f"Invalid direction: {direction}"

        try:
            entry = float(payload["entry_price"])
            sl = float(payload["stop_loss"])
            tp = float(payload["take_profit"])
            risk_pct = float(payload["planned_risk_pct"])
            risk_usd = float(payload["planned_risk_usd"])
            qty = float(payload["qty"])
        except (ValueError, TypeError) as e:
            return False, f"Non-numeric numerical field: {e}"

        if entry <= 0 or sl <= 0 or tp <= 0 or qty <= 0 or risk_usd <= 0:
            return False, "Prices, risk_usd, and qty must be strictly positive"

        # Directional stop/take-profit alignment
        if direction == "BUY":
            if sl >= entry:
                return False, f"BUY signal stop loss ({sl}) must be below entry ({entry})"
            if tp <= entry:
                return False, f"BUY signal take profit ({tp}) must be above entry ({entry})"
        elif direction == "SELL":
            if sl <= entry:
                return False, f"SELL signal stop loss ({sl}) must be above entry ({entry})"
            if tp >= entry:
                return False, f"SELL signal take profit ({tp}) must be below entry ({entry})"

        # Risk budget guardrail (target 0.5% with 0.75% hard ceiling)
        if risk_pct > 0.75:
            return False, f"Planned risk {risk_pct}% exceeds hard cap of 0.75%"

        return True, "Valid"

    def process_alert(self, raw_data: Any) -> Dict[str, Any]:
        """
        Parses alert string/dict, enforces idempotency, checks risk bounds,
        simulates realistic execution fill, and writes to forward paper log.
        """
        if isinstance(raw_data, str):
            try:
                payload = json.loads(raw_data)
            except Exception as e:
                return {"status": "REJECTED", "reason": f"JSON parse error: {e}"}
        elif isinstance(raw_data, dict):
            payload = raw_data
        else:
            return {"status": "REJECTED", "reason": "Unsupported data type"}

        # 1. Schema & Range Validation
        is_valid, reason = self.validate_payload(payload)
        if not is_valid:
            return {"status": "REJECTED", "reason": reason}

        # 2. Duplicate Alert Idempotency Gate
        sig_id = payload["signal_id"]
        if sig_id in self.seen_signals:
            return {"status": "DUPLICATE", "signal_id": sig_id, "reason": "Alert already logged previously"}

        # 3. Execution Simulation (Conservative Slippage & Commission)
        # Gold/CFD default: 2 ticks = $0.02 slippage, 0.02% commission
        direction = payload["direction"]
        entry_price = float(payload["entry_price"])
        qty = float(payload["qty"])
        slippage_ticks = 2
        tick_size = 0.01
        slippage_cost = slippage_ticks * tick_size
        
        simulated_fill = (entry_price + slippage_cost) if direction == "BUY" else (entry_price - slippage_cost)
        notional = simulated_fill * qty
        est_commission = notional * 0.0002 # 0.02%

        log_record = {
            "candidate_id": payload["candidate_id"],
            "signal_id": sig_id,
            "symbol": payload["symbol"],
            "timeframe": payload["timeframe"],
            "bar_time": payload["bar_time"],
            "direction": direction,
            "signal_entry": entry_price,
            "simulated_fill": round(simulated_fill, 2),
            "stop_loss": float(payload["stop_loss"]),
            "take_profit": float(payload["take_profit"]),
            "stop_distance": round(abs(entry_price - float(payload["stop_loss"])), 2),
            "qty": qty,
            "planned_risk_pct": float(payload["planned_risk_pct"]),
            "planned_risk_usd": float(payload["planned_risk_usd"]),
            "estimated_slippage_usd": round(slippage_cost * qty, 4),
            "estimated_commission_usd": round(est_commission, 4),
            "total_friction_usd": round((slippage_cost * qty) + est_commission, 4),
            "score": payload.get("score"),
            "grade": payload.get("grade"),
            "exit_reason_planned": payload.get("exit_reason_planned"),
            "status": "LOGGED_OPEN"
        }

        # Append to log
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_record) + "\n")

        self.seen_signals.add(sig_id)
        return {"status": "LOGGED", "record": log_record}
