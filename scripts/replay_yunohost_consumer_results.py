#!/usr/bin/env python3
"""Export and replay the YunoHost estimates from frozen paths and reduced observations."""
import argparse
from collections import Counter
import gzip
import json

import study_yunohost_holdout as initial
import study_yunohost_yarn_classic as followup
from verify_yunohost_holdout import verify_manuscript_table
from verify_yunohost_yarn_classic import verify_followup_table

REPLAY = followup.RUN / "registry_replay.json.gz"
CASES = followup.RUN / "confirmed_cases.md"


def read_graphs(path):
    return json.loads(gzip.decompress(path.read_bytes()))


def export_observations(receipts, account_slots, yarn=False):
    fields = ("conditional", "dependencies", "optional_dependencies", "bundles_dependencies") if yarn else ()
    rows = []
    for record in receipts:
        projected = {key: record[key] for key in ("package", "version", "status")}
        if record["status"] == "observed":
            projected.update({key: record[key] for key in fields})
            projected["integrity"] = sorted(initial.sha512_values(record.get("integrity")))
            accounts = record["accounts"]
            projected["accounts"] = None if accounts is None else sorted(
                account_slots[account] for account in accounts if account in account_slots
            )
        rows.append(projected)
    return rows


def export():
    members, slots = initial.frozen_portfolios()
    account_slots = {members[i]: i for indices in slots.values() for i in indices}
    sources = (initial.read(initial.RUN / "results.json"), initial.read(followup.RUN / "results.json"))
    assert sources[0]["registry_ledger_sha256"] == initial.sha(initial.PRIVATE / "registry.json")
    assert sources[1]["registry_ledger_sha256"] == initial.sha(followup.LEDGER)
    data = {
        "slots": slots,
        "initial": export_observations(initial.read_collection("registry"), account_slots),
        "yarn": export_observations(followup.read_ledger(followup.verify_protocol()), account_slots, yarn=True),
    }
    REPLAY.write_bytes(gzip.compress(json.dumps(data, separators=(",", ":")).encode(), mtime=0))
    traces, rows, index = replay()
    write_cases(traces, rows, index, {key: set(ids) for key, ids in slots.items()})


def registry_index(rows, stage):
    queue = initial.read(stage / "registry_queue.json")["requests"]
    assert [{"package": row["package"], "version": row["version"]} for row in rows] == queue
    index = {}
    for row in rows:
        if row["status"] == "observed":
            # Preserve the SRI string interface used by the original scoring functions.
            index[row["package"], row["version"]] = {**row, "integrity": " ".join(row["integrity"])}
    return index


def replay():
    data = read_graphs(REPLAY)
    protocol = initial.read(initial.RUN / "protocol.json")
    assert {k: initial.digest(json.dumps(v).encode()) for k, v in data["slots"].items()} == protocol["portfolio_fingerprints"]
    slots = {k: set(v) for k, v in data["slots"].items()}
    selected_indices = set.union(*slots.values())
    assert all(set(record.get("accounts") or []).issubset(selected_indices)
               for study in ("initial", "yarn") for record in data[study])
    initial_results = initial.read(initial.RUN / "results.json")
    yarn_results = initial.read(followup.RUN / "results.json")
    paths = initial.RUN / "paths.json.gz"
    assert initial_results["paths_sha256"] == initial.sha(paths)
    assert yarn_results["paths_sha256"] == initial.sha(followup.GRAPH)
    assert yarn_results["prior_results_sha256"] == initial.sha(initial.RUN / "results.json")

    traces = read_graphs(paths)
    index = registry_index(data["initial"], initial.RUN)
    old, joins = initial.frame_paths(traces, index)
    assert dict(joins) == initial_results["path_identity"]
    assert sum(row[2] for row in old) == initial_results["projects_with_complete_path_and_registry_evidence"]
    yarn_index = registry_index(data["yarn"], followup.RUN)
    yarn = {}
    reasons = Counter()
    for graph in read_graphs(followup.GRAPH):
        row, issues = followup.witnesses(graph, yarn_index)
        yarn[row[0]] = row
        reasons.update(issues)
    assert dict(reasons) == yarn_results["registry_path_issues"]
    combined = [yarn.get(row[0], row) for row in old]
    groups = [(f"version_{i}", slots["name"], slots[f"version_{i}"]) for i in range(1, 4)]
    groups.append(("identical_control", slots["control"], slots["control"]))
    for source, rows in ((initial_results, old), (yarn_results, combined)):
        assert len(rows) == source["denominator"]
        # Compare every project's documented outcomes and feasible states.
        assert {key: initial.paired(rows, name, version) for key, name, version in groups} == source["comparisons"]
    verify_manuscript_table(initial_results["comparisons"])
    verify_followup_table(yarn_results["comparisons"])
    result = yarn_results["comparisons"]["version_1"]
    print(f"Reproduced {len(combined)} project rows per contrast, before and after Yarn Classic")
    print(f"Primary turnover {result['turnover_bounds']}; net change {result['net_bounds']}")
    return traces, old, index


def write_cases(traces, rows, index, slots):
    from compare_yunohost_npm_extractors import previous_reader

    inputs = {row["frame_id"]: row for row, _ in initial.inputs()}
    lines = [
        "# Five confirmed differences in the primary YunoHost comparison", "",
        "Each case uses a complete mandatory production tree for the supported root importer. "
        "Every retained location joins to its exact npm version. One selected account has a "
        "documented path and the other selection has no match in that checked tree. "
        "The examples use current registry associations at collection time.", "",
        "| Project | Covered by | Corroborated dependency path | Checked locations | Pinned source |",
        "| --- | --- | --- | ---: | --- |",
    ]
    case_count = 0
    for (sample_id, observed, complete, confirmed), trace in zip(rows, traces, strict=True):
        name, version = (bool(observed & slots[k]) for k in ("name", "version_1"))
        if not complete or name == version:
            continue
        project = inputs[sample_id]
        earlier = previous_reader(project)[1]
        assert trace["complete"] and not trace["issues"] and confirmed == len(trace["witnesses"])
        key = "name" if name else "version_1"
        candidates = []
        for witness in trace["witnesses"]:
            package = witness["package"], witness["version"]
            record = index[package]
            matches = slots[key] & set(record["accounts"])
            if matches and (witness["location"], *package) in earlier:
                candidates.append(witness)
        witness = min(candidates, key=lambda w: (len(w["path"]), w["location"]))
        chain = " → ".join(f"`{edge['package']}@{edge['version']}`" for edge in witness["path"])
        commit = project["commit_sha"]
        url = f"https://github.com/{project['repository']}/blob/{commit}"
        lockfile = initial.choose_npm(project)
        lines.append(f"| {sample_id} | {'Name' if name else 'Version'} | {chain} | "
                     f"{confirmed} | [Manifest]({url}/package.json), [lockfile]({url}/{lockfile}) |")
        case_count += 1
    assert case_count == 5
    lines += ["", "The offline replay checks the opposing zero using all joined locations, "
              "including locations outside the displayed path. The earlier reader independently "
              "corroborated the displayed positive location."]
    CASES.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--export", action="store_true", help="Export from locally retained frozen registry receipts")
    if cli.parse_args().export:
        export()
    else:
        replay()
