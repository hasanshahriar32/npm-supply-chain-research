"""Inventory upstream source repositories in a captured YunoHost app catalog."""
from collections import Counter
from datetime import datetime, timezone

from collect_consumer_pilot import repo_url
from consumer_holdout import BASE, INCIDENCE, ORIGINAL, PILOT, ROOT, write, sha
from evaluate_consumer_pilot import load

OUT = ROOT / "research/consumer_parser_development"
CATALOG = OUT / "private" / "yunohost_catalog.json"
CATALOG_URL = "https://app.yunohost.org/default/v3/apps.json"
EFFECTIVE_URL = "https://apps.yunohost.org//default/v3/apps.json"


def main():
    apps = load(CATALOG)["apps"]
    frame = set(load(PILOT)["repositories"])
    original = {r["repository"].casefold() for r in load(ORIGINAL)["endpoints"]}
    training = {r.casefold() for r in load(INCIDENCE)["repositories"]}
    holdout = {r["repository"] for r in load(BASE / "runs/selfhosted-v1/protocol.json")["projects"]}
    rows = []
    for app_id, app in sorted(apps.items()):
        row = {"app_id": app_id}
        code = app.get("manifest", {}).get("upstream", {}).get("code")
        tags = app.get("antifeatures", [])
        if app.get("state") != "working":
            row["status"] = "state_not_working"
        elif {"deprecated-software", "replaced-by-another-app"} & set(tags):
            row["status"] = "deprecated_or_replaced"
        elif not isinstance(code, str) or not code:
            row["status"] = "upstream_code_missing"
        elif not (upstream := repo_url(code)):
            row["status"] = "upstream_not_github_root"
        elif upstream == repo_url(app.get("git", {}).get("url", "")):
            row["status"] = "upstream_equals_packaging_repository"
        else:
            row.update(status="github_upstream_candidate", repository=upstream)
        rows.append(row)
    repositories = {row["repository"] for row in rows if row["status"] == "github_upstream_candidate"}
    overlap = {"awesome_selfhosted_frame": len(repositories & frame),
               "original_endpoints": len(repositories & original), "training_endpoints": len(repositories & training),
               "first_holdout": len(repositories & holdout)}
    remaining = repositories - frame - original - training
    summary = {
        "requested_url": CATALOG_URL, "effective_url": EFFECTIVE_URL, "catalog_sha256": sha(CATALOG),
        "download_file_mtime_utc": datetime.fromtimestamp(CATALOG.stat().st_mtime, timezone.utc).isoformat(),
        "catalog_app_records": len(rows), "record_status": dict(Counter(r["status"] for r in rows)),
        "unique_github_upstream_candidates": len(repositories), "repository_key_overlaps": overlap,
        "remaining_after_previous_frame_and_endpoint_exclusions": len(remaining),
        "remaining_repository_keys": sorted(remaining), "project_dependency_files_inspected": 0,
        "records": rows,
    }
    write(OUT / "yunohost_frame_preflight.json", summary)
    for key, value in summary.items():
        if key not in ("records", "remaining_repository_keys"):
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
