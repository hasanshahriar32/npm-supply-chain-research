#!/usr/bin/env python3
"""Measure missingness and apply the same Yarn Classic path check in a second frame."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import gzip
import json
import subprocess

import study_selfhosted_lockfile_followup as locks
import study_selfhosted_registry_extension as extension
import study_yunohost_yarn_classic as yarn
from collect_yunohost_observations import url_for
from replay_yunohost_consumer_results import REPLAY, export_observations, read_graphs, registry_index

RUN = locks.RUN.with_name("selfhosted-yarn-evidence")
PROTOCOL = RUN / "protocol.json"
TRACES = RUN / "traces.json.gz"
QUEUE = RUN / "registry_queue.json"
RAW = RUN / "private/registry.json"
PROJECTED = RUN / "registry_projection.json.gz"
RESULTS = RUN / "results.json"
SOURCE = locks.selfhost.RUN
ROOT = locks.selfhost.ROOT
read, write, sha = locks.yuno.read, locks.yuno.write, locks.yuno.sha


def bindings():
    paths = (extension.RESULT, extension.PROJECTED, locks.TRACES, locks.FILES, locks.selfhost.RESULT,
             REPLAY, yarn.PARSER, ROOT / "scripts/study_yunohost_yarn_classic.py",
             ROOT / "scripts/collect_yarn_registry.py", ROOT / "scripts/study_selfhosted_yarn_evidence.py")
    return {str(path.relative_to(ROOT)): sha(path) for path in paths}


def previous(group):
    pairs = read(SOURCE / "results.json")["comparisons"][group]["projects"]
    roots = read(locks.selfhost.RESULT)["empty_roots"]
    extra = {(r["package"], r["version"]): r for r in read(extension.PROJECTED)["observations"]
             if r["status"] == "observed"}
    graph, _ = locks.joined(read_graphs(locks.TRACES)["traces"], extra)
    slots = read_graphs(REPLAY)["slots"]
    groups = ("control", "control") if group == "identical_control" else ("name", group)
    picks = [set(slots[key]) for key in groups]
    by_id = {}
    for pair in pairs:
        sid, feasible = pair["sample_id"], pair["feasible"]
        if sid in roots:
            feasible = [[0, 0]]
        elif sid in graph:
            accounts, complete = graph[sid]
            hits = [int(bool(accounts & pick)) for pick in picks]
            feasible = constrain(feasible, hits, complete) or feasible
        by_id[sid] = feasible
    expected = read(extension.RESULT)["comparisons"][group]
    assert summary(by_id) == {key: expected[key] for key in summary(by_id)}
    return by_id, picks


def constrain(states, hits, complete=False):
    return [state for state in states if (not complete or state == hits)
            and all(a >= b for a, b in zip(state, hits, strict=True))]


def summary(rows):
    deltas = [{v - n for n, v in states} for states in rows.values()]
    count = len(rows)
    return {"resolved_pairs": sum(len(states) == 1 for states in rows.values()),
            "turnover_bounds": [sum(0 not in delta for delta in deltas)/count,
                                sum(delta != {0} for delta in deltas)/count],
            "net_bounds": [sum(min(delta) for delta in deltas)/count, sum(max(delta) for delta in deltas)/count],
            "confirmed_differences": {sid: states[0] for sid, states in rows.items()
                                      if len(states) == 1 and sum(states[0]) == 1}}


def candidates():
    rows, _ = previous("version_1")
    for capture in read(locks.FILES):
        files = capture["files"]
        if len(rows[capture["sample_id"]]) > 1 and all(files.get(key, {}).get("status") == "retained"
                                                        for key in ("package.json", "yarn.lock")) and all(
            receipt.get("http_status") == 404 for key, receipt in files.items() if key not in ("package.json", "yarn.lock")
        ):
            yield capture


def freeze():
    RUN.mkdir(exist_ok=True)
    if PROTOCOL.exists():
        raise ValueError("Yarn analysis already frozen")
    origin = read(yarn.RUN / "protocol.json")
    assert origin["inputs"][str(yarn.NATIVE.relative_to(ROOT))] == sha(yarn.NATIVE)
    write(PROTOCOL, {"frozen_utc": locks.yuno.now(), "input_sha256": bindings(),
                     "source_native_sha256": sha(yarn.NATIVE),
                     "sample_ids": [row["sample_id"] for row in candidates()],
                     "design": "Post hoc evidence extension on every unresolved primary pair with a pinned root "
                               "manifest and Yarn lockfile, with 404 for all other root lockfiles. Reuse the YunoHost "
                               "Yarn Classic parser comparison and positive-only witness rules for regular root paths. "
                               "Use retained exact-version Yarn observations first. Query undiscovered keys from the "
                               "frozen trace once. Keep both evidence stages separate and retain the earlier feasible states."})


def trace():
    protocol = read(PROTOCOL)
    assert protocol["input_sha256"] == bindings() and protocol["source_native_sha256"] == sha(yarn.NATIVE)
    original = locks.selfhost.heldout.protocol_for(SOURCE)
    frame = {row["sample_id"]: row for row in original["projects"]}

    def read_source(capture):
        sid = capture["sample_id"]
        folder = locks.selfhost.heldout.check_observation(SOURCE, capture, frame[sid], original)
        command = ["node", str(yarn.PARSER), str(folder / "package.json"), str(folder / "yarn.lock"), str(yarn.NATIVE)]
        result = subprocess.run(command, text=True, capture_output=True, timeout=60)
        graph = json.loads(result.stdout) if result.returncode == 0 else {"status": "reader_error"}
        return {"sample_id": sid, "commit_sha": capture["commit_sha"], **graph}

    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(read_source, candidates()))
    assert protocol["sample_ids"] == [row["sample_id"] for row in rows]
    TRACES.write_bytes(gzip.compress(json.dumps(rows, separators=(",", ":")).encode(), mtime=0))
    print(dict(Counter(row["status"] for row in rows)))


def retained_index():
    return registry_index(read_graphs(REPLAY)["yarn"], yarn.RUN)


def requests_for(rows):
    keys = {(node["package"], node["version"]) for row in rows for node in row.get("nodes", {}).values()}
    return [{"package": name, "version": version} for name, version in sorted(keys - retained_index().keys())]


def freeze_registry():
    if QUEUE.exists():
        raise ValueError("Registry queue already frozen")
    requests = requests_for(read_graphs(TRACES))
    assert all(url_for("registry", request) for request in requests)
    write(QUEUE, {"frozen_utc": locks.yuno.now(), "stage": "yarn_classic_registry", "paths_sha256": sha(TRACES),
                  "protocol_sha256": sha(PROTOCOL), "requests": requests})
    print(f"Frozen {len(requests)} missing Yarn metadata requests")


def project():
    queue, raw = read(QUEUE), read(RAW)
    assert raw["queue_sha256"] == sha(QUEUE)
    assert all(row["url"] == url_for("registry", request)
               for row, request in zip(raw["observations"], queue["requests"], strict=True))
    names, slots = locks.yuno.frozen_portfolios()
    indices = {names[i]: i for ids in slots.values() for i in ids}
    rows = export_observations(raw["observations"], indices, yarn=True)
    for row, receipt in zip(rows, raw["observations"], strict=True):
        row["observed_at_utc"] = receipt["observed_at_utc"]
    projection = {"queue_sha256": sha(QUEUE), "receipt_sha256": sha(RAW),
                  "finished_utc": raw["finished_utc"], "observations": rows}
    PROJECTED.write_bytes(gzip.compress(json.dumps(projection, separators=(",", ":")).encode(), mtime=0))


def acquired_index():
    queue = read(QUEUE)
    assert queue["paths_sha256"] == sha(TRACES) and queue["protocol_sha256"] == sha(PROTOCOL)
    assert queue["requests"] == requests_for(read_graphs(TRACES))
    projection = read_graphs(PROJECTED)
    assert projection["queue_sha256"] == sha(QUEUE)
    start, end = map(datetime.fromisoformat, (queue["frozen_utc"], projection["finished_utc"]))
    for row, request in zip(projection["observations"], queue["requests"], strict=True):
        assert all(row[k] == v for k, v in request.items())
        assert start <= datetime.fromisoformat(row["observed_at_utc"]) <= end
    return registry_index(projection["observations"], RUN)


def measure(graphs, registry):
    witnesses = {graph["sample_id"]: yarn.witnesses(graph, registry)[0] for graph in graphs}
    comparisons = {}
    for group in ("version_1", "version_2", "version_3", "identical_control"):
        before, picks = previous(group)
        after = before.copy()
        changes = Counter()
        for sid, (_, accounts, _, _) in witnesses.items():
            hits = [int(bool(accounts & pick)) for pick in picks]
            states = constrain(before[sid], hits)
            if states:
                after[sid] = states
                changes["new_shared_hits"] += len(before[sid]) > 1 and states == [[1, 1]]
            else:
                changes["contradicts_prior"] += 1
        comparisons[group] = {**summary(after), **{k: v for k, v in changes.items() if v}}
    return {"projects_with_registry_link": sum(witness[3] > 0 for witness in witnesses.values()),
            "comparisons": comparisons}


def score():
    protocol = read(PROTOCOL)
    assert protocol["input_sha256"] == bindings()
    graphs = read_graphs(TRACES)
    assert protocol["sample_ids"] == [r["sample_id"] for r in candidates()] == [r["sample_id"] for r in graphs]
    index = retained_index()
    later = acquired_index()
    assert not index.keys() & later.keys()
    reused, combined = measure(graphs, index), measure(graphs, index | later)
    for key, earlier in reused["comparisons"].items():
        final = combined["comparisons"][key]
        assert earlier["resolved_pairs"] <= final["resolved_pairs"]
        for metric in ("turnover_bounds", "net_bounds"):
            lo, hi = final[metric]
            assert earlier[metric][0] <= lo <= hi <= earlier[metric][1]
    return {"paths_sha256": sha(TRACES), "projection_sha256": sha(PROJECTED),
            "path_status": dict(Counter(row["status"] for row in graphs)),
            "request_count": len(read(QUEUE)["requests"]),
            "usable_maintainer_lists": sum(row["accounts"] is not None for row in later.values()),
            "retained_registry": reused, "all_registry": combined}


if __name__ == "__main__":
    stages = {"freeze": freeze, "trace": trace, "freeze-registry": freeze_registry, "project": project}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=(*stages, "score", "verify"))
    stage = parser.parse_args().stage
    if stage in stages:
        stages[stage]()
    elif stage == "score":
        write(RESULTS, score())
    else:
        assert score() == read(RESULTS)
        print("Reproduced the Awesome-Selfhosted Yarn Classic follow-up")
