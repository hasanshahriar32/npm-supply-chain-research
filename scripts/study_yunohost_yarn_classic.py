#!/usr/bin/env python3
"""Measure the incremental positive evidence from classic Yarn lockfiles."""
import argparse
from collections import Counter, deque
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import gzip
import json
import subprocess

from collect_yunohost_observations import url_for
import study_yunohost_holdout as baseline
from study_yunohost_holdout import ROOT, CAPTURE, now, read, sha, write, sha512_values

RUN = baseline.RUN.with_name("yunohost-yarn-classic")
PRIVATE = RUN / "private"
NATIVE = PRIVATE / "yarn_lockfile_native.cjs"
PARSER = ROOT / "scripts/consumer_yarn_classic.cjs"
GRAPH = RUN / "paths.json.gz"
QUEUE = RUN / "registry_queue.json"
LEDGER = PRIVATE / "registry.json"


def dependencies():
    paths = [PARSER, NATIVE, RUN / "parser_origin.json", ROOT / "scripts/collect_yarn_registry.py",
             ROOT / "scripts/collect_yunohost_observations.py", ROOT / "scripts/study_yunohost_holdout.py",
             baseline.RUN / "protocol.json", baseline.RUN / "results.json",
             baseline.RUN / "paths.json.gz", baseline.PRIVATE / "registry.json", ROOT / __file__]
    return {str(p.relative_to(ROOT)): sha(p) for p in paths}


def verify_protocol():
    protocol = read(RUN / "protocol.json")
    if protocol["inputs"] != dependencies():
        raise ValueError("Frozen evidence or code changed")
    return protocol


def freeze():
    output = RUN / "protocol.json"
    if output.exists():
        raise ValueError("The follow-up has already been frozen")
    tools = {
        "node": subprocess.check_output(["node", "--version"], text=True).strip(),
        "yarn_lockfile_parser": "1.1.0",
    }
    write(output, {
        "scope": "Post-outcome evidence extension on all 35 Yarn-file candidates in the same 215-project frame. "
                 "Accept only Yarn Classic roots without workspaces, exact nominal SemVer descriptor paths agreed on by both readers, "
                 "regular edges, canonical registry identifiers and platform-unconditional targets. "
                 "Skip every edge affected by a named selective resolution. Use exact registry metadata to corroborate transitive declarations. "
                 "Yarn results can add positive witnesses only. Missing evidence leaves the opposing status unresolved.",
        "artifact_rule": "Canonical npm path or canonical Yarn registry mirror path with exact SHA-512 match. "
                         "Reject a contradictory SHA-512 for either host when both sides provide SHA-512.",
        "temporality": "Freeze before new account acquisition. Original npm and pnpm observations remain at their original date. "
                       "Interpret the combined bounds as a sensitivity to adding these Yarn observations.",
        "frozen_utc": now(), "inputs": dependencies(), "tools": tools,
    })


def trace(row):
    source = CAPTURE / "projects" / row["frame_id"]
    command = ["node", str(PARSER), str(source / "package.json"), str(source / "yarn.lock"), str(NATIVE)]
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, timeout=60)
        graph = json.loads(result.stdout)
    except (subprocess.SubprocessError, json.JSONDecodeError):
        graph = {"status": "reader_error"}
    return {"sample_id": row["frame_id"], "commit_sha": row["commit_sha"], **graph}


def paths():
    verify_protocol()
    rows = [row for row, state in baseline.inputs() if state["status"] == "yarn_file_available"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        graphs = list(pool.map(trace, rows))
    GRAPH.write_bytes(gzip.compress(json.dumps(graphs, separators=(",", ":")).encode(), mtime=0))
    keys = {(node["package"], node["version"]) for graph in graphs for node in graph.get("nodes", {}).values()}
    requests = [{"package": p, "version": v} for p, v in sorted(keys)]
    for request in requests:
        url_for("registry", request)
    write(QUEUE, {"protocol_sha256": sha(RUN / "protocol.json"), "paths_sha256": sha(GRAPH),
                  "stage": "yarn_classic_registry", "requests": requests})
    print(dict(Counter(graph["status"] for graph in graphs)), len(requests), "exact versions queued")


def read_ledger(protocol):
    queue, receipt = read(QUEUE), read(LEDGER)
    assert queue["protocol_sha256"] == sha(RUN / "protocol.json") and queue["paths_sha256"] == sha(GRAPH)
    assert receipt["queue_sha256"] == sha(QUEUE)
    earliest = datetime.fromisoformat(protocol["frozen_utc"])
    latest = datetime.fromisoformat(receipt["finished_utc"])
    for request, record in zip(queue["requests"], receipt["observations"], strict=True):
        assert (record["url"] == url_for("registry", request)
                and all(record[k] == v for k, v in request.items())
                and earliest <= datetime.fromisoformat(record["observed_at_utc"]) <= latest)
    return receipt["observations"]


def same_identity(node, record):
    locked = sha512_values(node["integrity"])
    registry = sha512_values(record["integrity"])
    if locked and registry:
        return bool(locked & registry)
    return node["origin"] == "npm"


def witnesses(graph, index):
    seen, accounts, keys = set(), set(), set()
    issues = Counter()
    pending = deque(graph.get("roots", []))
    nodes = graph.get("nodes", {})
    while pending:
        package, spec = pending.popleft()
        descriptor = f"{package}@{spec}"
        node = nodes.get(descriptor)
        if descriptor in seen or node is None:
            continue
        seen.add(descriptor)
        key = node["package"], node["version"]
        record = index.get(key)
        if record is None or not same_identity(node, record) or record["conditional"]:
            issues["artifact_or_condition_unresolved"] += 1
            continue
        keys.add(key)
        if record["accounts"] is not None:
            accounts.update(record["accounts"])
        deps, optional = record["dependencies"], record["optional_dependencies"]
        if deps is None or optional is None or record["bundles_dependencies"]:
            issues["dependency_metadata_unresolved"] += 1
            continue
        for name, spec in node["children"]:
            if deps.get(name) == spec and name not in optional:
                pending.append((name, spec))
            else:
                issues["dependency_declaration_disagrees"] += 1
    return (graph["sample_id"], accounts, False, len(keys)), issues


def score():
    protocol = verify_protocol()
    observations = read_ledger(protocol)
    index = {(row["package"], row["version"]): row for row in observations if row["status"] == "observed"}
    graphs = json.loads(gzip.decompress(GRAPH.read_bytes()))
    frame = baseline.inputs()
    assert [(r["frame_id"], r["commit_sha"]) for r, state in frame if state["status"] == "yarn_file_available"] == [
        (g["sample_id"], g["commit_sha"]) for g in graphs
    ]
    yarn = {}
    issues = Counter()
    for graph in graphs:
        row, reasons = witnesses(graph, index)
        yarn[row[0]] = row
        issues.update(reasons)
    earlier = read(baseline.RUN / "results.json")
    records = baseline.read_collection("registry")
    old_index = {(row["package"], row["version"]): row for row in records if row["status"] == "observed"}
    old_graphs = json.loads(gzip.decompress((baseline.RUN / "paths.json.gz").read_bytes()))
    old_rows, _ = baseline.frame_paths(old_graphs, old_index)
    combined = [yarn.get(row[0], row) for row in old_rows]
    members, slots = baseline.frozen_portfolios()
    portfolios = {key: {members[i] for i in indices} for key, indices in slots.items()}
    groups = {key: ("name", key) for key in ("version_1", "version_2", "version_3")}
    groups["identical_control"] = "control", "control"
    comparisons = {}
    for key, (name, version) in groups.items():
        assert baseline.paired(old_rows, portfolios[name], portfolios[version]) == earlier["comparisons"][key]
        result = baseline.paired(combined, portfolios[name], portfolios[version])
        for old, new in zip(earlier["comparisons"][key]["projects"], result["projects"], strict=True):
            assert old["sample_id"] == new["sample_id"]
            assert set(map(tuple, new["feasible"])) <= set(map(tuple, old["feasible"]))
            if old["sample_id"] not in yarn:
                assert old == new
        comparisons[key] = result
    output = {"denominator": len(combined), "yarn_candidates": len(graphs),
              "path_status": dict(Counter(g["status"] for g in graphs)), "registry_requests": len(observations),
              "registry_states": dict(Counter(r["status"] for r in observations)),
              "usable_maintainer_lists": sum(r["status"] == "observed" and r["accounts"] is not None for r in observations),
              "yarn_projects_with_verified_versions": sum(row[3] > 0 for row in yarn.values()),
              "yarn_verified_versions_summed_by_project": sum(row[3] for row in yarn.values()),
              "registry_path_issues": dict(issues), "paths_sha256": sha(GRAPH),
              "registry_ledger_sha256": sha(LEDGER), "prior_results_sha256": sha(baseline.RUN / "results.json"),
              "comparisons": comparisons}
    write(RUN / "results.json", output)
    print({k: v for k, v in output.items() if k != "comparisons"})
    print({k: v for k, v in comparisons["version_1"].items() if k != "projects"})


if __name__ == "__main__":
    stages = {"freeze": freeze, "paths": paths, "score": score}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=tuple(stages))
    stages[parser.parse_args().stage]()
