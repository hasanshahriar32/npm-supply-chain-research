#!/usr/bin/env python3
"""Check sample provenance, denominators and reported importer changes."""
from collections import Counter

from check_yunohost_single_edge import OUTPUT, RECEIPTS as CLOSURE_RECEIPTS, read_paths
from study_yunohost_importer_frame import QUEUE, RECEIPTS, RUN, evidence, read, sha
from study_yunohost_same_commit_spans import PATHS, REGISTRY, RESULT, RETRY, SOURCES, registry_index, source_rows


def verify():
    sample, labels = read(QUEUE), read(RUN / "recipes.json")
    assert sample["sample"] == {"workspace_marker": 39, "other": 60}
    assert sample["population"] == {"workspace_marker": 39, "other": 430}
    assert labels["sample_sha256"] == sha(QUEUE) and labels["receipts_sha256"] == sha(RECEIPTS)
    seen = Counter()
    for (expected, files, receipts), label in zip(evidence(), labels["projects"], strict=True):
        assert all(label[k] == v for k, v in expected.items())
        seen.update(r.get("http_status") for r in receipts.values())
        for marker in label.get("markers", []) + label["js_command_locations"]:
            p, n = marker["file"], marker["line"]
            assert 1 <= n <= len(files[p].splitlines())
            if "sha256" in marker:
                assert marker["sha256"] == receipts[p]["sha256"]
    assert seen == {200: 394, 404: 200}
    named = [row for row in labels["projects"] if row["status"] == "named_recipe_path"]
    assert Counter(r["stratum"] for r in named) == {"workspace_marker": 6, "other": 1}

    rows = list(source_rows())
    assert [r["sample_id"] for r, _, _ in rows] == [r["sample_id"] for r in named]
    assert sum(all(item.get("body_base64") for item in record["files"].values())
               for _, record, _ in rows if record["status"] in ("verified_archive", "patches_present")) == 4
    traces = read_paths()
    assert sum(r["same_as_screened_head"] is False for r in traces) == 6
    queue, index = registry_index()
    base, closure = read(RESULT), read(OUTPUT)
    assert base["recipes_sampled"] == len(sample["projects"]) == 99 and base["named_candidates"] == len(named) == 7
    assert base["paths_sha256"] == sha(PATHS) and base["registry_receipts_sha256"] == sha(REGISTRY)
    assert base["source_receipts_sha256"] == sha(SOURCES) and base["source_retry_sha256"] == sha(RETRY)
    assert base["registry_requests"] == len(queue["requests"]) == 772
    assert base["registry_observed"] == len(index) == 771
    assert base["root_and_named_readable"] == 2
    contexts = {r["sample_id"]: (r["root_joined_paths"], r["named_joined_paths"]) for r in base["contexts"]}
    assert contexts["D002"] == (83, 0) and contexts["D022"] == (1, 725)
    assert closure["status"] == "post_hoc" and closure["earlier_results_sha256"] == sha(RESULT)
    assert closure["receipts_sha256"] == sha(CLOSURE_RECEIPTS)
    assert closure["roots_checked"] == closure["verified_root_closure"] == ["D022"]
    for key, initial in base["importer_contrasts"].items():
        after = closure["contrasts"][key]
        assert initial["resolved_pairs"] == 0 and initial["turnover_counts"] == [0, 7]
        assert after["possible_by_project"]["D022"] == [[0, 1]]
        assert after["resolved_pairs"] == after["confirmed_gains"] == 1 and after["confirmed_losses"] == 0
        assert after["turnover_counts"] == [1, 7]
        assert all(states == initial["possible_by_project"][sid]
                   for sid, states in after["possible_by_project"].items() if sid != "D022")

    print("Verified 99 recipes, 7 named candidates, 2 matched extractions and 1 post hoc coverage change")


if __name__ == "__main__":
    verify()
