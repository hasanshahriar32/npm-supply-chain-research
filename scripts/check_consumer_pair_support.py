#!/usr/bin/env python3
"""Recount which retained files support the final paired outcomes in each frame."""
import argparse
from collections import Counter

import check_yunohost_npm_unresolved as npm
import study_selfhosted_yarn_evidence as selfhost

OUTPUT = selfhost.RUN / "support.json"
STRATA = ("npm", "pnpm", "yarn", "bun", "multiple", "no_lock", "no_manifest")
LOCKS = {"npm-shrinkwrap.json": "npm", "package-lock.json": "npm", "pnpm-lock.yaml": "pnpm",
         "yarn.lock": "yarn", "bun.lock": "bun", "bun.lockb": "bun"}


def selfhost_stratum(capture):
    files = capture["files"]
    if files.get("package.json", {}).get("status") != "retained":
        return "no_manifest"
    kinds = {LOCKS[name] for name, row in files.items() if name in LOCKS and row["status"] == "retained"}
    if len(kinds) > 1:
        return "multiple"
    return next(iter(kinds), "no_lock")


def yunohost_stratum(trace):
    status = trace["status"]
    if status == "multiple_manager_families":
        return "multiple"
    if status in ("no_root_lockfile_returned", "declared_lockfile_unavailable"):
        return "no_lock"
    manager, _, _ = status.partition("_")
    assert manager in STRATA[:4]
    return manager


def selfhosted_pairs(group="version_1"):
    old, picks = selfhost.previous(group)
    index = selfhost.retained_index() | selfhost.acquired_index()
    for graph in selfhost.read_graphs(selfhost.TRACES):
        sid, accounts, _, _ = selfhost.yarn.witnesses(graph, index)[0]
        hits = [int(bool(accounts & pick)) for pick in picks]
        old[sid] = selfhost.constrain(old[sid], hits) or old[sid]
    expected = selfhost.read(selfhost.RESULTS)["all_registry"]["comparisons"][group]
    actual = selfhost.summary(old)
    assert all(expected[key] == value for key, value in actual.items())
    return old


def yunohost_pairs():
    audit = selfhost.read(npm.RESULTS)
    zeros = set(audit["additional_common_negatives"])
    zeros.update(selfhost.read(npm.bun.EMPTY_RESULTS)["additional_common_negatives"])
    zeros.update(selfhost.read(npm.bun.PNPM_RESULTS)["verified_empty_roots"])
    positive_records = selfhost.read(npm.bun.RESULTS)["registry_join"] + audit["registry_join"]
    positives = {row["sample_id"] for row in positive_records if {"name", "version_1"} <= set(row["covered_by"])}
    assert not zeros & positives
    pairs = {}
    for row in selfhost.read(npm.bun.PAIRS)["comparisons"]["version_1"]["projects"]:
        sid, states = row["sample_id"], row["feasible"]
        if sid in zeros or sid in positives:
            outcome = [1, 1] if sid in positives else [0, 0]
            assert outcome in states and len(states) > 1
            states = [outcome]
        pairs[sid] = states
    actual = selfhost.summary(pairs)
    assert all(actual[key] == value for key, value in audit["comparisons"]["version_1"].items())
    return pairs


def classify(strata, pairs):
    assert strata.keys() == pairs.keys()
    result = {stratum: Counter(total=0, resolved=0, confirmed_turnover=0, possible_turnover=0) for stratum in STRATA}
    for project, states in pairs.items():
        row = result[strata[project]]
        row["total"] += 1
        row["resolved"] += len(states) == 1
        row["confirmed_turnover"] += all(n != v for n, v in states)
        row["possible_turnover"] += any(n != v for n, v in states)
    return result


def score():
    left = {row["sample_id"]: selfhost_stratum(row) for row in selfhost.read(selfhost.locks.FILES)}
    right = {row["sample_id"]: yunohost_stratum(row) for row in selfhost.read_graphs(npm.bun.TRACES)}
    return {"awesome_selfhosted": classify(left, selfhosted_pairs()), "yunohost": classify(right, yunohost_pairs())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("score", "verify"))
    result = score()
    if parser.parse_args().action == "score":
        selfhost.write(OUTPUT, result)
    else:
        assert selfhost.read(OUTPUT) == result
        print("Reproduced the primary comparison by retained lockfile support")
