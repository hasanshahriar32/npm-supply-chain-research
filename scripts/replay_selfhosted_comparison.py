#!/usr/bin/env python3
"""Reproduce the frozen Awesome-Selfhosted comparisons and scope sensitivity."""
import argparse
import gzip
import json
import subprocess

import consumer_holdout as heldout
from replay_yunohost_budgets import BUDGETS, PROJECTION as ORDERS_SOURCE
from replay_yunohost_consumer_results import read_graphs
from study_pnpm_parser_development import YAML_READER
from study_yunohost_empty_pnpm_roots import unique_object

ROOT = heldout.ROOT
RUN = heldout.BASE / "runs/selfhosted-v1"
CHECK = heldout.BASE / "runs/selfhosted-sensitivity"
PROJECTION = CHECK / "projection.json.gz"
RESULT = CHECK / "results.json"
INPUTS = ("protocol.json", "paths.json", "observations.json", "registry_manifest.json", "results.json")
PRODUCTION = ("dependencies", "optionalDependencies", "peerDependencies",
              "bundleDependencies", "bundledDependencies")


def source_hashes():
    return {name: heldout.sha(RUN / name) for name in INPUTS}


def empty_roots(protocol, references, original):
    verdicts = original["comparisons"]["version_1"]["projects"]
    candidates = []
    for entry, receipt, verdict in zip(protocol["projects"], references, verdicts, strict=True):
        sid = entry["sample_id"]
        assert sid == receipt["sample_id"] == verdict["sample_id"]
        manifest_receipt = receipt["files"].get("package.json", {})
        if len(verdict["feasible"]) == 1 or manifest_receipt.get("status") != "retained":
            continue
        folder = heldout.check_observation(RUN, receipt, entry, protocol)
        manifest = json.loads((folder / "package.json").read_text(), object_pairs_hook=unique_object)
        if any(manifest.get(key) for key in (*PRODUCTION, "workspaces")):
            continue
        manager = manifest.get("packageManager", "").partition("@")[0]
        locks = {name: item.get("http_status") for name, item in receipt["files"].items() if name != "package.json"}
        development = manifest.get("devDependencies", {})
        candidate = {"sample_id": sid, "commit": receipt["commit_sha"], "manager": manager,
                     "manifest_sha256": manifest_receipt["sha256"], "lock_receipts": locks,
                     "root_development_count": len(development),
                     "conclusion": "unresolved"}
        if set(locks.values()) == {404} and manager in ("", "npm", "pnpm", "yarn", "bun"):
            candidate["conclusion"] = "empty_manifest_no_root_lock"
        elif locks["pnpm-lock.yaml"] == 200 and manager in ("", "pnpm") and all(
                status == 404 for name, status in locks.items() if name != "pnpm-lock.yaml"):
            parsed = subprocess.run(["ruby", "-rpsych", "-rjson", "-e", YAML_READER],
                                    input=(folder / "pnpm-lock.yaml").read_text(), text=True,
                                    capture_output=True, timeout=45)
            if not parsed.returncode:
                lock = json.loads(parsed.stdout)["project"]
                importers = lock.get("importers", {})
                importer = importers.get(".")
                if str(lock.get("lockfileVersion")) == "9.0" and isinstance(importer, dict):
                    dev_lock = {key: value.get("specifier") for key, value in importer.get("devDependencies", {}).items()}
                    candidate["child_importers"] = len(importers) - 1
                    candidate["lock_sha256"] = receipt["files"]["pnpm-lock.yaml"]["sha256"]
                    if not any(importer.get(key) for key in PRODUCTION) and development == dev_lock:
                        candidate["conclusion"] = "empty_pnpm_root"
        elif locks["package-lock.json"] == 200 and manager in ("", "npm") and all(
                status == 404 for name, status in locks.items() if name != "package-lock.json"):
            lock = json.loads((folder / "package-lock.json").read_text(), object_pairs_hook=unique_object)
            importer = lock.get("packages", {}).get("")
            candidate["lock_sha256"] = receipt["files"]["package-lock.json"]["sha256"]
            if (lock.get("lockfileVersion") in (2, 3) and isinstance(importer, dict)
                    and not any(importer.get(key) for key in (*PRODUCTION, "workspaces"))
                    and development == importer.get("devDependencies", {})
                    and all(key not in obj or key not in manifest or obj[key] == manifest[key]
                            for obj in (lock, importer) for key in ("name", "version"))):
                candidate["conclusion"] = "empty_npm_root"
        candidates.append(candidate)
    return candidates


def export():
    training = heldout.read(heldout.INCIDENCE)
    assert heldout.sha(heldout.INCIDENCE) == heldout.FROZEN
    protocol = heldout.protocol_for(RUN)
    artifact = heldout.path_artifact(RUN)
    index = heldout.membership_index(RUN, [tuple(key) for key in artifact["version_keys"]], protocol)
    orders = read_graphs(ORDERS_SOURCE)["orders"]
    version = sorted(orders["version"][:5])
    alternatives = [version, *(v for v in heldout.optimal_sets(training["version_masks"], 5) if v != version)]
    portfolios = {"name": sorted(orders["name"][:5]), **{f"version_{i}": v for i, v in enumerate(alternatives, 1)},
                  "control": sorted(training["orders_name"]["greedy_coverage"][:100])}
    selected = {i for v in [*orders.values(), *portfolios.values()] for i in v}
    account_indices = {training["maintainers"][i]: i for i in selected}
    memberships = [[j, sorted(account_indices[a] for a in index[tuple(key)] if a in account_indices)]
                   for j, key in enumerate(artifact["version_keys"]) if tuple(key) in index]
    candidates = empty_roots(protocol, heldout.read(RUN / "observations.json"), heldout.read(RUN / "results.json"))
    data = {"inputs": source_hashes(), "order_source_sha256": heldout.sha(ORDERS_SOURCE),
            "portfolios": portfolios, "observed_memberships": memberships, "empty_root_checks": candidates}
    CHECK.mkdir(exist_ok=True)
    PROJECTION.write_bytes(gzip.compress(json.dumps(data, separators=(",", ":")).encode(), mtime=0))
    heldout.write(RESULT, score())


def score():
    data = read_graphs(PROJECTION)
    original = heldout.read(RUN / "results.json")
    protocol = heldout.read(RUN / "protocol.json")
    assert data["inputs"] == source_hashes() and data["order_source_sha256"] == heldout.sha(ORDERS_SOURCE)
    orders = read_graphs(ORDERS_SOURCE)["orders"]
    portfolios = data["portfolios"]
    assert {k: heldout.digest(json.dumps(v).encode()) for k, v in portfolios.items()} == protocol["portfolio_sha256"]
    assert all(sorted(orders[k][:5]) == portfolios[name] for k, name in (("name", "name"), ("version", "version_1")))
    selected = set().union(*orders.values(), *portfolios.values())
    artifact = heldout.path_artifact(RUN)
    keys = artifact["version_keys"]
    index = {}
    for row, members in data["observed_memberships"]:
        assert 0 <= row < len(keys) and set(members) <= selected
        index[tuple(keys[row])] = set(members)
    assert len(index) == len(data["observed_memberships"]) == original["versions_with_observed_membership"]

    traces = artifact["projects"]
    for key in original["comparisons"]:
        name = "control" if key == "identical_control" else "name"
        version = "control" if key == "identical_control" else key
        combined = heldout.compare_portfolios(traces, index, set(portfolios[name]), set(portfolios[version]))
        assert combined == original["comparisons"][key]

    unresolved = {v["sample_id"] for v in original["comparisons"]["version_1"]["projects"] if len(v["feasible"]) > 1}
    accepted = {r["sample_id"]: r["conclusion"] for r in data["empty_root_checks"] if r["conclusion"] != "unresolved"}
    assert accepted.keys() <= unresolved
    empty_trace = {"status": "compared", "custom_status": "ok", "arborist_locations": 0, "custom_locations": 0,
                   "corroborated_paths": 0}
    expanded = [{**empty_trace, "sample_id": t["sample_id"]} if t["sample_id"] in accepted else t for t in traces]
    budgets = {}
    for k in BUDGETS:
        name, version = (set(orders[key][:k]) for key in ("name", "version"))
        row = heldout.compare_portfolios(expanded, index, name, version)
        budgets[str(k)] = {**{field: row[field] for field in ("resolved_pairs", "complete_reference_turnover_bounds",
                                                               "complete_reference_net_bounds")},
                           "confirmed_differences": {p["sample_id"]: p["feasible"][0] for p in row["projects"]
                                                     if len(p["feasible"]) == 1 and sum(p["feasible"][0]) == 1}}
    return {"denominator": original["denominator"], "original_comparisons_reproduced": len(original["comparisons"]),
            "empty_roots": accepted, "budgets": budgets}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--export", action="store_true")
    if cli.parse_args().export:
        export()
    else:
        actual = score()
        assert actual == heldout.read(RESULT)
        print(f"Reproduced all original Awesome-Selfhosted pairs, {len(actual['empty_roots'])} root zeros and six budgets")
