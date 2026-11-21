#!/usr/bin/env python3
"""Read canonical npm tarballs and hash package files without installing dependencies."""
import argparse
import base64
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import tarfile
from urllib.parse import quote, unquote, urlsplit

from collect_yunohost_observations import fetch, now, url_for
from verify_yunohost_deployment_archives import ByteLimit

PACKAGE_CAP = 16 * 1024 * 1024
TOTAL_CAP = 96 * 1024 * 1024
UNPACKED_CAP = 128 * 1024 * 1024


def file_hashes(body, roots):
    """Index regular own files below each root and note links or duplicate names."""
    wanted = {PurePosixPath(r): r for r in roots}
    result = {str(root): {"files": {}, "unsupported_entries": 0} for root in wanted}
    with gzip.GzipFile(fileobj=io.BytesIO(body)) as stream:
        with tarfile.open(fileobj=ByteLimit(stream, UNPACKED_CAP), mode="r|") as archive:
            for entry in archive:
                path = PurePosixPath(entry.name)
                if path.is_absolute() or ".." in path.parts:
                    raise ValueError("Invalid archived path")
                root = next((p for p in path.parents if p in wanted), None)
                if root is None:
                    if path in wanted and not entry.isdir():
                        result[str(path)]["unsupported_entries"] += 1
                    continue
                relpath = path.relative_to(root)
                if "node_modules" in relpath.parts or entry.isdir():
                    continue
                row = result[str(root)]
                key = str(relpath)
                if not entry.isreg() or key in row["files"]:
                    row["unsupported_entries"] += 1
                    continue
                digest = hashlib.sha256()
                with archive.extractfile(entry) as source:
                    for chunk in iter(lambda: source.read(64 * 1024), b""):
                        digest.update(chunk)
                row["files"][key] = digest.hexdigest()
    return result


def observe(item, remaining):
    url = url_for("registry", item)
    receipt, raw = fetch(url, 4 * 1024 * 1024)
    result = {"request": item, "observed_at_utc": receipt["observed_at_utc"], "registry_receipt": receipt}
    if raw is None:
        return {**result, "status": "version_metadata_unavailable"}, 0
    doc = json.loads(raw)
    package, version = item["package"], item["version"]
    if not isinstance(doc, dict) or (doc.get("name"), doc.get("version")) != (package, version):
        return {**result, "status": "registry_identity_unresolved"}, 0
    dist = doc.get("dist", {})
    tarball, integrity = dist.get("tarball"), dist.get("integrity")
    if not isinstance(tarball, str) or not isinstance(integrity, str):
        return {**result, "status": "registry_identity_unresolved"}, 0
    parsed = urlsplit(tarball)
    canonical = f"/{package}/-/{package.split('/')[-1]}-{version}.tgz"
    if (parsed.scheme != "https" or parsed.netloc != "registry.npmjs.org" or parsed.query or parsed.fragment
            or unquote(parsed.path) != canonical):
        return {**result, "status": "registry_identity_unresolved"}, 0
    if remaining == 0:
        return {**result, "status": "download_budget"}, 0
    tar_receipt, body = fetch("https://registry.npmjs.org" + quote(canonical, safe="/@"), min(PACKAGE_CAP, remaining))
    result["tarball_receipt"] = tar_receipt
    if body is None:
        return {**result, "status": "tarball_unavailable"}, 0
    sha512 = "sha512-" + base64.b64encode(hashlib.sha512(body).digest()).decode()
    if sha512 not in integrity.split():
        return {**result, "status": "tarball_integrity_differs"}, len(body)
    try:
        files = file_hashes(body, ["package"])["package"]
    except (EOFError, OSError, ValueError, tarfile.TarError):
        return {**result, "status": "tarball_unreadable"}, len(body)
    raw_accounts = doc.get("maintainers")
    accounts = None
    if isinstance(raw_accounts, list) and all(isinstance(a, dict) and isinstance(a.get("name"), str) for a in raw_accounts):
        accounts = sorted({a["name"] for a in raw_accounts})
    return {**result, "status": "verified_tarball", "own_files": files,
            "integrity": sha512, "accounts": accounts}, len(body)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("queue", type=Path)
    args = cli.parse_args()
    raw = args.queue.read_bytes()
    queue = json.loads(raw)
    done, remaining = [], TOTAL_CAP
    if len(queue["requests"]) > 45:
        raise ValueError("Too many exact-version requests")
    for item in queue["requests"]:
        row, spent = observe(item, remaining)
        remaining -= spent
        done.append(row)
    print(json.dumps({"queue_sha256": hashlib.sha256(raw).hexdigest(), "finished_utc": now(),
                      "verified_download_bytes": TOTAL_CAP - remaining, "observations": done}, separators=(",", ":")))
