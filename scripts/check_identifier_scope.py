#!/usr/bin/env python3
"""Audit registry names versus context-like graph identifiers, entirely offline.

The original SQLite archive and prospective captures are read-only inputs.  A
greater-than marker identifies a separate graph identifier class; this script
does not rewrite it as a registry name or infer that its leaf has equal rights.
Only aggregate results are exported, without individual maintainer rankings.
"""
from __future__ import annotations

from collections import Counter, deque
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "data/npm_ecosystem.db.zip"
CAPTURE = ROOT / "manuscript/results/prospective_cohort/capture_records.jsonl"
SELECTION = ROOT / "manuscript/results/prospective_cohort/selection_manifest.json"
OUT = ROOT / "manuscript/results/graph_validity/identifier_scope.json"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_incidence(adjacency, initial):
    """Propagate source bitsets exactly, condensing cycles before DAG traversal."""
    reverse = [set() for _ in adjacency]
    for node, neighbors in enumerate(adjacency):
        for neighbor in neighbors:
            reverse[neighbor].add(node)
    seen, finish = set(), []
    for start in range(len(adjacency)):
        if start in seen:
            continue
        seen.add(start)
        stack = [(start, iter(adjacency[start]))]
        while stack:
            node, neighbors = stack[-1]
            neighbor = next(neighbors, None)
            if neighbor is None:
                finish.append(node)
                stack.pop()
            elif neighbor not in seen:
                seen.add(neighbor)
                stack.append((neighbor, iter(adjacency[neighbor])))
    component = [-1] * len(adjacency)
    masks = []
    for start in reversed(finish):
        if component[start] >= 0:
            continue
        number = len(masks)
        masks.append(0)
        component[start] = number
        pending = [start]
        while pending:
            node = pending.pop()
            masks[number] |= initial[node]
            for neighbor in reverse[node]:
                if component[neighbor] < 0:
                    component[neighbor] = number
                    pending.append(neighbor)
    edges = [set() for _ in masks]
    degree = [0] * len(masks)
    for node, neighbors in enumerate(adjacency):
        a = component[node]
        for neighbor in neighbors:
            b = component[neighbor]
            if a != b and b not in edges[a]:
                edges[a].add(b)
                degree[b] += 1
    queue = deque(i for i, d in enumerate(degree) if d == 0)
    visited = 0
    while queue:
        source = queue.popleft()
        visited += 1
        for target in edges[source]:
            masks[target] |= masks[source]
            degree[target] -= 1
            if degree[target] == 0:
                queue.append(target)
    assert visited == len(masks)
    return [masks[c] for c in component]


def aggregate_masks(endpoint_nodes, incidence):
    masks = {}
    for key, nodes in endpoint_nodes.items():
        value = 0
        for node in nodes:
            value |= incidence[node]
        masks[key] = value
    return masks


def incidence_comparison(before, after):
    assert before.keys() == after.keys()
    assert all(after[key] & ~before[key] == 0 for key in before)
    changed_sources = 0
    for key in before:
        changed_sources |= before[key] & ~after[key]
    return {
        "observed_endpoint_count": len(before),
        "endpoints_with_changed_maintainer_source_set": sum(before[k] != after[k] for k in before),
        "maintainers_with_changed_endpoint_set": changed_sources.bit_count(),
        "identity_endpoint_pairs_full_graph": sum(v.bit_count() for v in before.values()),
        "identity_endpoint_pairs_context_nodes_removed": sum(v.bit_count() for v in after.values()),
        "removed_identity_endpoint_pairs": sum((before[k] & ~after[k]).bit_count() for k in before),
        "reachable_endpoints_full_graph": sum(bool(v) for v in before.values()),
        "reachable_endpoints_context_nodes_removed": sum(bool(v) for v in after.values()),
    }


def main():
    # A context node really can mediate a path; do not infer irrelevance solely
    # from the absence of its own metadata or observed maintainer membership.
    assert source_incidence([{1}, {2}, set()], [1, 0, 0]) == [1, 1, 1]
    assert source_incidence([set(), set(), set()], [1, 0, 0]) == [1, 0, 0]
    assert source_incidence([{1}, {0, 2}, set()], [1, 2, 0]) == [3, 3, 3]
    input_hash = sha256(ARCHIVE)
    with tempfile.TemporaryDirectory(prefix="npm-identifier-scope-") as temporary:
        database = Path(temporary) / "ecosystem.db"
        with zipfile.ZipFile(ARCHIVE) as archive, archive.open("npm_ecosystem.db") as source, database.open("wb") as dest:
            shutil.copyfileobj(source, dest)
        connection = sqlite3.connect(f"file:{database}?mode=ro&immutable=1", uri=True)
        names = [r[0] for r in connection.execute("SELECT name FROM packages ORDER BY name")]
        indexes = {name: i for i, name in enumerate(names)}
        context = {name for name in names if ">" in name}
        identities = [r[0] for r in connection.execute("SELECT username FROM maintainers ORDER BY username")]
        identity_indexes = {name: i for i, name in enumerate(identities)}
        initial = [0] * len(names)
        relations = list(connection.execute("SELECT package_name,maintainer_username FROM package_maintainers"))
        for package, maintainer in relations:
            initial[indexes[package]] |= 1 << identity_indexes[maintainer]
        versions = list(connection.execute("SELECT package_name,github_owner,github_repo,has_github_workflows FROM package_versions"))
        edges = list(connection.execute("SELECT from_package,to_package FROM dependencies"))
        state_counts = [
            {"fetched_registry": row[0], "fetched_dependencies": row[1], "identifiers": row[2]}
            for row in connection.execute("SELECT fetched_registry,fetched_dependencies,COUNT(*) FROM packages WHERE instr(name,'>')>0 GROUP BY 1,2 ORDER BY 1,2")
        ]
        connection.close()

    adjacency = [set() for _ in names]
    filtered = [set() for _ in names]
    edge_classes = Counter()
    unique_classes = Counter()
    for dependent, dependency in edges:
        a, b = indexes[dependency], indexes[dependent]
        category = ("context" if dependency in context else "ordinary") + "_to_" + ("context" if dependent in context else "ordinary")
        edge_classes[category] += 1
        if b not in adjacency[a]:
            unique_classes[category] += 1
            adjacency[a].add(b)
        if dependency not in context and dependent not in context:
            filtered[a].add(b)
    workflow_packages, workflow_repositories = {}, {}
    for package, owner, repo, flag in versions:
        if flag != 1:
            continue
        workflow_packages[package] = {indexes[package]}
        if owner and repo:
            key = owner.casefold() + "/" + repo.casefold().removesuffix(".git")
            workflow_repositories.setdefault(key, set()).add(indexes[package])
    before = source_incidence(adjacency, initial)
    after = source_incidence(filtered, initial)
    comparisons = {}
    for label, endpoints in [("workflow_packages", workflow_packages), ("workflow_repositories", workflow_repositories)]:
        comparisons[label] = incidence_comparison(aggregate_masks(endpoints, before), aggregate_masks(endpoints, after))
    # A maintainer union can conceal a changed individual package closure.  The
    # separate root incidence check also resolves effects on sum/max baselines.
    ordinary_initial = [0 if name in context else 1 << i for i, name in enumerate(names)]
    root_before = source_incidence(adjacency, ordinary_initial)
    root_after = source_incidence(filtered, ordinary_initial)
    root_comparisons = {}
    for label, endpoints in [("workflow_packages", workflow_packages), ("workflow_repositories", workflow_repositories)]:
        roots_before = aggregate_masks(endpoints, root_before)
        roots_after = aggregate_masks(endpoints, root_after)
        values = incidence_comparison(roots_before, roots_after)
        changed_roots = 0
        for key in roots_before:
            changed_roots |= roots_before[key] & ~roots_after[key]
        root_comparisons[label] = {
            key.replace("identity_endpoint", "ordinary_root_endpoint").replace("maintainer_source", "ordinary_root_source").replace("maintainers_with", "ordinary_roots_with"): value
            for key, value in values.items()
        }
        root_comparisons[label]["changed_roots_with_observed_maintainer"] = sum(
            bool(initial[i]) and bool(changed_roots & (1 << i)) for i in range(len(names))
        )

    records = [json.loads(line) for line in CAPTURE.read_text().splitlines() if line.strip()]
    selected = json.loads(SELECTION.read_text())["selected_package_names"]
    assert len(selected) == len(set(selected)) == len(records) == 100
    assert sorted(selected) == sorted(row["package_name"] for row in records)
    assert all(row["documented_publisher_compromise"] is None and row["outcome_status"] == "pending" for row in records)
    prospective_counts = Counter(("context" if ">" in row["package_name"] else "ordinary", row.get("http_status"), row["capture_status"]) for row in records)
    for row in records:
        if ">" in row["package_name"]:
            assert row["package_name"] in context
    result = {
        "audit": "Registry-name scope and context-node influence audit",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "client_study_date": "2026-10-20",
        "source_sha256": {
            "data/npm_ecosystem.db.zip": input_hash,
            "scripts/check_identifier_scope.py": sha256(Path(__file__)),
            str(CAPTURE.relative_to(ROOT)): sha256(CAPTURE),
            str(SELECTION.relative_to(ROOT)): sha256(SELECTION),
        },
        "method": "Temporary extraction; immutable read-only SQLite; exact SCC source-bitset propagation; no network and no package execution",
        "identifier_classification": "Contains '>' marks a context-like identifier retained from dependency metadata; all remaining graph identifiers are called ordinary names, without asserting each remains a currently registered npm package.",
        "graph_identifier_count": len(names),
        "ordinary_name_count": len(names) - len(context),
        "context_marker_identifier_count": len(context),
        "context_identifier_fraction": len(context) / len(names),
        "context_metadata_rows": sum(row[0] in context for row in versions),
        "context_package_maintainer_relations": sum(package in context for package, _ in relations),
        "context_workflow_positive_rows": sum(row[0] in context and row[3] == 1 for row in versions),
        "context_collection_state_counts": state_counts,
        "edge_orientation": "Influence direction: dependency -> dependent; rows retain original distinct version-edge multiplicity",
        "version_edge_classes": dict(sorted(edge_classes.items())),
        "unique_package_edge_classes": dict(sorted(unique_classes.items())),
        "context_removal_source_incidence_sensitivity": comparisons,
        "context_removal_ordinary_root_incidence_sensitivity": root_comparisons,
        "primary_workflow_repository_incidence_identical_after_context_removal": comparisons["workflow_repositories"]["removed_identity_endpoint_pairs"] == 0,
        "workflow_package_incidence_identical_after_context_removal": comparisons["workflow_packages"]["removed_identity_endpoint_pairs"] == 0,
        "prospective_pilot": {
            "original_frozen_sample_size": len(selected),
            "ordinary_names_selected": sum(">" not in name for name in selected),
            "context_identifiers_selected": sum(">" in name for name in selected),
            "capture_status_by_identifier_class": [
                {"identifier_class": key[0], "http_status": key[1], "capture_status": key[2], "records": value}
                for key, value in sorted(prospective_counts.items(), key=lambda item: str(item[0]))
            ],
            "all_100_outcomes_null_and_pending": True,
            "reinterpretation": "Preserve the original sample and its failed observations. Context identifiers are not independent registry-package candidates. Do not replace them with their leaves or silently resample; any ordinary-name cohort requires a separately frozen selection.",
        },
        "validation": {"toy_context_mediation_and_cycle_checks": True, "source_archive_unchanged": sha256(ARCHIVE) == input_hash},
        "limitations": [
            "Context removal is a sensitivity, not a repaired dependency model; context nodes can encode bundle relationships and must not be aliased to ordinary package leaves.",
            "Identical primary source-incidence sets imply identical C/H/P for any fixed maintainer selection, but all-package endpoint counts and rankings may change when context endpoints are excluded.",
            "Registry failures and missing metadata do not imply safe, malicious, or benign outcomes.",
        ],
    }
    assert result["validation"]["source_archive_unchanged"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
