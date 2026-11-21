#!/usr/bin/env python3
"""Check what the two candidate archives actually record about dependency identity."""
import argparse
from collections import Counter
import gzip
from hashlib import sha256
import io
import json
from pathlib import Path, PurePosixPath
import re
import tarfile
from urllib.parse import urlsplit
from urllib.request import Request, build_opener

from collect_yunohost_observations import now
from collect_yunohost_release_archive_evidence import CAP, LOCKFILES, ReleaseRedirect, UNPACKED_CAP
from verify_yunohost_deployment_archives import ByteLimit

META_CAP = 2 * 1024 * 1024
SHA512 = re.compile(r"\bsha512-[A-Za-z0-9+/]{86}==")


def classify(body):
    counts, lockfiles = Counter(), []
    with gzip.GzipFile(fileobj=io.BytesIO(body)) as source:
        with tarfile.open(fileobj=ByteLimit(source, UNPACKED_CAP), mode="r|") as archive:
            for member in archive:
                path = PurePosixPath(member.name)
                if not member.isreg() or member.size > META_CAP or path.is_absolute() or ".." in path.parts:
                    continue
                if path.name not in LOCKFILES | {"package.json"}:
                    continue
                with archive.extractfile(member) as file:
                    data = file.read()
                if path.name == "package.json":
                    try:
                        doc = json.loads(data)
                    except (ValueError, UnicodeDecodeError):
                        counts["invalid_package_json"] += 1
                        continue
                    if not isinstance(doc, dict):
                        counts["invalid_package_json"] += 1
                        continue
                    if "node_modules" in path.parts:
                        counts["bundled_manifests"] += 1
                        if isinstance(doc.get("name"), str) and isinstance(doc.get("version"), str):
                            counts["bundled_named_versions"] += 1
                        for field in ("_integrity", "integrity"):
                            if isinstance(doc.get(field), str) and SHA512.search(doc[field]):
                                counts["bundled_sha512_indicators"] += 1
                                break
                        if isinstance(doc.get("_resolved"), str) and doc["_resolved"].startswith("https://registry.npmjs.org/"):
                            counts["bundled_public_resolved_urls"] += 1
                    else:
                        counts["standalone_manifests"] += 1
                        deps = doc.get("dependencies")
                        if isinstance(deps, dict) and deps:
                            counts["standalone_manifests_with_regular_dependencies"] += 1
                elif "node_modules" not in path.parts:
                    content = data.decode("utf-8", errors="replace")
                    classic = "# yarn lockfile v1" in content.splitlines()[:4]
                    lockfiles.append({"path": str(path), "sha256": sha256(data).hexdigest(),
                                      "yarn_classic_header": classic,
                                      "sha512_indicators": len(SHA512.findall(content))})
    return {"counts": dict(counts), "lockfiles": lockfiles}


def observe(item):
    url = urlsplit(item["url"])
    if (url.scheme != "https" or url.netloc != "github.com" or "/releases/download/" not in url.path
            or url.query or url.fragment or not item["asset"].endswith((".tar.gz", ".tgz"))):
        raise ValueError("Unexpected archive asset")
    observed_at = now()
    request = Request(item["url"], headers={"User-Agent": "npm-consumer-study/1"})
    with build_opener(ReleaseRedirect()).open(request, timeout=35) as response:
        body = response.read(CAP + 1)
    actual = sha256(body).hexdigest()
    if len(body) > CAP or actual != item["recipe_sha256"]:
        raise ValueError("Archive is outside the cap or differs from the pinned recipe")
    return {"request": item, "observed_at_utc": observed_at, "sha256": actual, **classify(body)}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("queue", type=Path)
    args = cli.parse_args()
    raw = args.queue.read_bytes()
    items = json.loads(raw)["requests"]
    if len(items) != 2 or sum(row["listed_size"] for row in items) > CAP:
        raise ValueError("Unexpected detailed archive scope")
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), "rows": [observe(item) for item in items],
                      "finished_utc": now()}, separators=(",", ":")))
