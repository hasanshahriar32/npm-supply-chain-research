#!/usr/bin/env python3
"""Trace and score the importers explicitly selected by verified packaging recipes."""
import argparse
from collections import Counter
from datetime import datetime
import gzip
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from collect_yunohost_observations import url_for
from study_pnpm_parser_development import YAML_READER
from study_yunohost_deployment_candidates import (
    AUDIT, RUN, SOURCE_INTAKE, SOURCE_LEDGER, digest, now, read, sha, source_evidence, write,
)
from study_yunohost_holdout import INCIDENCE, ROOT, frozen_portfolios, paired, sha512_values

ARCHIVES = RUN / "archive_checks.json"
PROTOCOL = RUN / "importer_protocol.json"
TRACES = RUN / "importer_paths.json.gz"
QUEUE = RUN / "importer_registry_queue.json"
RECEIPTS = RUN / "private/importer_registry.json"
RESULTS = RUN / "importer_results.json"


def input_hashes():
    paths = [AUDIT, SOURCE_INTAKE, SOURCE_LEDGER, ARCHIVES, INCIDENCE, RUN / "archive_queue.json"]
    paths += [ROOT / "scripts" / name for name in (
        "study_yunohost_recipe_importers.py", "verify_yunohost_deployment_archives.py",
        "study_yunohost_deployment_candidates.py", "study_yunohost_holdout.py", "study_pnpm_parser_development.py",
        "consumer_pnpm_development.cjs", "consumer_npm_development.cjs", "consumer_lock_evidence.cjs",
        "collect_yunohost_observations.py",
    )]
    return {str(path.relative_to(ROOT)): sha(path) for path in paths}


def projects():
    queue_path = RUN / "archive_queue.json"
    queue, archive = read(queue_path), read(ARCHIVES)
    assert queue["source_intake_sha256"] == sha(SOURCE_INTAKE) and archive["queue_sha256"] == sha(queue_path)
    start = datetime.fromisoformat(queue["frozen_utc"])
    end = datetime.fromisoformat(archive["finished_utc"])
    audit = {c["sample_id"]: c for c in read(AUDIT)["cases"]}
    sources = {r["sample_id"]: (ref, files) for r, ref, files, _ in source_evidence()}
    for expected, recorded in zip(queue["rows"], archive["rows"], strict=True):
        assert all(recorded[k] == v for k, v in expected.items())
        for field in ("archive", "packaging_tree"):
            assert start <= datetime.fromisoformat(recorded[field]["observed_at_utc"]) <= end
        sid = expected["sample_id"]
        ref, files = sources[sid]
        assert all(p in files for p in expected["paths"])
        archive_status = recorded["archive"]["status"]
        verified = (archive_status == "retained" and recorded["archive"]["sha256"] == expected["archive_sha256"]
                    and recorded["member_sha256"] == {p: digest(files[p]) for p in expected["paths"]}
                    and recorded["packaging_tree"]["status"] == "retained" and not recorded["patches"])
        yield audit[sid], ref, files, verified


def freeze():
    if PROTOCOL.exists():
        raise ValueError("Recipe importer protocol already frozen")
    sample = [{"sample_id": row["sample_id"], "paths": row["recipe_paths"], "commit": ref["commit"],
               "archive_and_patch_check": verified} for row, ref, _, verified in projects()]
    _, slots = frozen_portfolios()
    write(PROTOCOL, {"frozen_utc": now(), "inputs": input_hashes(), "projects": sample,
                     "portfolio_fingerprints": {k: digest(json.dumps(v).encode()) for k, v in slots.items()},
                     "scope": "Separate three-recipe diagnostic selected by literal paths and verified archive bytes. "
                              "Root-mandatory regular dependencies of named importers, pnpm v9 to three edges. "
                              "Cross-check the same named pnpm lock importer projected into a sterile directory with offline native listing. "
                              "Join a path only when every prefix has a registry identity and usable observation. Positive observations only.",
                     "aggregation": "Union the named importer witnesses within each recipe. Preserve the prior 215-project bounds."})


def npm(manifest, lockfile):
    with tempfile.TemporaryDirectory(prefix="yuno-recipe-npm-") as tmp:
        source = Path(tmp)
        (source / "package.json").write_bytes(manifest)
        (source / "package-lock.json").write_bytes(lockfile)
        proc = subprocess.run(["node", str(ROOT / "scripts/consumer_npm_development.cjs"), tmp, "package-lock.json"],
                              check=True, text=True, capture_output=True, timeout=60)
    data = json.loads(proc.stdout)
    return next((r for r in data["importers"] if r["importer"] == ""), {"status": "unavailable", "witnesses": []})


def pnpm(manifest, original, location):
    importer = original.get("importers", {}).get(location)
    if not isinstance(importer, dict):
        return {"status": "importer_unavailable", "witnesses": []}
    projected = {**original, "importers": {".": importer}}
    minimal = {key: manifest[key] for key in ("name", "version", "dependencies", "devDependencies", "optionalDependencies")
               if key in manifest}
    env = {**os.environ, "npm_config_manage_package_manager_versions": "false", "COREPACK_ENABLE_AUTO_PIN": "0",
           "npm_config_ignore_pnpmfile": "true", "npm_config_ignore_scripts": "true", "npm_config_userconfig": "/dev/null"}
    with tempfile.TemporaryDirectory(prefix="yuno-recipe-pnpm-") as tmp:
        source = Path(tmp)
        (source / "package.json").write_text(json.dumps(minimal))
        (source / "pnpm-lock.yaml").write_text(json.dumps(projected))
        native = subprocess.run([shutil.which("pnpm"), "list", "--lockfile-only", "--offline", "--prod", "--json", "--depth", "2"],
                                cwd=tmp, text=True, capture_output=True, check=True, timeout=60, env=env)
    comparison = subprocess.run(["node", str(ROOT / "scripts/consumer_pnpm_development.cjs")],
                                input=json.dumps({"manifest": manifest, "lock": projected, "native": json.loads(native.stdout)}),
                                text=True, capture_output=True, check=True, timeout=60)
    return json.loads(comparison.stdout)


def trace(row, files, verified):
    if not verified:
        return []
    use_pnpm = row["classification"].startswith("pnpm")
    if use_pnpm:
        parsed = subprocess.run(["ruby", "-rpsych", "-rjson", "-e", YAML_READER],
                                input=files["pnpm-lock.yaml"], check=True, capture_output=True, timeout=45)
        lock = json.loads(parsed.stdout)["project"]
    traces = []
    for location in row["recipe_paths"]:
        try:
            manifest = files[location + "/package.json"]
            result = pnpm(json.loads(manifest), lock, location) if use_pnpm else npm(
                manifest, files[location + "/package-lock.json"]
            )
        except (subprocess.SubprocessError, json.JSONDecodeError):
            result = {"status": "reader_error", "witnesses": []}
        traces.append({"importer": location, "manager": "pnpm" if use_pnpm else "npm",
                       "status": result["status"], "witnesses": result["witnesses"], "issues": result.get("issues", {})})
    return traces


def paths():
    assert read(PROTOCOL)["inputs"] == input_hashes()
    rows = [{"sample_id": row["sample_id"], "commit_sha": ref["commit"],
             "same_commit_as_root_study": ref["commit"] == row["upstream_commit"],
             "traces": trace(row, files, verified)} for row, ref, files, verified in projects()]
    TRACES.write_bytes(gzip.compress(json.dumps(rows, separators=(",", ":")).encode(), mtime=0))
    keys = {(w["package"], w["version"]) for row in rows for tr in row["traces"] for w in tr["witnesses"]
            if w["public_npm_tarball"] or sha512_values(w.get("registry_integrity_candidate"))}
    requests = [{"package": p, "version": v} for p, v in sorted(keys)]
    for request in requests:
        url_for("registry", request)
    write(QUEUE, {"stage": "registry", "protocol_sha256": sha(PROTOCOL), "paths_sha256": sha(TRACES),
                  "requests": requests})
    print("Importers", dict(Counter(t["manager"] + ":" + t["status"] for r in rows for t in r["traces"])))
    print("Exact-version registry queue", len(requests))


def join(trace, observations):
    field = "snapshot" if trace["manager"] == "pnpm" else "location"
    confirmed = {}
    for w in trace["witnesses"]:
        record = observations.get((w["package"], w["version"]))
        if record and (w["public_npm_tarball"] or sha512_values(w.get("registry_integrity_candidate"))
                       & sha512_values(record.get("integrity"))):
            confirmed[w["path"][-1][field]] = record["accounts"]
    accounts, count = set(), 0
    for w in trace["witnesses"]:
        if all(step[field] in confirmed for step in w["path"]):
            accounts.update(confirmed[w["path"][-1][field]])
            count += 1
    return accounts, count


def score():
    protocol = read(PROTOCOL)
    assert protocol["inputs"] == input_hashes()
    queue, receipts = read(QUEUE), read(RECEIPTS)
    assert queue["protocol_sha256"] == sha(PROTOCOL) and queue["paths_sha256"] == sha(TRACES)
    assert receipts["queue_sha256"] == sha(QUEUE)
    start, end = map(datetime.fromisoformat, (protocol["frozen_utc"], receipts["finished_utc"]))
    observed = {}
    for request, result in zip(queue["requests"], receipts["observations"], strict=True):
        assert all(result[k] == v for k, v in request.items()) and result["url"] == url_for("registry", request)
        assert start <= datetime.fromisoformat(result["observed_at_utc"]) <= end
        if result["status"] == "observed":
            observed[request["package"], request["version"]] = result
    rows = json.loads(gzip.decompress(TRACES.read_bytes()))
    evaluated = []
    importer_counts = []
    for row in rows:
        accounts, count = set(), 0
        for trace in row["traces"]:
            seen, n = join(trace, observed)
            accounts.update(seen)
            count += n
            importer_counts.append({"sample_id": row["sample_id"], "importer": trace["importer"],
                                    "status": trace["status"], "joined_paths": n})
        evaluated.append((row["sample_id"], accounts, False, count))
    maintainers, slots = frozen_portfolios()
    portfolios = {k: {maintainers[i] for i in indices} for k, indices in slots.items()}
    comparisons = {f"version_{i}": paired(evaluated, portfolios["name"], portfolios[f"version_{i}"])
                   for i in (1, 2, 3)}
    comparisons["identical_control"] = paired(evaluated, portfolios["control"], portfolios["control"])
    assert comparisons["identical_control"]["turnover_bounds"] == [0, 0]
    write(RESULTS, {"denominator": len(evaluated), "registry_requests": len(queue["requests"]),
                    "registry_observations": len(observed), "protocol_sha256": sha(PROTOCOL),
                    "paths_sha256": sha(TRACES), "receipts_sha256": sha(RECEIPTS), "importers": importer_counts,
                    "comparisons": comparisons})
    print("Importers with verified paths:", sum(row["joined_paths"] > 0 for row in importer_counts))
    print({key: value["documented_cells"] for key, value in comparisons.items()})


if __name__ == "__main__":
    stages = {"freeze": freeze, "paths": paths, "score": score}
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("stage", choices=tuple(stages))
    stages[cli.parse_args().stage]()
