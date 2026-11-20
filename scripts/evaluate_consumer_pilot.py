"""Replay a fixed paired comparison on acquired public consumer metadata, offline."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "research/consumer_pilot"
OUT = ROOT / "research/consumer_evaluation"
REV = ROOT / "manuscript_q1/results/revision_validation"
INCIDENCE = REV / "replication/incidence.json"
FROZEN = "74184752cc97d6ff0dcec3ae8ba39847d7303a54557be982b387235202215bc8"


def load(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def root_lock(files, manifest):
    manager = manifest.get("packageManager")
    if manager and (not isinstance(manager, str) or manager.split("@")[0] != "npm"):
        return None, "other_declared_manager"
    for name in ["npm-shrinkwrap.json", "package-lock.json"]:
        record = files[name]
        if record["status"] == "retained":
            if not manager:
                others = [files[k] for k in ("pnpm-lock.yaml", "yarn.lock")]
                if any(r["status"] == "retained" for r in others):
                    return None, "multiple_managers"
                if not all(r.get("http_status") == 404 for r in others):
                    return None, "unknown_other_manager_file"
            return name, None
        if record.get("http_status") != 404:
            return None, "unknown_npm_lockfile"
    return None, "no_root_npm_lockfile"


def compare(project, memberships, orders):
    files = project["files"]
    if not project.get("commit_sha"):
        return {"status": "no_commit"}
    if files["package.json"]["status"] != "retained":
        status = "no_root_manifest" if files["package.json"].get("http_status") == 404 else "unknown_root_manifest"
        return {"status": status}
    source = PILOT / "projects" / project["sample_id"]
    for name, rec in files.items():
        if rec["status"] == "retained" and sha(source / name) != rec["sha256"]:
            raise ValueError(f"Checksum mismatch for {project['sample_id']} {name}")
    try:
        manifest = load(source / "package.json")
    except (UnicodeDecodeError, ValueError):
        return {"status": "invalid_root_manifest"}
    if not isinstance(manifest, dict):
        return {"status": "invalid_root_manifest"}
    lock, reason = root_lock(files, manifest)
    if reason:
        return {"status": reason}
    with tempfile.TemporaryDirectory(prefix="consumer-virtual-") as tmp:
        for name in ("package.json", lock):
            shutil.copyfile(source / name, Path(tmp) / name)
        proc = subprocess.run(
            ["node", str(ROOT / "scripts/compare_consumer_parsers.cjs"), shutil.which("npm"), tmp, lock],
            check=True, capture_output=True, text=True,
        )
    record = json.loads(proc.stdout)
    record["lockfile"] = lock
    if record["status"] != "compared":
        return record
    witnesses = record.pop("witnesses")
    supported = set()
    for witness in witnesses:
        key = (witness["package"], witness["version"])
        if witness["public_npm_tarball"] and memberships.get(key):
            supported.add(key)
    record["corroborated_distinct_versions"] = len({(w["package"], w["version"]) for w in witnesses})
    record["exact_joined_distinct_versions"] = len(supported)
    associated = set().union(*(memberships[key] for key in supported))
    record["documented_hit"] = {rule: bool(associated & accounts) for rule, accounts in orders.items()}
    # Keep one auditable example per evaluable project. No account identities.
    example = next((w for w in witnesses if w["public_npm_tarball"] and
                    (w["package"], w["version"]) in supported), next(iter(witnesses), None))
    if example:
        record["example_path"] = example["path"]
        record["example_joined"] = example["public_npm_tarball"] and (example["package"], example["version"]) in supported
    return record


def main():
    if sha(INCIDENCE) != FROZEN:
        raise ValueError("The October selection input differs from the protocol.")
    training = load(INCIDENCE)
    orders = {rep: {training["maintainers"][i] for i in training["orders_" + rep]["greedy_coverage"][:100]}
              for rep in ("name", "version")}
    if any(len(accounts) != 100 for accounts in orders.values()):
        raise ValueError("Expected two distinct 100-slot selections")
    memberships = {}
    for path in sorted((REV / "replication/observations").glob("metadata_*.json")):
        obs = load(path)
        key = (obs.get("requested_package"), obs.get("requested_version"))
        if obs.get("http_status") == 200 and key == (obs.get("name"), obs.get("version")):
            if key in memberships:
                raise ValueError(f"Duplicate metadata response for {key}")
            memberships[key] = set(obs["maintainers"])
    sample = load(PILOT / "sample.json")
    acquisition = load(PILOT / "observations.json")
    if sha(PILOT / "sample.json") != acquisition["sample_sha256"]:
        raise ValueError("Sample changed since acquisition")
    expected = {p["sample_id"]: p["repository"] for p in sample["projects"]}
    observed = {p["sample_id"]: p["repository"] for p in acquisition["projects"]}
    if expected != observed or len(expected) != 40 or len(acquisition["projects"]) != 40:
        raise ValueError("Incomplete or duplicate acquisitions")
    original = {e["repository"].casefold() for e in load(REV / "baseline_incidence.json")["endpoints"]}
    training_repos = {name.casefold() for name in training["repositories"]}
    cases = []
    for project in acquisition["projects"]:
        row = {"sample_id": project["sample_id"], "commit_sha": project.get("commit_sha"),
               "original_endpoint_overlap": project["repository"].casefold() in original,
               "training_endpoint_overlap": project["repository"].casefold() in training_repos}
        cases.append(row | compare(project, memberships, orders))
    rows = [row for row in cases if row["status"] == "compared"]
    cells = Counter()
    for row in rows:
        flags = row["documented_hit"]
        cells["both" if all(flags.values()) else "name_only" if flags["name"] else
              "version_only" if flags["version"] else "neither_documented"] += 1
    total_keys = ("custom_locations", "arborist_locations", "common_locations", "corroborated_paths",
                  "corroborated_distinct_versions", "exact_joined_distinct_versions")
    overlap = len(orders["name"] & orders["version"])
    result = {"cohort_size": len(cases), "frame_size": sample["frame_size"], "status_counts": Counter(r["status"] for r in cases),
              "frozen_input_sha256": FROZEN, "sample_sha256": acquisition["sample_sha256"],
              "observations_sha256": sha(PILOT / "observations.json"), "cases_compared": len(rows),
              "shared_selection_slots": overlap, "selection_jaccard": overlap / (200 - overlap),
              "training_metadata_exact_records": len(memberships),
              "original_endpoint_overlap": sum(r["original_endpoint_overlap"] for r in cases),
              "training_endpoint_overlap": sum(r["training_endpoint_overlap"] for r in cases),
              "consumers_with_path": sum(bool(r["corroborated_paths"]) for r in rows),
              "consumers_with_exact_join": sum(bool(r["exact_joined_distinct_versions"]) for r in rows),
              "paired_documented_cells": {k: cells[k] for k in ("both","name_only","version_only","neither_documented")},
              "project_level_totals": {k: sum(r[k] for r in rows) for k in total_keys}}
    for name, data in [("reviews", cases), ("summary", result)]:
        (OUT / (name + ".json")).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
