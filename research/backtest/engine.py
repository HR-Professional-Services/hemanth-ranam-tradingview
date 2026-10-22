"""
HR TradingView Backtesting Framework — Core Simulation Engine
Implements TradingView Strategy Tester execution semantics:
- process_orders_on_close = true: Signals on bar i fill at open of bar i+1.
- commission modeling (0.02% per order).
- slippage modeling (2 ticks).
- stop-loss and take-profit limit/stop order handling with intrabar evaluation.
"""
from typing import List, Dict, Any, Optional

class Trade:
    def __init__(self, trade_id: int, direction: int, entry_bar: int, entry_time: str, 
                 entry_price: float, sl_price: float, tp_price: float, qty: float, 
                 score: float, grade: str):
        self.trade_id = trade_id
        self.direction = direction # 1 for Long, -1 for Short
        self.entry_bar = entry_bar
        self.entry_time = entry_time
        self.entry_price = entry_price
        self.sl_price = sl_price
        self.tp_price = tp_price
        self.qty = qty
        self.score = score
        self.grade = grade
        
        self.exit_bar: Optional[int] = None
        self.exit_time: Optional[str] = None
        self.exit_price: Optional[float] = None
        self.exit_reason: Optional[str] = None # "SL", "TP", "CLOSE"
        self.pnl_cash: float = 0.0
        self.pnl_pct: float = 0.0
        self.commission: float = 0.0
        self.slippage_loss: float = 0.0

class BacktestEngine:
    def __init__(self, initial_capital: float = 10000.0, 
                 commission_pct: float = 0.02, # 0.02%
                 slippage_ticks: int = 2, 
                 tick_size: float = 0.01,
                 tick_value: float = 0.01,
                 contract_size: float = 1.0,
                 risk_mode: str = "percent_of_equity", # "percent_of_equity" or "fixed_monetary_risk"
                 risk_value: float = 1.0):
        self.initial_capital = initial_capital
        self.equity = initial_capital
        self.cash = initial_capital
        self.commission_pct = commission_pct
        self.slippage_ticks = slippage_ticks
        self.tick_size = tick_size
        self.tick_value = tick_value
        self.contract_size = contract_size
        self.risk_mode = risk_mode
        self.risk_value = risk_value
        
        self.trades: List[Trade] = []
        self.active_trade: Optional[Trade] = None
        self.equity_curve: List[Dict[str, Any]] = []
        self.trade_counter = 0

    def calculate_position_size(self, entry_price: float, sl_price: float) -> float:
        """
        Calculates position size based on configured risk mode.
        If 'percent_of_equity' (TV default):
            qty = (equity * (risk_value / 100.0)) / entry_price
        If 'fixed_monetary_risk' (Real 1% Risk Sizing):
            risk_cash = equity * (risk_value / 100.0)
            sl_distance = abs(entry_price - sl_price)
            qty = risk_cash / (sl_distance * contract_size)
        """
        if entry_price <= 0:
            return 0.0
            
        if self.risk_mode == "percent_of_equity":
            allocated_capital = self.equity * (self.risk_value / 100.0)
            qty = allocated_capital / (entry_price * self.contract_size)
        elif self.risk_mode == "fixed_monetary_risk":
            sl_distance = abs(entry_price - sl_price)
            if sl_distance <= 0:
                sl_distance = entry_price * 0.005 # fallback
            risk_cash = self.equity * (self.risk_value / 100.0)
            qty = risk_cash / (sl_distance * self.contract_size)
        else:
            qty = 1.0
            
        return max(0.01, round(qty, 4))

    def run(self, candles: List[Dict[str, Any]], signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes backtest over candles.
        Signals list corresponds 1-to-1 with candles.
        signals[i] contains:
            'buy': bool, 'sell': bool, 'sl': float, 'tp': float, 'score': float, 'grade': str
        Signals evaluated on bar i are executed at open of bar i+1 (process_orders_on_close = true).
        """
        n = len(candles)
        self.trades.clear()
        self.active_trade = None
        self.equity = self.initial_capital
        self.equity_curve.clear()
        
        pending_order = None # {"dir": 1 or -1, "sl": float, "tp": float, "score": float, "grade": str}
        
        for i in range(n):
            c = candles[i]
            o = c['open']
            h = c['high']
            l = c['low']
            cl = c['close']
            t = c['time']
            
            # 1. Fill pending order at Open of bar i
            if pending_order is not None and self.active_trade is None:
                p_dir = pending_order["dir"]
                p_sl = pending_order["sl"]
                p_tp = pending_order["tp"]
                p_score = pending_order["score"]
                p_grade = pending_order["grade"]
                
                # Apply slippage on entry
                slip = self.slippage_ticks * self.tick_size
                fill_price = o + slip if p_dir == 1 else o - slip
                
                qty = self.calculate_position_size(fill_price, p_sl)
                
                self.trade_counter += 1
                self.active_trade = Trade(
                    trade_id=self.trade_counter,
                    direction=p_dir,
                    entry_bar=i,
                    entry_time=t,
                    entry_price=fill_price,
                    sl_price=p_sl,
                    tp_price=p_tp,
                    qty=qty,
                    score=p_score,
                    grade=p_grade
                )
                
                # Entry commission
                notional = fill_price * qty * self.contract_size
                comm = notional * (self.commission_pct / 100.0)
                self.active_trade.commission += comm
                self.equity -= comm
                pending_order = None

            # 2. Check exits on active trade during bar i
            if self.active_trade is not None:
                trade = self.active_trade
                is_closed = False
                exit_price = 0.0
                exit_reason = ""
                
                if trade.direction == 1:
                    # Long exit check
                    hit_sl = l <= trade.sl_price
                    hit_tp = h >= trade.tp_price
                    
                    if hit_sl and hit_tp:
                        # Ambiguity handling: conservative assumption - stop loss hit first
                        is_closed = True
                        exit_price = trade.sl_price
                        exit_reason = "SL"
                    elif hit_sl:
                        is_closed = True
                        exit_price = trade.sl_price
                        exit_reason = "SL"
                    elif hit_tp:
                        is_closed = True
                        exit_price = trade.tp_price
                        exit_reason = "TP"
                elif trade.direction == -1:
                    # Short exit check
                    hit_sl = h >= trade.sl_price
                    hit_tp = l <= trade.tp_price
                    
                    if hit_sl and hit_tp:
                        is_closed = True
                        exit_price = trade.sl_price
                        exit_reason = "SL"
                    elif hit_sl:
                        is_closed = True
                        exit_price = trade.sl_price
                        exit_reason = "SL"
                    elif hit_tp:
                        is_closed = True
                        exit_price = trade.tp_price
                        exit_reason = "TP"
                        
                if is_closed:
                    # Apply slippage on stop loss
                    if exit_reason == "SL":
                        slip = self.slippage_ticks * self.tick_size
                        exit_price = exit_price - slip if trade.direction == 1 else exit_price + slip
                        
                    trade.exit_bar = i
                    trade.exit_time = t
                    trade.exit_price = exit_price
                    trade.exit_reason = exit_reason
                    
                    # Calculate PnL
                    point_diff = (exit_price - trade.entry_price) if trade.direction == 1 else (trade.entry_price - exit_price)
                    cash_pnl = point_diff * trade.qty * self.contract_size
                    
                    # Exit commission
                    notional = exit_price * trade.qty * self.contract_size
                    comm = notional * (self.commission_pct / 100.0)
                    trade.commission += comm
                    
                    trade.pnl_cash = cash_pnl - comm
                    trade.pnl_pct = (trade.pnl_cash / self.equity) * 100.0 if self.equity > 0 else 0.0
                    
                    self.equity += (cash_pnl - comm)
                    self.trades.append(trade)
                    self.active_trade = None

            # 3. Check new signal generated on close of bar i
            sig = signals[i]
            if sig.get("buy") and self.active_trade is None and pending_order is None:
                pending_order = {
                    "dir": 1,
                    "sl": sig["sl"],
                    "tp": sig["tp"],
                    "score": sig.get("score", 0.0),
                    "grade": sig.get("grade", "A")
                }
            elif sig.get("sell") and self.active_trade is None and pending_order is None:
                pending_order = {
                    "dir": -1,
                    "sl": sig["sl"],
                    "tp": sig["tp"],
                    "score": sig.get("score", 0.0),
                    "grade": sig.get("grade", "A")
                }
                
            self.equity_curve.append({
                "bar": i,
                "time": t,
                "equity": self.equity
            })
            
        return self.compute_metrics()

    def compute_metrics(self) -> Dict[str, Any]:
        """Calculates comprehensive quantitative performance metrics."""
        total_trades = len(self.trades)
        if total_trades == 0:
            return {
                "total_trades": 0,
                "net_profit": 0.0,
                "net_return_pct": 0.0,
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "max_drawdown_cash": 0.0,
                "max_drawdown_pct": 0.0,
                "expectancy_cash": 0.0,
                "avg_trade_cash": 0.0,
                "total_commission": 0.0
            }
            
        wins = [t for t in self.trades if t.pnl_cash > 0]
        losses = [t for t in self.trades if t.pnl_cash <= 0]
        
        gross_profit = sum(t.pnl_cash for t in wins)
        gross_loss = abs(sum(t.pnl_cash for t in losses))
        net_profit = gross_profit - gross_loss
        net_return_pct = (net_profit / self.initial_capital) * 100.0
        
        win_rate = (len(wins) / total_trades) * 100.0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (999.0 if gross_profit > 0 else 0.0)
        
        total_commission = sum(t.commission for t in self.trades)
        
        # Max drawdown calculation
        peak = self.initial_capital
        max_dd_cash = 0.0
        max_dd_pct = 0.0
        
        for pt in self.equity_curve:
            eq = pt["equity"]
            if eq > peak:
                peak = eq
            dd_cash = peak - eq
            dd_pct = (dd_cash / peak) * 100.0 if peak > 0 else 0.0
            if dd_cash > max_dd_cash:
                max_dd_cash = dd_cash
            if dd_pct > max_dd_pct:
                max_dd_pct = dd_pct
                
        avg_win = (gross_profit / len(wins)) if wins else 0.0
        avg_loss = (gross_loss / len(losses)) if losses else 0.0
        expectancy = (net_profit / total_trades)
        
        return {
            "initial_capital": self.initial_capital,
            "final_equity": self.equity,
            "total_trades": total_trades,
            "win_trades": len(wins),
            "loss_trades": len(losses),
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_loss": round(gross_loss, 2),
            "net_profit": round(net_profit, 2),
            "net_return_pct": round(net_return_pct, 2),
            "max_drawdown_cash": round(max_dd_cash, 2),
            "max_drawdown_pct": round(max_dd_pct, 2),
            "avg_win": round(avg_win, 2),
            "avg_loss": round(avg_loss, 2),
            "expectancy_cash": round(expectancy, 2),
            "total_commission": round(total_commission, 2)
        }
