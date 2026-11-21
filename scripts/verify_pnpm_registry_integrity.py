"""Match pilot pnpm content identifiers to the public npm registry without package downloads."""
import argparse
import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import json

from consumer_holdout import ROOT, digest, fetch, now, registry_url, sha, write
from evaluate_consumer_pilot import load

OUT = ROOT / "research/consumer_parser_development"
PATHS = OUT / "pnpm_projects.json"
QUEUE = OUT / "pnpm_integrity_queue.json"
CACHE = OUT / "private" / "pnpm_registry"


def sha512_values(value):
    if not isinstance(value, str):
        return set()
    verified = set()
    for item in value.split():
        if not item.startswith("sha512-"):
            continue
        try:
            raw = base64.b64decode(item.removeprefix("sha512-"), validate=True)
        except ValueError:
            continue
        if len(raw) == 64:
            verified.add(item)
    return verified


def manifest():
    versions = set()
    for row in load(PATHS):
        for witness in row["witnesses"]:
            if sha512_values(witness["registry_integrity_candidate"]):
                versions.add((witness["package"], witness["version"]))
    return {"paths_sha256": sha(PATHS), "requests": [{"package": pkg, "version": ver, "url": registry_url(pkg, ver)}
                                                    for pkg, ver in sorted(versions)]}


def collect(item):
    target = CACHE / (digest(item["url"].encode()) + ".json")
    if target.exists():
        return
    record, body = fetch(item["url"], 4 * 1024 * 1024)
    record.update(package=item["package"], version=item["version"], public_integrity=[])
    if body is not None:
        try:
            data = json.loads(body)
            if isinstance(data, dict) and (data.get("name"), data.get("version")) == (item["package"], item["version"]):
                record["public_integrity"] = sorted(sha512_values((data.get("dist") or {}).get("integrity")))
        except (UnicodeDecodeError, ValueError, AttributeError):
            pass
    write(target, record)


def report(records, frozen):
    by_key = {(r["package"], r["version"]): set(r["public_integrity"]) for r in records}
    projects = []
    for row in load(PATHS):
        counts = Counter()
        for witness in row["witnesses"]:
            terms = sha512_values(witness["registry_integrity_candidate"])
            if not terms:
                continue
            observed = by_key.get((witness["package"], witness["version"]))
            label = "unresolved" if not observed else "matches" if terms & observed else "different"
            counts[label] += 1
        if counts:
            projects.append({"sample_id": row["sample_id"], **counts})
    result = {
        "queue_sha256": sha(QUEUE), "paths_sha256": frozen["paths_sha256"], "request_count": len(records),
        "usable_public_integrity": sum(bool(r["public_integrity"]) for r in records),
        "by_http_status": dict(Counter(str(r.get("http_status", r["status"])) for r in records)),
        "path_counts": dict(sum((Counter({k:v for k,v in row.items() if k != "sample_id"}) for row in projects), Counter())),
        "projects": projects,
    }
    write(OUT / "pnpm_integrity_observations.json", records)
    write(OUT / "pnpm_integrity_summary.json", result)
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "collect", "report"))
    args = parser.parse_args()
    candidate = manifest()
    if args.action == "freeze":
        if QUEUE.exists():
            raise ValueError("Existing integrity queue is already frozen")
        write(QUEUE, {**candidate, "frozen_utc": now()})
        print(len(candidate["requests"]), "exact versions frozen")
        return
    frozen = load(QUEUE)
    if any(frozen[k] != v for k, v in candidate.items()):
        raise ValueError("Witnesses or validation queue changed")
    if args.action == "collect":
        CACHE.mkdir(parents=True, exist_ok=True)
        with ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(collect, frozen["requests"]))
    records = []
    for item in frozen["requests"]:
        key = digest(item["url"].encode()) + ".json"
        source = CACHE / key
        record = load(source) if source.exists() else None
        records.append(record)
    if args.action == "report" and not all(records):
        records = load(OUT / "pnpm_integrity_observations.json")
    if len(records) != len(frozen["requests"]) or any(record is None or
       any(record[k] != item[k] for k in ("url", "package", "version"))
       for record, item in zip(records, frozen["requests"], strict=True)):
        raise ValueError("Unsealed, incomplete or conflicting integrity observations")
    report(records, frozen)


if __name__ == "__main__":
    main()
