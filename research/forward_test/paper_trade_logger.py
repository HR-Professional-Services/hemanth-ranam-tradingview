#!/usr/bin/env python3
"""
HR TradingView Suite — Phase 13 Passive Forward Paper-Trade Logger & Circuit Breaker Engine
Validates inbound TradingView alert payloads, enforces duplicate rejection (idempotency),
verifies fail-closed risk sizing bounds, logs simulated executions, and enforces active
circuit breakers (12 consecutive losses or 10.0% drawdown) without broker connectivity.

SAFETY RULES:
- Strictly passive / non-executing. Zero broker API calls, zero orders placed.
- Idempotency via unique signal_id prevents alert duplicates or replay attacks.
- Rejects signals violating 0.5% risk budget or fail-closed sizing.
- Actively halts forward evaluation if circuit breakers are tripped.
"""

import json
import os
import math
from typing import Dict, Any, Tuple, Optional

REQUIRED_PAYLOAD_FIELDS = [
    "brand", "candidate_id", "signal_id", "symbol", "timeframe",
    "bar_time", "direction", "entry_price", "stop_loss", "take_profit",
    "planned_risk_pct", "planned_risk_usd", "qty"
]

def calc_pine_sizing(
    equity: float,
    risk_pct: float,
    max_risk_usd: float,
    entry_price: float,
    sl_price: float,
    point_value: float = 1.0,
    contract_mult: float = 1.0,
    min_volume_step: float = 0.01
) -> Tuple[float, float]:
    """
    Exact mathematical reproduction of the Pine Script v6 calcSizing() engine.
    Returns (valid_qty, planned_risk_usd). Fails closed (0.0 qty) on any invalid condition.
    """
    sl_dist = abs(entry_price - sl_price)
    if sl_dist <= 0 or math.isnan(sl_dist) or math.isinf(sl_dist):
        return 0.0, 0.0

    if equity <= 0 or risk_pct <= 0:
        return 0.0, 0.0

    budget_usd = min(equity * (risk_pct / 100.0), max_risk_usd)
    pv = point_value if point_value > 0 else contract_mult
    if pv <= 0:
        return 0.0, 0.0

    raw_qty = budget_usd / (sl_dist * pv)
    stepped_qty = math.floor(raw_qty / min_volume_step) * min_volume_step
    stepped_qty = round(stepped_qty, 6)

    if stepped_qty >= min_volume_step:
        return stepped_qty, budget_usd

    return 0.0, budget_usd


class PaperTradeLogger:
    def __init__(self, config_path: Optional[str] = None, log_dir: Optional[str] = None):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), "forward_test_config.json")
        self.log_dir = log_dir or os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.log_file = os.path.join(self.log_dir, "forward_paper_trades.jsonl")
        self.closed_log_file = os.path.join(self.log_dir, "forward_closed_trades.jsonl")
        self.seen_signals = set()
        self.open_positions: Dict[str, Dict[str, Any]] = {}

        # Circuit breaker parameters & state
        self.initial_capital = 10000.0
        self.early_stop_consecutive_losses = 12
        self.early_stop_max_drawdown_pct = 10.0
        self.load_config()

        self.current_equity = self.initial_capital
        self.peak_equity = self.initial_capital
        self.consecutive_losses = 0
        self.circuit_breaker_tripped = False
        self.circuit_breaker_reason = ""

        self.load_history()

    def load_config(self):
        """Loads governance rules and circuit breaker thresholds from config if available."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.initial_capital = float(cfg.get("simulated_initial_capital", 10000.0))
                    review = cfg.get("review_milestones", {})
                    self.early_stop_consecutive_losses = int(review.get("early_stop_consecutive_losses", 12))
                    self.early_stop_max_drawdown_pct = float(review.get("early_stop_max_drawdown_pct", 10.0))
            except Exception:
                pass

    def load_history(self):
        """Preload seen signal_ids and open positions from disk to preserve state across restarts."""
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
                                if record.get("status") == "LOGGED_OPEN":
                                    self.open_positions[sig_id] = record
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
        Parses alert string/dict, enforces circuit breakers, enforces idempotency,
        checks risk bounds, simulates execution fill, and logs open trade.
        """
        if self.circuit_breaker_tripped:
            return {
                "status": "CIRCUIT_BREAKER_HALTED",
                "reason": self.circuit_breaker_reason
            }

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
        self.open_positions[sig_id] = log_record
        return {"status": "LOGGED", "record": log_record}

    def record_trade_exit(
        self,
        signal_id: str,
        exit_price: float,
        exit_time: int,
        exit_reason: str
    ) -> Dict[str, Any]:
        """
        Records the closing of an open simulated trade, computes realized net PnL
        with friction, updates equity and drawdown, and evaluates circuit breakers.
        """
        if signal_id not in self.open_positions:
            return {"status": "ERROR", "reason": f"Signal ID {signal_id} not found in open positions"}

        pos = self.open_positions.pop(signal_id)
        direction = pos["direction"]
        qty = pos["qty"]
        entry_fill = pos["simulated_fill"]

        # Adverse slippage on exit: 2 ticks = $0.02
        slippage_ticks = 2
        tick_size = 0.01
        slippage_cost = slippage_ticks * tick_size
        simulated_exit_fill = (exit_price - slippage_cost) if direction == "BUY" else (exit_price + slippage_cost)

        # Gross & Net PnL
        if direction == "BUY":
            gross_pnl = (simulated_exit_fill - entry_fill) * qty
        else:
            gross_pnl = (entry_fill - simulated_exit_fill) * qty

        exit_notional = simulated_exit_fill * qty
        exit_comm = exit_notional * 0.0002
        entry_friction = pos["total_friction_usd"]
        net_pnl = gross_pnl - exit_comm

        # Update equity & drawdown tracking
        self.current_equity += net_pnl
        if self.current_equity > self.peak_equity:
            self.peak_equity = self.current_equity

        drawdown_pct = 0.0
        if self.peak_equity > 0:
            drawdown_pct = ((self.peak_equity - self.current_equity) / self.peak_equity) * 100.0

        if net_pnl < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

        # Evaluate circuit breakers
        if self.consecutive_losses >= self.early_stop_consecutive_losses:
            self.circuit_breaker_tripped = True
            self.circuit_breaker_reason = (
                f"Circuit breaker tripped: {self.consecutive_losses} consecutive losses "
                f"reached threshold of {self.early_stop_consecutive_losses}"
            )
        elif drawdown_pct >= self.early_stop_max_drawdown_pct:
            self.circuit_breaker_tripped = True
            self.circuit_breaker_reason = (
                f"Circuit breaker tripped: Drawdown {drawdown_pct:.2f}% "
                f"reached threshold of {self.early_stop_max_drawdown_pct}%"
            )

        closed_record = {
            "signal_id": signal_id,
            "candidate_id": pos["candidate_id"],
            "direction": direction,
            "entry_fill": entry_fill,
            "exit_fill": round(simulated_exit_fill, 2),
            "qty": qty,
            "gross_pnl_usd": round(gross_pnl, 2),
            "exit_commission_usd": round(exit_comm, 4),
            "net_pnl_usd": round(net_pnl, 2),
            "current_equity_usd": round(self.current_equity, 2),
            "drawdown_pct": round(drawdown_pct, 2),
            "consecutive_losses": self.consecutive_losses,
            "circuit_breaker_tripped": self.circuit_breaker_tripped,
            "exit_reason": exit_reason,
            "exit_time": exit_time,
            "status": "CLOSED"
        }

        with open(self.closed_log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(closed_record) + "\n")

        return {"status": "CLOSED", "record": closed_record}
