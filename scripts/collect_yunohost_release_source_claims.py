#!/usr/bin/env python3
"""Extract declared Git commits from exact-digest public SLSA provenance statements."""
import argparse
import base64
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from collect_yunohost_observations import fetch, now, sha256
from collect_yunohost_release_metadata import bound_statement, url_for

COMMIT = re.compile(r"[a-f0-9]{40}")


def source_commits(predicate, repo):
    definition = predicate.get("buildDefinition", {}) if isinstance(predicate, dict) else {}
    if not isinstance(definition, dict):
        return []
    dependencies = definition.get("resolvedDependencies", [])
    if not isinstance(dependencies, list):
        return []
    commits = set()
    for item in dependencies:
        if not isinstance(item, dict) or not isinstance(item.get("uri"), str) or not isinstance(item.get("digest"), dict):
            continue
        parsed = urlsplit(item["uri"].removeprefix("git+"))
        name = parsed.path.strip("/").split("@", 1)[0].removesuffix(".git")
        commit = item["digest"].get("gitCommit")
        if parsed.scheme == "https" and parsed.netloc == "github.com" and name.casefold() == repo:
            if isinstance(commit, str) and COMMIT.fullmatch(commit):
                commits.add(commit)
    return sorted(commits)


def observe(item):
    receipt, payload = fetch(url_for("subject", item), 2 * 1024 * 1024)
    output = {"request": item, "receipt": receipt, "matching_provenance_statements": 0, "declared_commits": []}
    if payload is None:
        return output
    body = json.loads(payload)
    matches = []
    for record in body.get("attestations", []):
        bundle = record.get("bundle")
        meta = bound_statement(bundle, item["digest"])
        if meta and meta["predicate_type"] == "https://slsa.dev/provenance/v1":
            statement = json.loads(base64.b64decode(bundle["dsseEnvelope"]["payload"]))
            matches.append(source_commits(statement.get("predicate"), item["repo"]))
    return {**output, "matching_provenance_statements": len(matches),
            "declared_commits": sorted({c for m in matches for c in m})}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("queue", type=Path)
    args = cli.parse_args()
    raw = args.queue.read_bytes()
    items = json.loads(raw)["requests"]
    if len(items) > 10:
        raise ValueError("Unexpected provenance scope")
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), "observations": [observe(item) for item in items],
                      "finished_utc": now()}, separators=(",", ":")))
