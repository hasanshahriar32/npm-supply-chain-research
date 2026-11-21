#!/usr/bin/env python3
"""Collect exact-version metadata for the frozen Yarn Classic path queue."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

from collect_yunohost_observations import fetch, now, sha256, url_for


def string_map(value):
    return value if isinstance(value, dict) and all(isinstance(v, str) for v in value.values()) else None


def observe(entry):
    receipt, payload = fetch(url_for("registry", entry), 4 * 1024 * 1024)
    row = {**entry, **receipt}
    if payload is None:
        return row
    try:
        doc = json.loads(payload)
    except (UnicodeDecodeError, ValueError):
        return {**row, "status": "invalid_json"}
    if not isinstance(doc, dict) or (doc.get("name"), doc.get("version")) != (entry["package"], entry["version"]):
        return {**row, "status": "package_identity_mismatch"}
    members = doc.get("maintainers")
    usable = isinstance(members, list) and all(isinstance(m, dict) and isinstance(m.get("name"), str)
                                               and m["name"] for m in members)
    dist = doc.get("dist")
    return {
        **row, "status": "observed", "accounts": sorted({m["name"] for m in members}) if usable else None,
        "integrity": dist.get("integrity") if isinstance(dist, dict) else None,
        "conditional": any(bool(doc.get(k)) for k in ("os", "cpu", "libc")),
        "bundles_dependencies": bool(doc.get("bundleDependencies") or doc.get("bundledDependencies")),
        "dependencies": string_map(doc.get("dependencies", {})),
        "optional_dependencies": string_map(doc.get("optionalDependencies", {})),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue", type=Path)
    args = parser.parse_args()
    raw = args.queue.read_bytes()
    queue = json.loads(raw)
    requests = queue["requests"]
    urls = [url_for("registry", item) for item in requests]
    if queue["stage"] != "yarn_classic_registry" or len(set(urls)) != len(urls) or len(urls) > 26000:
        raise ValueError("Unexpected Yarn registry queue")
    with ThreadPoolExecutor(max_workers=8) as pool:
        observations = list(pool.map(observe, requests))
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), "finished_utc": now(),
                      "observations": observations}, separators=(",", ":")))


if __name__ == "__main__":
    main()
