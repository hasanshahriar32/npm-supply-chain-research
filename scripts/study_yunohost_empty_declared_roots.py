#!/usr/bin/env python3
"""Check declared production roots in newer Yarn and missing-lockfile strata."""
import argparse
from collections import Counter
import json
import subprocess

from study_yunohost_empty_pnpm_roots import (
    INITIAL, FOLLOWUP, RESULTS as PNPM_RESULTS, YAML_READER,
    check_bounds, declaration_count, unique_object,
)
from replay_yunohost_consumer_results import read_graphs
from collect_yunohost_root_evidence import FILES

RUN = INITIAL.RUN.with_name("yunohost-empty-declared-roots")
PROTOCOL = RUN / "protocol.json"
RESULTS = RUN / "results.json"
TRACE = INITIAL.RUN / "paths.json.gz"
PAIRS = FOLLOWUP.RUN / "results.json"
SCRIPT = INITIAL.ROOT / "scripts/study_yunohost_empty_declared_roots.py"
GROUPS = ("dependencies", "optionalDependencies", "peerDependencies", "devDependencies")
MISSING_LOCKFILE = ("no_root_lockfile_returned", "declared_lockfile_unavailable")


def selection():
    traces = read_graphs(TRACE)
    yarn_status = {row["sample_id"]: row["status"] for row in read_graphs(FOLLOWUP.GRAPH)}
    prior = INITIAL.read(PNPM_RESULTS)
    empty_pnpm = set(prior["verified_empty_roots"])
    projects = INITIAL.read(PAIRS)["comparisons"]["version_1"]["projects"]
    selected = {}
    for trace, row in zip(traces, projects, strict=True):
        sid = trace["sample_id"]
        assert sid == row["sample_id"]
        if len(row["feasible"]) == 1 or sid in empty_pnpm:
            continue
        if yarn_status.get(sid) == "unsupported_yarn_format":
            selected[sid] = "modern_yarn"
        elif trace["status"] in MISSING_LOCKFILE:
            selected[sid] = "missing_lockfile"
    return selected


def bindings():
    paths = (TRACE, PAIRS, FOLLOWUP.GRAPH, PNPM_RESULTS, SCRIPT)
    return {str(path.relative_to(INITIAL.ROOT)): INITIAL.sha(path) for path in paths}


def freeze():
    RUN.mkdir(exist_ok=True)
    if PROTOCOL.exists():
        raise ValueError("Protocol already exists")
    INITIAL.write(PROTOCOL, {
        "frozen_utc": INITIAL.now(),
        "input_sha256": bindings(),
        "selected": selection(),
        "design": "Post hoc structural-zero sensitivity. Preliminary manifest and lockfile inventories "
                  "informed the choice of two strata. Check all unresolved newer Yarn candidates and "
                  "all unresolved projects without a usable root lockfile in the specified intake statuses.",
        "shared_rule": "Require no root dependencies, optionalDependencies, peerDependencies, or bundled dependencies.",
        "modern_yarn": "Require a declared Yarn 3 or 4 manager, a version 6, 8 or 10 lockfile, "
                       "and one matching root workspace locator whose lock dependencies agree with "
                       "the manifest's devDependencies. Root workspaces are checked only at '.'; "
                       "child workspaces are outside this scope.",
        "missing_lockfile": "Require no declared child workspaces and every supported lockfile and pnpm workspace probe "
                            "to be HTTP 404. A structurally empty pinned manifest can supply the root "
                            "zero without a concrete lockfile path.",
        "outcome": "Bound only the frozen mandatory root dependency estimand. "
                   "Retain all original positives and report separately from the primary protocol.",
    })
    print(dict(Counter(selection().values())))


def read_lockfile(path, manifest):
    contents = subprocess.check_output(
        ["ruby", "-rpsych", "-rjson", "-e", YAML_READER],
        input=path.read_text(), text=True, timeout=45)
    lock = json.loads(contents)["project"]
    roots = [row for key, row in lock.items() if key != "__metadata" and
             isinstance(row, dict) and str(row.get("resolution", "")).endswith("@workspace:.")]
    lock_version = str(lock.get("__metadata", {}).get("version", ""))
    if len(roots) != 1:
        return {"version": lock_version, "root_count": len(roots), "dev_matches": False, "peerless": False}
    root = roots[0]
    development = manifest.get("devDependencies", {})
    locked = root.get("dependencies", {})
    development_matches = isinstance(locked, dict) and locked.keys() == development.keys() and all(
        isinstance(spec, str) and locked[name] in (spec, f"npm:{spec}")
        for name, spec in development.items()
    )
    expected_name = manifest.get("name")
    return {"version": lock_version, "root_count": len(roots),
            "dev_matches": development_matches,
            "locator_matches": isinstance(expected_name, str) and root["resolution"] == f"{expected_name}@workspace:."
                               or not expected_name and root["resolution"].startswith("root-workspace-"),
            "peerless": not root.get("peerDependencies")}


def record(row, stratum):
    sid = row["frame_id"]
    folder = INITIAL.CAPTURE / "projects" / sid
    manifest = json.loads((folder / "package.json").read_bytes(), object_pairs_hook=unique_object)
    info = {"sample_id": sid, "stratum": stratum, "repository": row["repository"],
            "commit_sha": row["commit_sha"], "manifest_sha256": row["files"]["package.json"]["sha256"],
            "counts": {key: declaration_count(manifest, key) for key in GROUPS},
            "workspaces": bool(manifest.get("workspaces")),
            "bundled": bool(manifest.get("bundledDependencies") or manifest.get("bundleDependencies"))}
    if stratum == "missing_lockfile":
        info["root_lockfile_http"] = {name: item.get("http_status") for name, item in row["files"].items()
                                     if name != "package.json"}
    else:
        info["yarn_declared"] = str(manifest.get("packageManager")).startswith(("yarn@3.", "yarn@4."))
        info["lockfile_sha256"] = row["files"]["yarn.lock"]["sha256"]
        try:
            info["lock"] = read_lockfile(folder / "yarn.lock", manifest)
        except (subprocess.SubprocessError, ValueError, KeyError, TypeError):
            info["lock"] = {"parse_unresolved": True}
    return info


def eligible(row):
    if row["bundled"] or any(row["counts"][key] for key in GROUPS[:-1]):
        return False
    if row["stratum"] == "missing_lockfile":
        probes = row["root_lockfile_http"]
        return not row["workspaces"] and probes == {
            name: 404 for name in FILES if name != "package.json"
        }
    lock = row["lock"]
    return (row["yarn_declared"] and lock.get("version") in ("6", "8", "10") and lock.get("root_count") == 1
            and all(lock.get(key) for key in ("dev_matches", "locator_matches", "peerless")))


def summaries(observations):
    additions = {row["sample_id"] for row in observations if eligible(row)}
    prior = set(INITIAL.read(PNPM_RESULTS)["verified_empty_roots"])
    assert not additions & prior
    return {"additional_common_negatives": sorted(additions),
            "additional_by_stratum": dict(Counter(row["stratum"] for row in observations if eligible(row))),
            "comparisons": check_bounds(prior | additions)}


def score():
    protocol = INITIAL.read(PROTOCOL)
    assert protocol["input_sha256"] == bindings() and protocol["selected"] == selection()
    projects = {row["frame_id"]: row for row, _ in INITIAL.inputs()}
    observations = [record(projects[sid], stratum) for sid, stratum in protocol["selected"].items()]
    result = {"protocol_sha256": INITIAL.sha(PROTOCOL), "observations": observations, **summaries(observations)}
    INITIAL.write(RESULTS, result)
    print(result["additional_by_stratum"], result["comparisons"]["version_1"])


def verify():
    protocol = INITIAL.read(PROTOCOL)
    result = INITIAL.read(RESULTS)
    assert protocol["input_sha256"] == bindings() and protocol["selected"] == selection()
    assert result["protocol_sha256"] == INITIAL.sha(PROTOCOL)
    observations = result["observations"]
    assert {row["sample_id"]: row["stratum"] for row in observations} == protocol["selected"]
    assert len(observations) == len(protocol["selected"])
    for key, expected in summaries(observations).items():
        assert result[key] == expected
    table = (INITIAL.ROOT / "manuscript_q1/tables/yunohost_consumer_holdout_table.tex").read_text()
    variants = [result["comparisons"][f"version_{n}"] for n in range(1, 4)]
    numbers = " & ".join(str(r["resolved_pairs"]) for r in variants)
    assert f"Combined resolved pairs & {numbers}" + r"\\" in table
    for label, field in ((r"Combined turnover (\%)", "turnover_bounds"),
                         ("Combined net change (pp)", "net_bounds")):
        expected = [f"$[{100*lo:.1f},{100*hi:.1f}]$" for lo, hi in (r[field] for r in variants)]
        assert " & ".join([label, *expected]) + r"\\" in table
    print("Reproduced the combined empty-root sensitivity:", result["additional_by_stratum"])


if __name__ == "__main__":
    stages = {"freeze": freeze, "score": score, "verify": verify}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=stages)
    stages[parser.parse_args().stage]()
