#!/usr/bin/env python3
"""Freeze, acquire and evaluate a bounded npm consumer study using public metadata."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import itertools
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

from collect_consumer_pilot import digest, now, read, write
from evaluate_consumer_pilot import INCIDENCE, FROZEN, root_lock, sha

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/consumer_holdout"
PILOT = ROOT / "research/consumer_pilot/sample.json"
ORIGINAL = ROOT / "manuscript_q1/results/revision_validation/baseline_incidence.json"
PATHS = ("package.json", "npm-shrinkwrap.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
         "bun.lock", "bun.lockb")
SEM_ID = re.compile(r"^(?:@[a-z0-9~][a-z0-9._~-]*/)?[a-z0-9~][a-z0-9._~-]*$", re.I)
VERSION = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(url, cap):
    requested = {"url": url, "observed_at_utc": now()}
    try:
        with build_opener(NoRedirect()).open(Request(url, headers={"User-Agent": "npm-consumer-study/1"}), timeout=15) as response:
            if response.geturl() != url:
                raise ValueError("Unexpected response URL")
            body = response.read(cap + 1)
            if len(body) > cap:
                return {**requested, "status": "above_size_cap", "http_status": response.status}, None
            return {**requested, "status": "retained", "http_status": response.status,
                    "sha256": digest(body), "bytes": len(body)}, body
    except HTTPError as exc:
        return {**requested, "status": "http_error", "http_status": exc.code}, None
    except (URLError, OSError, TimeoutError) as exc:
        return {**requested, "status": "transport_error", "error": type(exc).__name__}, None


def hash_paths():
    names = ["consumer_holdout.py", "collect_consumer_pilot.py", "evaluate_consumer_pilot.py",
             "compare_consumer_parsers.cjs", "consumer_lock_evidence.cjs"]
    return {f"scripts/{name}": sha(ROOT / "scripts" / name) for name in names}


def optimal_sets(masks, budget):
    scores = [int(value, 16).bit_count() for value in masks]
    cutoff = sorted(scores, reverse=True)[budget - 1]
    higher = [i for i, score in enumerate(scores) if score > cutoff]
    tied = [i for i, score in enumerate(scores) if score == cutoff]
    return [sorted(higher + list(part)) for part in itertools.combinations(tied, budget - len(higher))]


def freeze(run):
    if (run / "protocol.json").exists():
        raise ValueError("This run already has a frozen protocol")
    if sha(INCIDENCE) != FROZEN:
        raise ValueError("Training input differs from the audited snapshot")
    pilot = read(PILOT)
    graph = read(INCIDENCE)
    excluded = {row["repository"].lower() for row in pilot["projects"]}
    excluded.update(name.lower() for name in graph["repositories"])
    excluded.update(row["repository"].lower() for row in read(ORIGINAL)["endpoints"])
    eligible = sorted(set(pilot["repositories"]) - excluded)
    if not eligible or any(not REPO.fullmatch(repo) or ".." in repo.split("/") for repo in eligible):
        raise ValueError("Invalid or empty frame")
    names, versions = [optimal_sets(graph[f"{rep}_masks"], 5) for rep in ("name", "version")]
    baseline = sorted(graph["orders_name"]["exact_union"][:5])
    primary = sorted(graph["orders_version"]["exact_union"][:5])
    if names != [baseline] or primary not in versions or any(len(set(baseline) & set(v)) != 3 for v in versions):
        raise ValueError("Expected one name and three version optima with three slots shared")
    choices = [primary] + [v for v in versions if v != primary]
    control = sorted(graph["orders_name"]["greedy_coverage"][:100])
    if control != sorted(graph["orders_version"]["greedy_coverage"][:100]):
        raise ValueError("Expected a common greedy control")
    run.mkdir(parents=True, exist_ok=True)
    # Record fingerprints of portfolios, never export a ranked list from this study.
    portfolios = {"name": baseline, **{f"version_{i}": v for i, v in enumerate(choices, 1)}, "control": control}
    fingerprints = {key: digest(json.dumps(value).encode()) for key, value in portfolios.items()}
    protocol = {
        "frozen_utc": now(), "training_sha256": FROZEN, "pilot_sample_sha256": sha(PILOT),
        "original_incidence_sha256": sha(ORIGINAL), "code_sha256": hash_paths(),
        "portfolio_sha256": fingerprints, "primary": "name vs version_1, frozen additive orders at five slots",
        "unit": "one repository in the pinned self-hosted frame, excluding the feasibility sample and known training endpoint keys",
        "pin_method": "public default HEAD observed during collection; no retrospective commit-time or release-authority interpretation",
        "window_hours": 24, "root_paths": list(PATHS),
        "dependency_scope": "mandatory production npm dependencies of the root importer; unsupported manager/workspace/override cases retained as unknown",
        "registry_reference": "exact published public version metadata captured for every agreed public package/version, prior to matching portfolios",
        "inference": "finite frame descriptive documented coverage and joint feasible bounds; transport to a second frame is a separate study",
        "original_frame": len(pilot["repositories"]),
        "excluded_frame_keys": sorted(set(pilot["repositories"]) & excluded),
        "projects": [{"sample_id": f"H{i:03}", "repository": name} for i, name in enumerate(eligible, 1)],
    }
    write(run / "protocol.json", protocol)
    print(f"Frozen {len(eligible)} held-out frame entries. Protocol SHA-256 {sha(run / 'protocol.json')}")
    return protocol


def protocol_for(run):
    protocol = read(run / "protocol.json")
    if (protocol["code_sha256"] != hash_paths() or protocol["training_sha256"] != sha(INCIDENCE)
            or protocol["pilot_sample_sha256"] != sha(PILOT) or protocol["original_incidence_sha256"] != sha(ORIGINAL)):
        raise ValueError("A frozen code or input hash changed")
    return protocol


def in_window(value, protocol):
    start = datetime.fromisoformat(protocol["frozen_utc"])
    stamp = datetime.fromisoformat(value)
    return start <= stamp <= start + timedelta(hours=protocol["window_hours"])


def pin_project(run, row):
    folder = run / "private" / "projects" / row["sample_id"]
    record = folder / "observation.json"
    if record.exists():
        return read(record)
    folder.mkdir(parents=True, exist_ok=True)
    repo = row["repository"]
    url = f"https://github.com/{repo}.git"
    observed = {**row, "git_url": url, "pin_observed_at_utc": now(), "commit_sha": None, "files": {}}
    try:
        proc = subprocess.run(["git", "-c", "http.followRedirects=false", "-c", "credential.helper=",
                               "ls-remote", "--exit-code", url, "HEAD"], text=True, capture_output=True,
                              timeout=25, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
        fields = proc.stdout.strip().split()
        if proc.returncode == 0 and len(fields) == 2 and fields[1] == "HEAD" and COMMIT.fullmatch(fields[0]):
            observed["commit_sha"] = fields[0]
        else:
            observed["pin_error"] = proc.returncode
    except subprocess.TimeoutExpired:
        observed["pin_error"] = "timeout"
    if observed["commit_sha"]:
        for name in PATHS:
            rec, body = fetch(file_url(observed, name), 6 * 1024 * 1024)
            if body is not None:
                (folder / name).write_bytes(body)
            observed["files"][name] = rec
    write(record, observed)
    return observed


def file_url(project, name):
    return f"https://raw.githubusercontent.com/{project['repository']}/{project['commit_sha']}/{name}"


def check_observation(run, observed, row, protocol):
    if any(observed.get(k) != row[k] for k in ("sample_id", "repository")):
        raise ValueError("Observation differs from frozen project")
    if observed["git_url"] != f"https://github.com/{row['repository']}.git" or not in_window(observed["pin_observed_at_utc"], protocol):
        raise ValueError("HEAD observation has an invalid origin or timestamp")
    files = observed["files"]
    if observed["commit_sha"] is None:
        if files or "pin_error" not in observed:
            raise ValueError("Invalid unresolved HEAD observation")
        return None
    if not COMMIT.fullmatch(observed["commit_sha"]) or set(files) != set(PATHS):
        raise ValueError("Invalid commit or incomplete file ledger")
    folder = run / "private" / "projects" / row["sample_id"]
    for name, item in files.items():
        if item["url"] != file_url(observed, name) or not in_window(item["observed_at_utc"], protocol):
            raise ValueError("File ledger URL or time is inconsistent")
        if item["status"] == "retained" and (item["http_status"] != 200 or sha(folder / name) != item["sha256"]):
            raise ValueError("Downloaded bytes differ from observed evidence")
    return folder


def trace_project(run, observed, row, protocol):
    source = check_observation(run, observed, row, protocol)
    status = {"sample_id": row["sample_id"], "commit_sha": observed["commit_sha"]}
    if source is None:
        return {**status, "status": "unresolved_head"}
    files = observed["files"]
    if files["package.json"]["status"] != "retained":
        return {**status, "status": "manifest_404" if files["package.json"].get("http_status") == 404 else "manifest_unknown"}
    try:
        manifest = read(source / "package.json")
    except (ValueError, UnicodeDecodeError):
        return {**status, "status": "invalid_manifest"}
    if not isinstance(manifest, dict):
        return {**status, "status": "invalid_manifest"}
    if manifest.get("workspaces") is not None:
        return {**status, "status": "workspace_unsupported"}
    if not manifest.get("packageManager") and any(files[k].get("http_status") != 404 for k in ("bun.lock", "bun.lockb")):
        return {**status, "status": "bun_lock_or_unknown"}
    lock, reason = root_lock(files, manifest)
    if reason:
        return {**status, "status": reason}
    with tempfile.TemporaryDirectory(prefix="consumer-study-") as tmp:
        for name in ("package.json", lock):
            shutil.copyfile(source / name, Path(tmp) / name)
        proc = subprocess.run(["node", str(ROOT / "scripts/compare_consumer_parsers.cjs"),
                               shutil.which("npm"), tmp, lock, "--include-rejected"],
                              check=True, capture_output=True, text=True, timeout=60)
    return {**status, "lockfile": lock, **json.loads(proc.stdout)}


def version_keys(traces):
    return sorted({(w["package"], w["version"]) for r in traces for w in r.get("witnesses", [])
                   if w["public_npm_tarball"]})


def paths_stage(run, protocol):
    target = run / "paths.json"
    if target.exists():
        raise ValueError("Path observations are already sealed for this run")
    rows = protocol["projects"]
    with ThreadPoolExecutor(max_workers=5) as pool:
        observed = list(pool.map(lambda row: pin_project(run, row), rows))
    with ThreadPoolExecutor(max_workers=4) as pool:
        traced = list(pool.map(lambda args: trace_project(run, *args, protocol), zip(observed, rows)))
    write(run / "observations.json", observed)
    write(target, {"protocol_sha256": sha(run / "protocol.json"), "observations_sha256": sha(run / "observations.json"),
                   "projects": traced, "version_keys": version_keys(traced)})
    print(f"Sealed {len(traced)} projects and {len(version_keys(traced))} independent registry requests")


def registry_url(pkg, version):
    if not SEM_ID.fullmatch(pkg) or not VERSION.fullmatch(version):
        raise ValueError("Unsupported registry package or version identifier")
    return f"https://registry.npmjs.org/{quote(pkg, safe='')}/{quote(version, safe='')}"


def registry_record(run, item):
    package, version = item
    url = registry_url(package, version)
    target = run / "private" / "registry" / (digest(url.encode()) + ".json")
    if target.exists():
        return read(target)
    record, content = fetch(url, 4 * 1024 * 1024)
    record.update(package=package, version=version, membership_status="unresolved", accounts=[])
    if content is not None:
        try:
            doc = json.loads(content)
        except (UnicodeDecodeError, ValueError):
            doc = None
        if isinstance(doc, dict) and (doc.get("name"), doc.get("version")) == item:
            entries = doc.get("maintainers")
            if isinstance(entries, list) and all(isinstance(entry, dict) and isinstance(entry.get("name"), str) and
                                                 entry["name"] for entry in entries):
                record.update(membership_status="observed", accounts=sorted({entry["name"] for entry in entries}))
    write(target, record)
    return record


def path_artifact(run):
    artifact = read(run / "paths.json")
    if (artifact["protocol_sha256"] != sha(run / "protocol.json")
            or artifact["observations_sha256"] != sha(run / "observations.json")
            or [tuple(v) for v in artifact["version_keys"]] != version_keys(artifact["projects"])):
        raise ValueError("Path hashes or the frozen registry queue do not match")
    return artifact


def registry_stage(run):
    if (run / "registry_manifest.json").exists():
        raise ValueError("Reference memberships are already sealed")
    keys = version_keys(path_artifact(run)["projects"])
    (run / "private" / "registry").mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(lambda key: registry_record(run, key), keys))
    write(run / "private" / "memberships.json", records)
    write(run / "registry_manifest.json", {
        "paths_sha256": sha(run / "paths.json"), "memberships_sha256": sha(run / "private" / "memberships.json"),
        "requests": len(keys), "states": dict(Counter(record["membership_status"] for record in records)),
        "sealed_at_utc": now()})
    print(f"Sealed {len(keys)} exact-version metadata observations")


def membership_index(run, keys, protocol):
    seal = read(run / "registry_manifest.json")
    path = run / "private" / "memberships.json"
    if seal["paths_sha256"] != sha(run / "paths.json") or seal["memberships_sha256"] != sha(path):
        raise ValueError("Reference membership checksum failure")
    records = read(path)
    if [(record["package"], record["version"]) for record in records] != keys:
        raise ValueError("Registry reference is incomplete or differs from the requested queue")
    result = {}
    for item, key in zip(records, keys, strict=True):
        if item["url"] != registry_url(*key) or not in_window(item["observed_at_utc"], protocol):
            raise ValueError("Registry reference origin or time does not match the protocol")
        if item["membership_status"] == "observed":
            result[key] = set(item["accounts"])
    return result


def classify(trace, index, name, version):
    witnesses = trace.get("witnesses", [])
    witness_keys = {(w["package"], w["version"]) for w in witnesses if w["public_npm_tarball"]}
    observed = set().union(*(index.get(key, set()) for key in witness_keys))
    documented = [bool(observed & name), bool(observed & version)]
    complete = (trace["status"] == "compared" and trace["custom_status"] == "ok"
                and trace["custom_locations"] == trace["arborist_locations"] == trace["corroborated_paths"]
                and all(w["public_npm_tarball"] for w in witnesses) and witness_keys <= index.keys())
    feasible = [[a, b] for a, b in itertools.product((0, 1), repeat=2)
                if a >= documented[0] and b >= documented[1]
                and (not complete or [a, b] == documented)
                and (name != version or a == b)]
    return documented, feasible


def compare_portfolios(traces, index, name, version):
    cells = Counter()
    bounds = [0, 0, 0, 0]
    ledger = []
    for trace in traces:
        documented, feasible = classify(trace, index, name, version)
        cells["".join(str(int(flag)) for flag in documented)] += 1
        changes = [abs(v - n) for n, v in feasible]
        effects = [v - n for n, v in feasible]
        limits = [min(changes), max(changes), min(effects), max(effects)]
        bounds = [total + value for total, value in zip(bounds, limits)]
        ledger.append({"sample_id": trace["sample_id"], "documented": documented, "feasible": feasible})
    size = len(traces)
    return {"documented_cells": {label: cells[label] for label in ("00", "01", "10", "11")},
            "documented_turnover": (cells["01"] + cells["10"]) / size,
            "documented_net": (cells["01"] - cells["10"]) / size,
            "complete_reference_turnover_bounds": [x / size for x in bounds[:2]],
            "complete_reference_net_bounds": [x / size for x in bounds[2:]],
            "resolved_pairs": sum(len(r["feasible"]) == 1 for r in ledger), "projects": ledger}


def score(run, protocol):
    artifact = path_artifact(run)
    graph = read(INCIDENCE)
    keys = version_keys(artifact["projects"])
    index = membership_index(run, keys, protocol)
    observed = read(run / "observations.json")
    traces = artifact["projects"]
    if not (len(observed) == len(traces) == len(protocol["projects"])):
        raise ValueError("Missing frame rows in the assessment")
    for row, pin, trace in zip(protocol["projects"], observed, traces, strict=True):
        check_observation(run, pin, row, protocol)
        if [trace["sample_id"], trace["commit_sha"]] != [row["sample_id"], pin["commit_sha"]]:
            raise ValueError("Trace refers to a different observed project")
    name = sorted(graph["orders_name"]["exact_union"][:5])
    version = sorted(graph["orders_version"]["exact_union"][:5])
    alternatives = [version] + [v for v in optimal_sets(graph["version_masks"], 5) if v != version]
    same = sorted(graph["orders_name"]["greedy_coverage"][:100])
    def accounts(slots):
        return {graph["maintainers"][i] for i in slots}

    comparisons = {}
    for i, alternative in enumerate(alternatives, 1):
        comparisons[f"version_{i}"] = compare_portfolios(traces, index, accounts(name), accounts(alternative))
    comparisons["identical_control"] = compare_portfolios(traces, index, accounts(same), accounts(same))
    result = {
        "denominator": len(traces), "protocol_sha256": sha(run / "protocol.json"),
        "registry_manifest_sha256": sha(run / "registry_manifest.json"),
        "project_status": dict(Counter(r["status"] for r in traces)), "public_versions": len(keys),
        "versions_with_observed_membership": len(index), "comparisons": comparisons}
    write(run / "results.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "comparisons"}, indent=2))
    print(json.dumps({k: v for k, v in comparisons["version_1"].items() if k != "projects"}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "paths", "registry", "score"))
    parser.add_argument("run", help="Run identifier, such as selfhosted-v1")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.run):
        parser.error("Use lowercase letters, digits and hyphens for the run identifier")
    run = BASE / "runs" / args.run
    if args.action == "freeze":
        freeze(run)
        return
    protocol = protocol_for(run)
    if args.action in ("paths", "registry") and not in_window(now(), protocol):
        parser.error("Collection window expired. Freeze a new run before making new requests.")
    if args.action == "paths":
        paths_stage(run, protocol)
    elif args.action == "registry":
        registry_stage(run)
    else:
        score(run, protocol)


if __name__ == "__main__":
    main()
