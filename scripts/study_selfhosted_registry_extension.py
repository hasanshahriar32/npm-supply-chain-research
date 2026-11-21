#!/usr/bin/env python3
"""Replay a bounded collection of missing exact-version maintainer observations."""
import argparse
from datetime import datetime
import json

import study_selfhosted_lockfile_followup as base
from collect_yunohost_observations import now, url_for
from replay_yunohost_consumer_results import REPLAY, read_graphs, registry_index

RUN = base.RUN
QUEUE = RUN / "registry_queue.json"
PROJECTED = RUN / "registry_projection.json"
RESULT = RUN / "extension_results.json"
PRIVATE = RUN / "private" / "registry.json"


def overlap_audit():
    projection = read_graphs(base.selfhost.PROJECTION)
    keys = base.selfhost.heldout.path_artifact(base.selfhost.RUN)["version_keys"]
    local = {tuple(keys[j]): set(indices) for j, indices in projection["observed_memberships"]}
    retained = read_graphs(REPLAY)
    assert projection["portfolios"] == retained["slots"]
    previous = registry_index(retained["initial"], base.yuno.RUN)
    primary = set().union(*(indices for key, indices in retained["slots"].items() if key != "control"))
    traces = read_graphs(base.TRACES)["traces"]
    canonical = {(w["package"], w["version"]) for row in traces for w in row["witnesses"]
                 if w["public_npm_tarball"]}
    shared = canonical & local.keys() & previous.keys()
    differences = [local[key] ^ set(previous[key]["accounts"]) for key in shared]
    return {"canonical_keys_in_both_captures": len(shared),
            "five_account_membership_disagreements": sum(bool(delta & primary) for delta in differences),
            "all_projected_membership_disagreements": sum(bool(delta) for delta in differences)}


def missing():
    traces = read_graphs(base.TRACES)["traces"]
    graph, _ = base.joined(traces)
    projection = read_graphs(base.selfhost.PROJECTION)
    keys = base.selfhost.heldout.path_artifact(base.selfhost.RUN)["version_keys"]
    local = {tuple(keys[j]) for j, _ in projection["observed_memberships"]}
    previous = registry_index(read_graphs(REPLAY)["initial"], base.yuno.RUN)
    picks = [set(projection["portfolios"][key]) for key in ("name", "version_1")]
    rows = []
    for t in traces:
        accounts, complete = graph[t["sample_id"]]
        if complete or all(accounts & pick for pick in picks):
            continue
        missing = []
        for w in t["witnesses"]:
            key = w["package"], w["version"]
            canonical = w["public_npm_tarball"]
            if (canonical and key in local) or key in previous:
                continue
            if canonical or base.yuno.sha512_values(w.get("registry_integrity_candidate")):
                missing.append(key)
        if missing:
            rows.append((t["sample_id"], set(missing)))
    keys = sorted({key for _, missing in rows for key in missing})
    requests = [dict(zip(("package", "version"), key, strict=True)) for key in keys]
    for request in requests:
        url_for("registry", request)
    return [sid for sid, _ in rows], requests


def freeze():
    if QUEUE.exists():
        raise ValueError("Registry extension queue is already frozen")
    projects, requests = missing()
    base.yuno.write(QUEUE, {"stage": "registry", "frozen_utc": now(),
                            "traces_sha256": base.yuno.sha(base.TRACES), "base_sha256": base.yuno.sha(base.RESULTS),
                            "projects": projects, "requests": requests})
    print(f"Frozen {len(requests)} exact-version requests in {len(projects)} projects")


def project():
    queue = base.yuno.read(QUEUE)
    ledger = base.yuno.read(PRIVATE)
    assert ledger["queue_sha256"] == base.yuno.sha(QUEUE) and ledger["stage"] == "registry"
    first, last = map(datetime.fromisoformat, (queue["frozen_utc"], ledger["finished_utc"]))
    maintainers, portfolios = base.yuno.frozen_portfolios()
    indices = {maintainers[i]: i for slots in portfolios.values() for i in slots}
    rows = []
    for receipt, request in zip(ledger["observations"], queue["requests"], strict=True):
        assert receipt["url"] == url_for("registry", request)
        assert all(receipt[k] == v for k, v in request.items())
        observed = datetime.fromisoformat(receipt["observed_at_utc"])
        assert first <= observed <= last
        row = {k: receipt[k] for k in ("package", "version", "status", "observed_at_utc")}
        if receipt["status"] == "observed":
            row["accounts"] = sorted(indices[a] for a in receipt["accounts"] if a in indices)
            row["integrity"] = receipt.get("integrity")
        rows.append(row)
    base.yuno.write(PROJECTED, {"queue_sha256": base.yuno.sha(QUEUE), "observations": rows,
                               "finished_utc": ledger["finished_utc"], "receipt_sha256": base.yuno.sha(PRIVATE)})
    base.yuno.write(RESULT, score())


def score():
    queue = base.yuno.read(QUEUE)
    projects, requests = missing()
    assert queue["stage"] == "registry" and queue["projects"] == projects and queue["requests"] == requests
    assert queue["traces_sha256"] == base.yuno.sha(base.TRACES) and queue["base_sha256"] == base.yuno.sha(base.RESULTS)
    captured = base.yuno.read(PROJECTED)
    assert captured["queue_sha256"] == base.yuno.sha(QUEUE)
    observations = captured["observations"]
    first, last = map(datetime.fromisoformat, (queue["frozen_utc"], captured["finished_utc"]))
    index = {}
    for receipt, request in zip(observations, requests, strict=True):
        assert all(receipt[k] == v for k, v in request.items())
        assert first <= datetime.fromisoformat(receipt["observed_at_utc"]) <= last
        if receipt["status"] == "observed":
            index[receipt["package"], receipt["version"]] = receipt
    comparison = base.score(index)["comparisons"]
    for key, earlier in base.yuno.read(base.RESULTS)["comparisons"].items():
        later = comparison[key]
        for metric in ("turnover_bounds", "net_bounds"):
            lo, hi = later[metric]
            assert earlier[metric][0] <= lo <= hi <= earlier[metric][1]
        assert earlier["resolved_pairs"] <= later["resolved_pairs"]
    return {"projection_sha256": base.yuno.sha(PROJECTED), "request_count": len(requests),
            "usable_receipts": len(index), "retained_registry_overlap": overlap_audit(),
            "comparisons": comparison}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "project", "verify"))
    action = parser.parse_args().action
    if action == "freeze":
        freeze()
    elif action == "project":
        project()
        print(json.dumps(base.yuno.read(RESULT), indent=2))
    else:
        assert score() == base.yuno.read(RESULT)
        print("Reproduced the Awesome-Selfhosted registry extension")
