#!/usr/bin/env python3
"""Collect public files at the catalog's already pinned commits. No portfolio scoring."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

FILES = {
    "package.json": 512000, "npm-shrinkwrap.json": 6 * 1024**2,
    "package-lock.json": 6 * 1024**2, "pnpm-lock.yaml": 6 * 1024**2,
    "pnpm-workspace.yaml": 512000, "yarn.lock": 6 * 1024**2,
    "bun.lock": 6 * 1024**2, "bun.lockb": 6 * 1024**2,
}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def fetch(row, name, limit):
    url = f"https://raw.githubusercontent.com/{row['repository']}/{row['commit_sha']}/{name}"
    record = {"url": url, "requested_utc": now()}
    for attempt in (1, 2):
        record["attempts"] = attempt
        try:
            req = Request(url, headers={"User-Agent": "npm-consumer-study-root/1"})
            with build_opener(NoRedirect()).open(req, timeout=12) as response:
                data = response.read(limit + 1)
                status = response.status
            if len(data) > limit:
                return {**record, "http_status": status, "status": "above_limit"}, None
            return {**record, "http_status": status, "status": "retained",
                    "sha256": sha(data), "bytes": len(data)}, data
        except HTTPError as error:
            # Do not immediately retry rate limits.
            if error.code not in (500, 502, 503, 504) or attempt == 2:
                return {**record, "status": "http_error", "http_status": error.code}, None
        except (URLError, OSError, TimeoutError) as error:
            if attempt == 2:
                return {**record, "status": "transport_error", "error": type(error).__name__}, None
    raise AssertionError("Unreachable request state")


def observe(row, output):
    folder = output / "projects" / row["frame_id"]
    folder.mkdir(parents=True, exist_ok=False)
    receipt = {}
    for name, cap in FILES.items():
        metadata, payload = fetch(row, name, cap)
        receipt[name] = metadata
        if name == "package.json" and (payload is None or metadata["sha256"] != row["manifest_sha256"]):
            return {"frame_id": row["frame_id"], "repository": row["repository"], "commit_sha": row["commit_sha"],
                    "status": "manifest_unverified", "files": receipt}
        if payload is not None:
            (folder / name).write_bytes(payload)
    return {"frame_id": row["frame_id"], "repository": row["repository"], "commit_sha": row["commit_sha"],
            "status": "root_files_observed", "files": receipt}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frame", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    raw = args.frame.read_bytes()
    frame = json.loads(raw)
    projects = frame["eligible"]
    ids = [r["frame_id"] for r in projects]
    if len(set(ids)) != len(ids) or len(projects) != frame["eligible_root_projects"] or not 0 < len(ids) <= 500:
        raise ValueError("Expected a complete, unique, bounded frame")
    for row in projects:
        if (not re.fullmatch(r"Y[0-9]{3}", row["frame_id"])
                or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", row["repository"])
                or any(part in (".", "..") for part in row["repository"].split("/"))
                or not re.fullmatch(r"[0-9a-f]{40}", row["commit_sha"])):
            raise ValueError("Unexpected repository key or pinned commit")
    args.out.mkdir(parents=True, exist_ok=False)
    with ThreadPoolExecutor(max_workers=6) as pool:
        observations = list(pool.map(lambda row: observe(row, args.out), projects))
    ledger = {"frame_sha256": sha(raw), "started_scope": list(FILES), "sealed_utc": now(), "projects": observations}
    (args.out / "observations.json").write_text(json.dumps(ledger, indent=2) + "\n")
    print(f"Captured root observations for {len(observations)} pinned projects", file=sys.stderr)


if __name__ == "__main__":
    main()
