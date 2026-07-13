#!/usr/bin/env python3
"""
calculate_metrics.py
Calculates Wormability, Blast Radius, and Attacker ROI metrics for npm packages
stored in the npm_ecosystem database.
"""

import os
import sys
import sqlite3
import argparse
from collections import deque, defaultdict
import csv
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Calculate Wormability, Blast Radius, and Attacker ROI.")
    parser.add_argument("--db", type=str, default="npm_ecosystem.db", help="Path to SQLite database")
    parser.add_argument("--alpha", type=float, default=0.5, help="Alpha hyperparameter weight for Wormability")
    parser.add_argument("--beta", type=float, default=0.5, help="Beta hyperparameter weight for Blast Radius")
    parser.add_argument("--output-csv", type=str, default="metrics_summary.csv", help="Export summary to a CSV file")
    parser.add_argument("--top-k", type=int, default=50, help="Print top K packages by Attacker ROI")
    args = parser.parse_args()

    if not os.path.exists(args.db):
        print(f"[X] Database file not found: {args.db}")
        sys.exit(1)

    print(f"[*] Connecting to database: {args.db}")
    conn = sqlite3.connect(args.db)
    cursor = conn.cursor()

    # 1. Create target table for calculated metrics
    print("[*] Setting up 'package_metrics' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS package_metrics (
            package_name TEXT PRIMARY KEY,
            wormability_max INTEGER,
            wormability_sum INTEGER,
            blast_radius INTEGER,
            direct_dependents INTEGER,
            direct_dependents_with_workflows INTEGER,
            transitive_dependents INTEGER,
            attacker_roi REAL,
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # 2. Load all packages
    print("[*] Loading packages from database...")
    cursor.execute("SELECT name FROM packages")
    packages = [row[0] for row in cursor.fetchall()]
    total_packages = len(packages)
    print(f"[+] Loaded {total_packages} packages.")

    if total_packages == 0:
        print("[X] No packages found in the database. Please run scraper first.")
        conn.close()
        sys.exit(1)

    # 3. Load maintainer mapping and compute out-degrees
    print("[*] Loading maintainer mapping and computing out-degrees...")
    cursor.execute("SELECT package_name, maintainer_username FROM package_maintainers")
    pkg_maintainers = cursor.fetchall()
    
    # Map packages to their maintainers
    package_to_maintainers = defaultdict(set)
    # Count packages per maintainer
    maintainer_out_degree = defaultdict(int)
    
    for pkg, maintainer in pkg_maintainers:
        package_to_maintainers[pkg].add(maintainer)
        maintainer_out_degree[maintainer] += 1
        
    print(f"[+] Loaded maintainer mappings for {len(package_to_maintainers)} packages.")
    print(f"[+] Total unique maintainers: {len(maintainer_out_degree)}")

    # 4. Load package workflow flags
    print("[*] Loading package workflow presence...")
    # A package has workflows if any of its versions has has_github_workflows = 1
    cursor.execute("SELECT DISTINCT package_name FROM package_versions WHERE has_github_workflows = 1")
    packages_with_workflows = {row[0] for row in cursor.fetchall()}
    print(f"[+] Found {len(packages_with_workflows)} packages with active GitHub CI/CD workflows.")

    # 5. Load dependency edges and build adjacency lists
    print("[*] Loading dependency graph...")
    # We construct a package-level directed graph.
    # from_package (dependent) -> to_package (dependency)
    # For Blast Radius, we need to find all dependents of v, which means traversing edges in reverse (to_package -> from_package)
    cursor.execute("SELECT DISTINCT from_package, to_package FROM dependencies")
    dependency_edges = cursor.fetchall()
    
    # Adjacency list for reverse traversal (dependency -> dependent)
    reverse_adj = defaultdict(list)
    # Adjacency list for direct traversal (dependent -> dependency)
    direct_adj = defaultdict(list)
    
    for from_pkg, to_pkg in dependency_edges:
        reverse_adj[to_pkg].append(from_pkg)
        direct_adj[from_pkg].append(to_pkg)
        
    print(f"[+] Loaded {len(dependency_edges)} unique dependency edges.")

    # 6. Calculate Wormability and Blast Radius for each package
    print("[*] Calculating metrics for all packages...")
    
    # Store raw values
    wormability_max_dict = {}
    wormability_sum_dict = {}
    blast_radius_dict = {}
    direct_deps_dict = {}
    direct_deps_wf_dict = {}
    transitive_deps_dict = {}
    
    # To display progress
    progress_step = max(1, total_packages // 20)
    
    for idx, pkg in enumerate(packages):
        if idx % progress_step == 0 or idx == total_packages - 1:
            print(f"    Progress: {idx+1}/{total_packages} packages processed ({(idx+1)/total_packages*100:.1f}%)")
            
        # A. Wormability
        maintainers = package_to_maintainers.get(pkg, [])
        if maintainers:
            out_degrees = [maintainer_out_degree[m] for m in maintainers]
            w_max = max(out_degrees)
            w_sum = sum(out_degrees)
        else:
            w_max = 0
            w_sum = 0
            
        wormability_max_dict[pkg] = w_max
        wormability_sum_dict[pkg] = w_sum
        
        # B. Direct Dependents
        direct_dependents = reverse_adj.get(pkg, [])
        direct_deps_dict[pkg] = len(direct_dependents)
        direct_deps_wf_dict[pkg] = sum(1 for d in direct_dependents if d in packages_with_workflows)
        
        # C. Blast Radius & Transitive Dependents (BFS reverse traversal)
        visited = set()
        queue = deque([pkg])
        visited.add(pkg)
        
        while queue:
            curr = queue.popleft()
            for neighbor in reverse_adj.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
        # Exclude self from dependents
        visited.discard(pkg)
        
        transitive_deps_dict[pkg] = len(visited)
        # Blast Radius is the count of transitive dependents that have CI/CD workflows
        br = sum(1 for d in visited if d in packages_with_workflows)
        blast_radius_dict[pkg] = br

    # 7. Normalize metrics and calculate Attacker ROI
    # Max values for min-max scaling (normalization to [0,1] range)
    max_w_max = max(wormability_max_dict.values()) if wormability_max_dict else 1
    max_br = max(blast_radius_dict.values()) if blast_radius_dict else 1
    
    # Avoid division by zero
    if max_w_max == 0: max_w_max = 1
    if max_br == 0: max_br = 1
    
    print(f"[+] Maximum Wormability (Max): {max_w_max}")
    print(f"[+] Maximum Blast Radius:       {max_br}")
    print(f"[*] Calculating Attacker ROI (alpha={args.alpha}, beta={args.beta})...")
    
    roi_dict = {}
    for pkg in packages:
        # Normalize
        w_max_norm = wormability_max_dict[pkg] / max_w_max
        br_norm = blast_radius_dict[pkg] / max_br
        
        # Attacker ROI (normalized formulation to keep it scaled between [0, 1])
        roi = args.alpha * w_max_norm + args.beta * br_norm
        roi_dict[pkg] = roi

    # 8. Save to Database
    print("[*] Saving computed metrics to SQLite 'package_metrics' table...")
    cursor.execute("BEGIN TRANSACTION")
    try:
        # Clear existing metrics
        cursor.execute("DELETE FROM package_metrics")
        
        # Insert new metrics
        insert_data = [
            (
                pkg,
                wormability_max_dict[pkg],
                wormability_sum_dict[pkg],
                blast_radius_dict[pkg],
                direct_deps_dict[pkg],
                direct_deps_wf_dict[pkg],
                transitive_deps_dict[pkg],
                roi_dict[pkg]
            )
            for pkg in packages
        ]
        
        cursor.executemany("""
            INSERT OR REPLACE INTO package_metrics (
                package_name, wormability_max, wormability_sum, blast_radius, 
                direct_dependents, direct_dependents_with_workflows, transitive_dependents, attacker_roi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, insert_data)
        
        conn.commit()
        print(f"[+] Successfully wrote {len(insert_data)} metrics records to database.")
    except Exception as e:
        conn.rollback()
        print(f"[X] Failed to save metrics to database: {e}")
        conn.close()
        sys.exit(1)

    # 9. Output to CSV if requested
    if args.output_csv:
        csv_path = args.output_csv
        print(f"[*] Exporting all metrics to {csv_path}...")
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "package_name", "wormability_max", "wormability_sum", 
                    "blast_radius", "direct_dependents", "direct_dependents_with_workflows", 
                    "transitive_dependents", "attacker_roi"
                ])
                for pkg in sorted(packages, key=lambda x: roi_dict[x], reverse=True):
                    writer.writerow([
                        pkg,
                        wormability_max_dict[pkg],
                        wormability_sum_dict[pkg],
                        blast_radius_dict[pkg],
                        direct_deps_dict[pkg],
                        direct_deps_wf_dict[pkg],
                        transitive_deps_dict[pkg],
                        f"{roi_dict[pkg]:.6f}"
                    ])
            print(f"[+] Exported successfully to {csv_path}.")
        except Exception as e:
            print(f"[X] Failed to export CSV: {e}")

    # 10. Print Top K Packages
    print("\n" + "="*80)
    print(f"                TOP {args.top_k} PACKAGES BY ATTACKER ROI")
    print(f"                Formulation: ROI = {args.alpha}*Wormability_norm + {args.beta}*BlastRadius_norm")
    print("="*80)
    print(f"{'Rank':<5} {'Package Name':<35} {'ROI':<10} {'Worm(Max)':<10} {'Worm(Sum)':<10} {'BlastRad':<10} {'TransDeps':<10}")
    print("-"*80)
    
    sorted_packages = sorted(packages, key=lambda x: roi_dict[x], reverse=True)
    for i, pkg in enumerate(sorted_packages[:args.top_k]):
        print(f"{i+1:<5} {pkg:<35} {roi_dict[pkg]:.4f}      {wormability_max_dict[pkg]:<10} {wormability_sum_dict[pkg]:<10} {blast_radius_dict[pkg]:<10} {transitive_deps_dict[pkg]:<10}")
    print("="*80 + "\n")

    conn.close()

if __name__ == "__main__":
    main()
