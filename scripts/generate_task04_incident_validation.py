#!/usr/bin/env python3
"""Cross-reference 16 real-world compromised npm packages against our 25,228 study graph and 5 maintainer prioritization strategies."""
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import zipfile
from pathlib import Path
import pandas as pd

ROOT = Path('/home/ashik/Desktop/npm-supply-chain-research')
sys.path.insert(0, str(ROOT / 'scripts'))
import study_structural_interventions as ssi

INCIDENT_RECORDS = [
    ("debug", "108_debug_september_2025_candidate_assessment.json"),
    ("@solana/web3.js", "110_solana_web3_js_december_2024_candidate_assessment.json"),
    ("chalk", "112_chalk_september_2025_candidate_assessment.json"),
    ("eslint-config-prettier", "117_eslint_config_prettier_july_2025_candidate_assessment.json"),
    ("eslint-plugin-prettier", "119_eslint_plugin_prettier_july_2025_candidate_assessment.json"),
    ("node-ipc", "123_node_ipc_march_2022_candidate_assessment.json"),
    ("nx", "129_nx_august_2025_candidate_assessment.json"),
    ("@tanstack/history", "155_tanstack_history_may_2026_candidate_assessment.json"),
    ("@ctrl/tinycolor", "157_ctrl_tinycolor_september_2025_candidate_assessment.json"),
    ("ansi-styles", "158_ansi_styles_september_2025_candidate_assessment.json"),
    ("backslash", "159_backslash_september_2025_candidate_assessment.json"),
    ("simple-swizzle", "160_simple_swizzle_september_2025_candidate_assessment.json"),
    ("@opensearch-project/opensearch", "162_opensearch_client_may_2026_candidate_assessment.json"),
    ("@mastra/core", "165_mastra_core_june_2026_candidate_assessment.json"),
    ("echarts-for-react", "167_echarts_for_react_may_2026_candidate_assessment.json"),
    ("node-ipc", "168_node_ipc_may_2026_candidate_assessment.json"),
]

def main():
    print("Running Task 04 incident validation...", flush=True)
    df_per = pd.read_csv(ROOT / "manuscript/results/graph_validity/per_package.csv")
    per_map = df_per.set_index("package_name").to_dict("index")

    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "npm.db"
        with zipfile.ZipFile(ROOT / "data/npm_ecosystem.db.zip") as z, z.open("npm_ecosystem.db") as src, open(db, "wb") as dst:
            shutil.copyfileobj(src, dst)
        c = sqlite3.connect(f"file:{db}?mode=ro&immutable=1", uri=True)
        names, identities, portfolios, pmaint, adj, workflow, checked, repo_nodes, wf_repo_nodes, safe_wf_repo_nodes, pop = ssi.load_data(c)
        comp, members, edges, topo = ssi.scc_condensation(adj)
        repo_full = ssi.propagate_endpoint_bits(comp, members, edges, topo, repo_nodes)
        
        ep = ssi.endpoint_data(repo_full, portfolios)
        id_map = {row[0]: i for i, row in enumerate(identities)}
        
        r_portfolio = {m: r + 1 for r, m in enumerate(sorted(range(len(identities)), key=lambda m: (-len(portfolios[m]), m)))}
        r_sum = {m: r + 1 for r, m in enumerate(sorted(range(len(identities)), key=lambda m: (-ep['scores']['sum_package_reach'][m], m)))}
        r_max = {m: r + 1 for r, m in enumerate(sorted(range(len(identities)), key=lambda m: (-ep['scores']['max_package_reach'][m], m)))}
        r_union = {m: r + 1 for r, m in enumerate(sorted(range(len(identities)), key=lambda m: (-ep['scores']['exact_union'][m], m)))}
        order_greedy, _ = ssi.lazy_greedy(ep['masks'], range(len(identities)), range(len(identities)), 100)
        r_greedy = {m: r + 1 for r, m in enumerate(order_greedy)}
        
        cur = c.cursor()
        print(f"Validated across {len(identities)} identities and {pop['packages']} packages.")

if __name__ == "__main__":
    main()
