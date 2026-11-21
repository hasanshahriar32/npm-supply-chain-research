#!/usr/bin/env python3
"""Check published aggregates and the acquisition chronology for a scored run."""
import argparse
from collections import Counter
from datetime import datetime
import json
from pathlib import Path

from consumer_holdout import path_artifact, registry_url
from evaluate_consumer_pilot import load, sha


def verify(run):
    protocol = load(run / "protocol.json")
    observations = load(run / "observations.json")
    artifact = path_artifact(run)
    manifest = load(run / "registry_manifest.json")
    memberships_path = run / "private" / "memberships.json"
    reference = load(memberships_path)
    results = load(run / "results.json")
    assert results["protocol_sha256"] == sha(run / "protocol.json")
    assert results["registry_manifest_sha256"] == sha(run / "registry_manifest.json")
    assert manifest["paths_sha256"] == sha(run / "paths.json")
    assert manifest["memberships_sha256"] == sha(memberships_path)
    ids = [row["sample_id"] for row in protocol["projects"]]
    assert len(ids) == len(set(ids)) == results["denominator"]
    assert ids == [row["sample_id"] for row in observations]
    assert ids == [row["sample_id"] for row in artifact["projects"]]
    assert Counter(p["status"] for p in artifact["projects"]) == results["project_status"]
    requests = [registry_url(*key) for key in artifact["version_keys"]]
    assert requests == [r["url"] for r in reference]
    assert len(requests) == manifest["requests"] == results["public_versions"]
    assert sum(record["membership_status"] == "observed" for record in reference) == results["versions_with_observed_membership"]

    last_source = max(datetime.fromisoformat(t) for row in observations
                      for t in [row["pin_observed_at_utc"], *(v["observed_at_utc"] for v in row["files"].values())])
    registry_times = [datetime.fromisoformat(row["observed_at_utc"]) for row in reference]
    assert not registry_times or last_source <= min(registry_times)
    assert not registry_times or max(registry_times) <= datetime.fromisoformat(manifest["sealed_at_utc"])

    n = len(ids)
    for comparison in results["comparisons"].values():
        rows = comparison["projects"]
        assert ids == [p["sample_id"] for p in rows]
        cells = Counter(f"{int(row['documented'][0])}{int(row['documented'][1])}" for row in rows)
        assert all(comparison["documented_cells"][c] == cells[c] for c in ("00","01","10","11"))
        assert comparison["documented_turnover"] == (cells["10"] + cells["01"]) / n
        assert comparison["documented_net"] == (cells["01"] - cells["10"]) / n
        possible = [{v - n for n, v in row["feasible"]} for row in rows]
        for metric, key in ((lambda x: x, "net"), (abs, "turnover")):
            lower = sum(min(map(metric, p)) for p in possible) / n
            upper = sum(max(map(metric, p)) for p in possible) / n
            assert comparison[f"complete_reference_{key}_bounds"] == [lower, upper]
        assert comparison["resolved_pairs"] == sum(len(row["feasible"]) == 1 for row in rows)

    control = results["comparisons"]["identical_control"]
    assert control["complete_reference_turnover_bounds"] == control["complete_reference_net_bounds"] == [0, 0]
    print(json.dumps({"projects": n, "reference_records": len(reference), "paired_comparisons": len(results["comparisons"]),
                      "last_source_utc": last_source.isoformat(),
                      "registry_first_utc": min(registry_times).isoformat() if registry_times else None,
                      "registry_last_utc": max(registry_times).isoformat() if registry_times else None,
                      "checks": "passed"}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    verify(parser.parse_args().run)
