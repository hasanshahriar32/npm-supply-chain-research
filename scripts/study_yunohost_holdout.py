"""Freeze and score the YunoHost root-importer validation study."""
import argparse
import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import gzip
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from collect_yunohost_observations import url_for
from consumer_holdout import ROOT, INCIDENCE, FROZEN, now, read, sha, write, digest, optimal_sets
from study_npm_parser_development import workspace_locations
from study_pnpm_parser_development import root_record
from verify_pnpm_registry_integrity import sha512_values
from verify_yunohost_root_evidence import verify

BASE = ROOT / "research/consumer_parser_development"
CAPTURE = BASE / "private/yunohost_root_evidence/capture"
RUN = ROOT / "research/consumer_holdout/runs/yunohost-v2"
PRIVATE = RUN / "private"
SOURCES = ("study_yunohost_holdout.py", "collect_yunohost_observations.py", "consumer_holdout.py",
           "consumer_lock_evidence.cjs", "consumer_npm_development.cjs", "consumer_pnpm_development.cjs",
           "study_pnpm_parser_development.py", "study_npm_parser_development.py",
           "verify_yunohost_root_evidence.py", "verify_pnpm_registry_integrity.py")


def hashes():
    files = [ROOT / "scripts" / x for x in SOURCES]
    files += [INCIDENCE, BASE / "yunohost_root_frame.json", CAPTURE / "observations.json"]
    return {str(p.relative_to(ROOT)): sha(p) for p in files}


def frozen_portfolios():
    g = read(INCIDENCE)
    if sha(INCIDENCE) != FROZEN:
        raise ValueError("Unexpected training incidence")
    name = sorted(g["orders_name"]["exact_union"][:5])
    primary = sorted(g["orders_version"]["exact_union"][:5])
    variants = [primary] + [x for x in optimal_sets(g["version_masks"], 5) if x != primary]
    control = sorted(g["orders_name"]["greedy_coverage"][:100])
    if (optimal_sets(g["name_masks"], 5) != [name] or len(variants) != 3
            or any(len(set(name) & set(x)) != 3 for x in variants)
            or control != sorted(g["orders_version"]["greedy_coverage"][:100])):
        raise ValueError("Unexpected primary, tie or control portfolios")
    return g["maintainers"], {"name": name, **{f"version_{i}": x for i, x in enumerate(variants, 1)}, "control": control}


def freeze():
    RUN.mkdir(parents=True, exist_ok=True)
    PRIVATE.mkdir(exist_ok=True)
    protocol = RUN / "protocol.json"
    if protocol.exists():
        raise ValueError("Run already frozen")
    _, slots = frozen_portfolios()
    write(protocol, {"frozen_utc": now(), "inputs": hashes(),
                     "portfolio_fingerprints": {k: digest(json.dumps(v).encode()) for k, v in slots.items()},
                     "unit": "215 public upstream YunoHost projects with pinned and deduplicated root manifests",
                     "primary": "same frozen five-account additive name and version portfolios as first holdout",
                     "scope": "Committed root-importer mandatory production paths. Follow verified npm workspace links from root. "
                              "pnpm version 9 root paths are truncated at three edges. Separate workspace importers are diagnostics.",
                     "registry_identity": "Exact canonical public npm tarball path or exact SHA-512 equality to fresh public registry metadata",
                     "negatives": "Only npm paths evaluated completely under the supported root scope with all registry joins observed. "
                                  "A pnpm path can supply a positive witness. Other pnpm statuses and unsupported managers leave negatives unresolved.",
                     "estimands": "Paired documented gross and net coverage change on the full frame, with conservative incomplete-evidence bounds. "
                                  "No cross-frame generalization or sampling-based equivalence claim.",
                     "time": "Fixed consumer commits and a separate prospective registry observation queue. No historical publishing authority inferred."})
    print("Protocol frozen", sha(protocol))


def inputs():
    if read(RUN / "protocol.json")["inputs"] != hashes():
        raise ValueError("Input or code changed after study freeze")
    ledger, intake = verify(CAPTURE)
    return list(zip(ledger["projects"], intake["rows"], strict=True))


def workspace_queue():
    requests = []
    for row, state in inputs():
        if state["status"] != "npm_file_available":
            continue
        source = CAPTURE / "projects" / row["frame_id"]
        lock = choose_npm(row)
        if not lock:
            continue
        try:
            locations = workspace_locations(source / "package.json", source / lock)
        except (subprocess.SubprocessError, ValueError):
            continue
        for location in locations:
            requests.append({**{k: row[k] for k in ("frame_id", "repository", "commit_sha")}, "location": location})
    write(RUN / "workspaces_queue.json", {"stage": "workspaces", "protocol_sha256": sha(RUN / "protocol.json"),
                                         "requests": requests})
    print(len(requests), "pinned workspace manifests queued")


def read_collection(stage):
    queue = RUN / f"{stage}_queue.json"
    expected = read(queue)
    actual = read(PRIVATE / f"{stage}.json")
    if (expected["protocol_sha256"] != sha(RUN / "protocol.json")
            or actual["queue_sha256"] != sha(queue) or actual["stage"] != stage):
        raise ValueError("Collection does not match the frozen queue")
    observations = actual["observations"]
    for entry, row in zip(expected["requests"], observations, strict=True):
        if any(row[k] != v for k, v in entry.items()) or row["url"] != url_for(stage, entry):
            raise ValueError("Receipt identity mismatch")
    return observations


def choose_npm(row):
    files = row["files"]
    if files["npm-shrinkwrap.json"]["status"] == "retained":
        return "npm-shrinkwrap.json"
    if files["npm-shrinkwrap.json"].get("http_status") == 404 and files["package-lock.json"]["status"] == "retained":
        return "package-lock.json"
    return None


def npm_paths(row, source, receipts):
    lock = choose_npm(row)
    if not lock:
        return {"status": "ambiguous_npm_precedence", "witnesses": [], "complete": False}
    with tempfile.TemporaryDirectory(prefix="consumer-yuno-npm-") as tmp:
        dest = Path(tmp)
        for name in ("package.json", lock):
            shutil.copyfile(source / name, dest / name)
        for receipt in receipts:
            payload = base64.b64decode(receipt["manifest_base64"], validate=True)
            if digest(payload) != receipt["sha256"]:
                raise ValueError("Captured manifest bytes failed their checksum")
            p = dest / receipt["location"] / "package.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(payload)
        proc = subprocess.run(["node", str(ROOT / "scripts/consumer_npm_development.cjs"), tmp, lock],
                              check=True, capture_output=True, text=True, timeout=90)
    result = json.loads(proc.stdout)
    root = next((x for x in result["importers"] if x["importer"] == ""), None)
    return {
        "status": f"npm_{root['status']}" if root else "npm_unavailable",
        "witnesses": root["witnesses"] if root else [], "complete": bool(root and root["status"] == "ok"),
        "nonroot_importers_with_paths": sum(bool(x["importer"] and x["witnesses"]) for x in result["importers"]),
        "issues": dict(Counter(x["reason"] for x in root["issues"])) if root else {result.get("reason", "unknown"): 1},
    }


def assess(item, workspaces, pm):
    row, state = item
    sid = row["frame_id"]
    source = CAPTURE / "projects" / sid
    result = {"sample_id": sid, "commit_sha": row["commit_sha"], "status": state["status"],
              "complete": False, "witnesses": []}
    try:
        if state["status"] == "npm_file_available":
            return {**result, **npm_paths(row, source, workspaces.get(sid, []))}
        if state["status"] == "pnpm_file_available":
            parsed = root_record({**row, "sample_id": sid}, pm, folder=source)
            return {**result, **parsed, "status": "pnpm_" + parsed["status"]}
        return result
    except (subprocess.SubprocessError, UnicodeDecodeError, json.JSONDecodeError):
        return {**result, "status": state["status"].split("_")[0] + "_parser_error"}


def witnesses():
    rows = inputs()
    workspaces = {}
    for receipt in read_collection("workspaces"):
        if receipt["status"] == "retained":
            workspaces.setdefault(receipt["frame_id"], []).append(receipt)
    pm = shutil.which("pnpm")
    if not pm:
        raise RuntimeError("pnpm with offline lockfile list support is required")
    with ThreadPoolExecutor(max_workers=4) as pool:
        traces = list(pool.map(lambda item: assess(item, workspaces, pm), rows))
    path = RUN / "paths.json.gz"
    path.write_bytes(gzip.compress(json.dumps(traces, separators=(",", ":")).encode(), mtime=0))
    keys = set()
    for trace in traces:
        for w in trace["witnesses"]:
            if w["public_npm_tarball"] or sha512_values(w.get("registry_integrity_candidate")):
                item = {"package": w["package"], "version": w["version"]}
                try:
                    url_for("registry", item)
                except ValueError:
                    continue
                keys.add((w["package"], w["version"]))
    write(RUN / "registry_queue.json", {"stage": "registry", "protocol_sha256": sha(RUN / "protocol.json"),
                                       "paths_sha256": sha(path), "requests": [{"package": p, "version": v}
                                                                              for p, v in sorted(keys)]})
    print("Path statuses", dict(Counter(x["status"] for x in traces)), "registry requests", len(keys))


def frame_paths(traces, index):
    results = []
    joins = Counter()
    for trace in traces:
        accounts = set()
        fully_observed = trace["complete"]
        confirmed = 0
        for witness in trace["witnesses"]:
            key = witness["package"], witness["version"]
            row = index.get(key)
            if not row:
                joins["unresolved_version"] += 1
                fully_observed = False
                continue
            if witness["public_npm_tarball"]:
                joins["public_tarball"] += 1
            elif sha512_values(witness.get("registry_integrity_candidate")) & sha512_values(row.get("integrity")):
                joins["sha512_match"] += 1
            else:
                joins["unresolved_artifact_identity"] += 1
                fully_observed = False
                continue
            confirmed += 1
            accounts.update(row["accounts"])
        results.append((trace["sample_id"], accounts, fully_observed, confirmed))
    return results, joins


def paired(rows, name, version):
    cells = Counter()
    intervals = [0, 0, 0, 0]
    ledger = []
    for sid, observed, complete, confirmed in rows:
        known = [int(bool(observed & name)), int(bool(observed & version))]
        viable = [[i,j] for i,j in itertools.product((0,1), repeat=2)
                  if i >= known[0] and j >= known[1] and (not complete or [i,j] == known)
                  and (name != version or i == j)]
        gross = [abs(j-i) for i,j in viable]
        net = [j-i for i,j in viable]
        limits = [min(gross),max(gross),min(net),max(net)]
        intervals = [a+b for a,b in zip(intervals,limits,strict=True)]
        cells[f"{known[0]}{known[1]}"] += 1
        ledger.append({"sample_id":sid,"documented":known,"feasible":viable,"confirmed_paths":confirmed})
    n = len(ledger)
    return {"documented_cells": {k:cells[k] for k in ("00","01","10","11")},
            "resolved_pairs": sum(len(row["feasible"]) == 1 for row in ledger),
            "turnover_bounds": [i/n for i in intervals[:2]], "net_bounds": [i/n for i in intervals[2:]],
            "projects": ledger}


def score():
    rows = inputs()
    path = RUN / "paths.json.gz"
    if read(RUN / "registry_queue.json")["paths_sha256"] != sha(path):
        raise ValueError("Traced paths changed")
    traces = json.loads(gzip.decompress(path.read_bytes()))
    if [(row["frame_id"],row["commit_sha"]) for row,_ in rows] != [(t["sample_id"],t["commit_sha"]) for t in traces]:
        raise ValueError("Trace universe changed")
    observations = read_collection("registry")
    index = {(row["package"], row["version"]): row for row in observations if row["status"] == "observed"}
    evaluated, joins = frame_paths(traces,index)
    maintainers, slots = frozen_portfolios()
    accounts = {k:{maintainers[i] for i in v} for k,v in slots.items()}
    comparisons = {f"version_{i}":paired(evaluated, accounts["name"], accounts[f"version_{i}"]) for i in range(1,4)}
    comparisons["identical_control"] = paired(evaluated, accounts["control"], accounts["control"])
    assert comparisons["identical_control"]["turnover_bounds"] == [0,0]
    result = {"denominator":len(rows), "paths_sha256":sha(path), "registry_ledger_sha256":sha(PRIVATE/"registry.json"),
              "request_states":dict(Counter(row["status"] for row in observations)),
              "projects_with_registry_linked_paths":sum(r[3]>0 for r in evaluated), "path_identity":dict(joins),
              "projects_with_complete_path_and_registry_evidence":sum(r[2] for r in evaluated),
              "path_status":dict(Counter(x["status"] for x in traces)), "comparisons":comparisons}
    write(RUN/"results.json",result)
    print({k:v for k,v in result.items() if k!="comparisons"})
    print({k:v for k,v in comparisons["version_1"].items() if k!="projects"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    stages = {"freeze":freeze, "workspaces":workspace_queue, "paths":witnesses, "score":score}
    parser.add_argument("stage", choices=tuple(stages))
    stages[parser.parse_args().stage]()
