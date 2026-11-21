#!/usr/bin/env python3
"""Check empty pnpm roots in the unresolved post-Yarn comparison."""
import argparse
from collections import Counter
import json
import subprocess

import replay_yunohost_consumer_results as replay
from study_pnpm_parser_development import YAML_READER

INITIAL = replay.initial
FOLLOWUP = replay.followup
RUN = INITIAL.RUN.with_name("yunohost-empty-pnpm-roots")
PROTOCOL = RUN / "protocol.json"
RESULTS = RUN / "results.json"
SOURCE = FOLLOWUP.RUN / "results.json"
TRACES = INITIAL.RUN / "paths.json.gz"
SCRIPT = INITIAL.ROOT / "scripts/study_yunohost_empty_pnpm_roots.py"


def candidates():
    traces = replay.read_graphs(TRACES)
    projects = INITIAL.read(SOURCE)["comparisons"]["version_1"]["projects"]
    selected = []
    for trace, project in zip(traces, projects, strict=True):
        assert trace["sample_id"] == project["sample_id"]
        if len(project["feasible"]) > 1 and trace["status"] == "pnpm_ok" and not trace["witnesses"]:
            selected.append(trace["sample_id"])
    return selected


def inputs():
    files = (SOURCE, TRACES, SCRIPT)
    return {str(path.relative_to(INITIAL.ROOT)): INITIAL.sha(path) for path in files}


def freeze():
    RUN.mkdir(exist_ok=True)
    if PROTOCOL.exists():
        raise ValueError("Diagnostic protocol already frozen")
    INITIAL.write(PROTOCOL, {
        "frozen_utc": INITIAL.now(),
        "inputs": inputs(),
        "projects": candidates(),
        "design": "Post hoc diagnostic. Inspect every unresolved primary pair with pnpm_ok "
                  "and zero witnesses. Require no regular dependency declarations in both "
                  "the pinned root manifest and the pnpm v9 root importer. Preserve the "
                  "original production root scope and exclude optional and dev dependencies. "
                  "Recompute information bounds with strict empty roots as common negatives.",
    })
    print(len(candidates()), "empty-witness candidates")


def unique_object(pairs):
    mapped = dict(pairs)
    if len(mapped) != len(pairs):
        raise ValueError("Duplicate JSON field")
    return mapped


def declaration_count(source, key):
    values = source.get(key, {})
    if not isinstance(values, dict):
        raise ValueError(f"Invalid declaration group {key}")
    return len(values)


def inspect(row):
    source = INITIAL.CAPTURE / "projects" / row["frame_id"]
    manifest = json.loads((source / "package.json").read_bytes(), object_pairs_hook=unique_object)
    exported = subprocess.check_output(
        ["ruby", "-rpsych", "-rjson", "-e", YAML_READER],
        input=(source / "pnpm-lock.yaml").read_text(), text=True, timeout=45,
    )
    lock = json.loads(exported)["project"]
    assert str(lock["lockfileVersion"]) == "9.0"
    importer = lock["importers"]["."]
    groups = ("dependencies", "optionalDependencies", "devDependencies")
    return {
        "sample_id": row["frame_id"], "repository": row["repository"], "commit_sha": row["commit_sha"],
        "file_sha256": {f: row["files"][f]["sha256"] for f in ("package.json", "pnpm-lock.yaml")},
        "manifest": {key: declaration_count(manifest, key) for key in groups},
        "root_importer": {key: declaration_count(importer, key) for key in groups},
    }


def check_bounds(verified):
    source = INITIAL.read(SOURCE)
    followup = {}
    for key, comparison in source["comparisons"].items():
        states = []
        for row in comparison["projects"]:
            feasible = row["feasible"]
            if row["sample_id"] in verified:
                assert row["documented"] == [0, 0] and [0, 0] in feasible and len(feasible) > 1
                feasible = [[0, 0]]
            states.append({v - n for n, v in feasible})
        n = len(states)
        assert n == source["denominator"]
        record = {"resolved_pairs": sum(len(delta) == 1 for delta in states),
                  "turnover_bounds": [sum(0 not in d for d in states) / n,
                                      sum(d != {0} for d in states) / n],
                  "net_bounds": [sum(min(d) for d in states) / n, sum(max(d) for d in states) / n]}
        assert record["resolved_pairs"] == comparison["resolved_pairs"] + len(verified)
        for label in ("turnover_bounds", "net_bounds"):
            prior, new = comparison[label], record[label]
            assert prior[0] <= new[0] <= new[1] <= prior[1]
        followup[key] = record
    return followup


def score():
    protocol = INITIAL.read(PROTOCOL)
    assert protocol["inputs"] == inputs() and protocol["projects"] == candidates()
    frame = {row["frame_id"]: row for row, _ in INITIAL.inputs()}
    observations = [inspect(frame[sid]) for sid in protocol["projects"]]
    supported = {row["sample_id"] for row in observations
                 if row["manifest"]["dependencies"] == row["root_importer"]["dependencies"] == 0}
    comparisons = check_bounds(supported)
    INITIAL.write(RESULTS, {
        "protocol_sha256": INITIAL.sha(PROTOCOL),
        "verified_empty_roots": sorted(supported),
        "dependency_declaration_patterns": dict(Counter(
            f"optional={r['manifest']['optionalDependencies'] > 0},dev={r['manifest']['devDependencies'] > 0}"
            for r in observations if r["sample_id"] in supported
        )),
        "comparisons": comparisons, "observations": observations,
    })
    print(len(supported), "confirmed empty roots", comparisons["version_1"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    stages = {"freeze": freeze, "score": score}
    parser.add_argument("stage", choices=stages)
    stages[parser.parse_args().stage]()
