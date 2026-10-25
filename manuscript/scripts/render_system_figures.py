#!/usr/bin/env python3
"""Render vector study diagrams from measured counts and tested set semantics.

This script draws the implemented observational pipeline, not a trained predictor.
The small set example is illustrative and is independently checked before rendering.
No external images, generated imagery, TeX installation, or network are required.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "manuscript"
FIGURES = PAPER / "figures"
RESULTS = PAPER / "results"
INK = "#20374B"
MUTED = "#596D7C"
LINE = "#BCCBD5"
BLUE = "#2D6085"
TEAL = "#007F84"
GOLD = "#B78020"
PALE = "#F3F6F8"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "svg.hashsalt": "npm-maintainer-study-diagrams-v1",
        "axes.unicode_minus": False,
    }
)


def label(ax, x, y, text, *, size=8, color=INK, weight="normal", ha="left", **kw):
    return ax.text(
        x, y, text, fontsize=size, color=color, fontweight=weight,
        ha=ha, va="center", linespacing=1.25, **kw
    )


def box(ax, x, y, width, height, *, face="white", edge=LINE, radius=4, lw=0.7):
    patch = FancyBboxPatch(
        (x, y), width, height,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw, edgecolor=edge, facecolor=face, zorder=1,
    )
    ax.add_patch(patch)
    return patch


def arrow(ax, start, end, *, color=MUTED, lw=0.95, mutation=8, connectionstyle="arc3"):
    patch = FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=mutation,
        linewidth=lw, color=color, connectionstyle=connectionstyle,
        shrinkA=0, shrinkB=0, zorder=2,
    )
    ax.add_patch(patch)
    return patch


def canvas(width, height):
    fig = plt.figure(figsize=(width / 100, height / 100), facecolor="white")
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set(xlim=(0, width), ylim=(0, height))
    ax.set_axis_off()
    return fig, ax


def node(ax, x, y, kind, label_text):
    if kind == "maintainer":
        ax.add_patch(Circle((x, y), 9.7, facecolor=BLUE, edgecolor=BLUE, zorder=4))
    elif kind == "package":
        box(ax, x - 11, y - 9, 22, 18, face=TEAL, edge=TEAL, radius=3)
    else:
        ax.add_patch(Polygon(
            [(x, y + 11), (x + 12, y), (x, y - 11), (x - 12, y)],
            closed=True, facecolor=GOLD, edgecolor=GOLD, zorder=4,
        ))
    label(ax, x, y, label_text, size=7.5, color="white", weight="bold", ha="center", zorder=5)


def save(fig, stem):
    """Save fixed physical dimensions and fail if any text escapes the canvas."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bounds = fig.bbox
    for ax in fig.axes:
        for text in ax.texts:
            extent = text.get_window_extent(renderer)
            if (extent.x0 < bounds.x0 - 0.5 or extent.y0 < bounds.y0 - 0.5
                    or extent.x1 > bounds.x1 + 0.5 or extent.y1 > bounds.y1 + 0.5):
                raise ValueError(f"Clipped text in {stem}: {text.get_text()!r}")
    FIGURES.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "svg", "png"):
        kwargs = {"dpi": 240} if suffix == "png" else {}
        # Fixed metadata makes PDF/SVG assets reproducible between executions.
        metadata = {"CreationDate": None, "ModDate": None} if suffix == "pdf" else None
        if suffix == "svg":
            metadata = {"Date": None, "Creator": "render_system_figures.py"}
        fig.savefig(FIGURES / f"{stem}.{suffix}", metadata=metadata, **kwargs)
    plt.close(fig)


def system_figure(data):
    pop = data["population"]
    fig, ax = canvas(710, 216)
    stages = [(7, 132, "1  Observe"), (157, 211, "2  Model"),
              (387, 149, "3  Prioritize"), (555, 148, "4  Evaluate")]
    for x, width, title in stages:
        box(ax, x, 49, width, 143, face=PALE, edge="#DFE7EC", radius=5)
        label(ax, x + 2, 205, title, size=9, weight="bold")

    for cy, title, detail, color in [
        (162, "npm registry", "maintainer metadata", BLUE),
        (119, "deps.dev", "dependency edges", TEAL),
        (76, "GitHub", "workflow flags", GOLD),
    ]:
        box(ax, 17, cy - 16, 112, 32, edge="#D4E0E7", radius=3)
        ax.plot([20, 20], [cy - 9, cy + 9], color=color, lw=2.4, solid_capstyle="round")
        label(ax, 27, cy + 6, title, size=8, weight="bold")
        label(ax, 27, cy - 7, detail, size=6.7, color=MUTED)

    arrow(ax, (141, 120), (153, 120), lw=1.2, mutation=8)
    # A relation-typed schematic. Package arrows follow dependency -> dependent.
    for start, end, color in [
        ((185, 151), (218, 151), BLUE),
        ((185, 92), (264, 92), BLUE),
        ((242, 151), (264, 151), TEAL),
        ((239, 143), (266, 101), TEAL),
        ((288, 151), (322, 151), GOLD),
        ((288, 92), (322, 92), GOLD),
    ]:
        arrow(ax, start, end, color=color, lw=0.95, mutation=7)
    node(ax, 175, 151, "maintainer", "M")
    node(ax, 175, 92, "maintainer", "M")
    node(ax, 230, 151, "package", "P")
    node(ax, 276, 151, "package", "P")
    node(ax, 276, 92, "package", "P")
    node(ax, 335, 151, "repository", "R")
    node(ax, 335, 92, "repository", "R")
    label(ax, 197, 167, "maintains", size=6.2, ha="center", color=BLUE)
    label(ax, 262, 180, "reverse dependency", size=6.2, ha="center", color=TEAL)
    label(ax, 308, 166, "maps to", size=6.2, ha="center", color=GOLD)
    label(ax, 262, 62, "M: maintainer   P: package   R: repository", size=6.6, ha="center", color=MUTED)
    arrow(ax, (370, 120), (383, 120), lw=1.2, mutation=8)

    box(ax, 397, 128, 129, 49, edge="#CDDCE5", radius=4)
    label(ax, 461.5, 163, "Exact reachability", size=8, weight="bold", ha="center")
    label(ax, 461.5, 148, "SCC condensation", size=6.8, ha="center", color=MUTED)
    label(ax, 461.5, 136, "account–endpoint bitsets", size=6.8, ha="center", color=MUTED)
    arrow(ax, (461.5, 125), (461.5, 115), lw=1.05, mutation=7)
    box(ax, 397, 61, 129, 51, edge="#CDDCE5", radius=4)
    label(ax, 461.5, 98, "Budgeted selection", size=8, weight="bold", ha="center")
    label(ax, 461.5, 83, "5 deterministic rankings", size=7, ha="center", color=MUTED)
    label(ax, 461.5, 70, "+ random baseline", size=7, ha="center", color=MUTED)
    arrow(ax, (538, 120), (551, 120), lw=1.2, mutation=8)

    for y, symbol, text, color in [
        (158, "C", "Distinct review\ncoverage", BLUE),
        (119, "H", "Conditional exposure\nreduction", TEAL),
        (80, "P", "All-source\nexclusion", GOLD),
    ]:
        ax.add_patch(Circle((571, y), 9, facecolor=color, edgecolor=color))
        label(ax, 571, y, symbol, color="white", size=8.2, weight="bold", ha="center")
        label(ax, 587, y, text, size=7.5)

    box(ax, 7, 3, 696, 37, face="#EEF3F6", edge="#DFE7EC", radius=4)
    counts = (
        f"{pop['identities']:,} maintainer IDs    •    {pop['packages']:,} graph IDs "
        f"({data['context_identifiers']:,} context)    •    "
        f"{pop['maintainer_package_relations']:,} maintainer links    •    "
        f"{pop['unique_package_edges']:,} dependency pairs"
    )
    label(ax, 355, 27, counts, size=7.1, ha="center", color=MUTED)
    label(ax, 355, 13,
          f"Primary endpoints: {pop['workflow_positive_packages']:,} workflow-associated packages "
          f"→ {pop['workflow_positive_repositories']:,} distinct repository keys",
          size=7.6, ha="center", weight="bold")
    save(fig, "study_system")


def mechanism_figure(data):
    toy = data["illustrative_example"]
    fig, ax = canvas(345, 218)
    label(ax, 10, 204, "One exposure map, different selection objectives", size=8, weight="bold")
    label(ax, 10, 186, "Illustrative account–endpoint incidence", size=7, color=MUTED)
    for j in range(6):
        label(ax, 65 + j * 23, 168, str(j + 1), size=7.5, color=MUTED, ha="center")
    row_colors = {"A": BLUE, "B": GOLD, "C": TEAL}
    for i, (account, endpoints) in enumerate(toy["exposure_sets"].items()):
        y = 146 - i * 23
        label(ax, 29, y, account, size=8.5, weight="bold", color=row_colors[account], ha="center")
        for j in range(6):
            ax.add_patch(Circle((65 + j * 23, y), 4.1,
                               facecolor=row_colors[account] if j + 1 in endpoints else "white",
                               edgecolor=row_colors[account] if j + 1 in endpoints else "#D9E2E8",
                               linewidth=0.7))
    ax.plot([224, 224], [96, 174], color="#DEE6EB", lw=0.8)
    label(ax, 238, 151, "6 endpoints", size=7.5, weight="bold")
    label(ax, 238, 130, "9 account–\nendpoint pairs", size=7, color=MUTED)
    label(ax, 238, 105, "Budget: 2 accounts", size=7, color=MUTED)

    box(ax, 10, 8, 325, 73, face=PALE, edge="#DFE7EC", radius=4)
    label(ax, 22, 68, "Selection", size=7.1, color=MUTED)
    for x, metric in [(178, "C"), (237, "H"), (300, "P")]:
        label(ax, x, 68, metric, size=8, color=MUTED, weight="bold", ha="center")
    ax.plot([19, 325], [58, 58], color="#D7E1E8", lw=0.7)
    for y, row in zip((43, 21), toy["selections"]):
        label(ax, 22, y, " + ".join(row["accounts"]), size=8, weight="bold")
        label(ax, 178, y, str(row["coverage"]), size=8.5, weight="bold" if row["coverage"] == 6 else "normal", ha="center", color=BLUE)
        label(ax, 237, y, f"{row['removed_pairs']}/9", size=8.5, weight="bold" if row["removed_pairs"] == 7 else "normal", ha="center", color=TEAL)
        label(ax, 300, y, str(row["all_source_exclusion"]), size=8.5, ha="center", color=GOLD)
    save(fig, "objective_mechanism")


def main():
    sources = {
        "structural_interventions": RESULTS / "structural_interventions/results.json",
        "identifier_scope": RESULTS / "graph_validity/identifier_scope.json",
    }
    results = json.loads(sources["structural_interventions"].read_text())
    scope = json.loads(sources["identifier_scope"].read_text())
    exposure_sets = {"A": [1, 2, 3, 4], "B": [1, 2, 3], "C": [5, 6]}
    endpoint_sources = {
        q: {m for m, endpoints in exposure_sets.items() if q in endpoints}
        for q in range(1, 7)
    }
    selections = []
    for selected in ({"A", "B"}, {"A", "C"}):
        selections.append({
            "accounts": sorted(selected),
            "coverage": len(set().union(*(set(exposure_sets[m]) for m in selected))),
            "removed_pairs": sum(len(exposure_sets[m]) for m in selected),
            "all_source_exclusion": sum(bool(owners) and owners <= selected for owners in endpoint_sources.values()),
        })
    assert [(r["coverage"], r["removed_pairs"], r["all_source_exclusion"]) for r in selections] == [(4, 7, 4), (6, 6, 3)]
    data = {
        "diagram_kind": "Implemented logical architecture; representative topology is illustrative, counts are empirical",
        "source_sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sources.values()
        },
        "population": results["population"],
        "context_identifiers": scope["context_marker_identifier_count"],
        "influence_direction": "dependency -> dependent",
        "illustrative_example": {
            "kind": "Illustrative counterexample, not an observed subgraph",
            "exposure_sets": exposure_sets,
            "total_account_endpoint_pairs": sum(map(len, exposure_sets.values())),
            "selections": selections,
        },
        "dimensions_inches": {"study_system": [7.1, 3.35], "objective_mechanism": [3.45, 2.18]},
    }
    # The publication renderer now draws study_system natively after this evidence pass.
    mechanism_figure(data)
    (RESULTS / "system_figure_data.json").write_text(json.dumps(data, indent=2) + "\n")
    print("Rendered study_system and objective_mechanism as PDF, SVG, and PNG.")
    print("Source hashes, empirical counts, and checked illustrative values: manuscript/results/system_figure_data.json")


if __name__ == "__main__":
    main()
