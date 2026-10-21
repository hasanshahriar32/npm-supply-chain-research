#!/usr/bin/env python3
"""Render publication-quality vector figures for Q1 Journal expansion with 100% TrueType/Type 42 fonts.

Zero Type 3 fonts invariant enforced via pdf.fonttype: 42.
Outputs to both manuscript/results/q1_journal/ and manuscript_q1/figures/.
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/npm-q1-matplotlib")
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["font.family"] = "sans-serif"
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "manuscript/results"
Q1_DIR = RESULTS / "q1_journal"
Q1_FIGS = ROOT / "manuscript_q1/figures"
Q1_DIR.mkdir(parents=True, exist_ok=True)
Q1_FIGS.mkdir(parents=True, exist_ok=True)


def plot_pareto_frontier(data):
    fig, ax = plt.subplots(figsize=(4.8, 3.8))
    fig.subplots_adjust(left=0.15, right=0.95, top=0.92, bottom=0.14)

    name_data = data["pareto_name_graph"]
    vc_data = data["pareto_version_continuous_graph"]
    alphas = [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]

    # Package-Projected Curve
    c_name = [name_data[str(a)]["100"]["C_pct"] for a in alphas]
    h_name = [name_data[str(a)]["100"]["H_pct"] for a in alphas]
    ax.plot(c_name, h_name, color="#0072b2", marker="o", markersize=5, linewidth=1.5,
            label="Package-Projected Graph (Budget 100)")

    # Version-Continuous Curve
    c_vc = [vc_data[str(a)]["100"]["C_pct"] for a in alphas]
    h_vc = [vc_data[str(a)]["100"]["H_pct"] for a in alphas]
    ax.plot(c_vc, h_vc, color="#d55e00", marker="s", markersize=5, linewidth=1.5, linestyle="--",
            label="Version-Continuous Graph (Budget 100)")

    # Annotate key points
    # Alpha = 0.50 sweet spot
    ax.scatter([name_data["0.5"]["100"]["C_pct"]], [name_data["0.5"]["100"]["H_pct"]],
               color="#009e73", s=100, zorder=5, marker="*")
    ax.annotate("Sweet Spot ($\\alpha=0.50$)\n70.0% C, 31.2% H",
                xy=(name_data["0.5"]["100"]["C_pct"], name_data["0.5"]["100"]["H_pct"]),
                xytext=(name_data["0.5"]["100"]["C_pct"] - 14, name_data["0.5"]["100"]["H_pct"] - 6),
                arrowprops=dict(arrowstyle="->", color="#009e73", lw=1.2),
                fontsize=8, fontweight="bold", color="#009e73")

    # Alpha = 0.0 (Exact Union)
    ax.annotate("Exact Union\n($\\alpha=0.0$)",
                xy=(name_data["0.0"]["100"]["C_pct"], name_data["0.0"]["100"]["H_pct"]),
                xytext=(name_data["0.0"]["100"]["C_pct"] - 4, name_data["0.0"]["100"]["H_pct"] + 4),
                arrowprops=dict(arrowstyle="->", color="#0072b2", lw=1),
                fontsize=7.5)

    # Alpha = 1.0 (Greedy Coverage)
    ax.annotate("Greedy\n($\\alpha=1.0$)",
                xy=(name_data["1.0"]["100"]["C_pct"], name_data["1.0"]["100"]["H_pct"]),
                xytext=(name_data["1.0"]["100"]["C_pct"] - 5, name_data["1.0"]["100"]["H_pct"] + 4),
                arrowprops=dict(arrowstyle="->", color="#0072b2", lw=1),
                fontsize=7.5)

    ax.set_xlabel("Distinct Workflow Repositories Covered $C(S)$ (%)", fontsize=9)
    ax.set_ylabel("Scenario Exposure Reduction $H(S)$ (%)", fontsize=9)
    ax.set_title("Multi-Objective Pareto Frontier: Coverage vs. Exposure", fontsize=10, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.set_xlim(58, 80)
    ax.set_ylim(8, 45)
    ax.legend(loc="lower left", fontsize=8, frameon=True)

    out_pdf = Q1_DIR / "q1_pareto_frontier.pdf"
    out_png = Q1_DIR / "q1_pareto_frontier.png"
    fig.savefig(out_pdf, metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(out_png, dpi=300)
    plt.close(fig)

    shutil.copyfile(out_pdf, Q1_FIGS / "q1_pareto_frontier.pdf")
    shutil.copyfile(out_png, Q1_FIGS / "q1_pareto_frontier.png")
    print(f"Generated Q1 Pareto figure: {out_pdf} and {Q1_FIGS / 'q1_pareto_frontier.pdf'}")


def plot_supermodular_and_weights(data):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.8))
    fig.subplots_adjust(left=0.08, right=0.96, top=0.88, bottom=0.15, wspace=0.28)

    # Panel 1: Direct P(S) optimization vs Baselines
    p_data = data["direct_p_optimization"]
    budgets = [10, 25, 50, 100]
    p_direct = [p_data[str(b)]["P"] for b in budgets]
    p_greedy = [data["pareto_name_graph"]["1.0"][str(b)]["P"] for b in budgets]
    p_union = [data["pareto_name_graph"]["0.0"][str(b)]["P"] for b in budgets]

    ax1.plot(budgets, p_direct, color="#d55e00", marker="o", linewidth=1.6, label="Direct Supermodular $P(S)$ Heuristic")
    ax1.plot(budgets, p_greedy, color="#009e73", marker="s", linewidth=1.4, linestyle="--", label="Greedy Coverage $P(S)$")
    ax1.plot(budgets, p_union, color="#0072b2", marker="D", linewidth=1.4, linestyle=":", label="Exact Union $P(S)$")

    ax1.annotate("$P = 1{,}022$\n(+27.8% vs Gr.)\n(+91.4% vs Un.)",
                 xy=(100, 1022), xytext=(72, 850),
                 arrowprops=dict(arrowstyle="->", color="#d55e00", lw=1.2),
                 fontsize=8, fontweight="bold", color="#d55e00")

    ax1.set_xlabel("Hardening Budget $|S|$ (Maintainers)", fontsize=9)
    ax1.set_ylabel("All-Source Fully Excluded Repositories $P(S)$", fontsize=9)
    ax1.set_title("(a) Supermodular Exclusion Optimization", fontsize=10, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.set_xlim(5, 105)
    ax1.set_ylim(250, 1100)
    ax1.legend(loc="upper left", fontsize=8)

    # Panel 2: Heterogeneous Weighting
    w_data = data["heterogeneous_weights"]
    categories = ["Exact Union", "Greedy Cov.", "Pareto (0.50)", "Weight-Aware\nSole", "Weight-Aware\nPkg-Sole"]
    strat_keys = ["Exact Union (Unweighted)", "Greedy Coverage", "Pareto Hybrid (alpha=0.50)",
                  "Weight-Aware Sole Optimum", "Weight-Aware Package-Sole Optimum"]

    h_uniform = [w_data[k]["H_uniform_pct"] for k in strat_keys]
    h_sole = [w_data[k]["H_sole_pct"] for k in strat_keys]
    h_pkg = [w_data[k]["H_pkg_sole_pct"] for k in strat_keys]

    x = range(len(categories))
    width = 0.25

    ax2.bar([i - width for i in x], h_uniform, width=width, label="Uniform ($H$)", color="#0072b2")
    ax2.bar(x, h_sole, width=width, label="Sole Maintainer ($H_{\\text{sole}}$)", color="#d55e00")
    ax2.bar([i + width for i in x], h_pkg, width=width, label="Pkg-Sole ($H_{\\text{pkg-sole}}$)", color="#009e73")

    ax2.set_xticks(list(x))
    ax2.set_xticklabels(categories, fontsize=7.5)
    ax2.set_ylabel("Exposure Reduction Mass (%)", fontsize=9)
    ax2.set_title("(b) Heterogeneous Risk Sensitivity (Budget 100)", fontsize=10, fontweight="bold")
    ax2.grid(axis="y", linestyle=":", alpha=0.6)
    ax2.set_ylim(0, 100)
    ax2.legend(loc="upper right", fontsize=8)

    out_pdf = Q1_DIR / "q1_supermodular_p_and_weights.pdf"
    out_png = Q1_DIR / "q1_supermodular_p_and_weights.png"
    fig.savefig(out_pdf, metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(out_png, dpi=300)
    plt.close(fig)

    shutil.copyfile(out_pdf, Q1_FIGS / "q1_supermodular_p_and_weights.pdf")
    shutil.copyfile(out_png, Q1_FIGS / "q1_supermodular_p_and_weights.png")
    print(f"Generated Q1 Supermodular & Weights figure: {out_pdf} and {Q1_FIGS / 'q1_supermodular_p_and_weights.pdf'}")


def main():
    json_path = RESULTS / "q1_journal_experiments.json"
    if not json_path.exists():
        raise SystemExit(f"Missing Q1 results JSON: {json_path}")
    data = json.loads(json_path.read_text())
    plot_pareto_frontier(data)
    plot_supermodular_and_weights(data)


if __name__ == "__main__":
    main()
