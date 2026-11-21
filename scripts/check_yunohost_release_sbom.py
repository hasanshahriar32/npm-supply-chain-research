#!/usr/bin/env python3
"""Inspect the matched architecture's public SBOM candidates for artifact binding."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, build_opener

from collect_yunohost_observations import now
from collect_yunohost_release_archive_evidence import ReleaseRedirect


def nodes(value):
    pending = [value]
    while pending:
        current = pending.pop()
        yield current
        if isinstance(current, dict):
            pending.extend(current.values())
        elif isinstance(current, list):
            pending.extend(current)


def matches_component(node, name, digest):
    if not isinstance(node, dict) or not isinstance(node.get("hashes"), list):
        return False
    properties = node.get("properties")
    has_filename = isinstance(properties, list) and any(
        isinstance(p, dict) and p.get("name") == "Filename" and p.get("value") == name for p in properties
    )
    return (node.get("name") == name or has_filename) and any(
        isinstance(h, dict) and h.get("alg") == "SHA-256" and h.get("content") == digest for h in node["hashes"]
    )


def observe(item):
    url = urlsplit(item["url"])
    if (url.scheme != "https" or url.netloc != "github.com" or "/releases/download/" not in url.path
            or url.query or url.fragment or not item["name"].endswith(".json")):
        raise ValueError("Unexpected SBOM download")
    started = now()
    cap = 2 * 1024 * 1024
    req = Request(item["url"], headers={"User-Agent": "npm-consumer-study/1"})
    with build_opener(ReleaseRedirect()).open(req, timeout=30) as response:
        body = response.read(cap + 1)
    digest = sha256(body).hexdigest()
    if len(body) > cap or (item["api_digest"] and "sha256:" + digest != item["api_digest"]):
        raise ValueError("Document cap or release checksum check failed")
    doc = json.loads(body)
    values = {node for node in nodes(doc) if isinstance(node, str)}
    matches = sum(matches_component(node, item["selected_asset"], item["selected_sha256"]) for node in nodes(doc))
    return {"request": item, "observed_at_utc": started, "sha256": digest,
            "format": doc.get("bomFormat") or doc.get("spdxVersion"),
            "lists_selected_asset_name": item["selected_asset"] in values,
            "lists_selected_sha256": any(v.casefold().removeprefix("sha256:") == item["selected_sha256"] for v in values),
            "matching_name_and_hash_objects": matches,
            "npm_purl_strings": sum(v.startswith("pkg:npm/") for v in values)}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("queue", type=Path)
    args = cli.parse_args()
    raw = args.queue.read_bytes()
    rows = json.loads(raw)["requests"]
    if len(rows) != 2:
        raise ValueError("Unexpected sidecar scope")
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), "rows": [observe(r) for r in rows],
                      "finished_utc": now()}, separators=(",", ":")))
