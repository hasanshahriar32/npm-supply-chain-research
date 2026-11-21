#!/usr/bin/env python3
"""Check the declared archive and inventory packaging patches for named importers."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile
from urllib.parse import quote

from collect_yunohost_observations import REPO, fetch, now
from collect_yunohost_packaging import COMMIT, PACKAGING_REPO
from collect_yunohost_deployment_sources import TAG

ARCHIVE_CAP = 24 * 1024 * 1024
FILES_CAP = 128 * 1024 * 1024
PATCH_NAME = re.compile(r"patches/(?:main/)?[a-zA-Z0-9_.-]+\.patch")


class ByteLimit:
    def __init__(self, stream, limit):
        self.stream = stream
        self.remaining = limit

    def read(self, size):
        blob = self.stream.read(min(size, self.remaining + 1))
        self.remaining -= len(blob)
        if self.remaining < 0:
            raise ValueError("Archive exceeds the decompressed byte limit")
        return blob


def archive_files(blob, paths):
    needed = set(paths)
    hashes = {}
    with gzip.GzipFile(fileobj=io.BytesIO(blob)) as uncompressed:
        with tarfile.open(fileobj=ByteLimit(uncompressed, FILES_CAP), mode="r|") as archive:
            for item in archive:
                _, _, relative = item.name.partition("/")
                if relative not in needed:
                    continue
                if relative in hashes or not item.isreg() or item.size > 6 * 1024 * 1024:
                    raise ValueError("Invalid selected archive member")
                with archive.extractfile(item) as source:
                    hashes[relative] = hashlib.sha256(source.read()).hexdigest()
    return hashes


def observe(row):
    repo, ref = row["upstream"], row["ref"]
    package, commit = row["packaging_repository"], row["packaging_commit"]
    if (not REPO.fullmatch(repo) or not TAG.fullmatch(ref) or ".." in ref
            or not PACKAGING_REPO.fullmatch(package) or not COMMIT.fullmatch(commit)):
        raise ValueError("Unexpected archive or packaging revision")
    spec = "refs/tags/" + ref if row["ref_kind"] == "tag" else ref
    archive_url = f"https://codeload.github.com/{repo}/tar.gz/{quote(spec, safe='/@')}"
    archive, blob = fetch(archive_url, ARCHIVE_CAP)
    hashes = {}
    if blob is not None:
        if archive["sha256"] != row["archive_sha256"]:
            archive["status"] = "checksum_differs"
        else:
            try:
                hashes = archive_files(blob, row["paths"])
            except (ValueError, OSError, tarfile.TarError, EOFError):
                archive["status"] = "archive_member_scan_unresolved"
    tree_url = f"https://api.github.com/repos/{package}/git/trees/{commit}?recursive=1"
    tree, contents = fetch(tree_url, 512_000)
    patches = []
    if contents is not None:
        doc = json.loads(contents)
        if doc.get("truncated") is not False or not isinstance(doc.get("tree"), list):
            tree["status"] = "incomplete_tree"
        else:
            patches = sorted(item["path"] for item in doc["tree"] if PATCH_NAME.fullmatch(item["path"]))
    return {**row, "archive": archive, "member_sha256": hashes, "packaging_tree": tree, "patches": patches}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("queue", type=Path)
    args = cli.parse_args()
    raw = args.queue.read_bytes()
    rows = json.loads(raw)["rows"]
    if len(rows) != 3 or any(len(r["paths"]) > 6 for r in rows):
        raise ValueError("Unexpected archive check scope")
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(observe, rows))
    print(json.dumps({"queue_sha256": hashlib.sha256(raw).hexdigest(), "finished_utc": now(),
                      "rows": results}, separators=(",", ":")))


if __name__ == "__main__":
    main()
