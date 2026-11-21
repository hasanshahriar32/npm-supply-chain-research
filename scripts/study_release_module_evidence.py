#!/usr/bin/env python3
"""Audit bundle maps and compare physically packaged direct dependency files."""
import argparse
import base64
from collections import Counter
from datetime import datetime
import gzip
import io
import json
from pathlib import PurePosixPath
import re
import subprocess
import tarfile

from collect_release_registry_file_hashes import UNPACKED_CAP, file_hashes
from collect_yunohost_observations import url_for
from study_yunohost_holdout import INCIDENCE, ROOT, digest, frozen_portfolios, now, read, sha, write
from study_yunohost_release_delivery import RUN as DELIVERY
from verify_yunohost_deployment_archives import ByteLimit

RUN = DELIVERY.with_name("yunohost-release-modules")
QUEUE = RUN / "archive_queue.json"
CAPTURE = RUN / "private/archives.json"
MANIFEST = RUN / "module_inputs.json"
REGISTRY_QUEUE = RUN / "registry_queue.json"
REGISTRY = RUN / "private/registry.json"
RESULTS = RUN / "results.json"
JS = re.compile(r"\.js$")


def archives():
    queue, record = read(QUEUE), read(CAPTURE)
    assert queue["embedded_queue_sha256"] == sha(DELIVERY / "embedded_queue.json")
    assert queue["lock_results_sha256"] == sha(DELIVERY.with_name("yunohost-release-lock") / "results.json")
    assert record["queue_sha256"] == sha(QUEUE)
    begin, end = map(datetime.fromisoformat, (queue["frozen_utc"], record["finished_utc"]))
    output = {}
    for expected, item in zip(queue["requests"], record["archives"], strict=True):
        assert begin <= datetime.fromisoformat(item["observed_at_utc"]) <= end
        assert item["request"] == expected
        body = base64.b64decode(item["body"], validate=True)
        assert digest(body) == expected["recipe_sha256"] == item["sha256"] and len(body) == item["size"]
        output[expected["sample_id"]] = body
    config = record["webpack_config"]
    content = base64.b64decode(config["body"], validate=True)
    assert config["url"] == f"https://raw.githubusercontent.com/pterodactyl/panel/{queue['panel_commit']}/webpack.config.js"
    assert config["http_status"] == 200 and digest(content) == config["sha256"]
    return output, config["sha256"], content.decode()


def panel_assets(body, config_sha, config):
    maps, js, notices = [], [], []
    with gzip.GzipFile(fileobj=io.BytesIO(body)) as stream:
        with tarfile.open(fileobj=ByteLimit(stream, UNPACKED_CAP), mode="r|") as archive:
            for member in archive:
                path = PurePosixPath(member.name)
                if not member.isreg() or path.is_absolute() or ".." in path.parts or path.parts[:2] != ("public", "assets"):
                    continue
                name = str(path)
                if path.suffix == ".map":
                    maps.append(name)
                if "license" in path.name.casefold() or "notice" in path.name.casefold():
                    notices.append(name)
                if JS.search(name):
                    with archive.extractfile(member) as file:
                        code = file.read()
                    js.append({"file": name, "sha256": digest(code), "size": len(code),
                               "source_mapping_url_markers": code.count(b"sourceMappingURL"),
                               "source_url_markers": code.count(b"sourceURL"),
                               "literal_node_modules_markers": code.count(b"node_modules/"),
                               "license_markers": code.count(b"@license")})
    return {"assets": sorted(js, key=lambda row: row["file"]), "map_members": sorted(maps),
            "notice_members": sorted(notices), "webpack_sha256": config_sha,
            "source_map_settings": [{"line": n, "line_sha256": digest(line.encode()),
                                     "production_default_false": "isProduction ? false" in line}
                                    for n, line in enumerate(config.splitlines(), 1)
                                    if re.search(r"\b(?:devtool|sourceMap):", line)]}


def direct_manifests(body):
    manifests = {}
    with gzip.GzipFile(fileobj=io.BytesIO(body)) as stream:
        with tarfile.open(fileobj=ByteLimit(stream, UNPACKED_CAP), mode="r|") as archive:
            for member in archive:
                path = PurePosixPath(member.name)
                if path.is_absolute() or ".." in path.parts:
                    raise ValueError("Unexpected archive path")
                parts = path.parts
                direct = len(parts) == 4 or (len(parts) == 5 and parts[2].startswith("@"))
                if str(path) != "package/package.json" and not (
                    path.name == "package.json" and direct and parts[:2] == ("package", "node_modules")
                ):
                    continue
                if not member.isreg() or member.size > 2 * 1024 * 1024 or str(path.parent) in manifests:
                    raise ValueError("Unsupported Node package manifest")
                with archive.extractfile(member) as file:
                    manifests[str(path.parent)] = json.loads(file.read())
    root = manifests["package"]
    declared = root["dependencies"].keys() - root.get("optionalDependencies", {}).keys()
    records = []
    for name in sorted(declared):
        path = "package/node_modules/" + name
        child = manifests.get(path, {})
        matches = child.get("name") == name and isinstance(child.get("version"), str)
        records.append({"package": name, "location": path, "declared": root["dependencies"][name],
                        "version": child["version"] if matches else None})
    return records


def ranges(records):
    code = """
const fs = require('node:fs'), path = require('node:path');
const npm = path.resolve(path.dirname(fs.realpathSync(process.execPath)), '../lib/node_modules/npm/package.json');
const semver = require('node:module').createRequire(npm)('semver');
const rows = JSON.parse(fs.readFileSync(0, 'utf8'));
console.log(JSON.stringify(rows.map(({declared, version}) =>
    Boolean(version && semver.validRange(declared) && semver.satisfies(version, declared)))));
"""
    output = subprocess.check_output(["node", "-e", code], text=True, input=json.dumps(records), timeout=20)
    values = json.loads(output)
    return [{**row, "range_matches": valid} for row, valid in zip(records, values, strict=True)]


def freeze():
    if REGISTRY_QUEUE.exists():
        raise ValueError("Registry comparison already frozen")
    data, config_sha, config = archives()
    panel = panel_assets(data["D095"], config_sha, config)
    candidates = ranges(direct_manifests(data["D058"]))
    request = [{"package": r["package"], "version": r["version"]} for r in candidates if r["range_matches"]]
    for row in request:
        url_for("registry", row)
    write(MANIFEST, {"archive_receipts_sha256": sha(CAPTURE), "panel": panel, "mongo_direct": candidates})
    write(REGISTRY_QUEUE, {"frozen_utc": now(), "module_inputs_sha256": sha(MANIFEST),
                           "training_sha256": sha(INCIDENCE), "requests": request,
                           "collector_sha256": sha(ROOT / "scripts/collect_release_registry_file_hashes.py"),
                           "scope": "All regular direct dependencies whose packaged name and version match the root range. "
                                    "Require canonical tarball and SHA-512, then equality of own regular-file paths and bytes. "
                                    "Exclude nested node_modules in both views. No execution or runtime inclusion claim."})
    print(len(panel["assets"]), "JS files", len(panel["map_members"]), "maps",
          sum(a["source_mapping_url_markers"] for a in panel["assets"]), "mapping markers")
    print(len(candidates), "direct names", len(request), "range-consistent exact versions")


def compare():
    queue, captured = read(REGISTRY_QUEUE), read(REGISTRY)
    assert queue["collector_sha256"] == sha(ROOT / "scripts/collect_release_registry_file_hashes.py")
    assert queue["module_inputs_sha256"] == sha(MANIFEST) and captured["queue_sha256"] == sha(REGISTRY_QUEUE)
    assert queue["training_sha256"] == sha(INCIDENCE)
    start, end = map(datetime.fromisoformat, (queue["frozen_utc"], captured["finished_utc"]))
    index = {}
    for request, item in zip(queue["requests"], captured["observations"], strict=True):
        assert request == item["request"] and item["registry_receipt"]["url"] == url_for("registry", request)
        assert start <= datetime.fromisoformat(item["observed_at_utc"]) <= end
        index[request["package"], request["version"]] = item
    archives_bytes, _, _ = archives()
    manifest = read(MANIFEST)
    assert manifest["archive_receipts_sha256"] == sha(CAPTURE)
    paths = [row["location"] for row in manifest["mongo_direct"] if row["range_matches"]]
    bundled = file_hashes(archives_bytes["D058"], paths)
    results, accounts = [], set()
    for row in manifest["mongo_direct"]:
        package = row["package"]
        item = index.get((package, row["version"]))
        outcome = row | {"status": "unresolved_name_version_or_range"}
        if item is not None:
            outcome["status"] = item["status"]
        if item and item["status"] == "verified_tarball":
            observed, published = bundled[row["location"]], item["own_files"]
            a, b = observed["files"], published["files"]
            outcome.update({"archive_own_files": len(a), "registry_own_files": len(b),
                            "identical_file_paths": a.keys() == b.keys(),
                            "changed_shared_files": sum(a[k] != b[k] for k in a.keys() & b.keys()),
                            "archive_only_files": len(a.keys() - b.keys()), "registry_only_files": len(b.keys() - a.keys())})
            if observed["unsupported_entries"] or published["unsupported_entries"] or "package.json" not in a or "package.json" not in b:
                outcome["status"] = "unsupported_file_entries"
            elif a != b:
                outcome["status"] = "files_differ"
            else:
                outcome["status"] = "own_files_match"
                if item["accounts"] is not None:
                    accounts.update(item["accounts"])
        results.append(outcome)
    maintainers, slots = frozen_portfolios()
    hits = {k: bool(accounts & {maintainers[i] for i in indexes}) for k, indexes in slots.items()}
    write(RESULTS, {"archive_receipts_sha256": sha(CAPTURE), "module_inputs_sha256": sha(MANIFEST),
                    "registry_receipts_sha256": sha(REGISTRY), "statuses": dict(Counter(r["status"] for r in results)),
                    "packaged_direct_hits": hits, "direct_dependencies": results})
    print(read(RESULTS)["statuses"], hits)


if __name__ == "__main__":
    stages = {"freeze": freeze, "compare": compare}
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("stage", choices=tuple(stages))
    stages[cli.parse_args().stage]()
