#!/usr/bin/env python3
"""Render publication figures from the completed structural experiments.

No new observations or estimates are invented here. All marks come from
results/structural_interventions/results.json; an adjacent manifest records
the source hash and the rows used. Run from any working directory.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, FixedLocator, NullLocator


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/structural_interventions/results.json"
FIGURES = ROOT / "figures"
ENDPOINT = "workflow_repositories"
BUDGETS = [1, 5, 10, 25, 50, 100]

METHODS = {
    "greedy_coverage": ("Greedy coverage", "#007F84", "o", "-"),
    "exact_union": ("Exact union", "#2D6085", "s", "-"),
    "max_package_reach": ("Maximum reach", "#CC79A7", "^", "--"),
    "sum_package_reach": ("Sum of reach", "#D55E00", "D", "-."),
    "portfolio": ("Portfolio size", "#B78020", "v", ":"),
}
INK = "#20374B"
MUTED = "#596D7C"
GRID = "#E2E7EB"
BLUE = "#2D6085"
TEAL = "#007F84"
GOLD = "#B78020"
PALE = "#F3F6F8"


def configure() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8,
        "axes.titleweight": "bold",
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "axes.edgecolor": "#B8C2CB",
        "axes.linewidth": 0.6,
        "grid.color": GRID,
        "grid.linewidth": 0.55,
        "axes.axisbelow": True,
        "lines.linewidth": 1.35,
        "lines.markersize": 3.2,
        "legend.fontsize": 7,
        "legend.frameon": False,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "svg.hashsalt": "npm-maintainer-analysis-20261020",
    })


def clean(ax: plt.Axes, *, grid: str = "y") -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(length=2.4, width=0.6, pad=3)
    ax.grid(axis=grid)


def save(fig: plt.Figure, name: str) -> dict:
    """Keep designed physical dimensions; never tighten away the page margins."""
    FIGURES.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for extension in ("pdf", "svg", "png"):
        path = FIGURES / f"{name}.{extension}"
        metadata = ({"CreationDate": None, "ModDate": None, "Creator": "Research figure renderer"}
                    if extension == "pdf" else {"Date": None} if extension == "svg" else None)
        fig.savefig(path, dpi=300, metadata=metadata)
        outputs[extension] = {
            "path": str(path.relative_to(ROOT)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
    width, height = fig.get_size_inches()
    plt.close(fig)
    return {"width_inches": float(width), "height_inches": float(height), "outputs": outputs}


def selected_rows(data: dict, key: str, **conditions) -> list[dict]:
    return [r for r in data[key] if r["endpoint"] == ENDPOINT
            and all(r.get(k) == value for k, value in conditions.items())]


def objective_tradeoff(data: dict, manifest: dict) -> None:
    rows = selected_rows(data, "deterministic_curves")
    random_rows = sorted(selected_rows(data, "random_analytic_expectations"), key=lambda r: r["budget"])
    assert [r["budget"] for r in random_rows] == BUDGETS
    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.15))
    fig.subplots_adjust(left=0.070, right=0.977, bottom=0.340, top=0.87, wspace=0.34)
    specifications = [
        ("coverage_fraction_observed", "expected_coverage_fraction_observed", "(a) Review coverage", "Repositories covered (%)", [0, 20, 40, 60, 80], 88),
        ("scenario_exposure_reduction_fraction", "expected_scenario_exposure_reduction_fraction", "(b) Conditional exposure reduction", "Exposure removed (%)", [0, 10, 20, 30, 40], 41),
    ]
    handles = []
    for panel, (ax, (metric, random_metric, title, ylabel, ticks, upper)) in enumerate(zip(axes, specifications)):
        clean(ax)
        ax.set_xscale("log")
        ax.xaxis.set_major_locator(FixedLocator(BUDGETS))
        ax.xaxis.set_minor_locator(NullLocator())
        ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}"))
        ax.set(xlim=(0.86, 200), ylim=(0, upper), yticks=ticks, xlabel="Selected maintainer identities (log scale)", ylabel=ylabel)
        ax.set_title(title, loc="left", pad=8)
        for method, (label, color, marker, linestyle) in METHODS.items():
            curve = sorted((r for r in rows if r["method"] == method), key=lambda r: r["budget"])
            assert [r["budget"] for r in curve] == BUDGETS
            line, = ax.plot(BUDGETS, [100 * r[metric] for r in curve], label=label,
                            color=color, marker=marker, linestyle=linestyle,
                            markeredgewidth=0.6, markeredgecolor="white")
            if panel == 0:
                handles.append(line)
            if (panel == 0 and method == "greedy_coverage") or (panel == 1 and method == "exact_union"):
                value = 100 * curve[-1][metric]
                ax.annotate(f"{value:.1f}%", (100, value), xytext=(5, 2), textcoords="offset points",
                            color=color, fontsize=7.2, weight="bold", va="center")
        random_line, = ax.plot(BUDGETS, [100 * r[random_metric] for r in random_rows],
                               color="#7B838A", linestyle=(0, (3, 2)), marker="x",
                               linewidth=1.15, markersize=3, label="Uniform random (exact mean)")
        if panel == 0:
            handles.append(random_line)
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.52, 0.012), ncol=3,
               columnspacing=2.1, handlelength=2.6, handletextpad=0.7, labelspacing=0.6)
    manifest["objective_tradeoff"] = {
        **save(fig, "objective_tradeoff"),
        "deterministic_rows": rows,
        "analytic_random_rows": random_rows,
        "coverage_denominator": data["population"]["workflow_positive_repositories"],
        "conditional_exposure_denominator": data["diagnostics"][ENDPOINT]["total_identity_endpoint_pairs"],
        "interpretation": "Exact expectations are analytic random-design means, not confidence intervals; exposure assumes a fixed equal-identity single-source prior and perfect source hardening.",
    }


def coverage_partition(data: dict, manifest: dict) -> None:
    rows = selected_rows(data, "deterministic_curves", budget=100)
    by_method = {r["method"]: r for r in rows}
    order = ["greedy_coverage", "exact_union", "max_package_reach", "sum_package_reach", "portfolio"]
    total = data["population"]["workflow_positive_repositories"]
    reachable = data["diagnostics"][ENDPOINT]["reachable_endpoints"]
    excluded = total - reachable
    assert total == 7171 and reachable == 7158 and excluded == 13
    fig, ax = plt.subplots(figsize=(3.45, 2.10))
    fig.subplots_adjust(left=0.300, right=0.974, bottom=0.385, top=0.816)
    segments = []
    for y, method in enumerate(order):
        row = by_method[method]
        covered, all_selected = row["covered_endpoints"], row["fully_protected_endpoints"]
        other = covered - all_selected
        outside = reachable - covered
        assert 0 <= all_selected <= covered <= reachable
        assert row["covered_but_residually_exposed_endpoints"] == other
        assert all_selected + other + outside + excluded == total
        ax.barh(y, all_selected, height=0.58, color=GOLD, zorder=2)
        ax.barh(y, other, left=all_selected, height=0.58, color=BLUE, alpha=0.86, zorder=2)
        ax.barh(y, outside, left=covered, height=0.58, color="#E8ECEF", zorder=2)
        ax.text(all_selected / 2, y, f"{all_selected}", ha="center", va="center", color="#152B3B", fontsize=6.0)
        ax.text(covered + 95, y, f"{covered:,}", va="center", color=INK, fontsize=7)
        segments.append({"method": method, "all_sources_selected": all_selected,
                         "other_covered": other, "uncovered_reachable": outside,
                         "no_observed_source_excluded": excluded, "covered_total": covered})
    ax.set(yticks=range(len(order)), yticklabels=[METHODS[m][0] for m in order],
           xlim=(0, reachable), xticks=[0, 2000, 4000, 6000], ylim=(4.6, -0.65), xlabel="Reachable repositories (count)")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
    clean(ax, grid="x")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=6)
    fig.text(0.035, 0.935, "Coverage and remaining source paths", fontsize=8.2, weight="bold")
    fig.text(0.035, 0.860, "Budget 100 · 7,158 repositories with an observed source", fontsize=6.5, color=MUTED)
    legend = [Patch(facecolor=GOLD, label="All observed sources selected"),
              Patch(facecolor=BLUE, alpha=0.86, label="Other covered repositories"),
              Patch(facecolor="#E8ECEF", label="Uncovered repositories")]
    fig.legend(handles=legend, loc="lower left", bbox_to_anchor=(0.031, 0.001),
               ncol=1, fontsize=6.6, labelspacing=0.38, handlelength=1.4, handletextpad=0.7)
    manifest["coverage_partition"] = {
        **save(fig, "coverage_partition"),
        "budget": 100,
        "observed_repository_count": total,
        "plotted_reachable_repository_count": reachable,
        "segments": segments,
        "interpretation": "All observed sources selected is a structural model property, not verified real-world protection. Covered totals are printed at the blue/gray boundary; numbers inside the gold segment count endpoints with all observed sources selected.",
    }


def representation_detail(data: dict, manifest: dict) -> None:
    projected_pairs = data["diagnostics"][ENDPOINT]["total_identity_endpoint_pairs"]
    version_pairs = data["version_representation"][ENDPOINT]["total_identity_endpoint_pairs"]
    projected_rows = {r["method"]: r for r in selected_rows(data, "deterministic_curves", budget=100)}
    version_rows = {r["method"]: r for r in selected_rows(
        data, "version_representation_curves", budget=100,
        selection_representation="version_continuous", evaluation_representation="version_continuous")}
    drop = 100 * (1 - version_pairs / projected_pairs)
    fig = plt.figure(figsize=(3.45, 2.30))
    top = fig.add_axes([0.300, 0.671, 0.655, 0.129])
    bottom = fig.add_axes([0.300, 0.270, 0.655, 0.230])
    package_style = {"color": "#555F6B", "marker": "s", "s": 24, "zorder": 3, "linewidths": 0.6, "edgecolors": "white"}
    version_style = {"color": TEAL, "marker": "o", "s": 27, "zorder": 3, "linewidths": 0.6, "edgecolors": "white"}

    top.plot([version_pairs, projected_pairs], [0, 0], color="#BAC4CD", lw=2.4, solid_capstyle="round")
    top.scatter([projected_pairs], [0], **package_style)
    top.scatter([version_pairs], [0], **version_style)
    top.annotate(f"{projected_pairs:,}", (projected_pairs, 0), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=7, color="#555F6B")
    top.annotate(f"{version_pairs:,}", (version_pairs, 0), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=7, color=TEAL)
    top.set(xlim=(210000, 515000), ylim=(-0.7, 1.05), yticks=[], xticks=[250000, 350000, 450000])
    top.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value / 1000:g}k"))
    fig.text(0.035, 0.855, f"(a) Reachable identity–repository pairs: −{drop:.1f}%", fontsize=7.3, weight="bold")
    clean(top, grid="x")
    top.spines["left"].set_visible(False)
    details = []
    for y, method in enumerate(["exact_union", "greedy_coverage"]):
        p = projected_rows[method]["covered_endpoints"]
        v = version_rows[method]["covered_endpoints"]
        bottom.plot([p, v], [y, y], color="#BAC4CD", lw=2.4, solid_capstyle="round")
        bottom.scatter([p], [y], **package_style)
        bottom.scatter([v], [y], **version_style)
        bottom.annotate(f"{p:,}", (p, y), xytext=(-2, 5), textcoords="offset points", ha="right", fontsize=7, color="#555F6B")
        bottom.annotate(f"{v:,}", (v, y), xytext=(2, -10), textcoords="offset points", ha="left", fontsize=7, color=TEAL)
        details.append({"method": method, "package_projected_covered": p, "version_continuous_covered": v,
                        "package_row": projected_rows[method], "version_row": version_rows[method]})
    bottom.set(xlim=(4050, 5950), ylim=(-0.85, 1.7), yticks=[0, 1],
               yticklabels=["Exact union", "Greedy coverage"], xticks=[4500, 5000, 5500],
               xlabel="Covered repositories (count)")
    bottom.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
    fig.text(0.035, 0.563, "(b) Reoptimized coverage, budget 100 identities", fontsize=7.3, weight="bold")
    clean(bottom, grid="x")
    bottom.spines["left"].set_visible(False)
    bottom.tick_params(axis="y", length=0, pad=6, labelsize=6.7)
    fig.text(0.035, 0.944, "Graph representation and exposure", fontsize=8.2, weight="bold")
    fig.legend(handles=[Line2D([], [], color="#555F6B", marker="s", linestyle="none", markersize=4, label="Package projection"),
                        Line2D([], [], color=TEAL, marker="o", linestyle="none", markersize=4, label="Version continuity")],
               loc="lower center", bbox_to_anchor=(0.52, 0.005), ncol=2, fontsize=6.8, handletextpad=0.4, columnspacing=1.3)
    manifest["representation_detail"] = {
        **save(fig, "representation_detail"),
        "package_projected_identity_repository_pairs": projected_pairs,
        "version_continuous_identity_repository_pairs": version_pairs,
        "pair_mass_reduction_percent": drop,
        "covered_repository_rows": details,
        "interpretation": "Both selection and evaluation use each stated representation. Version continuity is a sensitivity analysis over the retained union, not an observed installation or historical reconstruction. The two panels have different units and scales.",
    }


def main() -> None:
    configure()
    source_bytes = SOURCE.read_bytes()
    data = json.loads(source_bytes)
    manifest = {
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "renderer": str(Path(__file__).relative_to(ROOT)),
        "renderer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "endpoint": ENDPOINT,
        "figures": {},
    }
    objective_tradeoff(data, manifest["figures"])
    coverage_partition(data, manifest["figures"])
    representation_detail(data, manifest["figures"])
    output = ROOT / "results/analysis_figure_data.json"
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(f"Rendered {len(manifest['figures'])} empirical figure sets from {manifest['source']}.")
    print(f"Traceable data and output hashes: {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
