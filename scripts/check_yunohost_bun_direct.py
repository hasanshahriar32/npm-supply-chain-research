#!/usr/bin/env python3
"""Evaluate direct Bun lockfile witnesses using registry receipts already retained."""
import argparse
from collections import Counter
import json
import subprocess

from replay_yunohost_consumer_results import REPLAY, read_graphs, registry_index
from study_yunohost_empty_pnpm_roots import (
    INITIAL, FOLLOWUP, RESULTS as PNPM_RESULTS, YAML_READER, unique_object,
)
from study_yunohost_empty_declared_roots import RESULTS as EMPTY_RESULTS

RUN = INITIAL.RUN.with_name("yunohost-bun-direct")
RESULTS = RUN / "results.json"
TRACES = INITIAL.RUN / "paths.json.gz"
PAIRS = FOLLOWUP.RUN / "results.json"
SEMVER_CHECK = """
const fs = require('node:fs'), path = require('node:path');
const npm = path.resolve(path.dirname(fs.realpathSync(process.execPath)), '../lib/node_modules/npm/package.json');
const semver = require('node:module').createRequire(npm)('semver');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
console.log(JSON.stringify(input.map(({version, range}) => Boolean(
    semver.valid(version) && semver.validRange(range) && semver.satisfies(version, range)
))));
"""


def candidates():
    projects = INITIAL.read(PAIRS)["comparisons"]["version_1"]["projects"]
    return [trace["sample_id"] for trace, row in zip(read_graphs(TRACES), projects, strict=True)
            if trace["status"] == "bun_file_available" and len(row["feasible"]) > 1]


def parse(row):
    sid = row["frame_id"]
    lock_receipt = row["files"]["bun.lock"]
    result = {"sample_id": sid, "repository": row["repository"], "commit_sha": row["commit_sha"],
              "manifest_sha256": row["files"]["package.json"]["sha256"], "witnesses": []}
    if lock_receipt["status"] != "retained":
        return {**result, "status": "text_lockfile_unavailable"}
    folder = INITIAL.CAPTURE / "projects" / sid
    manifest = json.loads((folder / "package.json").read_bytes(), object_pairs_hook=unique_object)
    lock = subprocess.check_output(
        ["ruby", "-rpsych", "-rjson", "-e", YAML_READER],
        input=(folder / "bun.lock").read_text(), text=True, timeout=45)
    lock = json.loads(lock)["project"]
    result["lockfile_sha256"] = lock_receipt["sha256"]
    if lock["lockfileVersion"] not in (1, 2) or set(lock["workspaces"]) != {""} or manifest.get("workspaces"):
        return {**result, "status": "unsupported_lockfile_or_workspace"}
    if any(doc.get(key) for doc in (manifest, lock) for key in ("overrides", "patchedDependencies", "resolutions")):
        return {**result, "status": "override_or_patch_present"}
    root = lock["workspaces"][""]
    declared = manifest.get("dependencies", {})
    if (manifest.get("name") != root.get("name") or declared != root.get("dependencies", {})
            or manifest.get("optionalDependencies", {}) != root.get("optionalDependencies", {})):
        return {**result, "status": "manifest_lockfile_disagreement"}
    accepted = []
    for name, constraint in sorted(declared.items()):
        values = lock["packages"].get(name, [])
        if name in manifest.get("optionalDependencies", {}) or not isinstance(values, list) or len(values) != 4:
            continue
        locator, host, metadata, integrity = values
        if not isinstance(locator, str) or not isinstance(constraint, str):
            continue
        actual_name, _, version = locator.rpartition("@")
        if (name != actual_name or host != "" or not isinstance(metadata, dict)
                or {"os", "cpu", "libc"} & metadata.keys() or not INITIAL.sha512_values(integrity)):
            continue
        accepted.append({"package": name, "version": version, "range": constraint, "integrity": integrity})
    semver = json.loads(subprocess.check_output(["node", "-e", SEMVER_CHECK],
                                              input=json.dumps(accepted), text=True, timeout=20))
    return {**result, "status": "direct_checked", "regular_declarations": len(declared),
            "witnesses": [w for w, valid in zip(accepted, semver, strict=True) if valid]}


def evaluate(observations):
    projected = read_graphs(REPLAY)
    slots = {key: set(value) for key, value in projected["slots"].items()}
    registries = [registry_index(projected["initial"], INITIAL.RUN),
                  registry_index(projected["yarn"], FOLLOWUP.RUN)]
    output = []
    for row in observations:
        accepted = []
        members = set()
        conflicting = 0
        for witness in row["witnesses"]:
            key = witness["package"], witness["version"]
            rows = [registry[key] for registry in registries if key in registry]
            matches = [record for record in rows if
                       witness["integrity"] in INITIAL.sha512_values(record["integrity"])
                       and record["accounts"] is not None]
            if not matches:
                continue
            accounts = {tuple(record["accounts"]) for record in matches}
            if len(accounts) != 1:
                conflicting += 1
                continue
            members.update(next(iter(accounts)))
            accepted.append(list(key))
        output.append({"sample_id": row["sample_id"], "matched_versions": accepted,
                       "conflicting_membership": conflicting,
                       "covered_by": [key for key, people in slots.items() if members & people]})
    return output


def bounds(joins):
    earlier = INITIAL.read(EMPTY_RESULTS)
    zeros = set(earlier["additional_common_negatives"]) | set(INITIAL.read(PNPM_RESULTS)["verified_empty_roots"])
    comparisons = INITIAL.read(PAIRS)["comparisons"]
    evaluated = {}
    for variant, data in comparisons.items():
        required = {"control"} if variant == "identical_control" else {"name", variant}
        positives = {r["sample_id"] for r in joins if required.issubset(r["covered_by"])}
        assert not positives & zeros
        resolved = 0
        deltas = []
        for row in data["projects"]:
            sid, feasible = row["sample_id"], row["feasible"]
            if sid in zeros or sid in positives:
                observed = [1, 1] if sid in positives else [0, 0]
                assert observed in feasible and len(feasible) > 1
                feasible = [observed]
            resolved += len(feasible) == 1
            deltas.append({version - name for name, version in feasible})
        n = len(deltas)
        results = {
            "resolved_pairs": resolved,
            "turnover_bounds": [sum(0 not in d for d in deltas) / n, sum(d != {0} for d in deltas) / n],
            "net_bounds": [sum(min(d) for d in deltas) / n, sum(max(d) for d in deltas) / n],
        }
        previous = earlier["comparisons"][variant]
        assert resolved == previous["resolved_pairs"] + len(positives)
        for key in ("turnover_bounds", "net_bounds"):
            lo, hi = results[key]
            assert previous[key][0] <= lo <= hi <= previous[key][1]
        evaluated[variant] = results
    return evaluated


def sources():
    paths = (TRACES, PAIRS, REPLAY, EMPTY_RESULTS, PNPM_RESULTS,
             INITIAL.ROOT / "scripts/check_yunohost_bun_direct.py")
    return {str(path.relative_to(INITIAL.ROOT)): INITIAL.sha(path) for path in paths}


def verify():
    result = INITIAL.read(RESULTS)
    assert result["input_sha256"] == sources()
    rows = result["observations"]
    assert [row["sample_id"] for row in rows] == candidates()
    assert evaluate(rows) == result["registry_join"]
    assert bounds(result["registry_join"]) == result["comparisons"]
    table = (INITIAL.ROOT / "manuscript_q1/tables/yunohost_consumer_holdout_table.tex").read_text()
    columns = [result["comparisons"][f"version_{i}"] for i in range(1, 4)]
    counts = " & ".join(str(row["resolved_pairs"]) for row in columns)
    assert f"Bun follow-up resolved pairs & {counts}" + r"\\" in table
    for label, field in ((r"Bun follow-up turnover (\%)", "turnover_bounds"),
                         ("Bun follow-up net change (pp)", "net_bounds")):
        expected = [f"$[{100*lo:.1f},{100*hi:.1f}]$" for lo, hi in (r[field] for r in columns)]
        assert " & ".join([label, *expected]) + r"\\" in table
    print("Reproduced the Bun direct-dependency follow-up and combined bounds")


def score():
    RUN.mkdir(exist_ok=True)
    source = INITIAL.read(EMPTY_RESULTS)
    assert not set(candidates()) & set(source["additional_common_negatives"])
    frame = {row["frame_id"]: row for row, _ in INITIAL.inputs()}
    observations = [parse(frame[sid]) for sid in candidates()]
    result = evaluate(observations)
    INITIAL.write(RESULTS, {
        "design": "Post hoc, positive-only Bun direct paths in the six unresolved Bun projects. "
                  "Use text lockfiles v1 or v2, regular root declarations, no overrides or "
                  "patches, matching same-name versions, and matching SHA-512 in retained npm "
                  "receipts. Require agreement of portfolio membership across matching receipts.",
        "input_sha256": sources(),
        "observations": observations, "registry_join": result, "comparisons": bounds(result),
    })
    print(dict(Counter(r["status"] for r in observations)))
    for row in result:
        print(row["sample_id"], len(row["matched_versions"]), row["covered_by"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    stages = {"score": score, "verify": verify}
    parser.add_argument("stage", choices=stages)
    stages[parser.parse_args().stage]()
