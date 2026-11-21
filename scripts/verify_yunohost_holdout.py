#!/usr/bin/env python3
"""Audit the YunoHost collection and recompute the paired evidence bounds."""
from collections import Counter
from datetime import datetime
import gzip
import json

from study_yunohost_holdout import RUN, PRIVATE, hashes, read, read_collection, sha


def time(value):
    return datetime.fromisoformat(value)


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

    print(json.dumps({"checks": "passed", "projects": len(ids), "receipts": receipt_counts,
                      "paired_comparisons": len(results["comparisons"])}, indent=2))


if __name__ == "__main__":
    verify()
