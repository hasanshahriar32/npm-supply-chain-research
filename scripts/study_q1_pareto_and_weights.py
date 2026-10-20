#!/usr/bin/env python3
"""Q1 Journal Expansion Experiment: Pareto Frontier, Direct P Optimization, and Heterogeneous Weights.

Standalone read-only analysis script for IEEE TSE / ACM TOSEM / EMSE journal expansion.
Operates on data/npm_ecosystem.db.zip without modifying any conference submission artifacts.
"""
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
    sole_pkg_count = [0] * M
    for p, maint_set in enumerate(pmaint):
        if len(maint_set) == 1:
            m = next(iter(maint_set))
            sole_pkg_count[m] += 1

    w_sole = [1.0 + float(sole_pkg_count[m]) for m in range(M)]
    w_log = [1.0 + math.log2(1.0 + len(portfolios[m])) for m in range(M)]

    denom_uniform = sum(sizes_name)
    denom_sole = sum(w_sole[m] * sizes_name[m] for m in range(M))
    denom_log = sum(w_log[m] * sizes_name[m] for m in range(M))

    order_union = sorted(range(M), key=lambda m: (-sizes_name[m], m))[:100]
    order_portfolio = sorted(range(M), key=lambda m: (-len(portfolios[m]), m))[:100]
    order_greedy, _ = ssi.lazy_greedy(masks_name, range(M), range(M), 100)

    # Also evaluate the Pareto alpha=0.50 selection at Budget 100
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

    weight_models = {
        "Exact Union": order_union,
        "Greedy Coverage": order_greedy,
        "Portfolio Size": order_portfolio,
        "Pareto (alpha=0.50)": order_p50,
    }
    weight_results = {}
    for name, sel in weight_models.items():
        c_val = ssi.union(masks_name[m] for m in sel).bit_count()
        sel_mask = ssi.union(1 << m for m in sel)
        p_val = ssi.full_protection(signatures_name, sel_mask, 100)
        h_u = (sum(sizes_name[m] for m in sel) / denom_uniform) * 100.0
        h_s = (sum(w_sole[m] * sizes_name[m] for m in sel) / denom_sole) * 100.0
        h_l = (sum(w_log[m] * sizes_name[m] for m in sel) / denom_log) * 100.0
        weight_results[name] = {
            "C": c_val,
            "C_pct": (c_val / N_WF_TOTAL) * 100.0,
            "H_uniform_pct": h_u,
            "H_sole_pct": h_s,
            "H_log_pct": h_l,
            "P": p_val,
        }

    # Save comprehensive results JSON
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
        },
        "pareto_name_graph": pareto_name,
        "pareto_version_continuous_graph": pareto_vc,
        "direct_p_optimization": direct_p_results,
        "heterogeneous_weights": weight_results,
    }
    out_path = ROOT / "manuscript/results/q1_journal_experiments.json"
    out_path.write_text(json.dumps(output_payload, indent=2) + "\n")
    print(f"\nWrote full Q1 experiment results to: {out_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
