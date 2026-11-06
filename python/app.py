"""
HR Bloomberg Quant Terminal — Python Desktop Companion Dashboard
Part of the HR Unified Master OS
Platform: Python (Tkinter / Matplotlib / Pandas / NumPy)
"""

import os
import sys
import json
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------
# CORE ANALYTICAL QUANT CALCULATIONS
# -----------------------------------------------------------------------------
class QuantAnalytics:
    @staticmethod
    def calculate_ema(series: pd.Series, period: int) -> pd.Series:
        return series.ewm(span=period, adjust=False).mean()

    @staticmethod
    def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / (loss + 1e-9)
        return 100 - (100 / (1 + rs))

    @staticmethod
    def calculate_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
        ema_fast = series.ewm(span=fast, adjust=False).mean()
        ema_slow = series.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        hist = macd_line - signal_line
        return macd_line, signal_line, hist

    @staticmethod
    def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
        h = df['high']
        l = df['low']
        c_prev = df['close'].shift(1)
        tr = pd.concat([h - l, (h - c_prev).abs(), (l - c_prev).abs()], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()

    @staticmethod
    def calculate_candle_pressure(df: pd.DataFrame) -> float:
        if df.empty:
            return 50.0
        last = df.iloc[-1]
        rng = last['high'] - last['low']
        if rng <= 0:
            return 50.0
        return float(((last['close'] - last['low']) / rng) * 100.0)

    @staticmethod
    def calculate_rvol(df: pd.DataFrame, period: int = 20) -> float:
        if 'volume' not in df.columns or len(df) < period:
            return 1.0
        avg_vol = df['volume'].iloc[-period:].mean()
        if avg_vol <= 0:
            return 1.0
        return float(df['volume'].iloc[-1] / avg_vol)

    @staticmethod
    def evaluate_structure(df: pd.DataFrame):
        if len(df) < 20:
            return "CONSOLIDATION", "EQUILIBRIUM", 50
        last_c = df['close'].iloc[-1]
        hi_20 = df['high'].iloc[-20:].max()
        lo_20 = df['low'].iloc[-20:].min()
        eq = (hi_20 + lo_20) / 2.0
        zone = "DISCOUNT" if last_c < eq else "PREMIUM"
        
        e9 = QuantAnalytics.calculate_ema(df['close'], 9).iloc[-1]
        e21 = QuantAnalytics.calculate_ema(df['close'], 21).iloc[-1]
        e200 = QuantAnalytics.calculate_ema(df['close'], 200).iloc[-1] if len(df) >= 200 else e21
        
        structure = "BULLISH" if (e9 > e21 and e21 > e200) else "BEARISH" if (e9 < e21 and e21 < e200) else "MIXED"
        
        # Scoring
        score = 50
        if structure == "BULLISH":
            score += 25
        elif structure == "BEARISH":
            score += 25
        if zone == "DISCOUNT" and structure == "BULLISH":
            score += 15
        elif zone == "PREMIUM" and structure == "BEARISH":
            score += 15

        return structure, zone, score

# -----------------------------------------------------------------------------
# LAST CANDLE SNAPSHOT MANAGER
# -----------------------------------------------------------------------------
class LastCandleStore:
    def __init__(self, base_dir: str):
        self.target_dir = os.path.join(base_dir, "data", "last_candles")
        os.makedirs(self.target_dir, exist_ok=True)

    def save_snapshot(self, symbol: str, row: pd.Series, timeframe: str = "M5"):
        path = os.path.join(self.target_dir, f"{symbol}_last_candle.json")
        data = {
            "symbol": symbol,
            "time": str(row.get('time', datetime.datetime.now(datetime.timezone.utc).isoformat())),
            "open": float(row.get('open', 0.0)),
            "high": float(row.get('high', 0.0)),
            "low": float(row.get('low', 0.0)),
            "close": float(row.get('close', 0.0)),
            "volume": float(row.get('volume', 0.0)),
            "timeframe": timeframe,
            "source": "Python Analytics Engine",
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

# -----------------------------------------------------------------------------
# DESKTOP UI APPLICATION (BLOOMBERG LIGHT/METALLIC THEME)
# -----------------------------------------------------------------------------
class HRBloombergQuantTerminal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HR Bloomberg Quant Terminal — HR Unified Master OS")
        self.geometry("1200x820")
        self.configure(bg="#f8fafc")
        
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.candle_store = LastCandleStore(self.base_dir)
        
        self.symbols = ["XAUUSD", "XAGUSD", "US500", "USTEC", "DXY"]
        self.data_frames = {}
        
        self._setup_style()
        self._build_header()
        self._build_macro_strip()
        self._build_four_panels()
        self._build_bottom_ribbon()
        
        self._load_all_symbol_data()

    def _setup_style(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Header.TFrame", background="#0f172a")
        self.style.configure("Card.TFrame", background="#ffffff", relief="solid", borderwidth=1)

    def _build_header(self):
        hdr = tk.Frame(self, bg="#0f172a", height=50)
        hdr.pack(fill="x", side="top")
        
        tk.Label(hdr, text="HR BLOOMBERG QUANT TERMINAL", font=("Helvetica", 14, "bold"), fg="#ffffff", bg="#0f172a").pack(side="left", padx=15, pady=8)
        tk.Label(hdr, text="HR UNIFIED MASTER OS | QUANT", font=("Helvetica", 10, "bold"), fg="#38bdf8", bg="#0f172a").pack(side="left", padx=5)
        
        now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        self.lbl_time = tk.Label(hdr, text=f"TIME: {now_str} | SESSION: ACTIVE", font=("Helvetica", 9), fg="#94a3b8", bg="#0f172a")
        self.lbl_time.pack(side="right", padx=15)

    def _build_macro_strip(self):
        strip = tk.Frame(self, bg="#e2e8f0", height=32, highlightbackground="#cbd5e1", highlightthickness=1)
        strip.pack(fill="x", side="top", padx=10, pady=5)
        
        self.lbl_dxy = tk.Label(strip, text="DXY MACRO REGIME: INITIALIZING MARKET DATA...", font=("Helvetica", 9, "bold"), fg="#0f172a", bg="#e2e8f0")
        self.lbl_dxy.pack(side="left", padx=10, pady=4)

    def _build_four_panels(self):
        container = tk.Frame(self, bg="#f8fafc")
        container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.panels = {}
        row_cols = [(0, 0), (0, 1), (1, 0), (1, 1)]
        core_syms = ["XAUUSD", "XAGUSD", "US500", "USTEC"]
        
        for idx, sym in enumerate(core_syms):
            r, c = row_cols[idx]
            frame = tk.Frame(container, bg="#ffffff", highlightbackground="#cbd5e1", highlightthickness=1)
            frame.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
            container.grid_columnconfigure(c, weight=1)
            container.grid_rowconfigure(r, weight=1)
            
            # Card Header
            c_hdr = tk.Frame(frame, bg="#f1f5f9", height=28)
            c_hdr.pack(fill="x", side="top")
            tk.Label(c_hdr, text=sym, font=("Helvetica", 11, "bold"), fg="#0f172a", bg="#f1f5f9").pack(side="left", padx=8, pady=4)
            lbl_price = tk.Label(c_hdr, text="--.--", font=("Helvetica", 10, "bold"), fg="#475569", bg="#f1f5f9")
            lbl_price.pack(side="right", padx=8)
            
            # Content Box
            box = tk.Text(frame, bg="#ffffff", fg="#0f172a", font=("Consolas", 9), relief="flat", padx=8, pady=8)
            box.pack(fill="both", expand=True)
            box.insert("1.0", "Loading market analytics data...")
            box.config(state="disabled")
            
            self.panels[sym] = {"frame": frame, "price": lbl_price, "box": box}

    def _build_bottom_ribbon(self):
        ribbon = tk.Frame(self, bg="#0f172a", height=32)
        ribbon.pack(fill="x", side="bottom")
        
        self.lbl_ribbon = tk.Label(ribbon, text="MARKET RIBBON: XAUUSD -- | XAGUSD -- | US500 -- | USTEC -- | DXY --", font=("Helvetica", 9, "bold"), fg="#38bdf8", bg="#0f172a")
        self.lbl_ribbon.pack(side="left", padx=15, pady=6)

    def _load_all_symbol_data(self):
        data_dir = os.path.join(self.base_dir, "data")
        ribbon_texts = []
        
        for sym in self.symbols:
            csv_path = os.path.join(data_dir, f"{sym}_M5.csv")
            if os.path.exists(csv_path):
                try:
                    df = pd.read_csv(csv_path)
                    df.columns = [c.lower().strip() for c in df.columns]
                    self.data_frames[sym] = df
                    self._update_symbol_display(sym, df)
                    last_c = df['close'].iloc[-1]
                    ribbon_texts.append(f"{sym} {last_c:.2f}")
                    # Save Last Candle Snapshot
                    self.candle_store.save_snapshot(sym, df.iloc[-1])
                except Exception as e:
                    print(f"Error loading {csv_path}: {e}")
            else:
                if sym in self.panels:
                    self._set_panel_waiting(sym, csv_path)
                ribbon_texts.append(f"{sym} [NO CSV]")
        
        self.lbl_ribbon.config(text="MARKET RIBBON: " + "  ●  ".join(ribbon_texts))
        
        if "DXY" in self.data_frames:
            dxy_df = self.data_frames["DXY"]
            struct, zone, _ = QuantAnalytics.evaluate_structure(dxy_df)
            last_c = dxy_df['close'].iloc[-1]
            self.lbl_dxy.config(text=f"DXY MACRO REGIME: {last_c:.2f} | BIAS: {struct} | ZONE: {zone}")

    def _update_symbol_display(self, sym: str, df: pd.DataFrame):
        if sym not in self.panels:
            return
        
        last_c = df['close'].iloc[-1]
        e9 = QuantAnalytics.calculate_ema(df['close'], 9).iloc[-1]
        e21 = QuantAnalytics.calculate_ema(df['close'], 21).iloc[-1]
        e200 = QuantAnalytics.calculate_ema(df['close'], 200).iloc[-1] if len(df) >= 200 else e21
        rsi = QuantAnalytics.calculate_rsi(df['close'], 14).iloc[-1]
        atr = QuantAnalytics.calculate_atr(df, 14).iloc[-1]
        press = QuantAnalytics.calculate_candle_pressure(df)
        rvol = QuantAnalytics.calculate_rvol(df)
        struct, zone, score = QuantAnalytics.evaluate_structure(df)
        
        self.panels[sym]["price"].config(text=f"{last_c:.2f}", fg="#15803d" if struct == "BULLISH" else "#b91c1c")
        
        details = (
            f"M5 EXECUTION / H1 FILTER: {struct}\n"
            f"EMA 9/21/200           : {e9:.2f} / {e21:.2f} / {e200:.2f}\n"
            f"RSI (14) / ATR (14)    : {rsi:.1f} / {atr:.2f}\n"
            f"CANDLE PRESSURE / RVOL : {press:.0f}% / {rvol:.2f}x\n"
            f"DEALING RANGE ZONE     : {zone}\n"
            f"STRUCTURE ALIGNMENT    : {struct}\n"
            f"ANALYTICAL CONFIDENCE  : {score}/100\n"
            f"RECOMMENDED SETUP      : {'BUY SETUP' if struct == 'BULLISH' and zone == 'DISCOUNT' else 'SELL SETUP' if struct == 'BEARISH' and zone == 'PREMIUM' else 'WATCH'}\n"
        )
        
        box = self.panels[sym]["box"]
        box.config(state="normal")
        box.delete("1.0", "end")
        box.insert("1.0", details)
        box.config(state="disabled")

    def _set_panel_waiting(self, sym: str, expected_path: str):
        box = self.panels[sym]["box"]
        box.config(state="normal")
        box.delete("1.0", "end")
        box.insert("1.0", f"Awaiting market candle data.\nPlace {os.path.basename(expected_path)} in data/ folder.\n\nRequired columns:\ntime,open,high,low,close,volume")
        box.config(state="disabled")

if __name__ == "__main__":
    app = HRBloombergQuantTerminal()
    app.mainloop()
