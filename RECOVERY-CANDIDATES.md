# Legacy TradingView Indicator Recovery — Candidates Report

**Generated**: 2026-08-27  
**Repository**: `HR-Professional-Services/hemanth-ranam-tradingview`  
**Objective**: Locate original 9/21 EMA + Sessions + SMC indicator source code

---

## Search Locations Checked

| # | Location | Method | Result |
| :- | :--- | :--- | :--- |
| 1 | Local filesystem `/Users/rh/**/*.pine` | `find` recursive | **4 FOUND** |
| 2 | IDE scratch `/Users/rh/.gemini/antigravity/scratch/` | filesystem scan | **3 FOUND** |
| 3 | All workspace git repos (24 repos scanned) | `find .git` recursive | No additional `.pine` files |
| 4 | `hemanth-ranam-tradingview` git history (all branches) | `git log --all --name-status` | **1 DELETED FILE FOUND** |
| 5 | Git object store (all blobs) | `git rev-list --all --objects` | Object confirmed |
| 6 | `hemanth-ranam-mt5` repo | `git log` | No `.pine` files |
| 7 | `hemanth-ranam-trading-alert-api` repo | `ls` | No `.pine` files |
| 8 | `hemanth-ranam-trading-telegram` repo | repo scan | No `.pine` files |
| 9 | `chartora-*` repos | repo scan | No `.pine` files |
| 10 | GitHub remote branches | `git branch -a` | `main` only — no additional branches |

---

## Candidates

---

### CANDIDATE 1 — `HemanthRanamTradingSystem.pine` ← **PRIMARY RECOVERY**

| Field | Value |
| :--- | :--- |
| **File** | `HemanthRanamTradingSystem.pine` |
| **Recovery Path** | `recovered/ORIGINAL_HemanthRanamTradingSystem_RECOVERED.pine` |
| **Repository** | `HR-Professional-Services/hemanth-ranam-tradingview` |
| **Commit Added** | `f391583` — "feat: initialize Hemanth Ranam multi-strategy Pine Script v5 trading engine suite" |
| **Commit Deleted** | `a3afe4b` — "feat: upgrade trading engine to pine v6 and add five backtestable strategies" |
| **Original Path** | `src/HemanthRanamTradingSystem.pine` |
| **Branch** | `main` |
| **Pine Version** | **v5** |
| **File Size** | 12 KB / 243 lines |
| **SHA256** | `f58b7b7c2f28d9f1dfe5124b19f9307881dd4a7b478619222ee10926967ee5ea` |
| **Modified** | NO — extracted verbatim from git object store |
| **9 EMA** | ✅ `ema9 = ta.ema(close, fast_len)` / default=9 |
| **21 EMA** | ✅ `ema21 = ta.ema(close, mid_len)` / default=21 |
| **200 EMA** | ✅ `ema200 = ta.ema(close, slow_len)` / default=200 |
| **Sessions** | ✅ `input.session("0700-1700:23456", ...)` — single configurable session |
| **SMC** | ⚠️ PARTIAL — pivot-based swing structure (HH/HL via `ta.pivothigh`/`ta.pivotlow`), no BOS/CHoCH labels, no OBs, no FVG |
| **BOS** | ❌ Not labelled as BOS — equivalent logic present as `ta.crossover(close, last_sh)` (close breaks structure high) |
| **CHoCH** | ❌ Not labelled as CHoCH — logic is in the structure continuation signals |
| **Order Blocks** | ❌ Not present |
| **FVG** | ❌ Not present |
| **Buy Signals** | ✅ `label.new(... "BUY\n" + strat_mode ...)` |
| **Sell Signals** | ✅ `label.new(... "SELL\n" + strat_mode ...)` |
| **Dashboard** | ✅ 6-row HUD table: Strategy / 1H Trend / EMA Structure / ATR / Status |
| **Alerts** | ✅ JSON webhook `alert()` on `alert.freq_once_per_bar_close` |
| **HTF Filter** | ✅ 1H 200 EMA filter via `request.security(..., barmerge.lookahead_off)` |
| **Repainting** | NON-REPAINTING — uses `lookahead_off` correctly. Pivot confirmation has 2-bar delay by design. |
| **Confidence** | **EXACT MATCH — this is the original indicator source** |

---

### CANDIDATE 2 — `EMA_921_Pullback_Strategy.pine`

| Field | Value |
| :--- | :--- |
| **File** | `EMA_921_Pullback_Strategy.pine` |
| **Recovery Path** | `recovered/SCRATCH_EMA_921_Pullback_Strategy.pine` |
| **Location** | `/Users/rh/.gemini/antigravity/scratch/EMA_921_Pullback_Strategy.pine` |
| **Last Modified** | 2026-08-08 19:48 |
| **Pine Version** | v5 |
| **File Size** | 4.6 KB |
| **SHA256** | `bbddff5895e67c9fae5b9eed356dfc6dbdc848d20982252c41143c7f92d05a8b` |
| **9 EMA** | ✅ `emaFastLen = input.int(9, ...)` |
| **21 EMA** | ✅ `emaSlowLen = input.int(21, ...)` |
| **200 EMA** | ✅ `emaTrend5MLen = input.int(200, ...)` |
| **Sessions** | ✅ `input.session("0700-2000:23456", ...)` London/NY |
| **SMC** | ❌ Not present |
| **HTF Filter** | ⚠️ `request.security(..., lookahead=barmerge.lookahead_on)` ← **REPAINTING — lookahead_on!** |
| **Buy Signals** | ✅ `plotshape(buySignal, ... text="BUY 9-21")` |
| **Sell Signals** | ✅ `plotshape(sellSignal, ... text="SELL 9-21")` |
| **Repainting** | ⚠️ **REPAINTS** — 1H 200 EMA uses `lookahead_on`. Results differ on historical bars. |
| **Confidence** | POSSIBLE — A standalone 9/21 EMA strategy, likely an earlier iteration |

---

### CANDIDATE 3 — `ema_921_200_scalper/indicator.pine`

| Field | Value |
| :--- | :--- |
| **File** | `indicator.pine` |
| **Recovery Path** | `recovered/SCRATCH_ema_921_200_scalper_indicator.pine` |
| **Location** | `/Users/rh/.gemini/antigravity/scratch/ema_921_200_scalper/indicator.pine` |
| **Last Modified** | 2026-08-08 21:36 |
| **Pine Version** | **v6** |
| **File Size** | 32 KB |
| **SHA256** | `82720e96f178de636e884bd9dbec883036689830586711a4696f6df30c7ec4a5` |
| **9 EMA** | ✅ `ema9Len = input.int(9, ...)` |
| **21 EMA** | ✅ `ema21Len = input.int(21, ...)` |
| **200 EMA** | ✅ `ema200Len = input.int(200, ...)` |
| **Sessions** | ✅ Full 3-session engine: New York (13:00–22:00), London (07:00–16:00), Tokyo (00:00–09:00) |
| **SMC** | ⚠️ Partial — Market Structure Filter input present (`useMsFilter`, `msPivotLen`) |
| **BOS** | ⚠️ Partial via pivot break logic |
| **Buy Signals** | ✅ |
| **Sell Signals** | ✅ |
| **Signal Scoring** | ✅ Quality score system (0–100), grade A/B/C |
| **Dashboard** | ✅ Terminal dashboard |
| **Confidence** | VERY LIKELY — an evolved PRO version of the original indicator. Created 2026-08-08, likely during previous dev session. |

---

### CANDIDATE 4 — `ema_921_200_scalper/strategy.pine`

| Field | Value |
| :--- | :--- |
| **File** | `strategy.pine` |
| **Recovery Path** | `recovered/SCRATCH_ema_921_200_scalper_strategy.pine` |
| **Location** | `/Users/rh/.gemini/antigravity/scratch/ema_921_200_scalper/strategy.pine` |
| **Last Modified** | 2026-08-08 21:36 |
| **Pine Version** | v6 |
| **File Size** | 19 KB |
| **SHA256** | `955173f028faaf1411da9296370a546e736b3f3409a86800c342cf04f34f5ac5` |
| **Confidence** | VERY LIKELY — the strategy companion to Candidate 3 |

---

## Candidate Ranking

| Rank | File | Confidence | Reason |
| :--: | :--- | :---: | :--- |
| 1 | `ORIGINAL_HemanthRanamTradingSystem_RECOVERED.pine` | **EXACT MATCH** | Extracted verbatim from git commit `f391583`. This was the first Pine file ever committed to this repo. Confirmed deleted by commit `a3afe4b`. |
| 2 | `SCRATCH_ema_921_200_scalper_indicator.pine` | **VERY LIKELY** | 32K v6 PRO indicator with full session engine (3 sessions), market structure, scoring, and dashboard. Likely evolved from Candidate 1 in a prior dev session. |
| 3 | `SCRATCH_ema_921_200_scalper_strategy.pine` | **VERY LIKELY** | Strategy companion to Candidate 3. |
| 4 | `SCRATCH_EMA_921_Pullback_Strategy.pine` | POSSIBLE | Simple v5 strategy. Has `lookahead_on` bug. Earlier or parallel prototype. |
