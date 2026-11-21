#!/usr/bin/env python3
"""Record recipe evidence and freeze the exact-source requests before portfolio joins."""
import re
import tomllib
from urllib.parse import unquote, urlsplit

from collect_yunohost_packaging import COMMIT
from study_yunohost_importer_frame import BASE, QUEUE, RECEIPTS, RUN, evidence, now, read, sha, write

NAMED = {
    "D002": ("npm", ["backend"], [("scripts/install", 32, "npm ci --prefix backend"),
                                   ("conf/systemd.service", 9, "WorkingDirectory=__INSTALL_DIR__/backend/")]),
    "D007": ("yarn", ["backend", "frontend"], [("scripts/install", 37, "pushd $install_dir/backend"),
           ("scripts/install", 38, "yarn install"), ("scripts/install", 42, "pushd $install_dir/frontend"),
           ("scripts/install", 43, "yarn install"), ("scripts/install", 44, "yarn build")]),
    "D011": ("yarn", ["server"], [("scripts/install", 29, "yarn build:server"),
                                   ("conf/systemd.service", 12, "WorkingDirectory=__INSTALL_DIR__/server")]),
    "D022": ("pnpm", ["apps/web", "apps/workers", "apps/cli", "apps/mcp"], [
        ("scripts/install", 126, "pnpm exec next build apps/web"),
        ("scripts/install", 128, 'pushd "$install_dir/apps/workers"'),
        ("scripts/install", 131, "pnpm deploy"),
        ("scripts/install", 134, 'pushd "$install_dir/apps/cli"'),
        ("scripts/install", 139, 'pushd "$install_dir/apps/mcp"'),
    ]),
    "D032": ("yarn", ["packages/web"], [("scripts/install", 36, "yarn build:web"),
                                         ("scripts/install", 53, "packages/web/dist/index.html")]),
    "D037": ("yarn", ["apps/www"], [("scripts/install", 49, "yarn build"),
                                     ("conf/systemd.service", 9, "WorkingDirectory=__INSTALL_DIR__/apps/www/")]),
    "D061": ("npm", ["api", "frontend"], [("scripts/install", 28, 'pushd "$install_dir/api"'),
           ("scripts/install", 29, "npm ci"), ("scripts/install", 33, 'pushd "$install_dir/frontend"'),
           ("scripts/install", 35, "npm ci"), ("scripts/install", 61, "npm run build")]),
}
COMMAND = re.compile(r"\b(?:npm|pnpm|yarn|bun)\b.*\b(?:install|build|workspace|workspaces|ci)\b")
MARKER = re.compile(r"\b(?:ynh_setup_source|dpkg -i|apt install)\b")


def exact_ref(repo, url):
    parsed = urlsplit(url)
    path = unquote(parsed.path).strip("/")
    prefix = repo + "/archive/"
    archive_type = next((ext for ext in (".tar.gz", ".zip") if path.endswith(ext)), None)
    if (parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.query or parsed.fragment
            or not path.casefold().startswith(prefix.casefold()) or not archive_type):
        raise ValueError("Unsupported recipe archive")
    ref = path[len(prefix):-len(archive_type)]
    if COMMIT.fullmatch(ref):
        return archive_type, "commit", ref
    if ref.startswith("refs/tags/"):
        return archive_type, "tag", ref.removeprefix("refs/tags/")
    raise ValueError("Archive does not name a commit or tag")


def selected_files(manager, paths):
    dirs = ["", *(path + "/" for path in paths)]
    files = [p + "package.json" for p in dirs]
    if manager == "npm":
        return files + [p + lock for p in dirs for lock in ("package-lock.json", "npm-shrinkwrap.json")]
    if manager == "pnpm":
        return files + ["pnpm-lock.yaml", "pnpm-workspace.yaml"]
    return files + [p + "yarn.lock" for p in dirs]


def release_urls(doc):
    for source in doc.get("resources", {}).get("sources", {}).values():
        if isinstance(source, dict):
            yield from (v for k, v in source.items() if k == "url" and isinstance(v, str))
            yield from (v["url"] for v in source.values() if isinstance(v, dict) and isinstance(v.get("url"), str))


def main():
    target = RUN / "source_queue.json"
    if target.exists():
        raise ValueError("Source queue is frozen")
    screen = {r["repository"]: r.get("commit_sha")
              for r in read(BASE / "yunohost_root_screen.json")["projects"]}
    coding, queue = [], []
    for row, files, receipts in evidence():
        sid = row["sample_id"]
        doc = tomllib.loads(files.get("manifest.toml", ""))
        commands = [{"file": p, "line": n} for p in ("scripts/install", "scripts/upgrade", "scripts/_common.sh")
                    for n, line in enumerate(files.get(p, "").splitlines(), 1)
                    if not line.lstrip().startswith("#") and COMMAND.search(line)]
        release = any("/releases/download/" in url for url in release_urls(doc))
        result = {**row, "upstream_head": screen.get(row["upstream"]), "js_command_locations": commands,
                  "declared_release_asset": release, "manifest_available": bool(doc), "install_available": "scripts/install" in files}
        if sid in NAMED:
            manager, paths, markers = NAMED[sid]
            markers = [{"file": p, "line": n, "sha256": receipts[p]["sha256"]} for p, n, clue in markers
                       if clue in files[p].splitlines()[n - 1]]
            assert len(markers) == len(NAMED[sid][2]), sid
            candidates = doc["resources"]["sources"]["main"]
            archive, kind, ref = exact_ref(row["upstream"], candidates["url"])
            assert re.fullmatch(r"[0-9a-f]{64}", candidates["sha256"])
            queue.append({**row, "upstream_head": result["upstream_head"], "manager": manager, "importers": paths,
                          "members": selected_files(manager, paths), "archive_type": archive,
                          "ref_kind": kind, "ref": ref, "archive_sha256": candidates["sha256"]})
            result.update(status="named_recipe_path", markers=markers, named_importers=paths)
        elif commands:
            result["status"] = "js_command_without_supported_named_source_path"
        elif release:
            result["status"] = "release_asset_declared_without_matched_js_command"
        elif "scripts/install" not in files or not doc:
            result["status"] = "recipe_files_incomplete"
        else:
            result["status"] = "neither_signal_in_checked_files"
        coding.append(result)
    assert len(queue) == len(NAMED)
    write(RUN / "recipes.json", {"sample_sha256": sha(QUEUE), "receipts_sha256": sha(RECEIPTS), "projects": coding})
    write(target, {"frozen_utc": now(), "recipes_sha256": sha(RUN / "recipes.json"), "projects": queue})
    print("Source queue", len(queue), "recipes")


if __name__ == "__main__":
    main()
