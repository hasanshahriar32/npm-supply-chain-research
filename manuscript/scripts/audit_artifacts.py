#!/usr/bin/env python3
"""Read-only, offline audit of the repository's two compressed data artifacts.

Uses only the Python standard library. No packages are installed or executed.
The source database is extracted into a temporary directory and opened read-only.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from datetime import datetime
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
OUT = PAPER / "results"
FIELDS = ["wormability_max", "wormability_sum", "blast_radius", "direct_dependents",
          "direct_dependents_with_workflows", "transitive_dependents", "attacker_roi"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ranks(values):
    order = sorted(range(len(values)), key=values.__getitem__)
    result = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and values[order[end]] == values[order[start]]:
            end += 1
        for pos in order[start:end]:
            result[pos] = (start + 1 + end) / 2
        start = end
    return result


def spearman(x, y):
    a, b = ranks(x), ranks(y)
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    numerator = sum((u - ma) * (v - mb) for u, v in zip(a, b))
    denominator = math.sqrt(sum((u - ma)**2 for u in a) * sum((v - mb)**2 for v in b))
    return numerator / denominator if denominator else None


def top(rows, field, k, reverse_names=False):
    # Explicit, locale-independent Unicode code-point ordering for reproducibility.
    ordered = sorted(rows, key=lambda r: r["package_name"], reverse=reverse_names)
    return {r["package_name"] for r in sorted(ordered, key=lambda r: -r[field])[:k]}


def boundary(rows, field, k):
    cutoff = sorted((r[field] for r in rows), reverse=True)[k - 1]
    above = sum(r[field] > cutoff for r in rows)
    tied = sum(r[field] == cutoff for r in rows)
    return {"cutoff": cutoff, "strictly_above": above, "tied_at_boundary": tied,
            "slots_in_tie": k - above}


def membership_probabilities(rows, field, k):
    b = boundary(rows, field, k)
    return {r["package_name"]: (1 if r[field] > b["cutoff"] else
            b["slots_in_tie"] / b["tied_at_boundary"] if r[field] == b["cutoff"] else 0)
            for r in rows}


def describe(rows):
    return {f: {"nonzero": sum(r[f] > 0 for r in rows),
                "min": min(r[f] for r in rows), "max": max(r[f] for r in rows),
                "mean": sum(r[f] for r in rows) / len(rows)} for f in FIELDS}


def read_csv(path):
    return list(csv.DictReader(io.StringIO(path.read_text())))


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def main():
    OUT.mkdir(exist_ok=True)
    sources = [ROOT / "data/metrics_summary.csv.zip", ROOT / "data/npm_ecosystem.db.zip"]
    with zipfile.ZipFile(sources[0]) as archive:
        csv_rows = list(csv.DictReader(io.TextIOWrapper(archive.open("metrics_summary.csv"))))
    for row in csv_rows:
        for field in FIELDS:
            row[field] = float(row[field]) if field == "attacker_roi" else int(row[field])
    csv_by_name = {r["package_name"]: r for r in csv_rows}
    with tempfile.TemporaryDirectory(prefix="npm-paper-audit-") as temp:
        database = Path(temp) / "ecosystem.db"
        with zipfile.ZipFile(sources[1]) as archive, archive.open("npm_ecosystem.db") as src, database.open("wb") as dst:
            shutil.copyfileobj(src, dst)
        connection = sqlite3.connect(f"file:{database}?mode=ro&immutable=1", uri=True)
        connection.row_factory = sqlite3.Row
        query = lambda sql: [dict(r) for r in connection.execute(sql)]
        db_rows = query("SELECT * FROM package_metrics ORDER BY package_name")
        db_by_name = {r["package_name"]: r for r in db_rows}
        if len(csv_by_name) != len(csv_rows) or len(db_by_name) != len(db_rows):
            raise ValueError("Duplicate metric package names")
        if csv_by_name.keys() != db_by_name.keys():
            raise ValueError("Metric package populations differ; revise comparison design")
        packages = [r["name"] for r in query("SELECT name FROM packages ORDER BY name")]
        if set(packages) != set(db_by_name):
            raise ValueError("Database metric and package populations differ")
        counts = {table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                  for table in ["packages", "package_versions", "maintainers", "package_maintainers", "dependencies", "advisories", "package_metrics"]}
        workflow_states = query("SELECT has_github_workflows AS present, fetched_workflows AS checked, COUNT(*) AS rows FROM package_versions GROUP BY 1,2")
        workflow_packages = {r["package_name"] for r in query("SELECT DISTINCT package_name FROM package_versions WHERE has_github_workflows=1")}
        maintainer_to_packages = defaultdict(set)
        package_to_maintainers = defaultdict(set)
        for row in query("SELECT * FROM package_maintainers"):
            maintainer_to_packages[row["maintainer_username"]].add(row["package_name"])
            package_to_maintainers[row["package_name"]].add(row["maintainer_username"])
        reverse = defaultdict(set)
        for row in query("SELECT DISTINCT from_package,to_package FROM dependencies"):
            reverse[row["to_package"]].add(row["from_package"])
        max_w = max((len(v) for v in maintainer_to_packages.values()), default=1)
        computed = {}
        for index, name in enumerate(packages):
            visited, pending = {name}, [name]
            while pending:
                current = pending.pop()
                for neighbor in reverse[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        pending.append(neighbor)
            visited.discard(name)
            portfolios = [len(maintainer_to_packages[m]) for m in package_to_maintainers[name]]
            computed[name] = {"wormability_max": max(portfolios, default=0),
                "wormability_sum": sum(portfolios), "blast_radius": len(visited & workflow_packages),
                "direct_dependents": len(reverse[name]),
                "direct_dependents_with_workflows": len(reverse[name] & workflow_packages),
                "transitive_dependents": len(visited)}
            if index and index % 5000 == 0:
                print(f"Verified graph traversal for {index}/{len(packages)} packages", flush=True)
        max_b = max(r["blast_radius"] for r in computed.values()) or 1
        for row in computed.values():
            row["attacker_roi"] = .5 * row["wormability_max"] / max_w + .5 * row["blast_radius"] / max_b
        consistency = {f: sum(abs(computed[n][f] - db_by_name[n][f]) > (1e-12 if f == "attacker_roi" else 0)
                              for n in packages) for f in FIELDS}
        mismatch = {f: sum(abs(db_by_name[n][f] - csv_by_name[n][f]) > (5.00001e-7 if f == "attacker_roi" else 0)
                           for n in packages) for f in FIELDS}
        tolerance_mismatch = sum(abs(round(db_by_name[n]["attacker_roi"], 6) - csv_by_name[n]["attacker_roi"]) > 1e-12 for n in packages)
        k = math.ceil(.01 * len(packages))
        overlap = {}
        for label, field in [("legacy_score", "attacker_roi"), ("reach", "transitive_dependents"), ("workflow_reach", "blast_radius")]:
            a, b = top(csv_rows, field, k), top(db_rows, field, k)
            pa, pb = membership_probabilities(csv_rows, field, k), membership_probabilities(db_rows, field, k)
            overlap[label] = {"intersection": len(a & b), "union": len(a | b),
                "jaccard": len(a & b)/len(a | b),
                "intersection_descending_names": len(top(csv_rows, field, k, True) & top(db_rows, field, k, True)),
                "expected_intersection_independent_uniform_ties": sum(pa[n]*pb[n] for n in packages),
                "csv_boundary": boundary(csv_rows, field, k), "database_boundary": boundary(db_rows, field, k)}
        within = {}
        for label, rows in [("csv", csv_rows), ("database", db_rows)]:
            a, b = top(rows, "attacker_roi", k), top(rows, "transitive_dependents", k)
            within[label] = {"score_reach_intersection": len(a & b), "score_reach_jaccard": len(a & b) / len(a | b),
                "score_reach_spearman": spearman([r["attacker_roi"] for r in rows], [r["transitive_dependents"] for r in rows])}
        weight_sweep = []
        for step in range(11):
            alpha = step / 10
            queues = []
            for rows in [csv_rows, db_rows]:
                mw = max(r["wormability_max"] for r in rows) or 1
                mb = max(r["blast_radius"] for r in rows) or 1
                scored = [{**r, "sweep_score": alpha*r["wormability_max"]/mw + (1-alpha)*r["blast_radius"]/mb} for r in rows]
                queues.append(top(scored, "sweep_score", k))
            weight_sweep.append({"alpha": alpha, "intersection": len(queues[0]&queues[1]), "jaccard": len(queues[0]&queues[1])/len(queues[0]|queues[1])})
        portfolio_counts = sorted((len(s) for s in maintainer_to_packages.values()), reverse=True)
        maintainer_budget = math.ceil(.01*len(portfolio_counts))
        metadata = {
            "counts": counts, "unique_package_edges": sum(len(s) for s in reverse.values()),
            "edge_relation_counts": query("SELECT relation, COUNT(*) AS rows FROM dependencies GROUP BY relation"),
            "workflow_states": workflow_states, "workflow_packages": len(workflow_packages),
            "github_linked_version_rows": connection.execute("SELECT COUNT(*) FROM package_versions WHERE github_owner IS NOT NULL AND github_repo IS NOT NULL").fetchone()[0],
            "metric_calculation_timestamps": query("SELECT calculated_at, COUNT(*) AS rows FROM package_metrics GROUP BY calculated_at"),
            "advisory_classifications": query("SELECT classification, COUNT(*) AS rows FROM advisories GROUP BY classification"),
            "advisory_package_overlap": connection.execute("SELECT COUNT(DISTINCT a.package_name) FROM advisories a JOIN package_metrics m ON a.package_name=m.package_name").fetchone()[0],
            "top_one_percent_maintainers": maintainer_budget,
            "top_one_percent_maintainer_relations": sum(portfolio_counts[:maintainer_budget]),
            "top_one_percent_maintainer_share": sum(portfolio_counts[:maintainer_budget])/counts["package_maintainers"],
        }
        connection.close()
    temporal_path = ROOT / "platform/research/65_package_temporal_companion_snapshots.csv"
    temporal_rows = read_csv(temporal_path)
    exact_rows = [r for r in temporal_rows if r["snapshot_status"] == "registry_reconstructed_exact"]
    edges_path = ROOT / "platform/research/65_package_temporal_companion_declared_edges.csv"
    temporal = {"ledger_records": len(temporal_rows), "family_identifiers": len({r["event_family"] for r in temporal_rows}),
        "retained_source_objects": len(exact_rows), "retained_family_identifiers": len({r["event_family"] for r in exact_rows}),
        "declared_edges": len(read_csv(edges_path)),
        "source_time_after_cutoff_rows": sum(datetime.fromisoformat(r["pre_event_latest_published_utc"]) >
            datetime.fromisoformat(r["feature_cutoff_utc"]) for r in exact_rows),
        "status": "Repository ledger inventory only; incident sources and raw registry responses not independently re-adjudicated in this audit.",
        "controls": 0}
    provenance = {str(p.relative_to(ROOT)): digest(p) for p in sources + [temporal_path, edges_path,
        ROOT/"platform/research/64_temporal_package_event_ledger.csv", ROOT/"scripts/calculate_metrics.py",
        ROOT/"scripts/collect_data.py", Path(__file__),
        ROOT/"platform/research/benchmark_snapshot_manifest.json",
        ROOT/"platform/research/66_temporal_baseline_and_calibration_gate.json",
        ROOT/"platform/research/51_current_snapshot_structural_analysis.json",
        ROOT/"platform/research/55_current_snapshot_ecosystem_structure.json"]}
    result = {"audit_date": "2026-10-20", "repository_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "scope": "Offline descriptive consistency audit, not prediction or historical installation reconstruction",
        "python_version": sys.version.split()[0],
        "sources_sha256": provenance, "population": len(packages), "review_budget": k,
        "database": metadata, "csv_summary": describe(csv_rows), "database_summary": describe(db_rows),
        "cross_archive_mismatched_packages_by_field": mismatch,
        "roi_mismatches_after_rounding_database_to_six_decimals": tolerance_mismatch,
        "database_recomputation_mismatches": consistency, "cross_archive_queues": overlap,
        "within_archive_queues": within, "weight_sweep": weight_sweep, "temporal_inventory": temporal,
        "tie_policy": "Descending metric, ascending package-name Unicode code points; sensitivity reverses name order. Expected overlap uses independent uniform tie breaking in each queue."}
    write_json(OUT / "artifact_audit.json", result)
    # The export has no package names, maintainer identities, emails, or payloads.
    with (OUT / "field_comparison.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["field", "csv_nonzero", "database_nonzero", "mismatched_packages", "recomputation_mismatches"])
        for f in FIELDS:
            writer.writerow([f, result["csv_summary"][f]["nonzero"], result["database_summary"][f]["nonzero"], mismatch[f], consistency[f]])
    macros = {"PackageCount": len(packages), "ReviewBudget": k,
        "CSVReachPositive": result["csv_summary"]["blast_radius"]["nonzero"],
        "DBReachPositive": result["database_summary"]["blast_radius"]["nonzero"],
        "ScoreQueueIntersection": overlap["legacy_score"]["intersection"],
        "WorkflowQueueIntersection": overlap["workflow_reach"]["intersection"],
        "TemporalRecords": temporal["ledger_records"], "TemporalFamilies": temporal["family_identifiers"],
        "TemporalRetained": temporal["retained_source_objects"], "TemporalEdges": temporal["declared_edges"]}
    (OUT / "numbers.tex").write_text("% Generated by scripts/audit_artifacts.py; do not edit.\n" +
        "".join("\\newcommand{\\"+key+"}{"+f"{value:,}"+"}\n" for key,value in macros.items()))
    (OUT / "field_rows.tex").write_text("% Generated field comparison.\n\\newcommand{\\FieldComparisonRows}{%\n" + "".join(
        f"{label} & {result['csv_summary'][f]['nonzero']:,} & {result['database_summary'][f]['nonzero']:,} & {mismatch[f]:,} \\\\\n"
        for f,label in [("wormability_max", "Maintainer portfolio (max)"), ("wormability_sum", "Maintainer portfolio (sum)"),
            ("blast_radius", "Workflow reach"), ("direct_dependents", "Direct dependents"),
            ("direct_dependents_with_workflows", "Workflow direct dependents"), ("transitive_dependents", "Transitive dependents"), ("attacker_roi", "Legacy score")]) + "}\n")
    print(json.dumps({"mismatches": mismatch, "recomputation": consistency, "queues": overlap,
                      "within": within, "temporal": temporal, "database": metadata}, indent=2))


if __name__ == "__main__":
    main()
