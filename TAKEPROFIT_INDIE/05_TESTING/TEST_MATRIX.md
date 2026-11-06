# Indie v5 Static Code & Rule Verification Suite

This test suite performs rigorous AST and Indie v5 rule verification against the official TakeProfit documentation:
1. `# indie:lang_version = 5` present as line 1
2. No banned imports (`numpy`, `pandas`, `requests`, `os`, `sys`)
3. Only documented `indie` packages imported (`indie`, `indie.algorithms`, `indie.plot`, `indie.color`, `indie.param`)
4. Explicit parameter declarations with valid min/max/step/title/options
5. Closed bar indexing check: Signals evaluate on confirmed bars index `[1]`, avoiding repainting
6. Proper use of `MutSeriesF.new(init=...)` for state persistence
7. Valid plot count matching decorator declarations

## Verification Results
| Indicator File | Syntax / AST | Line 1 Version | Import Guard | Index [1] Closed Bar | MutSeries State | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `HR_9_EMA_BUY_SELL.indie` | PASSED | `# indie:lang_version = 5` | Clean | Verified | Verified | **PASS** |
| `HR_9_21_200_EMA_PULLBACK.indie` | PASSED | `# indie:lang_version = 5` | Clean | Verified | Verified | **PASS** |
| `HR_LIQUIDITY_SWEEP.indie` | PASSED | `# indie:lang_version = 5` | Clean | Verified | Verified | **PASS** |
| `HR_MARKET_STRUCTURE_BOS_CHOCH.indie` | PASSED | `# indie:lang_version = 5` | Clean | Verified | Verified | **PASS** |
| `HR_VOLATILITY_EXPANSION_BREAKOUT.indie` | PASSED | `# indie:lang_version = 5` | Clean | Verified | Verified | **PASS** |
