#!/usr/bin/env python3
"""Q1 Journal Expansion Experiment: Pareto Frontier, Direct P Optimization, and Heterogeneous Weights.

Standalone read-only analysis script for IEEE TSE / ACM TOSEM / EMSE journal expansion.
Operates on data/npm_ecosystem.db.zip without modifying any conference submission artifacts.
Exports full result JSON, CSVs, and publication-ready LaTeX tables to manuscript/results/q1_journal/.
"""
import csv
import heapq
import json
import math
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import study_structural_interventions as ssi

BUDGETS = (10, 25, 50, 100)
ALPHAS = (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0)
N_WF_TOTAL = 7171


def main():
    print("=" * 80)
    print("STARTING Q1 JOURNAL EXPANSION EXPERIMENTS: PARETO FRONTIER & RISK WEIGHTS")
    print("=" * 80)
    t0 = time.perf_counter()

    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "npm.db"
        with zipfile.ZipFile(ROOT / "data/npm_ecosystem.db.zip") as z, z.open("npm_ecosystem.db") as src, open(db, "wb") as dst:
            shutil.copyfileobj(src, dst)
        conn = sqlite3.connect(f"file:{db}?mode=ro&immutable=1", uri=True)

        names, identities, portfolios, pmaint, adj, workflow, checked, repo_nodes, wf_repo_nodes, safe_wf_repo_nodes, pop = ssi.load_data(conn)
        comp, members, edges, topo = ssi.scc_condensation(adj)
        wf_repo_full = ssi.propagate_endpoint_bits(comp, members, edges, topo, wf_repo_nodes)
        wf_repo_data = ssi.endpoint_data(wf_repo_full, portfolios)
        source_masks = ssi.propagate_source_bits(comp, members, edges, topo, pmaint)

        # Version-continuous closures
        vc_pkg_reach, vc_repo_reach, vc_pkg_sources, vc_meta = ssi.version_continuous_representation(conn, names, pmaint, wf_repo_nodes)
        vc_repo_data = ssi.endpoint_data(vc_repo_reach, portfolios)
        vc_source_masks = vc_pkg_sources

    t_prep = time.perf_counter() - t0
    print(f"Loaded ecosystem graphs in {t_prep:.2f} s ({len(identities)} maintainers, {len(names)} packages).")

    # Precompute repository sources and signatures for P(S) evaluation
    wf_repo_sources = [0] * pop["distinct_linked_repositories"]
    for p, sources in enumerate(source_masks):
        for r in ssi.bit_indices(wf_repo_nodes[p]):
            wf_repo_sources[r] |= sources
    signatures_name = ssi.source_signature_groups(wf_repo_sources)

    vc_repo_sources = [0] * pop["distinct_linked_repositories"]
    for p, sources in enumerate(vc_source_masks):
        for r in ssi.bit_indices(wf_repo_nodes[p]):
            vc_repo_sources[r] |= sources
    signatures_vc = ssi.source_signature_groups(vc_repo_sources)

    M = len(identities)
    masks_name = wf_repo_data['masks']
    sizes_name = wf_repo_data['sizes']
    total_pairs_name = wf_repo_data['total_pairs']

    masks_vc = vc_repo_data['masks']
    sizes_vc = vc_repo_data['sizes']
    total_pairs_vc = vc_repo_data['total_pairs']

    # -------------------------------------------------------------------------
    # Experiment 1A: Pareto Frontier via Scalarized Greedy J_alpha(S)
    # -------------------------------------------------------------------------
    def run_scalarized(masks, sizes, total_pairs, signatures, budget=100):
        results = {}
        for alpha in ALPHAS:
            heap = [(-(alpha * (sizes[m] / N_WF_TOTAL) + (1.0 - alpha) * (sizes[m] / total_pairs)), m, m) for m in range(M)]
            heapq.heapify(heap)
            selected, covered, selected_mask, pair_sum = [], 0, 0, 0
            b_results = {}
            while heap and len(selected) < budget:
                bound, tie, m = heapq.heappop(heap)
                marginal_c = (masks[m] & ~covered).bit_count()
                gain = alpha * (marginal_c / N_WF_TOTAL) + (1.0 - alpha) * (sizes[m] / total_pairs)
                key = (-gain, tie, m)
                if not heap or key <= heap[0]:
                    selected.append(m)
                    covered |= masks[m]
                    selected_mask |= (1 << m)
                    pair_sum += sizes[m]
                    b = len(selected)
                    if b in BUDGETS:
                        c_val = covered.bit_count()
                        h_val = (pair_sum / total_pairs) * 100.0
                        p_val = ssi.full_protection(signatures, selected_mask, b)
                        b_results[b] = {
                            "C": c_val,
                            "C_pct": (c_val / N_WF_TOTAL) * 100.0,
                            "H_pct": h_val,
                            "P": p_val,
                        }
                else:
                    heapq.heappush(heap, key)
            results[alpha] = b_results
        return results

    print("\nRunning Experiment 1A: Pareto frontier scalarization on package-name graph...")
    pareto_name = run_scalarized(masks_name, sizes_name, total_pairs_name, signatures_name, 100)
    print("Running Experiment 1A: Pareto frontier scalarization on version-continuous graph...")
    pareto_vc = run_scalarized(masks_vc, sizes_vc, total_pairs_vc, signatures_vc, 100)

    # -------------------------------------------------------------------------
    # Experiment 1B: Direct Supermodular P(S) Maximization Heuristic
    # -------------------------------------------------------------------------
    def run_direct_p(repo_sources_list, masks, sizes, total_pairs, budget=100):
        valid_repos = [src for src in repo_sources_list if src]
        maint_repos = [[] for _ in range(M)]
        for r_idx, src in enumerate(valid_repos):
            for m in ssi.bit_indices(src):
                maint_repos[m].append(r_idx)

        rem_sources = list(valid_repos)
        rem_counts = [src.bit_count() for src in valid_repos]
        selected, selected_mask, covered, pair_sum = [], 0, 0, 0
        b_results = {}

        for step in range(1, budget + 1):
            best_m = None
            best_score = (-1, -1.0, -1, 0)
            active_m = set()
            for r_idx, count in enumerate(rem_counts):
                if count == 1:
                    active_m.add(rem_sources[r_idx].bit_length() - 1)
                elif 1 < count <= 10:
                    for m in ssi.bit_indices(rem_sources[r_idx]):
                        active_m.add(m)
            if not active_m:
                active_m = set(range(M))

            for m in active_m:
                if (selected_mask & (1 << m)):
                    continue
                imm = 0
                frac = 0.0
                for r_idx in maint_repos[m]:
                    c = rem_counts[r_idx]
                    if c == 1 and (rem_sources[r_idx] & (1 << m)):
                        imm += 1
                    elif c > 1 and (rem_sources[r_idx] & (1 << m)):
                        frac += 1.0 / c
                marginal_c = (masks[m] & ~covered).bit_count()
                score = (imm, frac, marginal_c, -m)
                if score > best_score:
                    best_score = score
                    best_m = m

            selected.append(best_m)
            selected_mask |= (1 << best_m)
            covered |= masks[best_m]
            pair_sum += sizes[best_m]

            for r_idx in maint_repos[best_m]:
                if rem_sources[r_idx] & (1 << best_m):
                    rem_sources[r_idx] &= ~(1 << best_m)
                    rem_counts[r_idx] -= 1

            if step in BUDGETS:
                p_curr = sum(1 for c in rem_counts if c == 0)
                c_val = covered.bit_count()
                b_results[step] = {
                    "C": c_val,
                    "C_pct": (c_val / N_WF_TOTAL) * 100.0,
                    "H_pct": (pair_sum / total_pairs) * 100.0,
                    "P": p_curr,
                }
        return b_results

    print("\nRunning Experiment 1B: Direct supermodular P(S) optimization...")
    direct_p_results = run_direct_p(wf_repo_sources, masks_name, sizes_name, total_pairs_name, 100)

    # -------------------------------------------------------------------------
    # Experiment 2: Non-Uniform / Heterogeneous Risk-Weighting Models H_w(S)
    # -------------------------------------------------------------------------
    print("\nRunning Experiment 2: Non-uniform risk weighting models...")

    # 1. Maintainer-level sole package count
    sole_pkg_count = [0] * M
    for p, maint_set in enumerate(pmaint):
        if len(maint_set) == 1:
            m = next(iter(maint_set))
            sole_pkg_count[m] += 1

    w_sole = [1.0 + float(sole_pkg_count[m]) for m in range(M)]
    w_log = [1.0 + math.log2(1.0 + len(portfolios[m])) for m in range(M)]

    # 2. Package-level sole-maintainer reachable repository closures
    # Endpoint reach through sole-maintained packages alone
    sizes_pkg_sole = [0] * M
    for m in range(M):
        m_sole_mask = 0
        for p in portfolios[m]:
            if len(pmaint[p]) == 1:
                m_sole_mask |= wf_repo_full[p]
        sizes_pkg_sole[m] = m_sole_mask.bit_count()

    denom_uniform = sum(sizes_name)
    denom_sole = sum(w_sole[m] * sizes_name[m] for m in range(M))
    denom_log = sum(w_log[m] * sizes_name[m] for m in range(M))
    denom_pkg_sole = sum(sizes_pkg_sole)

    # Unweighted selections
    order_union = sorted(range(M), key=lambda m: (-sizes_name[m], m))[:100]
    order_portfolio = sorted(range(M), key=lambda m: (-len(portfolios[m]), m))[:100]
    order_greedy, _ = ssi.lazy_greedy(masks_name, range(M), range(M), 100)

    # Pareto alpha=0.50
    heap_p50 = [(-(0.5 * (sizes_name[m] / N_WF_TOTAL) + 0.5 * (sizes_name[m] / total_pairs_name)), m, m) for m in range(M)]
    heapq.heapify(heap_p50)
    order_p50, cov_p50 = [], 0
    while heap_p50 and len(order_p50) < 100:
        b, tie, m = heapq.heappop(heap_p50)
        gain = 0.5 * ((masks_name[m] & ~cov_p50).bit_count() / N_WF_TOTAL) + 0.5 * (sizes_name[m] / total_pairs_name)
        key = (-gain, tie, m)
        if not heap_p50 or key <= heap_p50[0]:
            order_p50.append(m)
            cov_p50 |= masks_name[m]
        else:
            heapq.heappush(heap_p50, key)

    # Weight-aware selections: ranking directly by w_m * |E_m|
    order_sole_aware = sorted(range(M), key=lambda m: (-(w_sole[m] * sizes_name[m]), m))[:100]
    order_log_aware = sorted(range(M), key=lambda m: (-(w_log[m] * sizes_name[m]), m))[:100]
    order_pkg_sole_aware = sorted(range(M), key=lambda m: (-sizes_pkg_sole[m], m))[:100]

    evaluated_strategies = {
        # Unweighted selections evaluated under heterogeneous weights
        "Exact Union (Unweighted)": (order_union, "Unweighted"),
        "Greedy Coverage": (order_greedy, "Unweighted"),
        "Portfolio Size": (order_portfolio, "Unweighted"),
        "Pareto Hybrid (alpha=0.50)": (order_p50, "Unweighted"),
        # Weight-aware selections
        "Weight-Aware Sole Optimum": (order_sole_aware, "Weight-Aware"),
        "Weight-Aware Log Optimum": (order_log_aware, "Weight-Aware"),
        "Weight-Aware Package-Sole Optimum": (order_pkg_sole_aware, "Weight-Aware"),
    }

    weight_results = {}
    for name, (sel, mode) in evaluated_strategies.items():
        c_val = ssi.union(masks_name[m] for m in sel).bit_count()
        sel_mask = ssi.union(1 << m for m in sel)
        p_val = ssi.full_protection(signatures_name, sel_mask, 100)
        h_u = (sum(sizes_name[m] for m in sel) / denom_uniform) * 100.0
        h_s = (sum(w_sole[m] * sizes_name[m] for m in sel) / denom_sole) * 100.0
        h_l = (sum(w_log[m] * sizes_name[m] for m in sel) / denom_log) * 100.0
        h_ps = (sum(sizes_pkg_sole[m] for m in sel) / denom_pkg_sole) * 100.0 if denom_pkg_sole > 0 else 0.0
        weight_results[name] = {
            "mode": mode,
            "C": c_val,
            "C_pct": (c_val / N_WF_TOTAL) * 100.0,
            "H_uniform_pct": h_u,
            "H_sole_pct": h_s,
            "H_log_pct": h_l,
            "H_pkg_sole_pct": h_ps,
            "P": p_val,
        }

    # -------------------------------------------------------------------------
    # Export Artifacts: JSON, CSVs, and LaTeX Tables
    # -------------------------------------------------------------------------
    q1_dir = ROOT / "manuscript/results/q1_journal"
    q1_dir.mkdir(parents=True, exist_ok=True)

    # 1. Export JSON
    output_payload = {
        "experiment": "Q1 Journal Expansion: Pareto Frontier and Heterogeneous Risk Weighting",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "dataset": "data/npm_ecosystem.db.zip",
        "universe": {
            "maintainers": M,
            "packages": len(names),
            "workflow_repositories": N_WF_TOTAL,
            "name_graph_pairs": total_pairs_name,
            "version_graph_pairs": total_pairs_vc,
            "denom_pkg_sole": denom_pkg_sole,
        },
        "pareto_name_graph": pareto_name,
        "pareto_version_continuous_graph": pareto_vc,
        "direct_p_optimization": direct_p_results,
        "heterogeneous_weights": weight_results,
    }
    json_path = ROOT / "manuscript/results/q1_journal_experiments.json"
    json_path.write_text(json.dumps(output_payload, indent=2) + "\n")
    print(f"\nWrote full Q1 experiment results JSON to: {json_path}")

    # 2. Export Pareto Frontier CSV & LaTeX Table
    pareto_csv_path = q1_dir / "q1_pareto_frontier.csv"
    with pareto_csv_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["representation", "alpha", "budget", "C", "C_pct", "H_pct", "P"])
        for alpha, b_data in pareto_name.items():
            for b, vals in b_data.items():
                writer.writerow(["package_projected", alpha, b, vals["C"], f"{vals['C_pct']:.2f}", f"{vals['H_pct']:.2f}", vals["P"]])
        for alpha, b_data in pareto_vc.items():
            for b, vals in b_data.items():
                writer.writerow(["version_continuous", alpha, b, vals["C"], f"{vals['C_pct']:.2f}", f"{vals['H_pct']:.2f}", vals["P"]])
    print(f"Wrote Pareto CSV: {pareto_csv_path}")

    pareto_tex_path = q1_dir / "q1_pareto_table.tex"
    with pareto_tex_path.open("w") as f:
        f.write("% Auto-generated Pareto Frontier Table for Q1 Journal Expansion\n")
        f.write("\\begin{table*}[t]\n\\centering\n\\small\n")
        f.write("\\caption{Observed greedy tradeoffs across scalarization weight $\\alpha$ at budget $|S|=100$ ($|R_{\\text{wf}}| = 7{,}171$).}\n")
        f.write("\\label{tab:q1_pareto_frontier}\n")
        f.write("\\begin{tabular}{lrrrrrrrr}\n\\toprule\n")
        f.write("& \\multicolumn{4}{c}{Package-Projected Graph} & \\multicolumn{4}{c}{Version-Continuous Graph}\\\\\n")
        f.write("\\cmidrule(lr){2-5} \\cmidrule(lr){6-9}\n")
        f.write("Scalarization $\\alpha$ & $C$ & $C$ (\\%) & $H$ (\\%) & $P$ & $C$ & $C$ (\\%) & $H$ (\\%) & $P$\\\\\n\\midrule\n")
        for alpha in ALPHAS:
            v_name = pareto_name[alpha][100]
            v_vc = pareto_vc[alpha][100]
            tag = " (Exact Union)" if alpha == 0.0 else (" (Greedy Coverage)" if alpha == 1.0 else (" (Equal weighting)" if alpha == 0.5 else ""))
            f.write(f"{alpha:.2f}{tag} & {v_name['C']:,} & {v_name['C_pct']:.2f}\\% & {v_name['H_pct']:.2f}\\% & {v_name['P']:,} & {v_vc['C']:,} & {v_vc['C_pct']:.2f}\\% & {v_vc['H_pct']:.2f}\\% & {v_vc['P']:,}\\\\\n")
        f.write("\\bottomrule\n\\end{tabular}\n\\end{table*}\n")
    print(f"Wrote Pareto LaTeX: {pareto_tex_path}")

    # 3. Export Supermodular P Optimization CSV & LaTeX Table
    p_csv_path = q1_dir / "q1_supermodular_p_optimization.csv"
    with p_csv_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["budget", "direct_p", "direct_c", "direct_h", "greedy_p", "greedy_c", "greedy_h", "union_p", "union_c", "union_h", "gain_over_greedy", "gain_over_union"])
        for b in BUDGETS:
            dp = direct_p_results[b]
            gp = pareto_name[1.0][b]
            up = pareto_name[0.0][b]
            writer.writerow([b, dp["P"], dp["C"], f"{dp['H_pct']:.2f}", gp["P"], gp["C"], f"{gp['H_pct']:.2f}", up["P"], up["C"], f"{up['H_pct']:.2f}", dp["P"] - gp["P"], dp["P"] - up["P"]])
    print(f"Wrote Supermodular P CSV: {p_csv_path}")

    p_tex_path = q1_dir / "q1_supermodular_p_table.tex"
    with p_tex_path.open("w") as f:
        f.write("% Auto-generated Supermodular P(S) Optimization Table for Q1 Journal Expansion\n")
        f.write("\\begin{table}[t]\n\\centering\n\\small\n")
        f.write("\\caption{All-source exclusion $P(S)$ optimization via greedy minimum-source heuristic versus baseline single-objective rankings.}\n")
        f.write("\\label{tab:q1_supermodular_p}\n")
        f.write("\\begin{tabular}{rrrrrrrr}\n\\toprule\n")
        f.write("Budget & \\multicolumn{3}{c}{Direct $P(S)$ Heuristic} & Greedy $P$ & Union $P$ & Gain vs Gr. & Gain vs Un.\\\\\n")
        f.write("\\cmidrule(lr){2-4}\n")
        f.write("$|S|$ & $P$ & $C$ (\\%) & $H$ (\\%) & & & $\\Delta P$ & $\\Delta P$\\\\\n\\midrule\n")
        for b in BUDGETS:
            dp = direct_p_results[b]
            gp = pareto_name[1.0][b]
            up = pareto_name[0.0][b]
            f.write(f"{b} & \\textbf{{{dp['P']:,}}} & {dp['C_pct']:.1f}\\% & {dp['H_pct']:.2f}\\% & {gp['P']:,} & {up['P']:,} & +{dp['P'] - gp['P']:,} & +{dp['P'] - up['P']:,}\\\\\n")
        f.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")
    print(f"Wrote Supermodular P LaTeX: {p_tex_path}")

    # 4. Export Heterogeneous Weights CSV & LaTeX Table
    w_csv_path = q1_dir / "q1_heterogeneous_weights.csv"
    with w_csv_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["strategy", "selection_mode", "C", "C_pct", "H_uniform_pct", "H_sole_pct", "H_log_pct", "H_pkg_sole_pct", "P"])
        for strat, vals in weight_results.items():
            writer.writerow([strat, vals["mode"], vals["C"], f"{vals['C_pct']:.2f}", f"{vals['H_uniform_pct']:.2f}", f"{vals['H_sole_pct']:.2f}", f"{vals['H_log_pct']:.2f}", f"{vals['H_pkg_sole_pct']:.2f}", vals["P"]])
    print(f"Wrote Heterogeneous Weights CSV: {w_csv_path}")

    w_tex_path = q1_dir / "q1_heterogeneous_weights_table.tex"
    with w_tex_path.open("w") as f:
        f.write("% Auto-generated Heterogeneous Risk Weights Table for Q1 Journal Expansion\n")
        f.write("\\begin{table*}[t]\n\\centering\n\\small\n")
        f.write("\\caption{Maintainer prioritization outcomes at Budget $|S|=100$ under unweighted evaluation and weight-aware optimization.}\n")
        f.write("\\label{tab:q1_heterogeneous_weights}\n")
        f.write("\\begin{tabular}{llrrrrrr}\n\\toprule\n")
        f.write("Prioritization Strategy & Selection Mode & $C$ & $C$ (\\%) & $H_{\\text{uniform}}$ (\\%) & $H_{\\text{sole}}$ (\\%) & $H_{\\text{log}}$ (\\%) & $P$\\\\\n\\midrule\n")
        f.write("\\multicolumn{8}{l}{\\textit{Unweighted Baseline Strategies (Evaluated Under Risk Priors)}}\\\\\n")
        for strat, vals in weight_results.items():
            if vals["mode"] == "Unweighted":
                f.write(f"\\quad {strat} & {vals['mode']} & {vals['C']:,} & {vals['C_pct']:.1f}\\% & {vals['H_uniform_pct']:.2f}\\% & {vals['H_sole_pct']:.2f}\\% & {vals['H_log_pct']:.2f}\\% & {vals['P']:,}\\\\\n")
        f.write("\\midrule\n\\multicolumn{8}{l}{\\textit{Weight-Aware Optimal Strategies ($\arg\\max_S H_w(S)$)}}\\\\\n")
        for strat, vals in weight_results.items():
            if vals["mode"] == "Weight-Aware":
                f.write(f"\\quad {strat} & {vals['mode']} & {vals['C']:,} & {vals['C_pct']:.1f}\\% & {vals['H_uniform_pct']:.2f}\\% & \\textbf{{{vals['H_sole_pct']:.2f}\\%}} & \\textbf{{{vals['H_log_pct']:.2f}\\%}} & {vals['P']:,}\\\\\n")
        f.write("\\bottomrule\n\\end{tabular}\n\\end{table*}\n")
    print(f"Wrote Heterogeneous Weights LaTeX: {w_tex_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
