#!/usr/bin/env python3
"""Exact, offline structural intervention study; source archive is read-only.

No package, maintainer, repository names, emails, or individual rankings are
published.  A reverse dependency edge denotes possible structural influence,
not code execution, an exploitable dependency, or an observed incident.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import csv
from datetime import datetime, timezone
import hashlib
import heapq
import json
import math
from pathlib import Path
import random
import re
import shutil
import sqlite3
import statistics
import subprocess
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "manuscript/results/structural_interventions"
BUDGETS = (1, 5, 10, 25, 50, 100)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="") as stream:
        w = csv.DictWriter(stream, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def bit_indices(bits):
    while bits:
        low = bits & -bits
        yield low.bit_length() - 1
        bits ^= low


def union(values):
    answer = 0
    for value in values:
        answer |= value
    return answer


def quantile(values, q):
    """Linearly interpolated descriptive simulation quantile (not a CI)."""
    values = sorted(values)
    at = (len(values) - 1) * q
    lo = int(at)
    hi = min(lo + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (at - lo)


def describe(values):
    values = list(values)
    return {"n": len(values), "min": min(values), "median": statistics.median(values),
            "p90": quantile(values, .9), "p99": quantile(values, .99),
            "max": max(values), "mean": statistics.mean(values)}


def scc_condensation(adj):
    """Iterative Kosaraju, followed by an explicitly checked DAG order."""
    n = len(adj)
    backward = [[] for _ in adj]
    for source, targets in enumerate(adj):
        for target in targets:
            backward[target].append(source)
    seen = set()
    order = []
    for start in range(n):
        if start in seen:
            continue
        seen.add(start)
        pending = [(start, iter(adj[start]))]
        while pending:
            node, neighbors = pending[-1]
            target = next(neighbors, None)
            if target is None:
                order.append(node)
                pending.pop()
            elif target not in seen:
                seen.add(target)
                pending.append((target, iter(adj[target])))
    component = [-1] * n
    members = []
    for start in reversed(order):
        if component[start] >= 0:
            continue
        cid = len(members)
        members.append([])
        pending = [start]
        component[start] = cid
        while pending:
            node = pending.pop()
            members[cid].append(node)
            for target in backward[node]:
                if component[target] < 0:
                    component[target] = cid
                    pending.append(target)
    edges = [set() for _ in members]
    indegree = [0] * len(members)
    for source, targets in enumerate(adj):
        a = component[source]
        for target in targets:
            b = component[target]
            if a != b and b not in edges[a]:
                edges[a].add(b)
                indegree[b] += 1
    pending = deque(i for i, degree in enumerate(indegree) if degree == 0)
    topo = []
    while pending:
        node = pending.popleft()
        topo.append(node)
        for target in sorted(edges[node]):
            indegree[target] -= 1
            if not indegree[target]:
                pending.append(target)
    assert len(topo) == len(members)
    return component, members, edges, topo


def propagate_endpoint_bits(component, members, edges, topo, node_bits):
    masks = [union(node_bits[node] for node in group) for group in members]
    for source in reversed(topo):
        for target in edges[source]:
            masks[source] |= masks[target]
    return [masks[cid] for cid in component]


def propagate_source_bits(component, members, edges, topo, package_maintainers):
    masks = [union(1 << m for node in group for m in package_maintainers[node]) for group in members]
    for source in topo:
        for target in edges[source]:
            masks[target] |= masks[source]
    return [masks[cid] for cid in component]


def bfs(adj, start, max_depth=None):
    result = 1 << start
    pending = deque([(start, 0)])
    while pending:
        node, depth = pending.popleft()
        if max_depth is not None and depth >= max_depth:
            continue
        for target in adj[node]:
            if not result & (1 << target):
                result |= 1 << target
                pending.append((target, depth + 1))
    return result


def load_data(connection):
    names = [r[0] for r in connection.execute("SELECT name FROM packages ORDER BY name")]
    indexes = {name: i for i, name in enumerate(names)}
    identities = list(connection.execute("SELECT username,email_hash FROM maintainers ORDER BY username"))
    id_indexes = {row[0]: i for i, row in enumerate(identities)}
    portfolios = [set() for _ in identities]
    package_maintainers = [set() for _ in names]
    for package, maintainer in connection.execute("SELECT package_name,maintainer_username FROM package_maintainers"):
        p, m = indexes[package], id_indexes[maintainer]
        portfolios[m].add(p)
        package_maintainers[p].add(m)
    assert all(portfolios)
    adj = [set() for _ in names]
    version_edges = 0
    for dependent, dependency in connection.execute("SELECT from_package,to_package FROM dependencies"):
        adj[indexes[dependency]].add(indexes[dependent])
        version_edges += 1
    # GitHub owner/repo is case-insensitive. A trailing .git is a transport suffix.
    workflow = set()
    checked = set()
    repositories = set()
    mapped = defaultdict(set)
    positive_repo_packages = defaultdict(set)
    link_consistent_positive = defaultdict(set)
    inconsistent_rows = inconsistent_positive_rows = 0
    version_rows = list(connection.execute("SELECT package_name,github_owner,github_repo,has_github_workflows,fetched_workflows,repository_url FROM package_versions"))
    for package, owner, repository, flag, fetched, raw_url in version_rows:
        p = indexes[package]
        if flag == 1:
            workflow.add(p)
        if fetched == 1:
            checked.add(p)
        if owner and repository:
            repository = repository.lower()
            if repository.endswith(".git"):
                repository = repository[:-4]
            key = owner.lower() + "/" + repository
            repositories.add(key)
            mapped[p].add(key)
            parsed = parse_repo(raw_url)
            consistent = parsed == key
            inconsistent_rows += not consistent
            if flag == 1:
                positive_repo_packages[p].add(key)
                inconsistent_positive_rows += not consistent
                if consistent:
                    link_consistent_positive[p].add(key)
    repo_indexes = {key: i for i, key in enumerate(sorted(repositories))}
    repo_nodes = [union(1 << repo_indexes[key] for key in mapped[p]) for p in range(len(names))]
    workflow_repos = union(1 << repo_indexes[key] for keys in positive_repo_packages.values() for key in keys)
    workflow_repo_nodes = [union(1 << repo_indexes[key] for key in positive_repo_packages[p]) for p in range(len(names))]
    safe_workflow_repo_nodes = [union(1 << repo_indexes[key] for key in link_consistent_positive[p]) for p in range(len(names))]
    metadata = {
        "packages": len(names), "identities": len(identities),
        "maintainer_package_relations": sum(map(len, portfolios)),
        "packages_with_no_observed_maintainer": sum(not x for x in package_maintainers),
        "package_version_rows": len(version_rows), "version_edges": version_edges,
        "unique_package_edges": sum(map(len, adj)),
        "self_package_edges": sum(i in targets for i, targets in enumerate(adj)),
        "workflow_positive_packages": len(workflow), "workflow_checked_packages": len(checked),
        "workflow_unknown_packages": len(names) - len(checked),
        "linked_packages": sum(bool(v) for v in mapped.values()), "distinct_linked_repositories": len(repositories),
        "workflow_positive_repositories": workflow_repos.bit_count(),
        "packages_mapping_to_multiple_repositories": sum(len(v) > 1 for v in mapped.values()),
        "relation_row_counts": dict(connection.execute("SELECT relation,COUNT(*) FROM dependencies GROUP BY relation")),
        "registry_fetch_states": {str(k): v for k, v in connection.execute("SELECT fetched_registry,COUNT(*) FROM packages GROUP BY fetched_registry")},
        "distinct_email_hash_groups": len({row[1] for row in identities}),
        "email_hash_groups_with_multiple_usernames": sum(n > 1 for n in Counter(row[1] for row in identities).values()),
        "repository_link_inconsistent_version_rows": inconsistent_rows,
        "workflow_positive_link_inconsistent_version_rows": inconsistent_positive_rows,
        "link_consistent_workflow_positive_repositories": union(safe_workflow_repo_nodes).bit_count(),
    }
    # Names and hashes remain local memory only.
    return names, identities, portfolios, package_maintainers, adj, workflow, checked, repo_nodes, workflow_repo_nodes, safe_workflow_repo_nodes, metadata


def parse_repo(url):
    """Lexical source-URL check; does not validate redirects or actual identity."""
    if not isinstance(url, str):
        return None
    candidate = url.strip().replace("git+", "", 1)
    if candidate.startswith("github:"):
        candidate = "https://github.com/" + candidate[len("github:"):]
    match = re.search(r"(?:^|[/@])github\.com[:/]([^/#?]+)/([^/#?]+)", candidate, re.I)
    if not match:
        return None
    owner, repository = match.groups()
    if repository.endswith(".git"):
        repository = repository[:-4]
    return owner.lower() + "/" + repository.lower() if owner and repository else None


def version_continuous_representation(connection, names, package_maintainers, wf_repo_nodes):
    """Version-continuous UNION, still not one installed resolution context."""
    package_indexes = {name: p for p, name in enumerate(names)}
    rows = list(connection.execute("SELECT from_package,from_version,to_package,to_version FROM dependencies"))
    nodes = {(a, av) for a, av, b, bv in rows} | {(b, bv) for a, av, b, bv in rows}
    nodes.update(connection.execute("SELECT package_name,version FROM package_versions"))
    nodes = sorted(nodes)
    indexes = {node: v for v, node in enumerate(nodes)}
    adj = [set() for _ in nodes]
    for a, av, b, bv in rows:
        adj[indexes[b, bv]].add(indexes[a, av])
    component, members, edges, topo = scc_condensation(adj)
    node_packages = [package_indexes[name] for name, version in nodes]
    version_reach = propagate_endpoint_bits(component, members, edges, topo, [1 << p for p in node_packages])
    version_repo_reach = propagate_endpoint_bits(component, members, edges, topo, [wf_repo_nodes[p] for p in node_packages])
    version_sources = propagate_source_bits(component, members, edges, topo, [package_maintainers[p] for p in node_packages])
    package_reach = [1 << p for p in range(len(names))]
    repo_reach = list(wf_repo_nodes)
    package_sources = [union(1 << m for m in group) for group in package_maintainers]
    for v, p in enumerate(node_packages):
        package_reach[p] |= version_reach[v]
        repo_reach[p] |= version_repo_reach[v]
        package_sources[p] |= version_sources[v]
    return package_reach, repo_reach, package_sources, {
        "nodes": len(nodes), "sccs": len(members),
        "definition": "Seed every observed version for every maintained package; traverse exact matching version nodes in retained union; project resulting endpoints to package names. Missing-version seed names retain their own package. Workflow endpoint flags stay package-level to isolate path representation. Multiple resolution contexts still coexist."}


def endpoint_data(package_masks, portfolios, package_counts=None):
    masks = [union(package_masks[p] for p in portfolio) for portfolio in portfolios]
    sizes = [mask.bit_count() for mask in masks]
    if package_counts is None:
        package_counts = [mask.bit_count() for mask in package_masks]
    scores = {
        "portfolio": [len(p) for p in portfolios],
        "sum_package_reach": [sum(package_counts[p] for p in portfolio) for portfolio in portfolios],
        "max_package_reach": [max((package_counts[p] for p in portfolio), default=0) for portfolio in portfolios],
        "exact_union": sizes,
    }
    return {"masks": masks, "sizes": sizes, "scores": scores,
            "universe": union(masks), "total_pairs": sum(sizes)}


def lazy_greedy(masks, candidates, tie_order, budget):
    """Exact maximum-marginal greedy with lazy submodular upper bounds."""
    heap = [(-masks[m].bit_count(), tie_order[m], m) for m in candidates]
    heapq.heapify(heap)
    selected, covered, calls = [], 0, 0
    while heap and len(selected) < budget:
        old_bound, tie, m = heapq.heappop(heap)
        gain = (masks[m] & ~covered).bit_count()
        calls += 1
        key = (-gain, tie, m)
        if not heap or key <= heap[0]:
            selected.append(m)
            covered |= masks[m]
        else:
            heapq.heappush(heap, key)
    return selected, calls


def source_signature_groups(endpoint_sources):
    """Keep only signatures protectable by our largest identity budget."""
    grouped = Counter(mask for mask in endpoint_sources if mask)
    return [(sources, count, sources.bit_count()) for sources, count in grouped.items()
            if sources.bit_count() <= max(BUDGETS)]


def full_protection(signatures, selected_mask, budget):
    return sum(count for sources, count, cardinality in signatures
               if cardinality <= budget and sources & selected_mask == sources)


def evaluate_order(order, endpoint, signatures, method, endpoint_label, extra=None):
    rows = []
    covered, selected_mask, pair_sum = 0, 0, 0
    endpoint_total = endpoint["observed_endpoint_total"]
    for i, m in enumerate(order, 1):
        covered |= endpoint["masks"][m]
        selected_mask |= 1 << m
        pair_sum += endpoint["sizes"][m]
        if i not in BUDGETS:
            continue
        count = covered.bit_count()
        protected = full_protection(signatures, selected_mask, i)
        row = {"endpoint": endpoint_label, "method": method, "budget": i,
               "covered_endpoints": count,
               "coverage_fraction_observed": count / endpoint_total,
               "coverage_fraction_reachable": count / endpoint["universe"].bit_count(),
               "removed_identity_endpoint_pairs": pair_sum,
               "scenario_exposure_reduction_fraction": pair_sum / endpoint["total_pairs"],
               "uniform_scenario_residual_expected_endpoints": (endpoint["total_pairs"] - pair_sum) / len(endpoint["masks"]),
               "selected_overlap_redundancy_fraction": 1 - count / pair_sum if pair_sum else 0,
               "fully_protected_endpoints": protected,
               "covered_but_residually_exposed_endpoints": count - protected,
               "full_protection_fraction_reachable": protected / endpoint["universe"].bit_count(),
               "residual_possible_endpoints": endpoint["universe"].bit_count() - protected}
        if extra:
            row.update(extra)
        rows.append(row)
    return rows


def benchmark(endpoints, signatures, trials):
    deterministic, simulations, diagnostics = [], [], {}
    all_orders = {}
    for label, endpoint in endpoints.items():
        print(f"Benchmarking {label}", flush=True)
        n = len(endpoint["masks"])
        tie = list(range(n))  # usernames sorted in input; only aggregate output is released.
        orders = {method: sorted(range(n), key=lambda m: (-scores[m], tie[m]))[:max(BUDGETS)]
                  for method, scores in endpoint["scores"].items()}
        orders["greedy_coverage"], calls = lazy_greedy(endpoint["masks"], range(n), tie, max(BUDGETS))
        all_orders[label] = orders
        for method, order in orders.items():
            deterministic.extend(evaluate_order(order, endpoint, signatures[label], method, label))
        # A reverse identity-order rerun isolates deterministic tie sensitivity.
        reverse_tie = [n - i for i in range(n)]
        tie_results = []
        for method, scores in endpoint["scores"].items():
            order = sorted(range(n), key=lambda m: (-scores[m], reverse_tie[m]))[:max(BUDGETS)]
            tie_results.extend(evaluate_order(order, endpoint, signatures[label], method, label))
        order, _ = lazy_greedy(endpoint["masks"], range(n), reverse_tie, max(BUDGETS))
        tie_results.extend(evaluate_order(order, endpoint, signatures[label], "greedy_coverage", label))
        diagnostics[label] = {"greedy_marginal_evaluations": calls,
                              "reverse_tie_results": tie_results,
                              "identity_exposure_sizes": describe(endpoint["sizes"]),
                              "distinct_identity_endpoint_sets": len(set(endpoint["masks"])),
                              "zero_reach_identities": sum(size == 0 for size in endpoint["sizes"]),
                              "total_identity_endpoint_pairs": endpoint["total_pairs"],
                              "reachable_endpoints": endpoint["universe"].bit_count()}
        for seed in range(trials):
            order = random.Random(seed).sample(range(n), max(BUDGETS))
            simulations.extend(evaluate_order(order, endpoint, signatures[label], "uniform_random", label, {"seed": seed}))
    return deterministic, simulations, diagnostics, all_orders


def summarize_random(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["endpoint"], row["budget"])].append(row)
    results = []
    for (endpoint, budget), group in sorted(grouped.items()):
        result = {"endpoint": endpoint, "budget": budget, "trials": len(group)}
        for key in ("covered_endpoints", "coverage_fraction_observed", "scenario_exposure_reduction_fraction",
                    "fully_protected_endpoints", "selected_overlap_redundancy_fraction"):
            values = [r[key] for r in group]
            result.update({key + "_mean": statistics.mean(values),
                           key + "_sd": statistics.stdev(values) if len(values) > 1 else 0,
                           key + "_p025": quantile(values, .025),
                           key + "_p975": quantile(values, .975)})
        results.append(result)
    return results


def analytic_random_baseline(endpoint_sources, n, label, observed_total):
    """Finite-population expectations for a uniform k-subset of identities."""
    source_counts = Counter(mask.bit_count() for mask in endpoint_sources if mask)
    rows = []
    for budget in BUDGETS:
        covered = protected = 0.0
        for d, count in source_counts.items():
            if n - d < budget:
                hit = 1.0
            else:
                hit = -math.expm1(sum(math.log1p(-d / (n - j)) for j in range(budget)))
            all_selected = math.prod((budget - j) / (n - j) for j in range(d)) if d <= budget else 0.0
            covered += count * hit
            protected += count * all_selected
        rows.append({"endpoint": label, "budget": budget,
                     "expected_covered_endpoints": covered,
                     "expected_coverage_fraction_observed": covered / observed_total,
                     "expected_scenario_exposure_reduction_fraction": budget / n,
                     "expected_fully_protected_endpoints": protected})
    return rows


def checks(adj, full, endpoints, source_masks, connection, names):
    starts = sorted(set(random.Random(73191).sample(range(len(adj)), min(256, len(adj)))) |
                    set(sorted(range(len(full)), key=lambda p: -full[p].bit_count())[:32]))
    assert all(bfs(adj, start) == full[start] for start in starts)
    stored = dict(connection.execute("SELECT package_name,transitive_dependents FROM package_metrics"))
    mismatches = sum(full[p].bit_count() - 1 != stored[name] for p, name in enumerate(names))
    assert mismatches == 0
    for endpoint in endpoints.values():
        n = len(endpoint["masks"])
        for m in random.Random(9931).sample(range(n), min(100, n)):
            assert endpoint["sizes"][m] <= endpoint["scores"]["sum_package_reach"][m]
            assert endpoint["sizes"][m] >= endpoint["scores"]["max_package_reach"][m]
    # Dual propagation independently verifies identity-to-endpoint incidence.
    for p in starts:
        expected = union(1 << m for m, mask in enumerate(endpoints["all_packages"]["masks"]) if mask & (1 << p))
        assert expected == source_masks[p]
    # Small exact test checks lazy greedy against exhaustive marginal updates.
    masks = [0b00111, 0b11000, 0b11100, 0b00001]
    lazy, _ = lazy_greedy(masks, range(4), list(range(4)), 4)
    naive, covered = [], 0
    for _ in range(4):
        candidate = min((m for m in range(4) if m not in naive),
                        key=lambda m: (-(masks[m] & ~covered).bit_count(), m))
        naive.append(candidate)
        covered |= masks[candidate]
    assert lazy == naive
    return {"independent_bfs_roots_checked": len(starts),
            "all_package_metric_transitive_count_comparisons": len(names),
            "stored_transitive_count_mismatches": mismatches,
            "dual_incidence_package_checks": len(starts),
            "lazy_greedy_matches_exhaustive_small_example": True,
            "maintainer_sum_max_union_bounds": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=ROOT / "data/npm_ecosystem.db.zip")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--random-trials", type=int, default=200)
    args = parser.parse_args()
    assert args.random_trials >= 2
    started = time.monotonic()
    args.output.mkdir(parents=True, exist_ok=True)
    # Freeze the internally planned comparisons before extracting or analyzing
    # source data. This is a local analysis plan, not external preregistration.
    write_json(args.output / "run_config.json", {
        "status": "Plan saved before computations in this execution; exploratory study, not externally preregistered",
        "study_date": "2026-10-20", "budgets": list(BUDGETS),
        "random_seeds": list(range(args.random_trials)),
        "methods": ["portfolio", "sum_package_reach", "max_package_reach", "exact_union", "greedy_coverage", "uniform_random"],
        "primary_endpoints": ["all_packages", "workflow_packages", "workflow_repositories"],
        "visibility_endpoints": ["linked_repositories", "workflow_checked_packages"],
        "estimands": ["H(S)=sum_selected|E_m| / sum_all|E_m|", "C(S)=|union_selected E_m|", "P(S)=count_e(nonempty A_e subset S)"],
        "sensitivities": ["reverse_ties", "depth_0_1_full", "endpoint_transfer", "exclude_top_portfolios_1_5_10", "exact_email_hash_grouping", "version_continuous_union", "exclude_link_inconsistent_workflow_observations"],
        "source_archive_sha256": sha256(args.archive),
        "analysis_script_sha256": sha256(__file__)})
    with tempfile.TemporaryDirectory(prefix="npm-structural-study-") as tmp:
        database = Path(tmp) / "ecosystem.db"
        with zipfile.ZipFile(args.archive) as z, z.open("npm_ecosystem.db") as src, database.open("wb") as dst:
            shutil.copyfileobj(src, dst)
        database_hash = sha256(database)
        c = sqlite3.connect(f"file:{database}?mode=ro&immutable=1", uri=True)
        names, identities, portfolios, pmaint, adj, workflow, checked, repo_nodes, wf_repo_nodes, safe_wf_repo_nodes, population = load_data(c)
        print(f"Loaded {population['packages']} packages, {population['identities']} identities", flush=True)
        component, members, edges, topo = scc_condensation(adj)
        population.update({"strongly_connected_components": len(members),
                           "nontrivial_sccs": sum(len(group) > 1 for group in members),
                           "largest_scc_packages": max(map(len, members)),
                           "condensation_edges": sum(map(len, edges))})
        full = propagate_endpoint_bits(component, members, edges, topo, [1 << p for p in range(len(names))])
        source_masks = propagate_source_bits(component, members, edges, topo, pmaint)
        wf_bits = union(1 << p for p in workflow)
        checked_bits = union(1 << p for p in checked)
        repo_full = propagate_endpoint_bits(component, members, edges, topo, repo_nodes)
        wf_repo_full = propagate_endpoint_bits(component, members, edges, topo, wf_repo_nodes)
        node_masks = {"all_packages": full,
                      "workflow_packages": [mask & wf_bits for mask in full],
                      "workflow_repositories": wf_repo_full,
                      "linked_repositories": repo_full,
                      "workflow_checked_packages": [mask & checked_bits for mask in full]}
        observed_counts = {"all_packages": population["packages"],
                           "workflow_packages": population["workflow_positive_packages"],
                           "workflow_repositories": population["workflow_positive_repositories"],
                           "linked_repositories": population["distinct_linked_repositories"],
                           "workflow_checked_packages": population["workflow_checked_packages"]}
        endpoints = {label: endpoint_data(masks, portfolios) for label, masks in node_masks.items()}
        for label, endpoint in endpoints.items():
            endpoint["observed_endpoint_total"] = observed_counts[label]
        repo_sources = [0] * population["distinct_linked_repositories"]
        wf_repo_sources = [0] * population["distinct_linked_repositories"]
        for p, sources in enumerate(source_masks):
            for r in bit_indices(repo_nodes[p]):
                repo_sources[r] |= sources
            for r in bit_indices(wf_repo_nodes[p]):
                wf_repo_sources[r] |= sources
        signatures = {
            "all_packages": source_signature_groups(source_masks),
            "workflow_packages": source_signature_groups(source_masks[p] for p in workflow),
            "workflow_repositories": source_signature_groups(wf_repo_sources),
            "linked_repositories": source_signature_groups(repo_sources),
            "workflow_checked_packages": source_signature_groups(source_masks[p] for p in checked)}
        inverse_sources = {"all_packages": source_masks,
                           "workflow_packages": [source_masks[p] for p in workflow],
                           "workflow_repositories": wf_repo_sources,
                           "linked_repositories": repo_sources,
                           "workflow_checked_packages": [source_masks[p] for p in checked]}
        analytic_random = [row for label, sources in inverse_sources.items()
                           for row in analytic_random_baseline(sources, len(portfolios), label, observed_counts[label])]
        validation = checks(adj, full, endpoints, source_masks, c, names)
        print("Independent traversal and incidence checks passed", flush=True)
        deterministic, simulations, diagnostics, orders = benchmark(endpoints, signatures, args.random_trials)
        # Graph-depth ablation: rank/choose from 0- and 1-hop observations, evaluate
        # against the identical full-transitive endpoint target and denominator.
        ablations = []
        for depth in (0, 1):
            depth_packages = [(1 << p) | (union(1 << v for v in adj[p]) if depth else 0) for p in range(len(names))]
            depth_repo = [union(wf_repo_nodes[v] for v in bit_indices(mask)) for mask in depth_packages]
            for label, masks in [("all_packages", depth_packages),
                                 ("workflow_packages", [mask & wf_bits for mask in depth_packages]),
                                 ("workflow_repositories", depth_repo)]:
                data = endpoint_data(masks, portfolios)
                tie = list(range(len(portfolios)))
                selections = {method: sorted(range(len(portfolios)), key=lambda m: (-scores[m], m))[:max(BUDGETS)]
                              for method, scores in data["scores"].items()}
                selections["greedy_coverage"], _ = lazy_greedy(data["masks"], range(len(portfolios)), tie, max(BUDGETS))
                for method, order in selections.items():
                    ablations.extend(evaluate_order(order, endpoints[label], signatures[label], method, label,
                                                    {"ablation": "graph_depth", "source_representation": f"depth_{depth}"}))
        # Endpoint representation transfer isolates package-to-repository dedup.
        for source, target in [("all_packages", "workflow_repositories"),
                               ("workflow_packages", "workflow_repositories"),
                               ("workflow_repositories", "workflow_packages")]:
            for method, order in orders[source].items():
                ablations.extend(evaluate_order(order, endpoints[target], signatures[target], method, target,
                                                {"ablation": "endpoint_transfer", "source_representation": source}))
        # Exclusion is a candidate-set sensitivity, not a claim these are bots.
        portfolio_order = sorted(range(len(portfolios)), key=lambda m: (-len(portfolios[m]), m))
        for exclude in (1, 5, 10):
            candidates = [m for m in range(len(portfolios)) if m not in set(portfolio_order[:exclude])]
            for label in ("all_packages", "workflow_repositories"):
                data = endpoints[label]
                for method in ("portfolio", "exact_union", "greedy_coverage"):
                    if method == "greedy_coverage":
                        order, _ = lazy_greedy(data["masks"], candidates, list(range(len(portfolios))), max(BUDGETS))
                    else:
                        order = sorted(candidates, key=lambda m: (-data["scores"][method][m], m))[:max(BUDGETS)]
                    ablations.extend(evaluate_order(order, data, signatures[label], method, label,
                                                    {"ablation": "exclude_largest_portfolios", "source_representation": f"exclude_{exclude}"}))
        # Uniform identity-loss expectation has no event label or likelihood fit.
        concentration = []
        for label, data in endpoints.items():
            sorted_sizes = sorted(data["sizes"], reverse=True)
            for budget in BUDGETS:
                concentration.append({"endpoint": label, "budget": budget,
                                      "identity_fraction": budget / len(portfolios),
                                      "top_scenario_pair_fraction": sum(sorted_sizes[:budget]) / data["total_pairs"],
                                      "maximum_possible_distinct_endpoint_upper_bound": min(data["universe"].bit_count(), sum(sorted_sizes[:budget]))})
        # Email-hash equivalence sensitivity: does not assert common legal person.
        grouped = defaultdict(set)
        for m, row in enumerate(identities):
            grouped[row[1]].update(portfolios[m])
        cluster_portfolios = list(grouped.values())
        cluster_pmaint = [set() for _ in names]
        for m, portfolio in enumerate(cluster_portfolios):
            for p in portfolio:
                cluster_pmaint[p].add(m)
        cluster_sources = propagate_source_bits(component, members, edges, topo, cluster_pmaint)
        cluster_wf_repo_sources = [0] * population["distinct_linked_repositories"]
        for p, sources in enumerate(cluster_sources):
            for r in bit_indices(wf_repo_nodes[p]):
                cluster_wf_repo_sources[r] |= sources
        email_results = []
        for label in ("all_packages", "workflow_repositories"):
            data = endpoint_data(node_masks[label], cluster_portfolios)
            data["observed_endpoint_total"] = observed_counts[label]
            cluster_sigs = source_signature_groups(cluster_sources if label == "all_packages" else cluster_wf_repo_sources)
            for method in ("portfolio", "exact_union", "greedy_coverage"):
                if method == "greedy_coverage":
                    order, _ = lazy_greedy(data["masks"], range(len(cluster_portfolios)), list(range(len(cluster_portfolios))), max(BUDGETS))
                else:
                    order = sorted(range(len(cluster_portfolios)), key=lambda m: (-data["scores"][method][m], m))[:max(BUDGETS)]
                email_results.extend(evaluate_order(order, data, cluster_sigs, method, label,
                                                    {"identity_unit": "exact_email_hash_equivalence_group"}))
        # Every emitted order is nested, coverage and pair removal are monotone.
        for rows in (deterministic, simulations):
            groups = defaultdict(list)
            for row in rows:
                groups[(row["endpoint"], row["method"], row.get("seed"))].append(row)
            for group in groups.values():
                group.sort(key=lambda r: r["budget"])
                for field in ("covered_endpoints", "removed_identity_endpoint_pairs", "fully_protected_endpoints"):
                    assert all(a[field] <= b[field] for a, b in zip(group, group[1:]))
        validation["all_primary_and_random_budget_curves_monotone"] = True
        for label in endpoints:
            data = endpoints[label]
            expected = sum(data["sizes"]) / len(portfolios)
            assert abs(expected - data["total_pairs"] / len(portfolios)) < 1e-9
        print("Running version-continuity and repository-link sensitivities", flush=True)
        version_packages, version_repos, version_sources, version_metadata = version_continuous_representation(c, names, pmaint, wf_repo_nodes)
        assert all(v & ~p == 0 for v, p in zip(version_packages, full))
        version_metadata["package_roots_with_changed_reach"] = sum(v != p for v, p in zip(version_packages, full))
        version_repo_sources = [0] * population["distinct_linked_repositories"]
        for p, sources in enumerate(version_sources):
            for r in bit_indices(wf_repo_nodes[p]):
                version_repo_sources[r] |= sources
        version_sigs = {"all_packages": source_signature_groups(version_sources),
                        "workflow_packages": source_signature_groups(version_sources[p] for p in workflow),
                        "workflow_repositories": source_signature_groups(version_repo_sources)}
        version_nodes = {"all_packages": version_packages,
                         "workflow_packages": [v & wf_bits for v in version_packages],
                         "workflow_repositories": version_repos}
        version_results = []
        for label, masks in version_nodes.items():
            data = endpoint_data(masks, portfolios)
            data["observed_endpoint_total"] = observed_counts[label]
            version_metadata[label] = {
                "identities_with_changed_exact_union": sum(a != b for a, b in zip(data["masks"], endpoints[label]["masks"])),
                "total_identity_endpoint_pairs": data["total_pairs"],
                "reachable_endpoints": data["universe"].bit_count()}
            vorders = {method: sorted(range(len(portfolios)), key=lambda m: (-scores[m], m))[:max(BUDGETS)]
                       for method, scores in data["scores"].items()}
            vorders["greedy_coverage"], _ = lazy_greedy(data["masks"], range(len(portfolios)), list(range(len(portfolios))), max(BUDGETS))
            for method in vorders:
                for selection, evaluation, target, sig in (
                    ("version_continuous", "version_continuous", data, version_sigs[label]),
                    ("package_projected", "version_continuous", data, version_sigs[label]),
                    ("version_continuous", "package_projected", endpoints[label], signatures[label])):
                    order = vorders[method] if selection == "version_continuous" else orders[label][method]
                    version_results.extend(evaluate_order(order, target, sig, method, label,
                                                          {"selection_representation": selection, "evaluation_representation": evaluation}))
        safe_full = propagate_endpoint_bits(component, members, edges, topo, safe_wf_repo_nodes)
        safe_data = endpoint_data(safe_full, portfolios)
        safe_data["observed_endpoint_total"] = population["link_consistent_workflow_positive_repositories"]
        safe_repo_sources = [0] * population["distinct_linked_repositories"]
        for p, sources in enumerate(source_masks):
            for r in bit_indices(safe_wf_repo_nodes[p]):
                safe_repo_sources[r] |= sources
        safe_sigs = source_signature_groups(safe_repo_sources)
        mapping_results = []
        for method, scores in safe_data["scores"].items():
            order = sorted(range(len(portfolios)), key=lambda m: (-scores[m], m))[:max(BUDGETS)]
            mapping_results.extend(evaluate_order(order, safe_data, safe_sigs, method, "link_consistent_workflow_repositories"))
        safe_order, _ = lazy_greedy(safe_data["masks"], range(len(portfolios)), list(range(len(portfolios))), max(BUDGETS))
        mapping_results.extend(evaluate_order(safe_order, safe_data, safe_sigs, "greedy_coverage", "link_consistent_workflow_repositories"))
        validation.update({"version_continuous_reach_subset_of_package_union_all_roots": True,
                           "all_main_fully_protected_endpoints_are_covered": all(row["fully_protected_endpoints"] <= row["covered_endpoints"] for row in deterministic + simulations),
                           "repository_sources_agree_with_identity_reach": all(
                               sources == union(1 << m for m, mask in enumerate(endpoints["workflow_repositories"]["masks"]) if mask & (1 << r))
                               for r, sources in enumerate(wf_repo_sources) if r % 97 == 0)})
        assert validation["repository_sources_agree_with_identity_reach"]
        write_csv(args.output / "deterministic_curves.csv", deterministic)
        write_csv(args.output / "random_trials.csv", simulations)
        random_summary = summarize_random(simulations)
        write_csv(args.output / "random_summary.csv", random_summary)
        write_csv(args.output / "random_analytic_expectations.csv", analytic_random)
        write_csv(args.output / "ablations.csv", ablations)
        write_csv(args.output / "identity_grouping_sensitivity.csv", email_results)
        write_csv(args.output / "concentration.csv", concentration)
        write_csv(args.output / "version_representation_curves.csv", version_results)
        write_csv(args.output / "repository_mapping_sensitivity.csv", mapping_results)
        result = {"population": population, "checks": validation,
                  "diagnostics": diagnostics, "deterministic_curves": deterministic,
                  "random_summary": random_summary, "ablations": ablations,
                  "random_analytic_expectations": analytic_random,
                  "identity_grouping_sensitivity": email_results,
                  "concentration": concentration,
                  "version_representation": version_metadata,
                  "version_representation_curves": version_results,
                  "repository_mapping_sensitivity": mapping_results}
        write_json(args.output / "results.json", result)
        c.close()
    manifest = {
        "study": "Exact structural identity-hardening and endpoint-coverage comparison",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "client_study_date": "2026-10-20", "repository_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "python_version": sys.version, "random_generator": "Python random.Random; independent seeds 0..trials-1; same sampled orders across endpoints",
        "random_trials": args.random_trials, "budget_grid": list(BUDGETS),
        "tie_policy": "Descending score then ascending username Unicode order; reverse-order aggregate sensitivity included; no names released",
        "graph": "All stored version edges collapsed to directed package adjacency; reverse reach includes seed portfolios; SCC condensation with exact integer bitsets",
        "source_database_mode": "Extracted in temporary directory, immutable read-only SQLite connection; source archive unmodified",
        "source_sha256": {str(args.archive.relative_to(ROOT)) if args.archive.is_relative_to(ROOT) else str(args.archive): sha256(args.archive),
                          "uncompressed_sqlite": database_hash,
                          str(Path(__file__).relative_to(ROOT)): sha256(__file__),
                          "scripts/collect_data.py": sha256(ROOT / "scripts/collect_data.py")},
        "estimands": {
            "scenario_exposure_reduction": "H(S)=sum_{m in S}|E_m|/sum_m|E_m|. Uniform mutually exclusive identity-loss scenarios, hardening a selected source prevents that source scenario; other scenarios unaffected. No empirical scenario probabilities.",
            "endpoint_coverage": "C(S)=|union_{m in S} E_m|, prospective structural reach of selected hardening/review scenarios. A covered endpoint can still be exposed through any unhardened source.",
            "full_protection": "P(S)=|{e: A_e is nonempty and A_e subset S}| with A_e={m:e in E_m}. Residual possible exposure is full reachable universe minus P. Structural all-source exclusion, not a security guarantee.",
            "workflow_presence": "Any observed package-version row with positive GitHub workflow flag; does not imply secret access, exploitability, code execution, or historical presence.",
            "repository_endpoint": "Case-folded owner/repo, trailing .git removed; union over positively flagged package-version mappings; distinct repositories deduplicate monorepos.",
            "uncertainty": "Random mean, SD and central 95% empirical simulation range describe random-baseline variability; deterministic snapshot results have no sampling confidence interval.",
            "email_hash_sensitivity": "Group identical stored email hashes as a hypothetical control unit; identity linkage not independently established; budget is groups and scenario denominator changes.",
            "candidate_exclusion": "Remove 1/5/10 largest portfolio identities only from selectable controls, retain all source scenarios and endpoint denominators; no inference of bot/person or trustworthiness."
        },
        "limitations": ["Convenience snapshot with no shared collection cutoff; not full npm population or a temporal causal design.",
                        "Package union can combine incompatible versions; collector did not preserve extraction-root provenance.",
                        "Registry maintainer membership does not establish active publishing permissions, token scopes, shared credential control, or attack probabilities.",
                        "Graph reach indicates possible structural dependency paths and does not establish exploit propagation or CI secret access.",
                        "Workflow absence/unknown and repository metadata gaps are observational missingness, not demonstrated safety.",
                        "Exact greedy coverage and exact maintainer union are established methods, not a new optimization algorithm.",
                        "No incident labels, prediction, model fitting, expected real-world incidents, or causal security effects are claimed."],
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "outputs_sha256": {p.name: sha256(p) for p in sorted(args.output.iterdir()) if p.is_file() and p.name != "manifest.json"}}
    write_json(args.output / "manifest.json", manifest)
    print(json.dumps({"status": "complete", "output": str(args.output), "elapsed_seconds": manifest["elapsed_seconds"],
                      "population": population, "checks": validation}, indent=2), flush=True)


if __name__ == "__main__":
    main()
