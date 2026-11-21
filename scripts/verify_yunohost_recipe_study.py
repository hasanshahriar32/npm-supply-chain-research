#!/usr/bin/env python3
"""Check the packaging audit denominators, verified inputs, and paired diagnostic."""
from collections import Counter
import gzip
import json

from study_yunohost_packaging import INTAKE, read_evidence
from study_yunohost_deployment_candidates import AUDIT, SOURCE_INTAKE, source_evidence
from study_yunohost_recipe_importers import (
    PROTOCOL, QUEUE, RECEIPTS, RESULTS, TRACES, input_hashes, projects, read, sha,
)


def verify():
    audit = read(AUDIT)
    recipes = {row["sample_id"]: row for row in audit["cases"]}
    assert audit["intake_sha256"] == sha(INTAKE)
    receipts = Counter()
    for case, files, records in read_evidence():
        row = recipes[case["sample_id"]]
        assert all(row[k] == v for k, v in case.items())
        for marker in row["evidence"] + row["command_locations"]:
            name, n = marker["file"], marker["line"]
            assert 1 <= n <= len(files[name].splitlines())
            assert marker.get("sha256", records[name]["sha256"]) == records[name]["sha256"]
        receipts.update(r["http_status"] for r in records.values())
    assert receipts == {200: 151, 404: 97}
    assert Counter(row["group"] for row in recipes.values()) == {"no_root_lockfile": 16, "empty_pnpm_workspace_root": 15}
    assert sum(r["classification"] == "release_or_distribution_payload" for r in recipes.values()) == 12
    assert sum(bool(r["command_locations"]) for r in recipes.values()) == 6

    sources = list(source_evidence())
    assert len(sources) == 6
    assert sum(ref["commit"] != row["upstream_commit"] for row, ref, _, _ in sources) == 4
    assert len(read(SOURCE_INTAKE)["rows"]) == len(sources)
    eligible = list(projects())
    assert len(eligible) == 3 and all(verified for _, _, _, verified in eligible)
    assert sum(len(row["recipe_paths"]) for row, _, _, _ in eligible) == 4

    protocol, result = read(PROTOCOL), read(RESULTS)
    assert protocol["inputs"] == input_hashes() and result["protocol_sha256"] == sha(PROTOCOL)
    assert result["paths_sha256"] == sha(TRACES) and result["receipts_sha256"] == sha(RECEIPTS)
    assert read(RECEIPTS)["queue_sha256"] == sha(QUEUE)
    assert result["registry_requests"] == result["registry_observations"] == len(read(QUEUE)["requests"]) == 401
    traces = json.loads(gzip.decompress(TRACES.read_bytes()))
    assert sum(row["same_commit_as_root_study"] for row in traces) == 1
    assert result["denominator"] == len(traces) == 3
    expected = {row["sample_id"]: sum(len(t["witnesses"]) for t in row["traces"]) for row in traces}
    assert sum(expected.values()) == sum(r["joined_paths"] for r in result["importers"]) == 425
    for comparison in result["comparisons"].values():
        assert comparison["documented_cells"] == {"00": 0, "01": 0, "10": 0, "11": 3}
        assert comparison["resolved_pairs"] == 3
        assert comparison["turnover_bounds"] == comparison["net_bounds"] == [0, 0]
        assert [p["sample_id"] for p in comparison["projects"]] == list(expected)
        for pair in comparison["projects"]:
            assert pair["documented"] == [1, 1] and pair["feasible"] == [[1, 1]]
            assert pair["confirmed_paths"] == expected[pair["sample_id"]]

    print(json.dumps({"checks": "passed", "catalog_recipes": len(recipes), "observed_files": 151,
                      "source_references": len(sources), "verified_importers": 4, "matched_exact_versions": 401}, indent=2))


if __name__ == "__main__":
    verify()
