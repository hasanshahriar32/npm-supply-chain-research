#!/usr/bin/env python3
"""Replay observed declared Yarn paths from the one matched release and source archive."""
import argparse
import base64
from collections import Counter
from datetime import datetime
import gzip
import json
from pathlib import Path
import subprocess
import tempfile

from collect_yunohost_release_lock_pair import FILES, REPO, TAG, raw_url
from collect_yunohost_observations import url_for
from study_yunohost_holdout import INCIDENCE, ROOT, digest, frozen_portfolios, now, read, sha, write
from study_yunohost_release_delivery import RUN as RELEASE_RUN
from study_yunohost_yarn_classic import NATIVE, PARSER, witnesses

RUN = RELEASE_RUN.with_name("yunohost-release-lock")
SOURCE_QUEUE = RUN / "source_queue.json"
SOURCE = RUN / "private/source.json"
PROTOCOL = RUN / "protocol.json"
GRAPH = RUN / "declared_paths.json.gz"
QUEUE = RUN / "registry_queue.json"
REGISTRY = RUN / "private/registry.json"
RESULT = RUN / "results.json"


def input_files():
    paths = (SOURCE_QUEUE, SOURCE, INCIDENCE, NATIVE, PARSER, ROOT / __file__,
             ROOT / "scripts/collect_yarn_registry.py", ROOT / "scripts/study_yunohost_yarn_classic.py")
    return {str(p.relative_to(ROOT)): sha(p) for p in paths}


def verified_source():
    queue, source = read(SOURCE_QUEUE), read(SOURCE)
    assert source["queue_sha256"] == sha(SOURCE_QUEUE)
    assert queue["embedded_results_sha256"] == sha(RELEASE_RUN / "embedded_results.json")
    assert source["archive_sha256"] == queue["request"]["recipe_sha256"]
    assert datetime.fromisoformat(queue["frozen_utc"]) <= datetime.fromisoformat(source["observed_at_utc"])
    tag = source["tag_resolution"]
    ref = "refs/tags/" + TAG
    assert tag["status"] == "tag_resolved" and tag["commit"] == tag["refs"].get(ref + "^{}", tag["refs"][ref])
    assert set(source["archive"]) == set(source["source"]) == FILES
    blobs = {}
    for field in ("archive", "source"):
        blobs[field] = {}
        for name, entry in source[field].items():
            blob = base64.b64decode(entry["body"], validate=True)
            assert digest(blob) == entry["sha256"]
            if field == "source":
                assert entry["http_status"] == 200 and entry["url"] == raw_url(REPO, tag["commit"], name)
            blobs[field][name] = blob
    return source, blobs


def trace(data, label):
    with tempfile.TemporaryDirectory(prefix="release-lock-") as directory:
        folder = Path(directory)
        for path, content in data.items():
            (folder / path).write_bytes(content)
        process = subprocess.run(["node", str(PARSER), str(folder / "package.json"), str(folder / "yarn.lock"), str(NATIVE)],
                                 check=True, capture_output=True, text=True, timeout=60)
    return {"sample_id": label, **json.loads(process.stdout)}


def paths():
    if PROTOCOL.exists():
        raise ValueError("Release-lock comparison already frozen")
    source, files = verified_source()
    write(PROTOCOL, {"frozen_utc": now(), "inputs": input_files(),
                     "scope": "Positive evidence of regular declared Yarn Classic dependency paths in the exact release "
                              "archive and its tag-resolved source. A shared registry snapshot for both. "
                              "No installed-tree or asset-level inclusion claim. No changes to prior denominators."})
    graphs = {k: trace(v, k) for k, v in files.items()}
    GRAPH.write_bytes(gzip.compress(json.dumps(graphs, separators=(",", ":")).encode(), mtime=0))
    keys = {(node["package"], node["version"]) for graph in graphs.values() for node in graph.get("nodes", {}).values()}
    requests = [{"package": p, "version": v} for p, v in sorted(keys)]
    for request in requests:
        url_for("registry", request)
    write(QUEUE, {"stage": "yarn_classic_registry", "protocol_sha256": sha(PROTOCOL),
                  "graph_sha256": sha(GRAPH), "requests": requests})
    print(source["tag_resolution"]["commit"], {k: v["status"] for k, v in graphs.items()}, len(requests))


def score():
    source, inputs = verified_source()
    protocol, queue, captured = read(PROTOCOL), read(QUEUE), read(REGISTRY)
    assert protocol["inputs"] == input_files() and queue["protocol_sha256"] == sha(PROTOCOL)
    assert queue["graph_sha256"] == sha(GRAPH) and captured["queue_sha256"] == sha(QUEUE)
    begin, end = map(datetime.fromisoformat, (protocol["frozen_utc"], captured["finished_utc"]))
    index = {}
    for request, row in zip(queue["requests"], captured["observations"], strict=True):
        assert all(row[k] == v for k, v in request.items()) and row["url"] == url_for("registry", request)
        assert begin <= datetime.fromisoformat(row["observed_at_utc"]) <= end
        if row["status"] == "observed":
            index[request["package"], request["version"]] = row
    graphs = json.loads(gzip.decompress(GRAPH.read_bytes()))
    members, slots = frozen_portfolios()
    portfolios = {key: {members[i] for i in positions} for key, positions in slots.items()}
    comparisons = {}
    for label, graph in graphs.items():
        (_, accounts, _, keys), issues = witnesses(graph, index)
        comparisons[label] = {"status": graph["status"], "descriptor_candidates": len(graph.get("nodes", {})),
                              "joined_package_versions": keys, "join_issues": dict(issues),
                              "documented_hits": {key: bool(accounts & ids) for key, ids in portfolios.items()}}
    lock_matches = {k: inputs["archive"][k] == inputs["source"][k] for k in FILES}
    if all(lock_matches.values()):
        assert comparisons["archive"] == comparisons["source"]
    output = {"source_commit": source["tag_resolution"]["commit"], "archive_sha256": source["archive_sha256"],
              "files_match": dict(sorted(lock_matches.items())), "public_asset_js_files": source["public_asset_js_files"],
              "registry_requests": len(queue["requests"]), "registry_success": len(index),
              "usable_maintainer_lists": sum(row["accounts"] is not None for row in index.values()),
              "graph_sha256": sha(GRAPH), "registry_receipt_sha256": sha(REGISTRY),
              "declared_dependency_comparison": comparisons}
    write(RESULT, output)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    stages = {"paths": paths, "score": score}
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("stage", choices=tuple(stages))
    stages[cli.parse_args().stage]()
