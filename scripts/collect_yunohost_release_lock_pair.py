#!/usr/bin/env python3
"""Compare the verified release's npm metadata with its tag-resolved Git files."""
import argparse
import base64
import gzip
import io
import json
from pathlib import Path, PurePosixPath
import tarfile
from urllib.parse import urlsplit
from urllib.request import Request, build_opener

from collect_yunohost_importer_sources import raw_url
from collect_yunohost_deployment_sources import resolve
from collect_yunohost_observations import fetch, now, sha256
from collect_yunohost_release_archive_evidence import CAP, ReleaseRedirect, UNPACKED_CAP
from verify_yunohost_deployment_archives import ByteLimit

REPO = "pterodactyl/panel"
TAG = "v1.15.1"
URL = f"https://github.com/{REPO}/releases/download/{TAG}/panel.tar.gz"
FILES = {"package.json", "yarn.lock"}


def scan(body):
    fields, bundles = {}, set()
    with gzip.GzipFile(fileobj=io.BytesIO(body)) as stream:
        with tarfile.open(fileobj=ByteLimit(stream, UNPACKED_CAP), mode="r|") as archive:
            for member in archive:
                if not member.isreg():
                    continue
                path = PurePosixPath(member.name)
                if path.is_absolute() or ".." in path.parts:
                    continue
                if str(path) in FILES:
                    key = str(path)
                    if key in fields or member.size > 2 * 1024 * 1024:
                        raise ValueError("Duplicate or oversized dependency metadata")
                    with archive.extractfile(member) as file:
                        blob = file.read()
                    fields[key] = {"sha256": sha256(blob).hexdigest(), "body": base64.b64encode(blob).decode()}
                elif str(path).startswith("public/assets/") and path.suffix == ".js":
                    bundles.add(str(path))
    return fields, len(bundles)


def collect(item):
    if item["url"] != URL or item["asset"] != "panel.tar.gz":
        raise ValueError("Unexpected release asset")
    recorded = now()
    with build_opener(ReleaseRedirect()).open(Request(URL, headers={"User-Agent": "npm-consumer-study/1"}),
                                              timeout=35) as response:
        body = response.read(CAP + 1)
    digest = sha256(body).hexdigest()
    if len(body) > CAP or digest != item["recipe_sha256"]:
        raise ValueError("Release differs from the packaging pin")
    archive, bundles = scan(body)
    if set(archive) != FILES:
        raise ValueError("Expected both dependency files in the release archive")
    source, ref = {}, resolve(REPO, "tag", TAG)
    if "commit" in ref:
        for name in sorted(FILES):
            receipt, blob = fetch(raw_url(REPO, ref["commit"], name), 2 * 1024 * 1024)
            if blob is not None:
                receipt["body"] = base64.b64encode(blob).decode()
            source[name] = receipt
    return {"observed_at_utc": recorded, "finished_utc": now(), "archive_sha256": digest, "archive": archive,
            "public_asset_js_files": bundles, "tag_resolution": ref, "source": source}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("queue", type=Path)
    args = cli.parse_args()
    raw = args.queue.read_bytes()
    req = json.loads(raw)["request"]
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), **collect(req)}, separators=(",", ":")))
