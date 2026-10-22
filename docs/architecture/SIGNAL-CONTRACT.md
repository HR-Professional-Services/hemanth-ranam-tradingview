# HR TradingView — Signal Contract

**Version**: 1.0  
**Applies to**: All `src/indicators/` commercial indicator files  
**Last Updated**: 2026-10-22

---

## 1. What a Signal Is

A **BUY** or **SELL** signal from any HR TradingView indicator represents a specific, algorithmically defined condition being met at bar close. It is a notification that a configured setup has occurred based on historical price and indicator data.

A signal is **not**:
- A trade recommendation
- A guarantee of profitability
- Financial advice
- A guaranteed future outcome

---

## 2. Bar Confirmation Standard

All signals across every HR TradingView commercial indicator fire **only on confirmed closed bars**.

Implementation: `barstate.isconfirmed` is required to be `true` before any signal is emitted.

This means:
- No signal will fire mid-bar during live trading
- Historical signal markers are stable and do not move after the bar closes
- The signal you see in history is what would have appeared in real time at bar close

**Intrabar dashboard values** (EMA health score, quality score, trend state) may update during a live bar but will not trigger a signal label or alert until confirmation.

---

## 3. Higher-Timeframe Security Standard

All HTF data requests use the closed-bar pattern:

```pine
float htf200   = request.security(syminfo.tickerid, htfTF, ta.ema(close, htfEmaLen)[1], barmerge.gaps_off, barmerge.lookahead_off)
float htfClose = request.security(syminfo.tickerid, htfTF, close[1], barmerge.gaps_off, barmerge.lookahead_off)
```

- `[1]` indexing: requests the **previous confirmed HTF bar's value** — never the unclosed current HTF bar
- `lookahead_off`: prevents Pine Script from peeking at future bar data during historical calculation
- Result: HTF values used in signals reflect only information that was available at signal time

---

## 4. Pivot-Based Calculations

Where market structure uses `ta.pivothigh()` or `ta.pivotlow()`:

```pine
ph = ta.pivothigh(high, leftBars, rightBars)
```

A pivot high with `rightBars = N` is confirmed only **N bars after the actual high** occurs. This is an inherent property of pivot calculations — not a bug.

Implications:
- Market structure signals based on pivots have an inherent N-bar confirmation delay
- This delay is intentional and prevents false structure identification
- Documentation for each indicator states the exact `rightBars` value used

---

## 5. Signal Cooldown Mechanism

To prevent repeated signals in the same trend phase, all indicators use an EMA crossover-driven state machine:

```pine
var bool waitBuy  = false
var bool waitSell = false

if ta.crossover(ema9, ema21)
    waitBuy  := true
    waitSell := false
if ta.crossunder(ema9, ema21)
    waitSell := true
    waitBuy  := false

// Signal fires only once per trend phase, then resets
if buySignal
    waitBuy := false
```

One signal per trend phase per direction. Prevents alert spam.

---

## 6. Quality Score Definition

Every indicator includes a Quality Score (0–100) calculated from weighted components:

| Component | Weight | Criteria |
|:---|:---:|:---|
| EMA Health Score | 25% | Slope, stacking, gap ratio, position |
| EMA Structure | 20% | Full stack (9>21>200) vs partial alignment |
| HTF Confirmation | 20% | HTF close vs HTF EMA alignment |
| Candle Pattern | 15% | Engulfing / rejection wick quality |
| Market Structure | 10% | Pivot-based structural confirmation |
| Session Window | 10% | Signal within preferred session |

Grades:
- **A+** = Score ≥ 90
- **A** = Score ≥ 75
- **B** = Score ≥ 60
- **C** = Score < 60

Minimum entry score and grade are configurable inputs. The score reflects confluence — more conditions aligned = higher score.

---

## 7. Alert Payload Format

All indicators emit structured alert messages with `alert.freq_once_per_bar_close`.

Standard format:
```
SYMBOL | TIMEFRAME | DIRECTION | Grade: X | Quality Score: NN | EMA Health: NN | 5M: STATE | 1H: STATE | Session: NAME
```

Example:
```
XAUUSD | 5 | BUY | Grade: A+ | Quality Score: 87 | EMA Health: 92 | 5M: STRONG BULL | 1H: BULL | Session: London
```

Future webhook JSON payloads (planned for v2.0) will follow `research/schema/alert-payload.schema.json`.

---

## 8. Indicator vs Strategy Distinction

| Attribute | `indicator()` (src/indicators/) | `strategy()` (src/strategies/) |
|:---|:---|:---|
| Purpose | Chart visualization, signal alerts | Historical backtesting, performance metrics |
| Orders | None — reference levels only | Simulated entry/exit orders |
| Backtestable | No | Yes, via Strategy Tester |
| Live alerts | Yes | Yes (but strategy alerts fire differently) |
| Performance stats | None | Win rate, PF, drawdown (simulation only) |

Do not interpret indicator signal frequency or visual history as a backtest result.

---

## 9. What This Contract Does Not Guarantee

- Native TradingView compilation (must be verified manually by user in Pine Editor)
- Profitable outcomes in live trading
- Accuracy of ATR-based SL/TP levels as executable broker orders
- Behavior on all brokers, data feeds, or symbol types without user testing
