#!/usr/bin/env python3
"""Freeze and verify the packaging evidence used to identify deployment importers."""
import argparse
import base64
from collections import Counter
from datetime import datetime
import gzip
import json
import tomllib

from collect_yunohost_packaging import COMMIT, FILES, PACKAGING_REPO, url_for
from collect_consumer_pilot import repo_url
from study_yunohost_holdout import BASE, CAPTURE, ROOT, RUN as BASELINE, digest, now, read, sha, write

RUN = BASELINE.with_name("yunohost-packaging")
YARN = BASELINE.with_name("yunohost-yarn-classic")
PRIVATE = RUN / "private"
CATALOG = BASE / "private/yunohost_catalog.json"
OBSERVATIONS = CAPTURE / "observations.json"
QUEUE = RUN / "queue.json"
LEDGER = PRIVATE / "receipts.json"
INTAKE = RUN / "intake.json"

RULES = {
    "frame": "All 15 unresolved pnpm workspace cases with a successful empty root walk and retained workspace file, "
             "and all 16 unresolved projects without a conventional root lockfile.",
    "review": "Static evidence at the packaging revision captured in the app catalog. Classify whether the recipe "
              "builds a named JavaScript importer, builds from an explicit directory, uses a prebuilt artifact, "
              "or leaves the relevant importer ambiguous. Distinguish setup commands from compilation and runtime.",
    "deployment_mapping": "Require a literal directory or package selector tied to an install/build or service path, "
                          "and corroborate against an importer and manifest at the source actually selected. "
                          "A workspace manifest, generic root task, or CI test alone is insufficient.",
    "source_identity": "Compare the packaging source revision with the default HEAD captured by the root study. "
                       "Source archive tags and release artifact provenance are distinct. Never transfer dependency "
                       "evidence across source revisions without verifying identity.",
    "scope": "The packaging audit is a follow-up after both holdout analyses. Treat any deployment-importer "
             "comparison as a separate conditional scope. Keep prior paired outcomes immutable.",
}


def inputs():
    return {str(p.relative_to(ROOT)): sha(p) for p in (
        ROOT / __file__, ROOT / "scripts/collect_yunohost_packaging.py", CATALOG, OBSERVATIONS,
        BASE / "yunohost_frame_preflight.json", BASELINE / "paths.json.gz", YARN / "results.json",
    )}


def queue():
    if QUEUE.exists():
        raise ValueError("Packaging sample already frozen")
    apps = read(CATALOG)["apps"]
    preflight = read(BASE / "yunohost_frame_preflight.json")
    assert preflight["catalog_sha256"] == sha(CATALOG)
    mapping = {}
    for row in preflight["records"]:
        if row["status"] == "github_upstream_candidate":
            mapping.setdefault(row["repository"], []).append(row["app_id"])
    traces = {t["sample_id"]: t for t in json.loads(gzip.decompress((BASELINE / "paths.json.gz").read_bytes()))}
    unresolved = {p["sample_id"] for p in read(YARN / "results.json")["comparisons"]["version_1"]["projects"]
                  if len(p["feasible"]) > 1}
    cases = []
    for original in read(OBSERVATIONS)["projects"]:
        sid = original["frame_id"]
        status = traces[sid]["status"]
        if sid not in unresolved:
            continue
        if status == "no_root_lockfile_returned":
            group = "no_root_lockfile"
        elif status == "pnpm_ok" and not traces[sid]["witnesses"] and original["files"]["pnpm-workspace.yaml"]["status"] == "retained":
            group = "empty_pnpm_workspace_root"
        else:
            continue
        [app_id] = mapping[original["repository"]]
        git = apps[app_id]["git"]
        package = repo_url(git["url"])
        assert PACKAGING_REPO.fullmatch(package) and COMMIT.fullmatch(git["revision"])
        cases.append({"sample_id": sid, "group": group, "app_id": app_id, "upstream": original["repository"],
                      "upstream_commit": original["commit_sha"], "packaging_repository": package,
                      "packaging_commit": git["revision"]})
    assert Counter(c["group"] for c in cases) == {"empty_pnpm_workspace_root": 15, "no_root_lockfile": 16}
    PRIVATE.mkdir(parents=True, exist_ok=True)
    write(QUEUE, {"frozen_utc": now(), "inputs": inputs(), "rules": RULES, "projects": cases})
    print("Frozen", len(cases), "catalog packaging revisions")


def read_evidence():
    scope, ledger = read(QUEUE), read(LEDGER)
    assert scope["inputs"] == inputs()
    assert ledger["queue_sha256"] == sha(QUEUE)
    start, finish = map(datetime.fromisoformat, (scope["frozen_utc"], ledger["finished_utc"]))
    for case, observed in zip(scope["projects"], ledger["observations"], strict=True):
        assert all(observed[k] == v for k, v in case.items()) and set(observed["files"]) == set(FILES)
        evidence = {}
        for name, record in observed["files"].items():
            assert record["url"] == url_for(case, name)
            assert start <= datetime.fromisoformat(record["observed_at_utc"]) <= finish
            if record["status"] == "retained":
                payload = base64.b64decode(record["body_base64"], validate=True)
                assert record["http_status"] == 200 and digest(payload) == record["sha256"]
                evidence[name] = payload.decode()
            else:
                assert "body_base64" not in record
        yield case, evidence, observed["files"]


def intake():
    rows = []
    for case, evidence, receipts in read_evidence():
        manifest_path = next((p for p in ("manifest.toml", "manifest.json") if p in evidence), None)
        sources = {}
        if manifest_path == "manifest.toml":
            doc = tomllib.loads(evidence[manifest_path])
            assert doc["id"] == case["app_id"]
            sources = doc.get("resources", {}).get("sources", {})
        rows.append({**case, "manifest_path": manifest_path, "declared_sources": sources,
                     "files": {k: {f: v for f, v in receipt.items() if f != "body_base64"}
                               for k, receipt in receipts.items()}})
    write(INTAKE, {"queue_sha256": sha(QUEUE), "receipts_sha256": sha(LEDGER), "projects": rows})
    print(dict(Counter((r.get("http_status"), r["status"]) for row in rows for r in row["files"].values())))


if __name__ == "__main__":
    stages = {"queue": queue, "intake": intake}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=tuple(stages))
    stages[parser.parse_args().stage]()
