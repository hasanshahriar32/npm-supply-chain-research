"""Freeze and replay the bounded Awesome-Selfhosted consumer feasibility pilot."""
import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parents[1] / "research" / "consumer_pilot"
PROTOCOL = BASE / "protocol.json"
SAMPLE = BASE / "sample.json"
OBSERVATIONS = BASE / "observations.json"
RAW = "https://raw.githubusercontent.com"
API = "https://api.github.com"
PLATFORMS = {"nodejs", "javascript", "typescript"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read(path):
    return json.loads(path.read_text())


def write(path, obj):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(path)


def fetch(url, cap):
    record = {"url": url, "attempted_utc": now()}
    request = Request(url, headers={"User-Agent": "npm-consumer-feasibility/1.0"})
    try:
        with urlopen(request, timeout=25) as response:
            record["http_status"] = response.status
            blob = response.read(cap + 1)
            if len(blob) > cap:
                record["status"] = "above_size_cap"
                return record, None
            record.update(status="retained", bytes=len(blob), sha256=digest(blob))
            return record, blob
    except HTTPError as exc:
        record.update(http_status=exc.code, status="http_error")
        if exc.code in (403, 429):
            record["rate_limit_remaining"] = exc.headers.get("X-RateLimit-Remaining")
        return record, None
    except (URLError, OSError) as exc:
        record.update(status="transport_error", error_type=type(exc).__name__)
        return record, None


def repo_url(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
        return None
    path = parsed.path.strip("/").removesuffix(".git")
    return path.lower() if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", path) else None


def frame(blob):
    repos = {}
    language_matches = source_exclusions = 0
    for line in blob.decode().splitlines():
        entry = re.match(r"^- \[([^\]]+)\]\(([^)]+)\)", line)
        tags = re.findall(r"`([^`]+)`", line)
        if not entry or not tags or PLATFORMS.isdisjoint(tags[-1].lower().split("/")):
            continue
        language_matches += 1
        explicit = re.search(r"\[Source Code\]\(([^)]+)\)", line)
        repository = repo_url(explicit.group(1) if explicit else entry.group(2))
        if repository:
            repos[repository] = True
        else:
            source_exclusions += 1
    return sorted(repos), language_matches, source_exclusions


def freeze(protocol, local_index):
    url = f"{RAW}/{protocol['frame_repository']}/{protocol['frame_commit']}/{protocol['frame_path']}"
    if local_index:
        blob = Path(local_index).read_bytes()
    else:
        record, blob = fetch(url, 2_000_000)
        if blob is None:
            raise RuntimeError(record)
    repos, matched, excluded = frame(blob)
    seed = protocol["seed"]
    ranking = sorted(repos, key=lambda repo: (digest((seed + "\n" + repo).encode()), repo))
    n = protocol["sample_size"]
    if len(ranking) < n:
        raise ValueError("Eligible frame is smaller than the prespecified sample.")
    result = dict(protocol_sha256=digest(PROTOCOL.read_bytes()), index_url=url,
                  index_sha256=digest(blob), frame_size=len(repos), platform_matches=matched,
                  excluded_source_links=excluded, duplicate_records=matched-excluded-len(repos),
                  repositories=repos, inclusion_probability=n/len(repos),
                  projects=[{"sample_id": f"P{i:03d}", "repository": repo}
                            for i, repo in enumerate(ranking[:n], 1)])
    if SAMPLE.exists():
        if read(SAMPLE) != result:
            raise ValueError("Frozen frame or draw differs from the stored sample.")
    else:
        write(SAMPLE, result)
    print(f"Frame {len(repos)}; sample {n}; frozen sample SHA-256 {digest(SAMPLE.read_bytes())}")


def collect_project(row, protocol):
    repo, sid = row["repository"], row["sample_id"]
    params = urlencode({"until": protocol["cutoff_utc"], "per_page": 1})
    pin, body = fetch(f"{API}/repos/{repo}/commits?{params}", 1_500_000)
    obs = {**row, "commit_sha": None, "commit_request": pin, "files": {}}
    if body is None:
        obs["status"] = "unresolved_commit"
        return obs
    try:
        commits = json.loads(body)
        if not isinstance(commits, list) or not commits:
            raise ValueError("no commits")
        commit = commits[0]
        sha = commit["sha"]
        date = commit["commit"]["committer"]["date"]
        if not re.fullmatch(r"[0-9a-f]{40}", sha) or date > protocol["cutoff_utc"]:
            raise ValueError("invalid pin or later committer time")
    except (ValueError, KeyError, TypeError) as exc:
        obs.update(status="unresolved_commit", reason=str(exc))
        return obs
    obs.update(commit_sha=sha, commit_utc=date, status="commit_pinned")
    folder = BASE / "projects" / sid
    folder.mkdir(parents=True, exist_ok=True)
    for name in protocol["paths"]:
        file_record, body = fetch(f"{RAW}/{repo}/{sha}/{name}", protocol["max_bytes_per_path"])
        obs["files"][name] = file_record
        if body is not None:
            (folder / name).write_bytes(body)
    return obs


def verify_cache(row, protocol, replay):
    for name, meta in row["files"].items():
        if meta["status"] != "retained":
            continue
        path = BASE / "projects" / row["sample_id"] / name
        if path.exists():
            if digest(path.read_bytes()) != meta["sha256"]:
                raise RuntimeError(f"Local file differs from the pinned hash: {path}")
        elif replay:
            downloaded, body = fetch(meta["url"], protocol["max_bytes_per_path"])
            if body is None or downloaded["sha256"] != meta["sha256"]:
                raise RuntimeError(f"Replay failed for {row['sample_id']}/{name}: {downloaded}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        else:
            raise RuntimeError(f"Missing retained file: {path}. Run replay to retrieve it.")


def process(protocol, action):
    sample = read(SAMPLE)
    if sample["protocol_sha256"] != digest(PROTOCOL.read_bytes()):
        raise RuntimeError("Protocol has changed since sampling.")
    sample_hash = digest(SAMPLE.read_bytes())
    state = read(OBSERVATIONS) if OBSERVATIONS.exists() else {
        "sample_sha256": sample_hash, "projects": []}
    if state["sample_sha256"] != sample_hash:
        raise RuntimeError("Observation records refer to a different sample.")
    if action in {"verify", "replay"}:
        if [p["sample_id"] for p in state["projects"]] != [p["sample_id"] for p in sample["projects"]]:
            raise RuntimeError("Collection is incomplete.")
        for row in state["projects"]:
            verify_cache(row, protocol, action == "replay")
        print("Retained evidence hashes verified.")
        return
    done = {row["sample_id"] for row in state["projects"]}
    remaining = [p for p in sample["projects"] if p["sample_id"] not in done]
    with ThreadPoolExecutor(max_workers=5) as pool:
        for row in pool.map(lambda project: collect_project(project, protocol), remaining):
            state["projects"].append(row)
            write(OBSERVATIONS, state)
            print(row["sample_id"], row["status"], flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "collect", "verify", "replay"))
    parser.add_argument("--index-file", help="Previously downloaded pinned README for offline freeze.")
    args = parser.parse_args()
    protocol = read(PROTOCOL)
    if args.action == "freeze":
        freeze(protocol, args.index_file)
    else:
        process(protocol, args.action)


if __name__ == "__main__":
    main()
