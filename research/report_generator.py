#!/usr/bin/env python3
"""
HEMANTH RANAM TRADINGVIEW STRATEGY SUITE
Automated Validation Report Generator

Reads all normalised JSON result files from research/results/
and generates:
  - VALIDATION-REPORT.md   (human-readable)
  - validation-results.json (machine-readable)

Usage:
  python research/report_generator.py
"""

import json
import os
import glob
from datetime import datetime

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
REPO_ROOT   = os.path.dirname(__file__)


def load_results() -> list:
    pattern = os.path.join(RESULTS_DIR, "*.json")
    results = []
    for f in glob.glob(pattern):
        try:
            with open(f) as fp:
                results.append(json.load(fp))
        except Exception as e:
            print(f"[WARN] Could not load {f}: {e}")
    return results


def validation_status_label(status: str) -> str:
    labels = {
        "SIMULATED":          "🟡 SIMULATED",
        "NATIVE-TV-PENDING":  "🔵 NATIVE-TV PENDING",
        "NATIVE-TV-VERIFIED": "🟢 NATIVE-TV VERIFIED",
        "OOS-VERIFIED":       "🟢 OOS VERIFIED",
        "FORWARD-TESTING":    "🟢 FORWARD TESTING",
        "PAPER-TRADING":      "🟢 PAPER TRADING",
        "LIVE-ELIGIBLE":      "✅ LIVE ELIGIBLE",
        "REJECTED":           "🔴 REJECTED",
    }
    return labels.get(status, f"❓ {status}")


def generate_markdown(results: list) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Hemanth Ranam TradingView Strategy Suite — Validation Report",
        f"\n**Generated**: {now}  ",
        "**Source**: Automated from `research/results/*.json`  ",
        "\n> ⚠️ Results marked `SIMULATED` are from the custom Python engine and are research evidence only — not native TradingView measurements.",
        "\n---",
        "\n## Master Results Table",
        "\n| Strategy | Symbol | TF | Period | Trades | PF | Win % | Expectancy | DD % | Scenario | Status |",
        "| :--- | :---: | :---: | :--- | ---: | ---: | ---: | ---: | ---: | :---: | :--- |",
    ]

    if not results:
        lines.append("| — | — | — | — | N/A | N/A | N/A | N/A | N/A | — | **NO RESULTS IMPORTED YET** |")
        lines.append("\n> No result files found in `research/results/`. Import TradingView CSV exports using `research/scripts/tv_importer.py`.")
    else:
        for r in sorted(results, key=lambda x: x.get("strategy", "")):
            pf   = r.get("profit_factor");  pf_str   = f"{pf:.2f}" if pf is not None else "N/A"
            wr   = r.get("win_rate");        wr_str   = f"{wr:.1f}%" if wr is not None else "N/A"
            exp  = r.get("expectancy");      exp_str  = f"{exp:.3f}" if exp is not None else "N/A"
            dd   = r.get("max_drawdown_pct");dd_str   = f"{dd:.2f}%" if dd is not None else "N/A"
            tr   = r.get("total_trades",  "N/A")
            period = f"{r.get('period_start','?')} – {r.get('period_end','?')}"
            status = validation_status_label(r.get("validation_status", "SIMULATED"))
            lines.append(f"| {r['strategy']} | {r['symbol']} | {r['timeframe']} | {period} | {tr} | {pf_str} | {wr_str} | {exp_str} | {dd_str} | {r.get('cost_scenario','?')} | {status} |")

    lines += [
        "\n---",
        "\n## Strategy Validation Status",
        "\n| Strategy | Simulation | Native TV | OOS | Forward | Current Stage |",
        "| :--- | :---: | :---: | :---: | :---: | :--- |",
        "| HR_EMA_Pullback_Pro        | ✅ COMPLETE | ⏳ PENDING | ⏳ PENDING | ⏳ PENDING | **NATIVE-TV-PENDING** |",
        "| HR_Breakout_Retest_Pro     | ✅ COMPLETE | ⏳ PENDING | ⏳ PENDING | ⏳ PENDING | **NATIVE-TV-PENDING** |",
        "| HR_Market_Structure_Pro    | ✅ COMPLETE | ⏳ PENDING | ⏳ PENDING | ⏳ PENDING | **NATIVE-TV-PENDING** |",
        "| HR_VWAP_Mean_Reversion_Pro | ✅ COMPLETE | ⏳ PENDING | ⏳ PENDING | ⏳ PENDING | **NATIVE-TV-PENDING** |",
        "| HR_Momentum_Volatility_Pro | ✅ COMPLETE | ⏳ PENDING | ⏳ PENDING | ⏳ PENDING | **NATIVE-TV-PENDING** |",
        "\n---",
        "\n## How to Advance Validation",
        "\n1. Complete native TradingView testing following `docs/TRADINGVIEW-TEST-PROTOCOL.md`.",
        "2. Export 'List of Trades' CSV for each strategy/symbol/timeframe combination.",
        "3. Import using: `python research/scripts/tv_importer.py --csv <file> --strategy <name> ...`",
        "4. Re-run this report generator: `python research/report_generator.py`",
    ]

    return "\n".join(lines)


def main():
    results = load_results()
    print(f"[REPORT GENERATOR] Loaded {len(results)} result file(s).")

    md = generate_markdown(results)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    report_md = os.path.join(REPO_ROOT, "..", "VALIDATION-REPORT.md")
    with open(report_md, "w") as f:
        f.write(md)
    print(f"[REPORT GENERATOR] Written: VALIDATION-REPORT.md")

    machine_out = os.path.join(REPORTS_DIR, "validation-results.json")
    with open(machine_out, "w") as f:
        json.dump({
            "generated_at": datetime.utcnow().isoformat(),
            "total_results": len(results),
            "results": results,
        }, f, indent=2)
    print(f"[REPORT GENERATOR] Written: research/reports/validation-results.json")


if __name__ == "__main__":
    main()
