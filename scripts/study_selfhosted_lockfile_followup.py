#!/usr/bin/env python3
"""Check retained npm and pnpm lockfiles in the unresolved Awesome-Selfhosted frame."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import gzip
import json
import shutil
import subprocess

import replay_selfhosted_comparison as selfhost
import study_yunohost_holdout as yuno
from replay_yunohost_consumer_results import REPLAY, read_graphs, registry_index
from study_pnpm_parser_development import root_record

RUN = selfhost.RUN.with_name("selfhosted-lockfile-followup")
TRACES = RUN / "traces.json.gz"
RESULTS = RUN / "results.json"
FILES = selfhost.RUN / "observations.json"
SOURCES = ("study_selfhosted_lockfile_followup.py", "consumer_npm_development.cjs",
           "consumer_pnpm_development.cjs", "study_pnpm_parser_development.py", "study_yunohost_holdout.py")
LOCKS = {"npm-shrinkwrap.json": "npm", "package-lock.json": "npm", "pnpm-lock.yaml": "pnpm"}


def evidence_hashes():
    paths = (selfhost.PROJECTION, selfhost.RESULT, REPLAY, FILES, *(selfhost.ROOT / "scripts" / name for name in SOURCES))
    return {str(p.relative_to(selfhost.ROOT)): yuno.sha(p) for p in paths}


def candidates():
    raw = yuno.read(selfhost.RUN / "results.json")["comparisons"]["version_1"]["projects"]
    zeros = yuno.read(selfhost.RESULT)["empty_roots"]
    projects = yuno.read(FILES)
    out = []
    for project, pair in zip(projects, raw, strict=True):
        sid = project["sample_id"]
        assert sid == pair["sample_id"]
        files = project["files"]
        if len(pair["feasible"]) == 1 or sid in zeros or files.get("package.json", {}).get("status") != "retained":
            continue
        manager_files = [name for name, receipt in files.items()
                         if name != "package.json" and receipt["status"] == "retained"]
        if len(manager_files) != 1 or manager_files[0] not in LOCKS:
            continue
        chosen = manager_files[0]
        if any(files[k].get("http_status") != 404 for k in files if k not in ("package.json", chosen)):
            continue
        out.append((project, chosen))
    return out


def inspect(item, frame, protocol, pnpm):
    capture, lock = item
    sid = capture["sample_id"]
    folder = selfhost.heldout.check_observation(selfhost.RUN, capture, frame[sid], protocol)
    assert folder is not None
    family = LOCKS[lock]
    result = {"sample_id": sid, "commit_sha": capture["commit_sha"], "lockfile": lock,
              "status": f"{family}_unavailable", "complete": False, "witnesses": []}
    manifest = yuno.read(folder / "package.json")
    selected_manager = manifest.get("packageManager")
    if selected_manager and (not isinstance(selected_manager, str) or selected_manager.partition("@")[0] != family):
        return {**result, "status": "manager_disagrees"}
    try:
        if family == "npm":
            result.update(yuno.npm_paths(capture, folder, []))
        else:
            parsed = root_record(capture, pnpm, folder=folder)
            result.update(parsed)
            result["status"] = f"pnpm_{parsed['status']}"
    except (subprocess.SubprocessError, ValueError, UnicodeDecodeError):
        result["status"] = f"{family}_parser_error"
    return result


def trace():
    pnpm = shutil.which("pnpm")
    if pnpm is None:
        raise RuntimeError("pnpm is required for source replay")
    protocol = selfhost.heldout.protocol_for(selfhost.RUN)
    frame = {r["sample_id"]: r for r in protocol["projects"]}
    version = subprocess.check_output([pnpm, "--version"], text=True, cwd="/tmp", timeout=15).strip()
    with ThreadPoolExecutor(max_workers=4) as executor:
        rows = list(executor.map(lambda item: inspect(item, frame, protocol, pnpm), candidates()))
    RUN.mkdir(exist_ok=True)
    item = {"input_sha256": evidence_hashes(), "pnpm_version": version, "traces": rows}
    TRACES.write_bytes(gzip.compress(json.dumps(item, separators=(",", ":")).encode(), mtime=0))
    print("Source outcomes:", dict(Counter(r["status"] for r in rows)))


def joined(traces, extra_registry=None):
    projection = read_graphs(selfhost.PROJECTION)
    keys = selfhost.heldout.path_artifact(selfhost.RUN)["version_keys"]
    local = {tuple(keys[j]): set(accounts) for j, accounts in projection["observed_memberships"]}
    ext = registry_index(read_graphs(REPLAY)["initial"], yuno.RUN)
    if extra_registry:
        assert not ext.keys() & extra_registry.keys()
        ext.update(extra_registry)
    graph = {}
    evidence = Counter()
    for row in traces:
        accounts, complete = set(), row["complete"]
        for witness in row["witnesses"]:
            key = witness["package"], witness["version"]
            other = ext.get(key)
            lock_sri = yuno.sha512_values(witness.get("registry_integrity_candidate"))
            if witness["public_npm_tarball"] and key in local:
                accounts.update(local[key])
                evidence["original_registry"] += 1
            elif other and (witness["public_npm_tarball"]
                            or lock_sri & yuno.sha512_values(other.get("integrity"))):
                accounts.update(other["accounts"])
                evidence["reused_yunohost_registry"] += 1
            else:
                complete = False
                evidence["unlinked_locations"] += 1
        graph[row["sample_id"]] = (accounts, complete)
    return graph, evidence


def score(extra_registry=None):
    item = read_graphs(TRACES)
    assert item["input_sha256"] == evidence_hashes()
    traces = item["traces"]
    assert [(r["sample_id"], r["lockfile"]) for r in traces] == [(r["sample_id"], lock) for r, lock in candidates()]
    graph, evidence = joined(traces, extra_registry)
    original = yuno.read(selfhost.RUN / "results.json")
    projection = read_graphs(selfhost.PROJECTION)
    portfolios = {k: set(v) for k, v in projection["portfolios"].items()}
    zeros = yuno.read(selfhost.RESULT)["empty_roots"]
    results = {}
    for key, baseline in original["comparisons"].items():
        name = "control" if key == "identical_control" else "name"
        version = "control" if key == "identical_control" else key
        outcomes = []
        gains = Counter()
        differences = {}
        for case in baseline["projects"]:
            sid, states = case["sample_id"], case["feasible"]
            if sid in zeros:
                states = [[0, 0]]
            elif sid in graph:
                accounts, complete = graph[sid]
                observed = [int(bool(accounts & portfolios[which])) for which in (name, version)]
                constrained = [s for s in states if all(a >= b for a, b in zip(s, observed, strict=True))
                               and (not complete or s == observed)]
                if constrained:
                    if len(states) > 1 and len(constrained) == 1:
                        gains["".join(str(bit) for bit in constrained[0])] += 1
                    states = constrained
                else:
                    gains["inconsistent_followup"] += 1
            if len(states) == 1 and sum(states[0]) == 1:
                differences[sid] = states[0]
            outcomes.append(states)
        n = len(outcomes)
        deltas = [{v - u for u, v in states} for states in outcomes]
        results[key] = {"resolved_pairs": sum(len(s) == 1 for s in outcomes), "new_resolved": dict(gains),
                        "turnover_bounds": [sum(0 not in d for d in deltas)/n, sum(d != {0} for d in deltas)/n],
                        "net_bounds": [sum(min(d) for d in deltas)/n, sum(max(d) for d in deltas)/n],
                        "confirmed_differences": differences}
    return {"traces_sha256": yuno.sha(TRACES), "candidate_count": len(traces),
            "projects_with_witnesses": sum(bool(r["witnesses"]) for r in traces),
            "statuses": dict(Counter(r["status"] for r in traces)), "join_counts": dict(evidence),
            "comparisons": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("trace", "score", "verify"))
    action = parser.parse_args().action
    if action == "trace":
        trace()
    elif action == "score":
        result = score()
        yuno.write(RESULTS, result)
        print(json.dumps(result, indent=2))
    else:
        assert score() == yuno.read(RESULTS)
        print("Reproduced the Awesome-Selfhosted lockfile follow-up")
