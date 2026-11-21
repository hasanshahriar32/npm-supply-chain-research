#!/usr/bin/env python3
"""Collect a frozen workspace or registry queue over public HTTPS."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPRedirectHandler, Request, build_opener

REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
PACKAGE = re.compile(r"(?:@[a-zA-Z0-9~][a-zA-Z0-9._~-]*/)?[a-zA-Z0-9~][a-zA-Z0-9._~-]*")
VERSION = re.compile(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?")
SEGMENT = re.compile(r"[A-Za-z0-9_@.~-]+")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def url_for(stage, item):
    if stage == "workspaces":
        repository, commit, location = (item[key] for key in ("repository", "commit_sha", "location"))
        if (not REPO.fullmatch(repository) or not re.fullmatch(r"[0-9a-f]{40}", commit)
                or not all(SEGMENT.fullmatch(part) and part not in {".", ".."} for part in location.split("/"))
                or any(part in (".", "..") for part in repository.split("/"))):
            raise ValueError("Invalid pinned workspace identity")
        return f"https://raw.githubusercontent.com/{repository}/{commit}/{quote(location, safe='/')}/package.json"
    if stage != "registry" or not PACKAGE.fullmatch(item["package"]) or not VERSION.fullmatch(item["version"]):
        raise ValueError("Invalid public registry request")
    return "https://registry.npmjs.org/" + "/".join(quote(item[k], safe="") for k in ("package", "version"))


def fetch(url, cap):
    row = {"url": url, "observed_at_utc": now()}
    for attempt in (1, 2):
        row["attempts"] = attempt
        try:
            req = Request(url, headers={"User-Agent": "npm-consumer-study/1"})
            with build_opener(NoRedirect()).open(req, timeout=16) as response:
                blob = response.read(cap + 1)
                row["http_status"] = response.status
            if len(blob) > cap:
                return {**row, "status": "above_limit"}, None
            return {**row, "status": "retained", "sha256": sha256(blob).hexdigest()}, blob
        except HTTPError as err:
            row["http_status"] = err.code
            if attempt == 2 or err.code not in (500, 502, 503, 504):
                return {**row, "status": "http_error"}, None
        except (URLError, OSError, TimeoutError):
            if attempt == 2:
                return {**row, "status": "transport_error"}, None
    raise AssertionError("Unexpected request state")


def observe(stage, entry):
    url = url_for(stage, entry)
    receipt, payload = fetch(url, 512_000 if stage == "workspaces" else 4 * 1024 * 1024)
    row = {**entry, **receipt}
    if payload is None:
        return row
    if stage == "workspaces":
        # Exact bytes are needed for the manifest identity check on replay.
        import base64
        return {**row, "manifest_base64": base64.b64encode(payload).decode("ascii")}
    try:
        meta = json.loads(payload)
    except (UnicodeDecodeError, ValueError):
        return {**row, "status": "invalid_json"}
    if not isinstance(meta, dict) or (meta.get("name"), meta.get("version")) != (entry["package"], entry["version"]):
        return {**row, "status": "package_identity_mismatch"}
    members = meta.get("maintainers")
    if (not isinstance(members, list)
            or not all(isinstance(m, dict) and isinstance(m.get("name"), str) and m["name"] for m in members)):
        return {**row, "status": "maintainer_list_unavailable"}
    dist = meta.get("dist")
    integrity = dist.get("integrity") if isinstance(dist, dict) else None
    return {**row, "status": "observed", "accounts": sorted({m["name"] for m in members}), "integrity": integrity}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue", type=Path)
    args = parser.parse_args()
    raw = args.queue.read_bytes()
    queue = json.loads(raw)
    stage = queue["stage"]
    ids = queue["requests"]
    urls = [url_for(stage, entry) for entry in ids]
    if len(set(urls)) != len(urls) or len(ids) > 26000:
        raise ValueError("Queue contains duplicates or exceeds the collection cap")
    with ThreadPoolExecutor(max_workers=8) as pool:
        ledger = list(pool.map(lambda entry: observe(stage, entry), ids))
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), "stage": stage,
                      "finished_utc": now(), "observations": ledger}, separators=(",", ":")))


if __name__ == "__main__":
    main()
