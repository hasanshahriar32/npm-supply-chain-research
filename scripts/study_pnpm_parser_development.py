"""Check pnpm v9 root snapshots against pnpm's offline native listing on pilot data."""
from collections import Counter
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from consumer_holdout import ROOT, write, sha
from evaluate_consumer_pilot import load

PILOT = ROOT / "research/consumer_pilot"
OUT = ROOT / "research/consumer_parser_development"
# pnpm v9 can prepend a toolchain document. Keep it separate from the project.
YAML_READER = """
tree = Psych.parse_stream(STDIN.read)
raise 'expected one project document and at most one boot document' unless (1..2).cover?(tree.children.size)
check = lambda do |node|
  raise 'aliases are outside the supported lockfile subset' if node.is_a?(Psych::Nodes::Alias)
  if node.is_a?(Psych::Nodes::Mapping)
    keys = node.children.each_slice(2).map do |key, _|
      raise 'non-scalar key' unless key.is_a?(Psych::Nodes::Scalar)
      key.value
    end
    raise 'duplicate key' unless keys.uniq == keys
  end
  (node.children || []).each { |child| check.call(child) }
end
check.call(tree)
documents = tree.children.map do |doc|
  stream = Psych::Nodes::Stream.new
  stream.children << doc
  Psych.safe_load(stream.to_yaml, aliases: false)
end
if documents.length == 2
  boot, project = documents
  scopes = boot.fetch('importers').values
  unless boot.fetch('lockfileVersion').to_s == project.fetch('lockfileVersion').to_s &&
    scopes.all? { |imp| (imp.keys - ['configDependencies', 'packageManagerDependencies']).empty? }
    raise 'unexpected boot document'
  end
end
puts JSON.generate({project: documents.last, boot_document: documents.length == 2})
"""


def root_record(row, pm, *, folder=None):
    if folder is None:
        folder = PILOT / "projects" / row["sample_id"]
    evidence = row["files"]
    status = {"sample_id": row["sample_id"], "commit_sha": row.get("commit_sha")}
    if evidence.get("pnpm-lock.yaml", {}).get("status") != "retained":
        return {**status, "status": "no_retained_pnpm_lock", "witnesses": []}
    if evidence.get("package.json", {}).get("status") != "retained":
        return {**status, "status": "no_retained_manifest", "witnesses": []}
    for name in ("pnpm-lock.yaml", "package.json"):
        if evidence[name]["sha256"] != sha(folder / name):
            raise ValueError("Pinned pilot data changed")
    manifest = load(folder / "package.json")
    manager = manifest.get("packageManager")
    if manager and (not isinstance(manager, str) or not manager.startswith("pnpm@")):
        return {**status, "status": "different_declared_manager", "witnesses": []}
    if not manager and any(evidence[name].get("http_status") != 404
                           for name in ("package-lock.json", "npm-shrinkwrap.json", "yarn.lock")):
        return {**status, "status": "ambiguous_manager", "witnesses": []}
    proc = subprocess.run(["ruby", "-rpsych", "-rjson", "-e", YAML_READER],
                          input=(folder / "pnpm-lock.yaml").read_text(), capture_output=True, text=True, timeout=45)
    if proc.returncode:
        return {**status, "status": "unsupported_yaml", "witnesses": []}
    parsed = json.loads(proc.stdout)
    lock = parsed["project"]
    if str(lock.get("lockfileVersion")) != "9.0":
        return {**status, "status": "unsupported_lockfile_version", "witnesses": []}
    with tempfile.TemporaryDirectory(prefix="consumer-pnpm-") as tmp:
        dest = Path(tmp)
        # Supply metadata only. Exclude project configuration, version switching
        # fields and package lifecycle scripts from the native listing inputs.
        minimal = {key: manifest[key] for key in ("name", "version", "dependencies",
                   "devDependencies", "optionalDependencies") if key in manifest}
        (dest / "package.json").write_text(json.dumps(minimal))
        (dest / "pnpm-lock.yaml").write_text(json.dumps(lock))
        config = {**os.environ, "npm_config_manage_package_manager_versions": "false",
                  "COREPACK_ENABLE_AUTO_PIN": "0", "npm_config_ignore_pnpmfile": "true",
                  "npm_config_ignore_scripts": "true", "npm_config_userconfig": "/dev/null"}
        native = subprocess.run([pm, "list", "--lockfile-only", "--offline", "--prod", "--json",
                                 "--depth", "2"], cwd=dest, capture_output=True, text=True, env=config, timeout=60)
    if native.returncode:
        return {**status, "status": "native_listing_unavailable", "witnesses": []}
    compared = subprocess.run(["node", str(ROOT / "scripts/consumer_pnpm_development.cjs")],
                              input=json.dumps({"manifest": manifest, "lock": lock, "native": json.loads(native.stdout)}),
                              text=True, capture_output=True, check=True, timeout=45)
    return {**status, "boot_document": parsed["boot_document"], **json.loads(compared.stdout)}


def main():
    pm = shutil.which("pnpm")
    if not pm:
        raise RuntimeError("pnpm with list --lockfile-only support is required")
    version = subprocess.check_output([pm, "--version"], cwd="/tmp", text=True).strip()
    rows = [root_record(row, pm) for row in load(PILOT / "observations.json")["projects"]]
    summary = {
        "scope": "Development pilot, pnpm v9 root importer, up to three mandatory edges",
        "input_sha256": sha(PILOT / "observations.json"), "pnpm_version": version,
        "status": dict(Counter(row["status"] for row in rows)),
        "with_paths": sum(bool(row["witnesses"]) for row in rows),
        "paths": sum(len(row["witnesses"]) for row in rows),
        "with_boot_document": sum(bool(row.get("boot_document")) for row in rows),
        "with_integrity_candidates": sum(any(w["registry_integrity_candidate"] for w in r["witnesses"]) for r in rows),
        "with_public_url": sum(any(w["public_npm_tarball"] for w in r["witnesses"]) for r in rows),
        "path_issues": dict(sum((Counter(row.get("issues", {})) for row in rows), Counter())),
    }
    write(OUT / "pnpm_projects.json", rows)
    write(OUT / "pnpm_summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
