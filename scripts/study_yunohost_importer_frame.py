#!/usr/bin/env python3
"""Freeze and verify the expanded same-commit comparison of root and named recipe importers."""
import argparse
import base64
from collections import Counter
from datetime import datetime

from collect_consumer_pilot import repo_url
from collect_yunohost_importer_frame import FILES, url_for
from collect_yunohost_packaging import COMMIT, PACKAGING_REPO
from study_yunohost_packaging import BASE, CATALOG, QUEUE as EARLIER, ROOT, RUN as PILOT, digest, now, read, sha, write

RUN = PILOT.with_name("yunohost-importer-frame")
QUEUE = RUN / "sample.json"
PRIVATE = RUN / "private"
RECEIPTS = PRIVATE / "recipes.json"
SEED = "yunohost-same-commit-importer-2026-11-21"


def inputs():
    return (CATALOG, BASE / "yunohost_frame_preflight.json", BASE / "yunohost_root_frame.json",
            BASE / "yunohost_lockfile_observations.json", EARLIER)


def freeze():
    if QUEUE.exists():
        raise ValueError("The sample has already been frozen")
    catalog, preflight, frame, observed, previous = (read(p) for p in inputs())
    assert preflight["catalog_sha256"] == sha(CATALOG)
    exclude = {r["upstream"] for r in previous["projects"]}
    root_files = {r["repository"]: r["files"] for r in observed["projects"]}
    marked = {r["repository"] for r in frame["eligible"] if r["has_workspace_declaration"]
              or root_files[r["repository"]]["pnpm-workspace.yaml"]["status"] == "retained"}
    eligible = {r["repository"] for r in frame["all_screened"]} - exclude
    links = {}
    for row in sorted(preflight["records"], key=lambda r: r["app_id"]):
        if row["status"] == "github_upstream_candidate":
            links.setdefault(row["repository"], row["app_id"])
    selected = sorted(eligible & marked) + sorted(
        eligible - marked, key=lambda repo: digest(f"{SEED}\n{repo}".encode())
    )[:60]
    rows = []
    for i, upstream in enumerate(selected, 1):
        app_id = links[upstream]
        app = catalog["apps"][app_id]
        package = repo_url(app["git"]["url"])
        commit = app["git"]["revision"]
        assert PACKAGING_REPO.fullmatch(package) and COMMIT.fullmatch(commit)
        rows.append({"sample_id": f"D{i:03d}", "upstream": upstream, "app_id": app_id,
                     "stratum": "workspace_marker" if upstream in marked else "other",
                     "packaging_repository": package, "packaging_commit": commit})
    assert len(rows) == 99 and len(eligible) == 469
    PRIVATE.mkdir(parents=True, exist_ok=True)
    write(QUEUE, {
        "frozen_utc": now(), "seed": SEED, "population": {"workspace_marker": len(eligible & marked),
                                                        "other": len(eligible - marked)},
        "sample": dict(Counter(row["stratum"] for row in rows)),
        "inputs": {str(p.relative_to(ROOT)): sha(p) for p in inputs()},
        "collector_sha256": sha(ROOT / "scripts/collect_yunohost_importer_frame.py"),
        "design": "Exclude the 31 previously audited recipe keys. Take all observed workspace markers and rank "
                  "the remaining keys by seeded SHA-256 for a 60-project draw. Use the captured catalog revision. "
                  "The sample is frozen before reading these recipes or calculating portfolio outcomes.",
        "comparison": "Code recipe actions with pinned line evidence. A named importer requires an explicit directory "
                      "or exact package selector connected to an install, build artifact, or service. "
                      "Compare root and named importers at the same recipe-selected upstream commit and shared registry snapshot. "
                      "Retain release payloads, ambiguous recipes, and missing proofs in the attrition ledger. "
                      "Report the conditional comparison and its eligibility denominator.",
        "projects": rows,
    })
    print(f"Frozen {len(rows)} recipes from {len(eligible)} keys")


def evidence():
    queue, receipts = read(QUEUE), read(RECEIPTS)
    assert queue["inputs"] == {str(p.relative_to(ROOT)): sha(p) for p in inputs()}
    assert queue["collector_sha256"] == sha(ROOT / "scripts/collect_yunohost_importer_frame.py")
    assert receipts["queue_sha256"] == sha(QUEUE)
    start, end = map(datetime.fromisoformat, (queue["frozen_utc"], receipts["finished_utc"]))
    for expected, record in zip(queue["projects"], receipts["observations"], strict=True):
        assert all(record[k] == v for k, v in expected.items()) and set(record["files"]) == set(FILES)
        files = {}
        for path, item in record["files"].items():
            assert item["url"] == url_for(expected, path)
            assert start <= datetime.fromisoformat(item["observed_at_utc"]) <= end
            if item["status"] == "retained":
                body = base64.b64decode(item["body_base64"], validate=True)
                assert item["http_status"] == 200 and digest(body) == item["sha256"]
                files[path] = body.decode()
        yield expected, files, record["files"]


def inspect():
    counts = Counter()
    for _, _, records in evidence():
        counts.update(r.get("http_status", r["status"]) for r in records.values())
    print(dict(counts))


if __name__ == "__main__":
    stages = {"freeze": freeze, "inspect": inspect}
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("stage", choices=tuple(stages))
    stages[cli.parse_args().stage]()
