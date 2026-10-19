#!/usr/bin/env python3
"""Generate paper figures and TeX rows from completed aggregate experiments."""
from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import platform

os.environ.setdefault("MPLCONFIGDIR", "/tmp/npm-paper-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

PAPER = Path(__file__).resolve().parents[1]
RESULTS = PAPER / "results"
FIGURES = PAPER / "figures"
STUDY = RESULTS / "structural_interventions"
ENDPOINT = "workflow_repositories"
BUDGETS = (1, 5, 10, 25, 50, 100)
METHODS = [
    ("portfolio", "Portfolio", "#6c6c6c", "s"),
    ("sum_package_reach", "Summed reach", "#d17b00", "v"),
    ("max_package_reach", "Max reach", "#9863a0", "^"),
    ("exact_union", "Exact union", "#0072b2", "D"),
    ("greedy_coverage", "Greedy coverage", "#009e73", "o"),
]


def only(rows, **conditions):
    matches = [r for r in rows if all(r.get(k) == v for k, v in conditions.items())]
    if len(matches) != 1:
        raise ValueError(f"Expected one row for {conditions}, found {len(matches)}")
    return matches[0]


def save_figure(fig, stem):
    fig.savefig(FIGURES / (stem + ".pdf"), metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(FIGURES / (stem + ".png"), dpi=300)
    plt.close(fig)


def review_coverage(data):
    fig, axes = plt.subplots(2, 1, figsize=(3.45, 3.85), sharex=True)
    fig.subplots_adjust(left=.17, right=.98, top=.79, bottom=.13, hspace=.34)
    fields = ["coverage_fraction_observed", "scenario_exposure_reduction_fraction"]
    for panel, (ax, field) in enumerate(zip(axes, fields)):
        for method, label, color, marker in METHODS:
            rows = [only(data["deterministic_curves"], endpoint=ENDPOINT, method=method, budget=k) for k in BUDGETS]
            ax.plot(BUDGETS, [100 * r[field] for r in rows], label=label,
                    color=color, marker=marker, markersize=3.2, linewidth=1.15)
        random_rows = [only(data["random_analytic_expectations"], endpoint=ENDPOINT, budget=k) for k in BUDGETS]
        ax.plot(BUDGETS, [100 * r["expected_" + field] for r in random_rows],
                label="Random mean", color="black", linestyle=":", linewidth=1.3)
        ax.set_xscale("log")
        ax.set_xlim(.86, 117)
        ax.grid(axis="y", color=".88", linewidth=.5)
        ax.set_ylim(bottom=0)
        ax.set_ylabel("Coverage C (%)" if panel == 0 else "Scenario reduction H (%)")
        ax.text(.02, .94, "(a)" if panel == 0 else "(b)", transform=ax.transAxes,
                va="top", fontsize=8)
    axes[0].set_ylim(0, 85)
    axes[1].set_ylim(0, 37)
    axes[1].set_xticks(BUDGETS)
    axes[1].xaxis.set_major_formatter(ScalarFormatter())
    axes[1].minorticks_off()
    axes[1].set_xlabel("Identity budget (log scale)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=2, loc="upper center", bbox_to_anchor=(.54, .995),
               frameon=False, columnspacing=1.05, handlelength=1.8,
               handletextpad=.5, labelspacing=.45, fontsize=8)
    save_figure(fig, "review_coverage")


def representation_sensitivity(data):
    fig, axes = plt.subplots(1, 2, figsize=(3.45, 2.5))
    fig.subplots_adjust(left=.13, right=.99, top=.79, bottom=.25, wspace=.5)
    representations = [("Package graph", "#4477aa"), ("Version graph", "#cc6677")]
    method_names = ["exact_union", "greedy_coverage"]
    repo_total = data["population"]["workflow_positive_repositories"]
    for ax, field, title in zip(axes, ["covered_endpoints", "scenario_exposure_reduction_fraction"],
                               ["(a) Coverage C (%)", "(b) Reduction H (%)"]):
        for j, (label, color) in enumerate(representations):
            values = []
            for method in method_names:
                if j == 0:
                    row = only(data["deterministic_curves"], endpoint=ENDPOINT, method=method, budget=100)
                else:
                    row = only(data["version_representation_curves"], endpoint=ENDPOINT, method=method,
                               budget=100, selection_representation="version_continuous",
                               evaluation_representation="version_continuous")
                values.append(100 * row[field] / repo_total if field == "covered_endpoints" else 100 * row[field])
            bars = ax.bar([i + (j - .5) * .36 for i in range(2)], values, width=.34,
                          label=label, color=color, edgecolor="white", linewidth=.3)
            for bar, value in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, value / 2, f"{value:.1f}",
                        ha="center", va="center", rotation=90, color="white", fontsize=8)
        ax.set_xticks([0, 1], ["Union", "Greedy"])
        ax.set_ylim(0, 90 if field == "covered_endpoints" else 49)
        ax.set_title(title, fontsize=8, pad=7)
        ax.grid(axis="y", color=".9", linewidth=.5)
        ax.set_axisbelow(True)
        ax.set_yticks([0, 25, 50, 75] if field == "covered_endpoints" else [0, 15, 30, 45])
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=2, loc="upper center", bbox_to_anchor=(.52, 1),
               frameon=False, fontsize=8, columnspacing=1.1, handlelength=1.1)
    pairs = data["diagnostics"][ENDPOINT]["total_identity_endpoint_pairs"]
    version_pairs = data["version_representation"][ENDPOINT]["total_identity_endpoint_pairs"]
    decline = 100 * (1 - version_pairs / pairs)
    fig.text(.52, .075, f"Identity–repository pairs: {pairs:,} → {version_pairs:,}\n"
             f"({decline:.1f}% decrease); budget = 100", ha="center", va="center", fontsize=8)
    save_figure(fig, "representation_sensitivity")


def write_tex(data):
    greedy = only(data["deterministic_curves"], endpoint=ENDPOINT, method="greedy_coverage", budget=100)
    exact = only(data["deterministic_curves"], endpoint=ENDPOINT, method="exact_union", budget=100)
    p = data["population"]
    pairs = data["diagnostics"][ENDPOINT]["total_identity_endpoint_pairs"]
    vpairs = data["version_representation"][ENDPOINT]["total_identity_endpoint_pairs"]
    macros = {
        "StudyPackages": f"{p['packages']:,}",
        "StudyMaintainers": f"{p['identities']:,}",
        "StudyWorkflowPackages": f"{p['workflow_positive_packages']:,}",
        "StudyWorkflowRepos": f"{p['workflow_positive_repositories']:,}",
        "GreedyCovered": f"{greedy['covered_endpoints']:,}",
        "GreedyCoveragePercent": f"{100*greedy['coverage_fraction_observed']:.1f}",
        "GreedyExposurePercent": f"{100*greedy['scenario_exposure_reduction_fraction']:.2f}",
        "UnionCovered": f"{exact['covered_endpoints']:,}",
        "UnionExposurePercent": f"{100*exact['scenario_exposure_reduction_fraction']:.2f}",
        "GreedyExcluded": f"{greedy['fully_protected_endpoints']:,}",
        "VersionPairsDecreasePercent": f"{100*(1-vpairs/pairs):.2f}",
        "ChangedRoots": f"{data['version_representation']['package_roots_with_changed_reach']:,}",
    }
    (RESULTS / "research_numbers.tex").write_text(
        "% Generated by scripts/render_research_figures.py from structural_interventions/results.json.\n"
        + "".join("\\newcommand{\\" + key + "}{" + value + "}\n" for key, value in macros.items()))
    labels = {"portfolio": "Portfolio", "sum_package_reach": "Summed reach",
              "max_package_reach": "Maximum reach", "exact_union": "Exact union", "greedy_coverage": "Greedy coverage"}
    rows = []
    for method, _, _, _ in METHODS:
        row = only(data["deterministic_curves"], endpoint=ENDPOINT, method=method, budget=100)
        rows.append(f"{labels[method]} & {row['covered_endpoints']:,} & {100*row['coverage_fraction_observed']:.1f} & "
                    f"{100*row['scenario_exposure_reduction_fraction']:.2f} & {row['fully_protected_endpoints']:,} \\\\")
    row = only(data["random_summary"], endpoint=ENDPOINT, budget=100)
    rows.append(f"Random (mean) & {row['covered_endpoints_mean']:,.1f} & {100*row['coverage_fraction_observed_mean']:.1f} & "
                f"{100*row['scenario_exposure_reduction_fraction_mean']:.2f} & {row['fully_protected_endpoints_mean']:,.1f} \\\\")
    (RESULTS / "research_method_rows.tex").write_text(
        "% Generated rows: method, C count, C percent, H percent, P count; budget 100.\n"
        "% Random row is the mean of 200 trials; figure random curve uses exact analytic expectation.\n"
        + "\\newcommand{\\ResearchMethodRows}{%\n" + "%\n".join(rows) + "%\n}\n")


def main():
    FIGURES.mkdir(exist_ok=True)
    data = json.loads((STUDY / "results.json").read_text())
    plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 8,
                         "axes.labelsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8,
                         "legend.fontsize": 8, "axes.spines.top": False, "axes.spines.right": False,
                         "pdf.fonttype": 42, "ps.fonttype": 42})
    write_tex(data)
    # The current paper uses these research-derived diagrams and analysis plots.
    # Earlier chart functions above remain available for the historical figures.
    import render_system_figures
    import render_analysis_figures
    render_system_figures.main()
    render_analysis_figures.main()
    stems = {
        "study_system": {"kind": "Implemented pipeline schematic with empirical counts", "in_paper": True},
        "objective_tradeoff": {"kind": "Measured budget curves and analytic random expectations", "in_paper": True},
        "coverage_partition": {"kind": "Measured source-incidence partition at budget 100", "in_paper": True},
        "representation_detail": {"kind": "Measured version-continuity sensitivity", "in_paper": True},
        "objective_mechanism": {"kind": "Illustrative counterexample computed from declared sets", "in_paper": False},
    }
    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()
    inputs = [PAPER / "results/structural_interventions/results.json",
              PAPER / "results/graph_validity/identifier_scope.json"]
    scripts = [Path(__file__).resolve(), PAPER / "scripts/render_system_figures.py",
               PAPER / "scripts/render_analysis_figures.py"]
    outputs = [FIGURES / f"{stem}.{suffix}" for stem in stems for suffix in ("pdf", "svg", "png")]
    outputs += [RESULTS / "system_figure_data.json", RESULTS / "analysis_figure_data.json"]
    manifest = {
        "generator": "Matplotlib drawing primitives and plots; no external imagery or network calls",
        "python_version": platform.python_version(), "matplotlib_version": matplotlib.__version__,
        "figures": stems,
        "inputs_sha256": {str(p.relative_to(PAPER.parent)): sha(p) for p in inputs},
        "scripts_sha256": {str(p.relative_to(PAPER.parent)): sha(p) for p in scripts},
        "outputs_sha256": {str(p.relative_to(PAPER)): sha(p) for p in outputs},
    }
    (RESULTS / "figure_manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print("Generated five reproducible PDF/SVG/PNG figure sets, numeric TeX inputs and figure_manifest.json.")


if __name__ == "__main__":
    main()
