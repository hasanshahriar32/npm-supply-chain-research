#!/usr/bin/env python3
"""Audit the YunoHost collection and recompute the paired evidence bounds."""
from collections import Counter
from datetime import datetime
from functools import lru_cache
import gzip
import json

from compare_yunohost_npm_extractors import previous_reader
from study_yunohost_holdout import (
    ROOT, RUN, PRIVATE, frozen_portfolios, hashes, inputs, read, read_collection, sha, sha512_values,
)


def time(value):
    return datetime.fromisoformat(value)


def verify_manuscript_table(comparisons):
    versions = [comparisons[f"version_{index}"] for index in (1, 2, 3)]
    table = (ROOT / "manuscript_q1/tables/yunohost_consumer_holdout_table.tex").read_text()
    measures = {
        "Documented under both": [r["documented_cells"]["11"] for r in versions],
        "Documented name only": [r["documented_cells"]["10"] for r in versions],
        "Documented version only": [r["documented_cells"]["01"] for r in versions],
        "Documented under neither": [r["documented_cells"]["00"] for r in versions],
        "Fully resolved pairs": [r["resolved_pairs"] for r in versions],
        "Fully resolved differences": [
            sum(len(p["feasible"]) == 1 and sum(p["documented"]) == 1 for p in r["projects"])
            for r in versions
        ],
    }
    for label, key in (("Turnover bounds (\\%)", "turnover_bounds"), ("Net change bounds (pp)", "net_bounds")):
        measures[label] = [f"$[{100 * lo:.1f},{100 * hi:.1f}]$" for lo, hi in (r[key] for r in versions)]
    for label, values in measures.items():
        assert " & ".join([label, *map(str, values)]) + r"\\" in table, label


def verify_confirmed_positive_paths(comparisons, traces, registry_receipts):
    """Post-outcome cross-check of positive locations in fully resolved discordant pairs."""
    maintainers, slots = frozen_portfolios()
    portfolios = {key: {maintainers[i] for i in ids} for key, ids in slots.items()}
    projects = {row["frame_id"]: row for row, _ in inputs()}
    registry = {(r["package"], r["version"]): r for r in registry_receipts if r["status"] == "observed"}
    by_id = {trace["sample_id"]: trace for trace in traces}

    @lru_cache(maxsize=None)
    def earlier_locations(sample_id):
        return previous_reader(projects[sample_id])[1]

    counts = {}
    for variant in ("version_1", "version_2", "version_3"):
        checked = 0
        for row in comparisons[variant]["projects"]:
            if len(row["feasible"]) != 1 or sum(row["documented"]) != 1:
                continue
            sample_id = row["sample_id"]
            selected = portfolios["name" if row["documented"][0] else variant]
            corroborated = earlier_locations(sample_id)
            positive = set()
            for w in by_id[sample_id]["witnesses"]:
                key = w["package"], w["version"]
                record = registry.get(key)
                if not record or selected.isdisjoint(record["accounts"]):
                    continue
                integrity = sha512_values(w.get("registry_integrity_candidate")) & sha512_values(record.get("integrity"))
                if w["public_npm_tarball"] or integrity:
                    positive.add((w["location"], *key))
            assert positive & corroborated, (variant, sample_id)
            checked += 1
        counts[variant] = checked
    return counts


def verify():
    protocol = read(RUN / "protocol.json")
    results = read(RUN / "results.json")
    paths = RUN / "paths.json.gz"
    traces = json.loads(gzip.decompress(paths.read_bytes()))
    ids = [trace["sample_id"] for trace in traces]
    assert protocol["inputs"] == hashes()
    assert len(ids) == len(set(ids)) == results["denominator"] == 215
    assert results["paths_sha256"] == sha(paths) == read(RUN / "registry_queue.json")["paths_sha256"]
    assert results["registry_ledger_sha256"] == sha(PRIVATE / "registry.json")
    assert results["path_status"] == dict(Counter(t["status"] for t in traces))
    assert all(not t["complete"] for t in traces if not t["status"].startswith("npm_"))

    earliest = time(protocol["frozen_utc"])
    receipt_counts = {}
    for stage in ("workspaces", "registry"):
        rows = read_collection(stage)
        finished = time(read(PRIVATE / f"{stage}.json")["finished_utc"])
        assert all(earliest <= time(row["observed_at_utc"]) <= finished for row in rows)
        earliest = finished
        receipt_counts[stage] = len(rows)
    assert results["request_states"] == dict(Counter(row["status"] for row in rows))

    for comparison_id, result in results["comparisons"].items():
        projects = result["projects"]
        assert ids == [row["sample_id"] for row in projects]
        cells = Counter()
        deltas = []
        for row in projects:
            name, version = row["documented"]
            cells[f"{name}{version}"] += 1
            states = row["feasible"]
            assert len(states) == len(set(map(tuple, states)))
            assert row["documented"] in states
            assert all(n in (0, 1) and v in (0, 1) and n >= name and v >= version for n, v in states)
            if comparison_id == "identical_control":
                assert all(n == v for n, v in states)
            deltas.append({v - n for n, v in states})
        assert result["documented_cells"] == {cell: cells[cell] for cell in ("00", "01", "10", "11")}
        assert result["resolved_pairs"] == sum(len(row["feasible"]) == 1 for row in projects)
        assert result["net_bounds"] == [
            sum(min(delta) for delta in deltas) / len(ids),
            sum(max(delta) for delta in deltas) / len(ids),
        ]
        assert result["turnover_bounds"] == [
            sum(0 not in delta for delta in deltas) / len(ids),
            sum(delta != {0} for delta in deltas) / len(ids),
        ]

    verify_manuscript_table(results["comparisons"])
    earlier_positive_counts = verify_confirmed_positive_paths(results["comparisons"], traces, rows)
    print(json.dumps({"checks": "passed", "projects": len(ids), "receipts": receipt_counts,
                      "paired_comparisons": len(results["comparisons"]),
                      "discordant_positive_paths_corroborated_by_earlier_reader": earlier_positive_counts}, indent=2))


if __name__ == "__main__":
    verify()
