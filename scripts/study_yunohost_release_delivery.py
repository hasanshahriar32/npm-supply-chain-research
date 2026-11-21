#!/usr/bin/env python3
"""Audit exact release assets selected by pinned YunoHost recipes."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime
import re
import tomllib
from urllib.parse import unquote, urlsplit

from study_yunohost_importer_frame import RECEIPTS as RECIPE_RECEIPTS, ROOT, RUN as FRAME, evidence, now, read, sha, write

RUN = FRAME.with_name("yunohost-release-delivery")
PRIVATE = RUN / "private"
FRAME_LABELS = FRAME / "recipes.json"
QUEUE = RUN / "release_queue.json"
RELEASES = PRIVATE / "releases.json"
SUBJECT_QUEUE = RUN / "subject_queue.json"
SUBJECTS = PRIVATE / "subjects.json"
RESULT = RUN / "results.json"
SOURCE_COMMAND = re.compile(r"^\s*(?:(?:ynh_exec_as_app|ynh_hide_warnings)\s+)*ynh_setup_source(?:\s|$)")
SOURCE_OPT = re.compile(r"""(?:^|\s)--source_id(?:=|\s+)(?:"([^"]+)"|'([^']+)'|([^\s]+))""")
LITERAL = re.compile(r"[A-Za-z0-9_-]+")
GITHUB_REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
SHA256 = re.compile(r"[a-f0-9]{64}")


def asset_key(url):
    parsed = urlsplit(url)
    parts = parsed.path.split("/")
    if (parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.query or parsed.fragment
            or len(parts) != 7 or parts[3:5] != ["releases", "download"]):
        return None
    repo = "/".join(parts[1:3]).casefold()
    tag, name = map(unquote, parts[5:7])
    if not GITHUB_REPO.fullmatch(repo) or any(p in {"", ".", ".."} for p in repo.split("/")):
        return None
    if not tag or not name or "/" in name or any(ord(c) < 32 for c in tag + name):
        return None
    return repo, tag, name


def source_calls(files):
    calls = defaultdict(list)
    for path in ("scripts/install", "scripts/_common.sh"):
        for n, line in enumerate(files.get(path, "").splitlines(), 1):
            if not SOURCE_COMMAND.match(line):
                continue
            option = SOURCE_OPT.search(line)
            if option:
                source = next(value for value in option.groups() if value)
            elif "--source_id" in line:
                continue
            else:
                source = "main"
            if LITERAL.fullmatch(source):
                calls[source].append({"path": path, "line": n})
    return calls


def inputs():
    return {str(p.relative_to(ROOT)): sha(p) for p in (
        FRAME_LABELS, RECIPE_RECEIPTS, ROOT / "scripts/study_yunohost_release_delivery.py",
        ROOT / "scripts/collect_yunohost_release_metadata.py",
    )}


def freeze():
    if QUEUE.exists():
        raise ValueError("Release sample already frozen")
    labels = read(FRAME_LABELS)
    assert labels["receipts_sha256"] == sha(RECIPE_RECEIPTS)
    eligible = {r["sample_id"] for r in labels["projects"]
                if r["status"] == "release_asset_declared_without_matched_js_command"}
    rows, tags = [], set()
    for row, files, receipts in evidence():
        if row["sample_id"] not in eligible:
            continue
        manifest = tomllib.loads(files["manifest.toml"])
        resources = manifest["resources"]["sources"]
        calls = source_calls(files)
        items = []
        for source, locations in calls.items():
            config = resources.get(source, {})
            arch = config.get("amd64", {})
            # An architecture-specific resource may be unavailable on amd64.
            asset = arch if arch else config
            key = asset_key(asset.get("url", ""))
            if not key:
                continue
            repo, tag, name = key
            expected = asset.get("sha256", "").lower()
            if not SHA256.fullmatch(expected):
                expected = None
            tags.add((repo, tag))
            items.append({"source_id": source, "release_repo": repo, "tag": tag, "asset": name, "recipe_sha256": expected,
                          "evidence": [{**location, "sha256": receipts[location["path"]]["sha256"]}
                                       for location in locations]})
        rows.append({**row, "assets": items, "literal_sources": len(calls)})
    assert len(rows) == len(eligible) == 39
    PRIVATE.mkdir(parents=True, exist_ok=True)
    write(QUEUE, {"frozen_utc": now(), "inputs": inputs(), "projects": rows,
                  "requests": [{"repo": repo, "tag": tag} for repo, tag in sorted(tags)],
                  "scope": "All 39 release-declaration flags without a matched JavaScript command in the 99-recipe sample. "
                           "Audit literal install/common setup-source references, amd64 fields taking precedence. "
                           "Multiple named resources remain separate, including helpers and conditional variants. "
                           "Only exact GitHub release downloads. Never assume that a release tag is artifact provenance."})
    print("Recipes", len(rows), "with exact GitHub asset references", sum(bool(r["assets"]) for r in rows),
          "release lookups", len(tags))


def read_collection(queue_path, receipt_path):
    queue, received = read(queue_path), read(receipt_path)
    assert received["queue_sha256"] == sha(queue_path)
    start, end = map(datetime.fromisoformat, (queue["frozen_utc"], received["finished_utc"]))
    for request, observation in zip(queue["requests"], received["observations"], strict=True):
        assert observation["request"] == request
        assert start <= datetime.fromisoformat(observation["receipt"]["observed_at_utc"]) <= end
    return queue, received["observations"]


def evidence_index():
    queue, rows = read_collection(QUEUE, RELEASES)
    assert queue["inputs"] == inputs()
    releases = {(r["request"]["repo"], r["request"]["tag"]): r for r in rows}
    joined = []
    for project in queue["projects"]:
        for asset in project["assets"]:
            repo, tag, name = (asset[k] for k in ("release_repo", "tag", "asset"))
            release = releases[repo, tag]
            seen = [a for a in release.get("assets", []) if asset_key(a["url"]) == (repo, tag, name) and a["name"] == name]
            status, actual = release["status"], None
            if status == "observed":
                status = "asset_not_identified"
                if len(seen) == 1:
                    actual, = seen
                    api_digest = actual.get("digest")
                    if not api_digest or not asset["recipe_sha256"]:
                        status = "digest_unavailable"
                    elif api_digest == "sha256:" + asset["recipe_sha256"]:
                        status = "digest_agrees"
                    else:
                        status = "digest_differs"
            joined.append({**asset, "sample_id": project["sample_id"], "asset_status": status, "release_asset": actual})
    return queue, rows, joined


def subjects():
    if SUBJECT_QUEUE.exists():
        raise ValueError("Subject queue already frozen")
    _, _, joined = evidence_index()
    keys = {(row["release_repo"], row["recipe_sha256"]) for row in joined if row["asset_status"] == "digest_agrees"}
    items = [{"repo": repo, "digest": digest} for repo, digest in sorted(keys)]
    write(SUBJECT_QUEUE, {"frozen_utc": now(), "release_receipts_sha256": sha(RELEASES), "requests": items,
                          "scope": "Public repository attestation list by the agreed digest. Parse returned statements "
                                   "for exact subject binding and declared predicate class. No signature verification."})
    print("Attestation subject lookups", len(items))


def score():
    queue, releases, joined = evidence_index()
    scope, statements = read_collection(SUBJECT_QUEUE, SUBJECTS)
    assert scope["release_receipts_sha256"] == sha(RELEASES)
    observations = {(r["request"]["repo"], r["request"]["digest"]): r for r in statements}
    for row in joined:
        if row["asset_status"] == "digest_agrees":
            lookup = observations[row["release_repo"], row["recipe_sha256"]]
            row["attestation_lookup"] = lookup["status"]
            row["bound_claims"] = lookup.get("matching_statements", [])
    write(RESULT, {"recipes": len(queue["projects"]), "release_receipts_sha256": sha(RELEASES),
                   "subject_receipts_sha256": sha(SUBJECTS),
                   "recipes_with_direct_assets": sum(bool(p["assets"]) for p in queue["projects"]),
                   "release_states": dict(Counter(r["status"] for r in releases)),
                   "asset_states": dict(Counter(a["asset_status"] for a in joined)),
                   "subject_states": dict(Counter(r["status"] for r in statements)),
                   "digest_bound_statements": sum(len(r.get("matching_statements", [])) for r in statements),
                   "projects": [{"sample_id": p["sample_id"], "assets": [a for a in joined if a["sample_id"] == p["sample_id"]]}
                                for p in queue["projects"]]})
    print({k: v for k, v in read(RESULT).items() if k != "projects"})


if __name__ == "__main__":
    stages = {"freeze": freeze, "subjects": subjects, "score": score}
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("stage", choices=tuple(stages))
    stages[cli.parse_args().stage]()
