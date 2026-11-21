#!/usr/bin/env python3
"""Verify the pinned YunoHost capture and inventory lockfile availability."""
import argparse
from collections import Counter
import json
from pathlib import Path

from collect_yunohost_root_evidence import FILES, sha

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/consumer_parser_development"
FAMILIES = {"npm": ("npm-shrinkwrap.json", "package-lock.json"),
            "pnpm": ("pnpm-lock.yaml",), "yarn": ("yarn.lock",), "bun": ("bun.lock", "bun.lockb")}


def classify(manifest, files):
    available = [family for family, paths in FAMILIES.items()
                 if any(files[name]["status"] == "retained" for name in paths)]
    declaration = manifest.get("packageManager")
    if declaration is not None:
        if not isinstance(declaration, str) or "@" not in declaration:
            return "invalid_manager_declaration"
        manager = declaration.split("@", 1)[0]
        if manager not in FAMILIES:
            return "other_declared_manager"
        if manager not in available:
            return "declared_lockfile_unavailable"
        return f"{manager}_file_available"
    if len(available) > 1:
        return "multiple_manager_families"
    probes = [row for name, row in files.items()
              if name in {item for paths in FAMILIES.values() for item in paths}]
    if any(row["status"] != "retained" and row.get("http_status") != 404 for row in probes):
        return "lockfile_probes_unresolved"
    return f"{available[0]}_file_available" if available else "no_root_lockfile_returned"


def verify(capture):
    frame_path = BASE / "yunohost_root_frame.json"
    frozen = json.loads(frame_path.read_bytes())
    ledger = json.loads((capture / "observations.json").read_bytes())
    if ledger["frame_sha256"] != sha(frame_path.read_bytes()) or ledger["started_scope"] != list(FILES):
        raise ValueError("Capture differs from the planned pinned frame or file scope")
    report = []
    requests = Counter()
    for record, expected in zip(ledger["projects"], frozen["eligible"], strict=True):
        for key in ("frame_id", "repository", "commit_sha"):
            if record[key] != expected[key]:
                raise ValueError("Mismatch between frame entry and receipt")
        root = capture / "projects" / record["frame_id"]
        files = record["files"]
        prefix = f"https://raw.githubusercontent.com/{record['repository']}/{record['commit_sha']}"
        for name, receipt in files.items():
            if name not in FILES or receipt["url"] != f"{prefix}/{name}":
                raise ValueError("Receipt differs from expected URL")
            requests[str(receipt.get("http_status", receipt["status"]))] += 1
            # A manifest with a new checksum fails the acquisition gate and has no stored payload.
            if receipt["status"] != "retained" or record["status"] == "manifest_unverified":
                continue
            content = (root / name).read_bytes()
            if len(content) != receipt["bytes"] or sha(content) != receipt["sha256"]:
                raise ValueError("Retained bytes do not match their acquisition receipt")
        if record["status"] == "manifest_unverified":
            label = "manifest_unverified"
        else:
            if set(files) != set(FILES) or files["package.json"]["sha256"] != expected["manifest_sha256"]:
                raise ValueError("Missing file observations or changed root manifest")
            manifest = json.loads((root / "package.json").read_bytes())
            label = classify(manifest, files)
        report.append({"frame_id": record["frame_id"], "status": label,
                       "workspace_declared": expected["has_workspace_declaration"]})
    return ledger, {"frame_sha256": ledger["frame_sha256"], "projects": len(report),
                    "capture_sealed_utc": ledger["sealed_utc"], "http_counts": dict(requests),
                    "intake": dict(Counter(row["status"] for row in report)), "rows": report}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path)
    args = parser.parse_args()
    ledger, report = verify(args.capture)
    (BASE / "yunohost_lockfile_observations.json").write_text(json.dumps(ledger, indent=2) + "\n")
    (BASE / "yunohost_lockfile_intake.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))
