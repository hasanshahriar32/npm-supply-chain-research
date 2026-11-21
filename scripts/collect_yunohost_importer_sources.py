#!/usr/bin/env python3
"""Verify archived sources and retain only commit-matched dependency metadata."""
import base64
from concurrent.futures import ThreadPoolExecutor
import gzip
from hashlib import sha256
import io
import json
from pathlib import Path
import sys
import tarfile
from urllib.parse import quote
from zipfile import BadZipFile, ZipFile

from collect_yunohost_deployment_sources import resolve, url_for
from collect_yunohost_observations import fetch, now
from collect_yunohost_packaging import COMMIT, PACKAGING_REPO
from verify_yunohost_deployment_archives import ARCHIVE_CAP, ByteLimit, FILES_CAP


def tar_hashes(body, wanted, unpacked_cap):
    found = {}
    with gzip.GzipFile(fileobj=io.BytesIO(body)) as unpacked:
        with tarfile.open(fileobj=ByteLimit(unpacked, unpacked_cap), mode="r|") as archive:
            for item in archive:
                _, _, path = item.name.partition("/")
                if path not in wanted:
                    continue
                if path in found or not item.isreg() or item.size > 6 * 1024 * 1024:
                    raise ValueError("Invalid TAR member")
                with archive.extractfile(item) as member:
                    found[path] = sha256(member.read()).hexdigest()
    return found


def raw_url(repo, commit, path):
    if path.split("/")[-1] == "yarn.lock":
        validated = url_for(repo, commit, path[:-len("yarn.lock")] + "package.json")
        return validated[:-len("package.json")] + "yarn.lock"
    return url_for(repo, commit, path)


def zip_hashes(body, wanted):
    found = {}
    with ZipFile(io.BytesIO(body)) as archive:
        for item in archive.infolist():
            _, _, path = item.filename.partition("/")
            if path not in wanted:
                continue
            if path in found or item.file_size > 6 * 1024 * 1024:
                raise ValueError("Invalid ZIP member")
            found[path] = sha256(archive.read(item)).hexdigest()
    return found


def observe(row, cap, unpacked_cap):
    repo, kind, ref = row["upstream"], row["ref_kind"], row["ref"]
    packaging, pin = row["packaging_repository"], row["packaging_commit"]
    if not PACKAGING_REPO.fullmatch(packaging) or not COMMIT.fullmatch(pin):
        raise ValueError("Invalid packaging Git location")
    resolved = resolve(repo, kind, ref)
    output = {"sample_id": row["sample_id"], "resolved": resolved, "files": {}, "observed_at_utc": now()}
    if "commit" not in resolved:
        return {**output, "status": "source_commit_unresolved"}
    ref_path = "refs/tags/" + ref if kind == "tag" else ref
    archive_kind = {".tar.gz": "tar.gz", ".zip": "zip"}[row["archive_type"]]
    archive, body = fetch(f"https://codeload.github.com/{repo}/{archive_kind}/{quote(ref_path, safe='/@')}", cap)
    output["archive"] = archive
    if body is None or archive["sha256"] != row["archive_sha256"]:
        return {**output, "status": "archive_unavailable_or_hash_differs"}
    try:
        hashes = (zip_hashes(body, row["members"]) if archive_kind == "zip"
                  else tar_hashes(body, row["members"], unpacked_cap))
    except (OSError, ValueError, EOFError, BadZipFile, tarfile.TarError) as exc:
        return {**output, "status": "archive_scan_unresolved", "error_type": type(exc).__name__}
    del body
    output["archive_members"] = hashes
    tree_url = f"https://api.github.com/repos/{packaging}/git/trees/{pin}?recursive=1"
    tree, tree_body = fetch(tree_url, 512_000)
    output["packaging_tree"] = tree
    if tree_body is None:
        return {**output, "status": "patch_inventory_unavailable"}
    tree_data = json.loads(tree_body)
    if tree_data.get("truncated") is not False or not isinstance(tree_data.get("tree"), list):
        return {**output, "status": "patch_inventory_incomplete"}
    patches = sorted(i["path"] for i in tree_data["tree"] if i["path"].startswith("patches/"))
    output["patch_paths"] = patches
    for path in hashes:
        receipt, data = fetch(raw_url(repo, resolved["commit"], path), 6 * 1024 * 1024)
        if data is not None and receipt["sha256"] == hashes[path]:
            receipt["body_base64"] = base64.b64encode(data).decode()
        output["files"][path] = receipt
    return {**output, "status": "patches_present" if patches else "verified_archive"}


if __name__ == "__main__":
    raw = Path(sys.argv[1]).read_bytes()
    queue = json.loads(raw)
    projects = queue["projects"]
    if not 1 <= len(projects) <= 12 or any(len(row["members"]) > 16 for row in projects):
        raise ValueError("Source batch exceeds scope")
    retry = queue.get("retry_reason") == "compressed_size_limit"
    if retry and (len(projects) > 2 or any(r["manager"] not in ("npm", "pnpm") for r in projects)):
        raise ValueError("Retry accepts at most two supported-manager projects")
    cap, unpacked_cap = (128 * 1024**2, 768 * 1024**2) if retry else (ARCHIVE_CAP, FILES_CAP)
    with ThreadPoolExecutor(max_workers=1 if retry else 3) as pool:
        rows = list(pool.map(lambda row: observe(row, cap, unpacked_cap), projects))
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), "finished_utc": now(), "observations": rows},
                     separators=(",", ":")))
