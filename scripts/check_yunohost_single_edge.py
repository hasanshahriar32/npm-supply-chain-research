#!/usr/bin/env python3
"""Post hoc closure check for roots with exactly one corroborated pnpm dependency."""
import argparse
from datetime import datetime
import gzip
import json
import subprocess

from collect_yunohost_observations import url_for
from study_pnpm_parser_development import YAML_READER
from study_yunohost_holdout import frozen_portfolios, sha512_values
from study_yunohost_same_commit_spans import (
    PATHS, PRIVATE, RESULT, RUN, context, importer_contrast, now, read, registry_index, sha, source_rows, write,
)

QUEUE = RUN / "single_edge_queue.json"
RECEIPTS = PRIVATE / "single_edge_registry.json"
OUTPUT = RUN / "single_edge_sensitivity.json"


def read_paths():
    return json.loads(gzip.decompress(PATHS.read_bytes()))


def candidate_roots(rows):
    candidates = {}
    for row in rows:
        [root] = row["root"]
        if root.get("manager") == "pnpm" and root["status"] == "ok" and len(root["witnesses"]) == 1:
            [path] = root["witnesses"]
            if len(path["path"]) == 1:
                candidates[row["sample_id"]] = path
    return candidates


def freeze():
    if QUEUE.exists():
        raise ValueError("Single-edge check already frozen")
    candidates = candidate_roots(read_paths())
    keys = sorted({(w["package"], w["version"]) for w in candidates.values()})
    write(QUEUE, {"stage": "yarn_classic_registry", "frozen_utc": now(), "paths_sha256": sha(PATHS),
                  "earlier_results_sha256": sha(RESULT),
                  "purpose": "Post hoc metadata-only closure check for all corroborated single-edge pnpm roots. "
                             "Require the lock snapshot and fresh metadata to agree on zero mandatory children, "
                             "both artifact digests to agree and the earlier account observation to reproduce.",
                  "requests": [{"package": p, "version": v} for p, v in keys]})
    print(len(keys), "exact version records for the closure check")


def verify_root(files, path, old, new):
    if (new.get("status") != "observed" or new.get("accounts") != old["accounts"] or new.get("conditional")
            or new.get("bundles_dependencies") or new["dependencies"] is None or new["optional_dependencies"] is None):
        return False
    integrity = sha512_values(path.get("registry_integrity_candidate"))
    if not integrity & sha512_values(old.get("integrity")) & sha512_values(new.get("integrity")):
        return False
    manifest = json.loads(files["package.json"])
    package, version = path["package"], path["version"]
    if set(manifest.get("dependencies", {})) - set(manifest.get("optionalDependencies", {})) != {package}:
        return False
    parsed = subprocess.run(["ruby", "-rpsych", "-rjson", "-e", YAML_READER], input=files["pnpm-lock.yaml"],
                            check=True, capture_output=True, timeout=45)
    lock = json.loads(parsed.stdout)["project"]
    selected = lock["importers"]["."]["dependencies"][package]
    if selected["specifier"] != manifest["dependencies"][package] or selected["version"] != version:
        return False
    snapshot = lock["snapshots"][path["path"][0]["snapshot"]]
    return (not (set(snapshot.get("dependencies", {})) - set(snapshot.get("optionalDependencies", {})))
            and not (set(new["dependencies"]) - set(new["optional_dependencies"])))


def score():
    queue, records = read(QUEUE), read(RECEIPTS)
    assert queue["paths_sha256"] == sha(PATHS) and queue["earlier_results_sha256"] == sha(RESULT)
    assert records["queue_sha256"] == sha(QUEUE)
    lower, upper = map(datetime.fromisoformat, (queue["frozen_utc"], records["finished_utc"]))
    observations = {}
    for request, record in zip(queue["requests"], records["observations"], strict=True):
        assert record["url"] == url_for("registry", request) and all(record[k] == v for k, v in request.items())
        assert lower <= datetime.fromisoformat(record["observed_at_utc"]) <= upper
        observations[request["package"], request["version"]] = record
    _, earlier = registry_index()
    traces = read_paths()
    roots = candidate_roots(traces)
    files = {c["sample_id"]: files for c, _, files in source_rows()}
    covered = set()
    for sid, path in roots.items():
        key = path["package"], path["version"]
        if key in earlier and verify_root(files[sid], path, earlier[key], observations[key]):
            covered.add(sid)
    contexts = []
    for row in traces:
        sid = row["sample_id"]
        accounts, complete, paths = context(row["root"], earlier)
        contexts.append((sid, (accounts, complete or sid in covered, paths), context(row["named"], earlier)))
    members, slots = frozen_portfolios()
    contrasts = {name: importer_contrast(contexts, {members[i] for i in indices})
                 for name, indices in slots.items()}
    original = read(RESULT)["importer_contrasts"]
    for name, contrast in contrasts.items():
        for sid, viable in contrast["possible_by_project"].items():
            assert set(viable) <= set(map(tuple, original[name]["possible_by_project"][sid]))
    write(OUTPUT, {"status": "post_hoc", "roots_checked": sorted(roots), "verified_root_closure": sorted(covered),
                   "receipts_sha256": sha(RECEIPTS), "earlier_results_sha256": sha(RESULT), "contrasts": contrasts})
    print("Verified closed roots:", len(covered))
    print({k: v["confirmed_gains"] for k, v in contrasts.items()})


if __name__ == "__main__":
    methods = {"freeze": freeze, "score": score}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=tuple(methods))
    methods[parser.parse_args().stage]()
