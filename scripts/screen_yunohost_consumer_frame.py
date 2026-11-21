"""Inventory upstream source repositories in a captured YunoHost app catalog."""
import argparse
from collections import Counter
from datetime import datetime, timezone

from collect_consumer_pilot import repo_url
from consumer_holdout import BASE, INCIDENCE, ORIGINAL, PILOT, ROOT, write, sha
from evaluate_consumer_pilot import load

OUT = ROOT / "research/consumer_parser_development"
CATALOG = OUT / "private" / "yunohost_catalog.json"
CATALOG_URL = "https://app.yunohost.org/default/v3/apps.json"
EFFECTIVE_URL = "https://apps.yunohost.org//default/v3/apps.json"


def catalog():
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


def root_frame():
    queue_path = OUT / "yunohost_root_screen_queue.json"
    screen_path = OUT / "yunohost_root_screen.json"
    pilot_observations = PILOT.with_name("observations.json")
    holdout_observations = BASE / "runs/selfhosted-v1/observations.json"
    queue, screened = load(queue_path), load(screen_path)
    identities = ("frame_id", "repository")
    expected = [tuple(r[k] for k in identities) for r in queue["projects"]]
    actual = [tuple(r[k] for k in identities) for r in screened["projects"]]
    if (queue["preflight_sha256"] != sha(OUT / "yunohost_frame_preflight.json")
            or screened["queue_sha256"] != sha(queue_path) or expected != actual
            or dict(Counter(r["status"] for r in screened["projects"])) != screened["outcomes"]):
        raise ValueError("Root-screen evidence disagrees with the frozen catalog queue")
    earlier = load(pilot_observations)["projects"] + load(holdout_observations)
    earlier_pins = {r["commit_sha"] for r in earlier if r["commit_sha"]}
    records = []
    eligible = []
    seen = set()
    for row in sorted(screened["projects"], key=lambda r: r["repository"]):
        status = row["status"]
        pin = row["commit_sha"]
        if status == "root_manifest_observed":
            if pin in earlier_pins:
                status = "same_commit_as_prior_consumer"
            elif pin in seen:
                status = "same_commit_in_yunohost_frame"
            else:
                status = "eligible_root_manifest"
                eligible.append(row)
                seen.add(pin)
        records.append({**{k: row[k] for k in identities}, "status": status})
    result = {
        "scope": "Public upstream applications in the captured catalog with an observed root package manifest",
        "screen_sha256": sha(screen_path),
        "prior_pilot_observations_sha256": sha(pilot_observations),
        "prior_holdout_observations_sha256": sha(holdout_observations),
        "duplicate_policy": "exclude prior exact commits, retain the lexically first key for same-frame exact commits",
        "funnel": dict(Counter(row["status"] for row in records)),
        "eligible_root_projects": len(eligible),
        "declared_managers": dict(Counter(row["declared_manager"] for row in eligible)),
        "eligible_with_workspace_declaration": sum(row["has_workspace_declaration"] for row in eligible),
        "eligible_with_production_declarations": sum(row["has_production_declarations"] for row in eligible),
        "dependency_lockfiles_opened": 0,
        "eligible": eligible,
        "all_screened": records,
    }
    write(OUT / "yunohost_root_frame.json", result)
    print({k: v for k, v in result.items() if k not in ("eligible", "all_screened")})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("catalog", "root-frame"), nargs="?", default="catalog")
    if parser.parse_args().stage == "catalog":
        catalog()
    else:
        root_frame()
