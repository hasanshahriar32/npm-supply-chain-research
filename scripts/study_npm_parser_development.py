"""Evaluate the wider npm witness extractor on the previously inspected 40-project pilot."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import gzip
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from urllib.parse import quote

from consumer_holdout import COMMIT, REPO, ROOT, fetch, sha, write
from evaluate_consumer_pilot import root_lock, load

PILOT = ROOT / "research/consumer_pilot"
OUT = ROOT / "research/consumer_parser_development"
WORKSPACE_MATCHER = """
const fs = require('node:fs');
const {workspaceLocations} = require(process.argv[1]);
const manifest = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const lock = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
console.log(JSON.stringify(lock?.packages?.[''] ? workspaceLocations(manifest, lock) : null));
"""


def workspace_locations(manifest, lock):
    proc = subprocess.run(["node", "-e", WORKSPACE_MATCHER, str(ROOT / "scripts/consumer_npm_development.cjs"),
                           str(manifest), str(lock)], check=True, capture_output=True, text=True, timeout=30)
    return json.loads(proc.stdout) or []


def selected_inputs(row):
    if not COMMIT.fullmatch(row.get("commit_sha") or ""):
        return None, None, "missing_commit"
    manifest = row["files"]["package.json"]
    if manifest["status"] != "retained":
        return None, None, "missing_root_manifest"
    folder = PILOT / "projects" / row["sample_id"]
    for name, info in row["files"].items():
        if info["status"] == "retained" and info["sha256"] != sha(folder / name):
            raise ValueError(f"Source checksum mismatch for {row['sample_id']} {name}")
    name, reason = root_lock(row["files"], load(folder / "package.json"))
    return folder, name, reason


def workspaces(row, folder, name, acquire):
    locations = workspace_locations(folder / "package.json", folder / name)
    repo = row["repository"]
    if not REPO.fullmatch(repo) or ".." in repo.split("/"):
        raise ValueError("Invalid repository in retained pilot")
    base = OUT / "private" / row["sample_id"]
    records = []
    paths = {}
    for location in locations:
        key = quote(location, safe="/")
        url = f"https://raw.githubusercontent.com/{repo}/{row['commit_sha']}/{key}/package.json"
        local = base / location / "package.json"
        ledger = local.with_suffix(".receipt.json")
        if not ledger.exists() and acquire:
            record, body = fetch(url, 512_000)
            local.parent.mkdir(parents=True, exist_ok=True)
            if body is not None:
                local.write_bytes(body)
            write(ledger, record)
        if not ledger.exists():
            records.append({"location": location, "url": url, "status": "uncollected"})
            continue
        record = load(ledger)
        if record["url"] != url:
            raise ValueError("Workspace receipt refers to a different commit or path")
        if record["status"] == "retained":
            if sha(local) != record["sha256"]:
                raise ValueError("Workspace manifest checksum mismatch")
            paths[location] = local
        records.append({"location": location, **record})
    return records, paths


def run_one(row, acquire):
    folder, lock, reason = selected_inputs(row)
    key = {"sample_id": row["sample_id"], "commit_sha": row.get("commit_sha")}
    if reason:
        return {**key, "status": reason, "workspace_requests": [], "importers": []}
    records, paths = workspaces(row, folder, lock, acquire)
    with tempfile.TemporaryDirectory(prefix="consumer-npm-input-") as tmp:
        for name in ("package.json", lock):
            shutil.copyfile(folder / name, Path(tmp) / name)
        for location, source in paths.items():
            dest = Path(tmp) / location / "package.json"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
        proc = subprocess.run(["node", str(ROOT / "scripts/consumer_npm_development.cjs"), tmp, lock],
                              check=True, capture_output=True, text=True, timeout=90)
    return {**key, "lockfile": lock, "workspace_requests": records, **json.loads(proc.stdout)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch-workspaces", action="store_true")
    args = parser.parse_args()
    subjects = load(PILOT / "observations.json")["projects"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(lambda row: run_one(row, args.fetch_workspaces), subjects))
    witnessed = [r for r in rows if any(i["witnesses"] for i in r["importers"])]
    summary = {
        "cohort": "previously inspected development pilot",
        "input_sha256": sha(PILOT / "observations.json"), "projects": len(rows),
        "status": dict(Counter(r["status"] for r in rows)),
        "projects_with_public_paths": sum(any(w["public_npm_tarball"] for i in r["importers"] for w in i["witnesses"]) for r in rows),
        "projects_with_any_paths": len(witnessed),
        "projects_with_nonroot_paths": sum(any(i["importer"] and i["witnesses"] for i in r["importers"]) for r in rows),
        "legacy_root_positive_in_same_projects": sum(r.get("legacy_root_witnesses", 0) > 0 for r in rows),
        "project_ids_with_paths": [r["sample_id"] for r in witnessed],
        "workspace_manifest_states": dict(Counter(t["status"] for r in rows for t in r["workspace_requests"])),
        "paths_using_changed_range": sum(any(e["effective"] != e["nominal"] for e in w["path"])
                                         for r in rows for i in r["importers"] for w in i["witnesses"]),
    }
    payload = json.dumps(rows, separators=(",", ":"), ensure_ascii=False).encode()
    (OUT / "npm_projects.json.gz").write_bytes(gzip.compress(payload, mtime=0))
    write(OUT / "npm_summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
