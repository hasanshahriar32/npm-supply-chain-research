#!/usr/bin/env python3
"""Read a bounded set of commit-pinned public YunoHost packaging files."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re

from collect_yunohost_observations import fetch, now, sha256

FILES = ("manifest.toml", "manifest.json", "scripts/install", "scripts/upgrade", "scripts/_common.sh",
         "conf/app.src", "conf/systemd.service", "conf/nginx.conf")
PACKAGING_REPO = re.compile(r"yunohost-apps/[a-z0-9_.-]+_ynh", re.I)
COMMIT = re.compile(r"[a-f0-9]{40}")


def url_for(row, path):
    repo, commit = row["packaging_repository"], row["packaging_commit"]
    if not PACKAGING_REPO.fullmatch(repo) or not COMMIT.fullmatch(commit) or path not in FILES:
        raise ValueError("Unexpected packaging source")
    return f"https://raw.githubusercontent.com/{repo}/{commit}/{path}"


def observe(row):
    receipts = {}
    for name in FILES:
        receipt, content = fetch(url_for(row, name), 512_000)
        if content is not None:
            receipt["body_base64"] = base64.b64encode(content).decode()
        receipts[name] = receipt
    return {**row, "files": receipts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue", type=Path)
    args = parser.parse_args()
    raw = args.queue.read_bytes()
    projects = json.loads(raw)["projects"]
    if len(projects) != 31 or len({row["sample_id"] for row in projects}) != 31:
        raise ValueError("Unexpected scope for the pinned evidence audit")
    with ThreadPoolExecutor(max_workers=5) as pool:
        observations = list(pool.map(observe, projects))
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), "finished_utc": now(),
                      "observations": observations}, separators=(",", ":")))


if __name__ == "__main__":
    main()
