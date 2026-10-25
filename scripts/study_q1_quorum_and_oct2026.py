r"""Q1 Journal Expansion: Generalized k-of-n Quorum Exclusion & October 2026 Incident Analysis.

Motivated by the October 21, 2026 LiteLLM 1.107.0 multi-token compromise and the
October 13, 2026 npm Trusted Publishing flaw.

Computes:
1. k-Quorum Exclusion P_k(S) = |{r in R_wf : |Sources(r) \ S| < k}|
   for k in {1, 2, 3, 5} across budgets |S| in {10, 25, 50, 100}
   for Portfolio, Greedy Coverage, Exact Union, Pareto Hybrid (alpha=0.50), and Direct Supermodular P(S).
2. Imperfect hardening efficacy H_eta(S) = eta * H(S) for eta in {1.0, 0.95, 0.90, 0.75}.
3. Exports CSV, JSON, and publication-ready LaTeX tables to manuscript/results/q1_journal/ and manuscript_q1/tables/.
"""
from __future__ import annotations

import csv
import heapq
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import study_structural_interventions as ssi

BUDGETS = (10, 25, 50, 100)
K_VALS = (1, 2, 3, 5)
ETA_VALS = (1.00, 0.95, 0.90, 0.75)
N_WF_TOTAL = 7171


def main():
    print("=" * 80)
    print("RUNNING Q1 GENERALIZED k-OF-n QUORUM EXCLUSION EXPERIMENT")
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

    M = len(identities)
    masks_name = wf_repo_data["masks"]
    sizes_name = wf_repo_data["sizes"]
    total_pairs_name = wf_repo_data["total_pairs"]

    wf_repo_sources = [0] * pop["distinct_linked_repositories"]
    for p, sources in enumerate(source_masks):
        for r in ssi.bit_indices(wf_repo_nodes[p]):
            wf_repo_sources[r] |= sources

    active_sources = [src for src in wf_repo_sources if src]
    print(f"Loaded graph with {M} maintainers, {len(names)} packages, {len(active_sources)} active workflow endpoints.")

    # -------------------------------------------------------------------------
    # 1. Strategy Selections up to Budget 100
    # -------------------------------------------------------------------------
    # A. Portfolio Size
    order_portfolio = sorted(range(M), key=lambda m: (-len(portfolios[m]), m))[:100]

    # B. Greedy Coverage
    order_greedy, _ = ssi.lazy_greedy(masks_name, range(M), range(M), 100)

    # C. Exact Union
    order_union = sorted(range(M), key=lambda m: (-sizes_name[m], m))[:100]

    # D. Pareto Hybrid (alpha=0.50)
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

    # E. Direct Supermodular P(S) Heuristic
    valid_repos = [src for src in wf_repo_sources if src]
    maint_repos = [[] for _ in range(M)]
    for r_idx, src in enumerate(valid_repos):
        for m in ssi.bit_indices(src):
            maint_repos[m].append(r_idx)

    rem_sources = list(valid_repos)
    rem_counts = [src.bit_count() for src in valid_repos]
    order_direct_p = []
    selected_mask = 0
    for step in range(1, 101):
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
            if selected_mask & (1 << m):
                continue
            imm = 0
            frac = 0.0
            for r_idx in maint_repos[m]:
                c = rem_counts[r_idx]
                if c == 1 and (rem_sources[r_idx] & (1 << m)):
                    imm += 1
                elif c > 1 and (rem_sources[r_idx] & (1 << m)):
                    frac += 1.0 / c
            marginal_c = (masks_name[m] & ~0).bit_count()
            score = (imm, frac, marginal_c, -m)
            if score > best_score:
                best_score = score
                best_m = m

        order_direct_p.append(best_m)
        selected_mask |= (1 << best_m)
        for r_idx in maint_repos[best_m]:
            if rem_sources[r_idx] & (1 << best_m):
                rem_sources[r_idx] &= ~(1 << best_m)
                rem_counts[r_idx] -= 1

    strategies = {
        "Portfolio Size": order_portfolio,
        "Greedy Coverage": order_greedy,
        "Exact Union": order_union,
        r"Pareto Hybrid ($\alpha=0.50$)": order_p50,
        r"Direct Supermodular $P(S)$": order_direct_p,
    }

    # -------------------------------------------------------------------------
    # 2. Evaluation across Budgets and k
    # -------------------------------------------------------------------------
    rows = []
    for s_name, order in strategies.items():
        for b in BUDGETS:
            sub_sel = order[:b]
            sub_mask = sum(1 << m for m in sub_sel)
            c_val = ssi.union(masks_name[m] for m in sub_sel).bit_count()
            h_val = (sum(sizes_name[m] for m in sub_sel) / total_pairs_name) * 100.0

            pk_dict = {}
            for k in K_VALS:
                pk_dict[k] = sum(1 for src in active_sources if (src & ~sub_mask).bit_count() < k)

            eta_dict = {}
            for eta in ETA_VALS:
                eta_dict[eta] = h_val * eta

            row = {
                "strategy": s_name,
                "budget": b,
                "C": c_val,
                "C_pct": (c_val / N_WF_TOTAL) * 100.0,
                "H_pct": h_val,
                "P_1": pk_dict[1],
                "P_2": pk_dict[2],
                "P_3": pk_dict[3],
                "P_5": pk_dict[5],
                "H_eta_095": eta_dict[0.95],
                "H_eta_090": eta_dict[0.90],
                "H_eta_075": eta_dict[0.75],
            }
            rows.append(row)

    # -------------------------------------------------------------------------
    # 3. Export CSV and JSON
    # -------------------------------------------------------------------------
    out_dir = ROOT / "manuscript/results/q1_journal"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "q1_quorum_exclusion.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved CSV: {csv_path}")

    json_path = out_dir / "q1_quorum_exclusion.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
    print(f"Saved JSON: {json_path}")

    # -------------------------------------------------------------------------
    # 4. Export LaTeX Table
    # -------------------------------------------------------------------------
    tex_path = out_dir / "q1_quorum_exclusion_table.tex"
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("% Auto-generated Generalized k-of-n Quorum Exclusion Table for Q1 Journal Expansion\n")
        f.write("\\begin{table*}[t]\n")
        f.write("\\centering\n")
        f.write("\\small\n")
        f.write("\\caption{Generalized $k$-of-$n$ Quorum Exclusion $P_k(S)$ and coverage across maintainer hardening strategies ($|R_{\\text{wf}}| = 7{,}171$).}\n")
        f.write("\\label{tab:q1_quorum_exclusion}\n")
        f.write("\\begin{tabular}{lrrrrrrrr}\n")
        f.write("\\toprule\n")
        f.write("Prioritization Strategy & Budget & $C(S)$ & $C$ (\\%) & $H(S)$ (\\%) & $P_1(S)$ & $P_2(S)$ & $P_3(S)$ & $P_5(S)$ \\\\\n")
        f.write(" & $|S|$ & & & & ($k=1$) & ($k=2$) & ($k=3$) & ($k=5$) \\\\\n")
        f.write("\\midrule\n")

        curr_strat = None
        for r in rows:
            strat_label = r["strategy"]
            if strat_label != curr_strat:
                if curr_strat is not None:
                    f.write("\\midrule\n")
                curr_strat = strat_label
                display_strat = strat_label
            else:
                display_strat = ""

            f.write(
                f"{display_strat:<30} & {r['budget']} & "
                f"{r['C']:,} & {r['C_pct']:.2f}\\% & {r['H_pct']:.2f}\\% & "
                f"{r['P_1']:,} & {r['P_2']:,} & {r['P_3']:,} & {r['P_5']:,} \\\\\n"
            )

        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table*}\n")

    print(f"Saved TeX table: {tex_path}")

    # Copy to manuscript_q1/tables/
    q1_tbl_dir = ROOT / "manuscript_q1/tables"
    q1_tbl_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(tex_path, q1_tbl_dir / "q1_quorum_exclusion_table.tex")
    print(f"Synchronized to: {q1_tbl_dir / 'q1_quorum_exclusion_table.tex'}")

    t_total = time.perf_counter() - t0
    print(f"Completed k-quorum exclusion experiment in {t_total:.2f} s.")


if __name__ == "__main__":
    main()
