#!/usr/bin/env python3
"""Describe pinned root manifests without inspecting consumer lockfiles."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def digest(body):
    return hashlib.sha256(body).hexdigest()


def inspect(row):
    repo = row["repository"]
    result = {**row, "head_observed_utc": timestamp(), "commit_sha": None, "status": "head_unresolved"}
    try:
        proc = subprocess.run(["git", "-c", "http.followRedirects=false", "-c", "credential.helper=",
                               "ls-remote", "--exit-code", f"https://github.com/{repo}.git", "HEAD"],
                              text=True, capture_output=True, timeout=22, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
        part = proc.stdout.split()
        if proc.returncode or len(part) != 2 or part[1] != "HEAD" or not re.fullmatch(r"[0-9a-f]{40}", part[0]):
            return {**result, "head_exit_code": proc.returncode}
    except subprocess.TimeoutExpired:
        return {**result, "head_exit_code": "timeout"}
    result["commit_sha"] = part[0]
    url = f"https://raw.githubusercontent.com/{repo}/{part[0]}/package.json"
    result.update(url=url, manifest_observed_utc=timestamp())
    try:
        req = Request(url, headers={"User-Agent": "npm-consumer-frame-screen/1"})
        with build_opener(NoRedirect()).open(req, timeout=18) as response:
            result["http_status"] = response.status
            payload = response.read(512001)
    except HTTPError as exc:
        return {**result, "http_status": exc.code, "status": "manifest_404" if exc.code == 404 else "manifest_http_error"}
    except (URLError, OSError, TimeoutError):
        return {**result, "status": "manifest_transport_error"}
    if len(payload) > 512000:
        return {**result, "status": "manifest_above_limit"}
    result["manifest_sha256"] = digest(payload)
    try:
        manifest = json.loads(payload)
    except (ValueError, UnicodeDecodeError):
        return {**result, "status": "manifest_invalid"}
    if not isinstance(manifest, dict):
        return {**result, "status": "manifest_invalid"}
    pm = manifest.get("packageManager")
    declared = pm.split("@", 1)[0] if isinstance(pm, str) and "@" in pm else None
    group = declared if declared in ("npm", "pnpm", "yarn", "bun") else "other" if pm else "undeclared"
    return {**result, "status": "root_manifest_observed", "declared_manager": group,
            "has_workspace_declaration": bool(manifest.get("workspaces")),
            "has_production_declarations": bool(manifest.get("dependencies"))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue", type=Path)
    args = parser.parse_args()
    raw = args.queue.read_bytes()
    queue = json.loads(raw)
    subjects = queue["projects"]
    repos = [row["repository"] for row in subjects]
    if not 0 < len(repos) <= 600 or len(set(repos)) != len(repos) or not all(
            re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) and ".." not in repo.split("/") for repo in repos):
        raise ValueError("Expected a unique bounded set of public GitHub repository keys")
    with ThreadPoolExecutor(max_workers=8) as pool:
        outcomes = list(pool.map(inspect, subjects))
    result = {"queue_sha256": digest(raw), "scope": "pinned public GitHub root package.json",
              "observed_at_utc": timestamp(), "project_count": len(outcomes),
              "outcomes": dict(Counter(r["status"] for r in outcomes)), "projects": outcomes}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
