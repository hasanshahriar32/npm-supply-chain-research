#!/usr/bin/env python3
"""Hash small public release assets and inspect dependency metadata paths without extraction."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import gzip
from hashlib import sha256
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import tarfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from zipfile import BadZipFile, ZipFile

from collect_yunohost_observations import now
from verify_yunohost_deployment_archives import ByteLimit

CAP = 12 * 1024 * 1024
UNPACKED_CAP = 128 * 1024 * 1024
HOSTS = {"github.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com"}
LOCKFILES = {"package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb"}
SBOM = re.compile(r"\b(?:sbom|spdx|cyclonedx|cdx)\b.*(?:\.json|\.xml|\.spdx)$", re.I)


class ReleaseRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        url = urlsplit(newurl)
        if url.scheme == "https" and url.netloc in HOSTS:
            return super().redirect_request(req, fp, code, msg, headers, newurl)
        return None


def summarize(filenames):
    metadata = Counter()
    manifests, locks, sboms = set(), set(), set()
    for name in filenames:
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts:
            continue
        if path.name == "package.json":
            if "node_modules" in path.parts:
                metadata["node_modules_manifests"] += 1
            else:
                manifests.add(str(path.parent))
        if path.name in LOCKFILES and "node_modules" not in path.parts:
            locks.add(str(path))
        if SBOM.search(path.name):
            sboms.add(str(path))
    return {"standalone_manifest_directories": len(manifests), "lockfiles": sorted(locks),
            "manifest_lockfile_pairs": sum(str(PurePosixPath(lock).parent) in manifests for lock in locks),
            "node_modules_manifests": metadata["node_modules_manifests"], "sbom_filename_candidates": sorted(sboms)}


def scan(body, name):
    if name.endswith(".zip"):
        with ZipFile(io.BytesIO(body)) as archive:
            return summarize(item.filename for item in archive.infolist()
                             if not item.is_dir() and not stat.S_ISLNK(item.external_attr >> 16))
    if name.endswith((".tgz", ".tar.gz")):
        with gzip.GzipFile(fileobj=io.BytesIO(body)) as stream:
            with tarfile.open(fileobj=ByteLimit(stream, UNPACKED_CAP), mode="r|") as archive:
                return summarize(item.name for item in archive if item.isreg())
    return None


def observe(item):
    url = urlsplit(item["url"])
    if (url.scheme != "https" or url.netloc != "github.com" or "/releases/download/" not in url.path
            or url.query or url.fragment or not 0 < item["listed_size"] <= CAP):
        raise ValueError("Unexpected release download")
    row = {"request": item, "observed_at_utc": now()}
    try:
        request = Request(item["url"], headers={"User-Agent": "npm-consumer-study/1"})
        with build_opener(ReleaseRedirect()).open(request, timeout=35) as response:
            body = response.read(CAP + 1)
            row["http_status"] = response.status
    except HTTPError as exc:
        return {**row, "status": "http_error", "http_status": exc.code}
    except (URLError, OSError, TimeoutError):
        return {**row, "status": "transport_error"}
    if len(body) > CAP:
        return {**row, "status": "above_limit"}
    digest = sha256(body).hexdigest()
    row.update(sha256=digest, size=len(body), agrees_with_recipe=digest == item["recipe_sha256"],
               agrees_with_api=("sha256:" + digest == item["api_digest"] if item["api_digest"] else None))
    if not row["agrees_with_recipe"]:
        return {**row, "status": "download_digest_differs"}
    try:
        inventory = scan(body, item["asset"])
    except (OSError, ValueError, EOFError, tarfile.TarError, BadZipFile):
        return {**row, "status": "archive_scan_unresolved"}
    return {**row, "status": "archive_scanned" if inventory is not None else "verified_nonarchive",
            "inventory": inventory}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("queue", type=Path)
    args = cli.parse_args()
    raw = args.queue.read_bytes()
    rows = json.loads(raw)["requests"]
    if len(rows) > 20 or sum(r["listed_size"] for r in rows) > 128 * 1024**2:
        raise ValueError("Archive queue exceeds the study budget")
    with ThreadPoolExecutor(max_workers=3) as pool:
        result = list(pool.map(observe, rows))
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), "finished_utc": now(), "rows": result},
                     separators=(",", ":")))
