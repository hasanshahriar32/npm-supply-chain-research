#!/usr/bin/env python3
"""Independent semantic and randomized checks for the structural study.

Checks a hand-derived coverage/protection counterexample and compares SCC/bitset
methods with simple graph searches and an exhaustive small-budget oracle.
"""
from collections import deque
from itertools import combinations
import importlib.util
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("interventions", ROOT / "scripts/study_structural_interventions.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def reachable(adjacency, start):
    visited, queue = {start}, deque([start])
    while queue:
        for neighbor in adjacency[queue.popleft()]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return sum(1 << node for node in visited)


def naive_greedy(masks, budget):
    remaining = set(range(len(masks)))
    selected, covered = [], 0
    for _ in range(min(budget, len(masks))):
        best = min(remaining, key=lambda m: (-(masks[m] & ~covered).bit_count(), m))
        remaining.remove(best)
        selected.append(best)
        covered |= masks[best]
    return selected


def main():
    # a,b overlap heavily; c adds new targets. Coverage and source loss differ.
    masks = [0b001111, 0b000111, 0b110000]
    chosen, _ = study.lazy_greedy(masks, range(3), list(range(3)), 2)
    assert chosen == [0, 2]
    assert study.union(masks[m] for m in chosen).bit_count() == 6
    assert sum(masks[m].bit_count() for m in chosen) == 6
    reach_order = sorted(range(3), key=lambda m: (-masks[m].bit_count(), m))[:2]
    assert reach_order == [0, 1]
    assert sum(masks[m].bit_count() for m in reach_order) == 7
    assert study.union(masks[m] for m in reach_order).bit_count() == 4
    assert sum(masks[m].bit_count() for m in reach_order) == max(
        sum(masks[m].bit_count() for m in chosen) for chosen in combinations(range(3), 2))

    graph = [{1}, {2}, {1}, set()]
    portfolios = [{0}, {1}, {3}]
    package_maintainers = [{0}, {1}, set(), {2}]
    c, groups, dag, order = study.scc_condensation(graph)
    endpoints = study.propagate_endpoint_bits(c, groups, dag, order, [1 << p for p in range(4)])
    assert endpoints == [0b0111, 0b0110, 0b0110, 0b1000]
    sources = study.propagate_source_bits(c, groups, dag, order, package_maintainers)
    assert sources == [0b001, 0b011, 0b011, 0b100]
    signatures = study.source_signature_groups(sources)
    assert study.full_protection(signatures, 0b001, 1) == 1
    assert study.full_protection(signatures, 0b011, 2) == 3
    assert study.full_protection(signatures, 0b000, 0) == 0
    data = study.endpoint_data(endpoints, portfolios)
    assert data["masks"] == [0b0111, 0b0110, 0b1000]

    # A version switch can create a package-projection path that does not exist
    # between exact nodes: x@1 -> y@1; y@2 -> z@1 in influence orientation.
    version_graph = [{1}, set(), {3}, set()]
    assert reachable(version_graph, 0) == 0b0011
    projected_graph = [{1}, {2}, set()]
    assert reachable(projected_graph, 0) == 0b111

    rng = random.Random(20261020)
    graph_checks = 0
    for _ in range(60):
        n = rng.randint(2, 18)
        adjacency = [{j for j in range(n) if rng.random() < .12} for _ in range(n)]
        c, groups, dag, order = study.scc_condensation(adjacency)
        exact = study.propagate_endpoint_bits(c, groups, dag, order, [1 << p for p in range(n)])
        assert exact == [reachable(adjacency, p) for p in range(n)]
        graph_checks += n
        portfolios = [set(rng.sample(range(n), rng.randint(1, min(4, n)))) for _ in range(7)]
        pm = [{m for m, portfolio in enumerate(portfolios) if p in portfolio} for p in range(n)]
        sources = study.propagate_source_bits(c, groups, dag, order, pm)
        expected = [0] * n
        masks = [study.union(reachable(adjacency, p) for p in portfolio) for portfolio in portfolios]
        for m, mask in enumerate(masks):
            for p in range(n):
                if mask & (1 << p):
                    expected[p] |= 1 << m
        assert sources == expected
        selected, _ = study.lazy_greedy(masks, range(7), list(range(7)), 5)
        assert selected == naive_greedy(masks, 5)
        signatures = study.source_signature_groups(sources)
        for k in range(6):
            selection = sum(1 << m for m in selected[:k])
            exact_protected = sum(bool(s) and s & selection == s for s in expected)
            assert study.full_protection(signatures, selection, k) == exact_protected

    result = {"hand_derived_coverage_vs_hardening_counterexample": True,
              "cycle_seed_and_protection_checks": True, "version_continuity_counterexample": True,
              "random_graph_trials": 60, "independently_checked_graph_roots": graph_checks,
              "lazy_greedy_equals_naive_marginal_greedy": True,
              "source_duality_and_full_protection_equal_naive": True,
              "random_seed": 20261020}
    target = ROOT / "manuscript/results/structural_interventions/independent_validation.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
