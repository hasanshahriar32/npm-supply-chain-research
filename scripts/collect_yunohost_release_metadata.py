#!/usr/bin/env python3
"""Collect release and exact-digest attestation metadata from the public GitHub API."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
from urllib.parse import quote

from collect_yunohost_observations import fetch, now, sha256

REPOSITORY = re.compile(r"[a-z0-9_.-]+/[a-z0-9_.-]+")
SHA256 = re.compile(r"[a-f0-9]{64}")
SIDECAR = re.compile(r"\b(?:sbom|spdx|cyclonedx|cdx|provenance|intoto|attestation)\b", re.I)
STATEMENT_TYPES = {"https://in-toto.io/Statement/v0.1", "https://in-toto.io/Statement/v1"}


def url_for(stage, item):
    repo = item["repo"]
    if not REPOSITORY.fullmatch(repo) or any(p in {"", ".", ".."} for p in repo.split("/")):
        raise ValueError("Invalid public GitHub repository")
    root = f"https://api.github.com/repos/{repo}"
    if stage == "release":
        tag = item["tag"]
        if not tag or len(tag) > 160 or any(ord(c) < 32 for c in tag):
            raise ValueError("Invalid release tag")
        return root + "/releases/tags/" + quote(tag, safe="")
    if stage == "subject" and SHA256.fullmatch(item["digest"]):
        return root + "/attestations/sha256:" + item["digest"]
    raise ValueError("Invalid subject request")


def releases(doc, item):
    assets = doc.get("assets")
    if doc.get("tag_name") != item["tag"] or doc.get("draft") is not False or not isinstance(assets, list):
        return {"status": "unexpected_release"}
    rows = []
    for asset in assets:
        url, name, size = (asset.get(k) for k in ("browser_download_url", "name", "size"))
        if not isinstance(url, str) or not isinstance(name, str) or not isinstance(size, int):
            continue
        sha = asset.get("digest")
        rows.append({"url": url, "name": name, "size": size, "digest": sha if isinstance(sha, str) else None,
                     "metadata_name_signal": bool(SIDECAR.search(name))})
    return {"status": "observed", "assets": rows}


def bound_statement(bundle, expected):
    if not isinstance(bundle, dict):
        return None
    envelope = bundle.get("dsseEnvelope")
    if not isinstance(envelope, dict) or envelope.get("payloadType") != "application/vnd.in-toto+json":
        return None
    try:
        statement = json.loads(base64.b64decode(envelope["payload"], validate=True))
    except (KeyError, ValueError, TypeError, UnicodeDecodeError):
        return None
    if not isinstance(statement, dict) or statement.get("_type") not in STATEMENT_TYPES:
        return None
    subjects = statement.get("subject")
    if not isinstance(subjects, list):
        return None
    if not any(isinstance(s, dict) and isinstance(s.get("digest"), dict)
               and s["digest"].get("sha256") == expected for s in subjects):
        return None
    kind = statement.get("predicateType")
    if not isinstance(kind, str) or len(kind) > 240:
        return None
    classifier = "other"
    if kind.startswith("https://slsa.dev/provenance/"):
        classifier = "provenance"
    if kind.startswith(("https://spdx.dev/Document", "https://cyclonedx.org/bom")):
        classifier = "sbom"
    return {"predicate_type": kind, "class": classifier}


def attestations(doc, item):
    rows = doc.get("attestations")
    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
        return {"status": "unexpected_attestation_list"}
    matches = [a for row in rows if (a := bound_statement(row.get("bundle"), item["digest"])) is not None]
    if not rows:
        return {"status": "empty_public_list", "bundles_returned": 0}
    return {"status": "digest_bound_statement" if matches else "bundle_returned_without_parsed_match",
            "bundles_returned": len(rows), "matching_statements": matches}


def observe(stage, item):
    receipt, payload = fetch(url_for(stage, item), 2 * 1024 * 1024)
    row = {"request": item, "receipt": receipt}
    if payload is None:
        return {**row, "status": receipt["status"] + "_" + str(receipt.get("http_status", "unknown"))}
    try:
        doc = json.loads(payload)
    except (ValueError, UnicodeDecodeError):
        return {**row, "status": "invalid_response"}
    if not isinstance(doc, dict):
        return {**row, "status": "invalid_response"}
    return {**row, **(releases(doc, item) if stage == "release" else attestations(doc, item))}


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("stage", choices=("release", "subject"))
    cli.add_argument("queue", type=Path)
    args = cli.parse_args()
    raw = args.queue.read_bytes()
    requests = json.loads(raw)["requests"]
    urls = {url_for(args.stage, item) for item in requests}
    if len(urls) != len(requests) or len(urls) > 65:
        raise ValueError("Unexpected request count")
    with ThreadPoolExecutor(max_workers=4) as pool:
        observations = list(pool.map(lambda item: observe(args.stage, item), requests))
    print(json.dumps({"queue_sha256": sha256(raw).hexdigest(), "finished_utc": now(), "observations": observations},
                     separators=(",", ":")))
