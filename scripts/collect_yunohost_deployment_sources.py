#!/usr/bin/env python3
"""Resolve public GitHub archive tags and read only specified files at the resolved commits."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import quote

from collect_yunohost_observations import REPO, fetch, now, sha256
from collect_yunohost_packaging import COMMIT

TAG = re.compile(r"[A-Za-z0-9._@+/-]{1,120}")
FILE = re.compile(r"[A-Za-z0-9_.@/-]{1,140}")
NAMES = {"package.json", "pnpm-lock.yaml", "pnpm-workspace.yaml", "package-lock.json",
         "npm-shrinkwrap.json", "assets.rake"}


def url_for(repo, commit, path):
    if (not REPO.fullmatch(repo) or not COMMIT.fullmatch(commit) or not FILE.fullmatch(path)
            or any(part in {"", ".", ".."} for part in path.split("/"))
            or path.split("/")[-1] not in NAMES):
        raise ValueError("Unexpected GitHub file location")
    return f"https://raw.githubusercontent.com/{repo}/{commit}/{quote(path, safe='/')}"


def resolve(repo, kind, ref):
    if not REPO.fullmatch(repo):
        raise ValueError("Unexpected upstream repository")
    if kind == "commit" and COMMIT.fullmatch(ref):
        return {"status": "declared_commit", "commit": ref}
    if kind != "tag" or not TAG.fullmatch(ref) or ".." in ref or "//" in ref or ref.endswith(".lock"):
        raise ValueError("Unexpected upstream archive reference")
    tag = f"refs/tags/{ref}"
    env = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0"}
    try:
        result = subprocess.run(["git", "ls-remote", "--exit-code", f"https://github.com/{repo}.git", tag, tag + "^{}"],
                                text=True, capture_output=True, timeout=45, env=env)
    except subprocess.TimeoutExpired:
        return {"status": "tag_request_timed_out"}
    if result.returncode:
        return {"status": "tag_absent" if result.returncode == 2 else "tag_request_failed"}
    rows = [line.split() for line in result.stdout.splitlines() if line]
    refs = {name: commit for commit, name in rows if name in {tag, tag + "^{}"} and COMMIT.fullmatch(commit)}
    if tag not in refs:
        return {"status": "tag_response_unresolved"}
    return {"status": "tag_resolved", "commit": refs.get(tag + "^{}", refs[tag]), "refs": refs}


def observe(row):
    ref = resolve(row["upstream"], row["ref_kind"], row["ref"])
    files = {}
    if "commit" in ref:
        for path in row["files"]:
            receipt, body = fetch(url_for(row["upstream"], ref["commit"], path), 6 * 1024 * 1024)
            if body is not None:
                receipt["body_base64"] = base64.b64encode(body).decode()
            files[path] = receipt
    return {**row, "observed_at_utc": now(), "resolved": ref, "receipts": files}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("queue", type=Path)
    args = cli.parse_args()
    raw = args.queue.read_bytes()
    rows = json.loads(raw)["requests"]
    if len(rows) != 6 or any(len(r["files"]) > 8 for r in rows):
        raise ValueError("Unexpected scope")
    with ThreadPoolExecutor(max_workers=4) as pool:
        items = list(pool.map(observe, rows))
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), "finished_utc": now(), "observations": items},
                     separators=(",", ":")))


if __name__ == "__main__":
    main()
