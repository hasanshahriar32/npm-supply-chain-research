#!/usr/bin/env python3
"""Render publication figures from aggregate audit output; no external data."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

PAPER = Path(__file__).resolve().parents[1]
data = json.loads((PAPER / "results/artifact_audit.json").read_text())
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 8,
    "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42,
    "ps.fonttype": 42, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7})
blue, gold = "#1a436b", "#a86618"

fig, ax = plt.subplots(figsize=(3.5, 2.55), layout="constrained")
fields = ["blast_radius", "direct_dependents_with_workflows", "transitive_dependents"]
labels = ["Workflow\nreach", "Workflow direct\ndependents", "Transitive\ndependents"]
positions = list(range(3))
for offset, key, label, color in [(-.18, "csv_summary", "CSV archive", gold), (.18, "database_summary", "SQLite archive", blue)]:
    counts = [data[key][f]["nonzero"] for f in fields]
    bars = ax.bar([p+offset for p in positions], counts, .34, color=color, label=label)
    for bar, value in zip(bars, counts):
        ax.annotate(f"{value:,}", (bar.get_x()+bar.get_width()/2, value), xytext=(0,3),
                    textcoords="offset points", ha="center", fontsize=6)
ax.set_xticks(positions, labels)
ax.set_ylabel("Packages with a positive value")
ax.set_ylim(0, 27000)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x/1000)}k"))
ax.legend(frameon=False, loc="upper left", fontsize=7)
for suffix in ["pdf", "png"]:
    fig.savefig(PAPER/f"figures/artifact_comparison.{suffix}", dpi=240)
plt.close(fig)

fig, ax = plt.subplots(figsize=(3.5, 2.4), layout="constrained")
sweep = data["weight_sweep"]
ax.plot([r["alpha"] for r in sweep], [r["jaccard"] for r in sweep], "o-", color=blue, linewidth=1.4, markersize=3)
ax.set(xlabel=r"Maintainer coefficient $\alpha$", ylabel="Cross-archive Jaccard overlap", xlim=(-.02,1.02), ylim=(0,1.07))
ax.grid(axis="y", color=".9", linewidth=.5)
ax.annotate("Equal weight", xy=(.5,sweep[5]["jaccard"]), xytext=(.27,.52), fontsize=7,
    arrowprops={"arrowstyle":"->", "color":gold}, color=gold)
for suffix in ["pdf", "png"]:
    fig.savefig(PAPER/f"figures/weight_sensitivity.{suffix}", dpi=240)
plt.close(fig)
print("Rendered two figures (PDF and PNG).")
