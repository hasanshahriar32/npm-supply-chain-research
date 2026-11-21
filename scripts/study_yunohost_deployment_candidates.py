#!/usr/bin/env python3
"""Bind runtime and build importer decisions to the pinned recipe lines that support them."""
import argparse
import base64
from collections import Counter
from datetime import datetime
import re
from urllib.parse import unquote, urlsplit

from collect_yunohost_deployment_sources import url_for
from collect_yunohost_packaging import COMMIT
from study_yunohost_packaging import INTAKE, LEDGER, PRIVATE, ROOT, RUN, digest, now, read, read_evidence, sha, write

AUDIT = RUN / "classification.json"
SOURCE_QUEUE = RUN / "source_queue.json"
SOURCE_LEDGER = PRIVATE / "source_receipts.json"
SOURCE_INTAKE = RUN / "source_intake.json"

# Analyst coding is evidence of recipe instructions. It does not verify an executed installation.
BUILD = {
    "Y097": ("pnpm_root_asset_build", [], [
        ("scripts/install", 133, 'pushd "$install_dir/discourse"'),
        ("scripts/install", 135, "pnpm install --frozen-lockfile"),
        ("scripts/install", 146, "rake assets:precompile"),
    ]),
    "Y205": ("pnpm_named_workspace_build", ["packages/frontend"], [
        ("scripts/install", 21, '_pnpm_build_install "$install_dir/source"'),
        ("scripts/_common.sh", 21, 'pushd "$sourcedir/packages/frontend"'),
        ("scripts/_common.sh", 25, "pnpm build"),
        ("scripts/_common.sh", 30, 'mv "$sourcedir/packages/frontend/dist"'),
    ]),
    "Y222": ("npm_named_directory_install", ["server"], [
        ("scripts/install", 36, "pushd $install_dir/server"),
        ("scripts/install", 37, "npm ci"),
        ("conf/systemd.service", 10, "WorkingDirectory=__INSTALL_DIR__"),
    ]),
    "Y342": ("pnpm_multiple_deployment_paths", ["apps/papra-client", "apps/papra-server"], [
        ("scripts/install", 51, "pnpm -r build"),
        ("scripts/install", 53, "apps/papra-client/dist/* apps/papra-server/public/"),
        ("conf/systemd.service", 10, "WorkingDirectory=__INSTALL_DIR__/apps/papra-server"),
        ("conf/systemd.service", 12, "pnpm start:with-migrations"),
    ]),
    "Y436": ("npm_root_install", ["."], [
        ("scripts/install", 76, 'pushd "$install_dir"'), ("scripts/install", 77, "npm install"),
        ("scripts/install", 78, "npm run build"),
    ]),
    "Y466": ("npm_root_install", ["."], [
        ("scripts/install", 45, 'pushd $install_dir'), ("scripts/install", 46, "npm install"),
        ("conf/systemd.service", 12, "__INSTALL_DIR__/server.js"),
    ]),
}

PAYLOAD = {
    "Y038": ("scripts/install", 14, 'source_id="ynh_build"'),
    "Y066": ("scripts/install", 15, 'ynh_setup_source --dest_dir="$install_dir"'),
    "Y118": ("scripts/install", 15, 'ynh_setup_source --dest_dir="$install_dir"'),
    "Y165": ("scripts/install", 17, "ynh_setup_source --dest_dir=$install_dir"),
    "Y175": ("conf/systemd.service", 9, "/usr/bin/nomad"),
    "Y183": ("scripts/install", 26, 'source_id="immich_prebuilt_$YNH_DEBIAN_VERSION"'),
    "Y203": ("scripts/install", 15, 'ynh_setup_source --dest_dir="$install_dir"'),
    "Y209": ("scripts/install", 11, 'ynh_setup_source --dest_dir="$tmpdir"'),
    "Y321": ("scripts/install", 13, 'ynh_setup_source --dest_dir="$install_dir"'),
    "Y345": ("scripts/install", 40, 'ynh_setup_source --dest_dir="$install_dir/frontend"'),
    "Y363": ("scripts/install", 21, 'ynh_setup_source --dest_dir="$install_dir"'),
    "Y486": ("conf/systemd.service", 11, "jetty/start.jar"),
}

JS_COMMAND = re.compile(r"\b(?:npm|pnpm|yarn|bun)\s+(?:ci\b|install\b|run\b|build\b|-r\s+build\b)")


def source_ref(repo, url):
    parsed = urlsplit(url)
    path = unquote(parsed.path).strip("/")
    if (parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.query or parsed.fragment
            or not path.casefold().startswith(f"{repo}/archive/".casefold()) or not path.endswith(".tar.gz")):
        raise ValueError("Recipe source is outside the supported archive format")
    ref = path[len(repo) + len("/archive/"):-len(".tar.gz")]
    if COMMIT.fullmatch(ref):
        return "commit", ref
    if ref.startswith("refs/tags/"):
        return "tag", ref.removeprefix("refs/tags/")
    raise ValueError("Archive does not name an exact commit or tag")


def classify_and_queue():
    if SOURCE_QUEUE.exists():
        raise ValueError("Source queue already frozen")
    intake = read(INTAKE)
    assert intake["receipts_sha256"] == sha(LEDGER)
    cases = {row["sample_id"]: row for row in intake["projects"]}
    audits, requests = [], []
    for case, evidence, _ in read_evidence():
        sid = case["sample_id"]
        if sid in BUILD:
            mode, importers, markers = BUILD[sid]
        elif sid in PAYLOAD:
            mode, importers, markers = "release_or_distribution_payload", [], [PAYLOAD[sid]]
        else:
            mode, importers, markers = "no_explicit_js_package_command", [], []
        # Record the search space and corroborating locations without copying shell bodies.
        commands = [{"file": path, "line": n} for path in ("scripts/install", "scripts/upgrade", "scripts/_common.sh")
                    for n, line in enumerate(evidence.get(path, "").splitlines(), 1)
                    if not line.lstrip().startswith("#") and JS_COMMAND.search(line)]
        assert bool(commands) == (sid in BUILD), sid
        lines = []
        for path, n, needle in markers:
            assert needle in evidence[path].splitlines()[n - 1], (sid, path, n)
            lines.append({"file": path, "line": n, "sha256": cases[sid]["files"][path]["sha256"]})
        audits.append({**case, "classification": mode, "recipe_paths": importers, "evidence": lines,
                       "command_locations": commands})
        if sid not in BUILD:
            continue
        source = cases[sid]["declared_sources"]["main"]
        kind, ref = source_ref(case["upstream"], source["url"])
        assert re.fullmatch(r"[0-9a-f]{64}", source["sha256"])
        if mode.startswith("pnpm"):
            files = ["package.json", "pnpm-lock.yaml", "pnpm-workspace.yaml"]
            files += [f"{path}/package.json" for path in importers]
            if mode == "pnpm_root_asset_build":
                files.append("lib/tasks/assets.rake")
        else:
            files = ["package.json", "package-lock.json", "npm-shrinkwrap.json"]
            files += [f"{path}/{name}" for path in importers if path != "." for name in
                      ("package.json", "package-lock.json", "npm-shrinkwrap.json")]
        requests.append({k: case[k] for k in ("sample_id", "upstream", "upstream_commit")} |
                        {"ref_kind": kind, "ref": ref, "declared_archive_sha256": source["sha256"], "files": files})
    write(AUDIT, {"intake_sha256": sha(INTAKE), "coding": "Exploratory recipe coding with static line evidence",
                  "counts": dict(Counter((r["group"] + ":" + r["classification"]) for r in audits)),
                  "cases": audits})
    write(SOURCE_QUEUE, {"frozen_utc": now(), "classification_sha256": sha(AUDIT),
                        "collector_sha256": sha(ROOT / "scripts/collect_yunohost_deployment_sources.py"),
                        "requests": requests})
    print("Pinned source file requests for", len(requests), "projects")


def source_evidence():
    scope, ledger = read(SOURCE_QUEUE), read(SOURCE_LEDGER)
    assert scope["classification_sha256"] == sha(AUDIT) and ledger["queue_sha256"] == sha(SOURCE_QUEUE)
    assert scope["collector_sha256"] == sha(ROOT / "scripts/collect_yunohost_deployment_sources.py")
    start, end = map(datetime.fromisoformat, (scope["frozen_utc"], ledger["finished_utc"]))
    for expected, actual in zip(scope["requests"], ledger["observations"], strict=True):
        assert all(actual[k] == v for k, v in expected.items())
        assert start <= datetime.fromisoformat(actual["observed_at_utc"]) <= end
        resolved, receipts = actual["resolved"], actual["receipts"]
        commit = resolved.get("commit")
        if expected["ref_kind"] == "commit":
            assert commit == expected["ref"] and resolved["status"] == "declared_commit"
        elif commit:
            tag = "refs/tags/" + expected["ref"]
            assert resolved["status"] == "tag_resolved" and commit == resolved["refs"].get(tag + "^{}", resolved["refs"][tag])
        assert set(receipts) == (set(expected["files"]) if commit else set())
        blobs = {}
        for name, receipt in receipts.items():
            assert receipt["url"] == url_for(actual["upstream"], commit, name)
            assert start <= datetime.fromisoformat(receipt["observed_at_utc"]) <= end
            if receipt["status"] == "retained":
                body = base64.b64decode(receipt["body_base64"], validate=True)
                assert digest(body) == receipt["sha256"] and receipt["http_status"] == 200
                blobs[name] = body
        yield expected, resolved, blobs, receipts


def source_intake():
    rows = []
    for case, resolved, blobs, receipts in source_evidence():
        commit = resolved.get("commit")
        row = {**case, "resolved": resolved,
               "same_source_commit_as_root_study": (commit == case["upstream_commit"] if commit else None),
               "retained_paths": sorted(blobs), "files": {k: {f: v for f, v in receipt.items() if f != "body_base64"}
                                                        for k, receipt in receipts.items()}}
        rows.append(row)
    write(SOURCE_INTAKE, {"source_queue_sha256": sha(SOURCE_QUEUE), "source_receipts_sha256": sha(SOURCE_LEDGER),
                          "rows": rows})
    for row in rows:
        print(row["sample_id"], row["resolved"]["status"], row["same_source_commit_as_root_study"],
              row["retained_paths"])


if __name__ == "__main__":
    stages = {"queue": classify_and_queue, "intake": source_intake}
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("stage", choices=tuple(stages))
    stages[cli.parse_args().stage]()
