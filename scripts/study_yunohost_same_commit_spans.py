#!/usr/bin/env python3
"""Trace root and recipe importers at one verified upstream revision per application."""
import argparse
import base64
from collections import Counter
from datetime import datetime
import gzip
import itertools
import json
import subprocess

from collect_yunohost_importer_sources import raw_url
from collect_yunohost_observations import url_for
from study_pnpm_parser_development import YAML_READER
from study_yunohost_holdout import INCIDENCE, frozen_portfolios, paired, sha512_values
from study_yunohost_importer_frame import PRIVATE, ROOT, RUN, digest, now, read, sha, write
from study_yunohost_recipe_importers import join, npm, pnpm

SOURCE_QUEUE = RUN / "source_queue.json"
SOURCES = PRIVATE / "sources.json"
RETRY_QUEUE = RUN / "source_retry_queue.json"
RETRY = PRIVATE / "source_retry.json"
PROTOCOL = RUN / "comparison_protocol.json"
PATHS = RUN / "comparison_paths.json.gz"
REGISTRY_QUEUE = RUN / "registry_queue.json"
REGISTRY = PRIVATE / "registry.json"
RESULT = RUN / "results.json"
SUPPORTED = {"ok", "partial"}


def receipt_rows(queue_path, receipt_path):
    queue, raw = read(queue_path), read(receipt_path)
    assert raw["queue_sha256"] == sha(queue_path)
    start, end = map(datetime.fromisoformat, (queue["frozen_utc"], raw["finished_utc"]))
    for case, record in zip(queue["projects"], raw["observations"], strict=True):
        assert case["sample_id"] == record["sample_id"]
        assert start <= datetime.fromisoformat(record["observed_at_utc"]) <= end
        ref = record["resolved"]
        if "commit" in ref:
            if case["ref_kind"] == "commit":
                assert ref["commit"] == case["ref"]
            else:
                tag = "refs/tags/" + case["ref"]
                assert ref["commit"] == ref["refs"].get(tag + "^{}", ref["refs"][tag])
        if record["status"] in ("verified_archive", "patches_present"):
            assert record["archive"]["sha256"] == case["archive_sha256"]
            assert set(record["archive_members"]) == set(record["files"]) <= set(case["members"])
        blobs = {}
        for p, receipt in record["files"].items():
            assert receipt["url"] == raw_url(case["upstream"], ref["commit"], p)
            if "body_base64" in receipt:
                body = base64.b64decode(receipt["body_base64"], validate=True)
                assert digest(body) == receipt["sha256"] == record["archive_members"][p]
                blobs[p] = body
        yield case, record, blobs


def source_rows():
    assert read(SOURCE_QUEUE)["recipes_sha256"] == sha(RUN / "recipes.json")
    retry = read(RETRY_QUEUE)
    assert retry["source_queue_sha256"] == sha(SOURCE_QUEUE) and retry["original_receipts_sha256"] == sha(SOURCES)
    later = {case["sample_id"]: (case, item, files) for case, item, files in receipt_rows(RETRY_QUEUE, RETRY)}
    for case, item, files in receipt_rows(SOURCE_QUEUE, SOURCES):
        sid = case["sample_id"]
        if sid in later:
            assert item["archive"]["status"] == "above_limit" and later[sid][0] == case
            yield later[sid]
        else:
            yield case, item, files


def input_hashes():
    files = [SOURCE_QUEUE, SOURCES, RETRY_QUEUE, RETRY, INCIDENCE, RUN / "recipes.json"]
    files += [ROOT / "scripts" / name for name in (
        "study_yunohost_same_commit_spans.py", "collect_yunohost_importer_sources.py",
        "study_yunohost_recipe_importers.py", "study_pnpm_parser_development.py",
        "consumer_npm_development.cjs", "consumer_lock_evidence.cjs", "consumer_pnpm_development.cjs",
        "collect_yunohost_observations.py",
    )]
    return {str(p.relative_to(ROOT)): sha(p) for p in files}


def freeze():
    if PROTOCOL.exists():
        raise ValueError("Comparison is already frozen")
    write(PROTOCOL, {"frozen_utc": now(), "inputs": input_hashes(),
                     "scope": "For each named recipe, compare the repository root against the union of explicitly named "
                              "recipe importers at the same verified archive commit. Keep every candidate row in the ledger.",
                     "lock_scope": "npm v2/v3 and pnpm v9 root-context projection. Positive paths use the same exact-version "
                                   "metadata observations across both views and require corroboration along all prefixes. "
                                   "Negative evidence requires a checked npm tree with all joins or a checked empty pnpm importer.",
                     "unresolved": "Missing files, unsupported managers, unreviewed packaging patches and partial "
                                   "path evidence contribute unknowns. Track former upstream HEAD equality separately."})


def missing(p, status):
    return {"importer": p, "status": status, "witnesses": [], "empty_declarations": False}


def trace(case, record, files, p, lock):
    if record["status"] != "verified_archive":
        return missing(p, record["status"])
    manager = case["manager"]
    if manager not in {"npm", "pnpm"}:
        return missing(p, "unsupported_yarn_importer")
    prefix = "" if p == "." else p + "/"
    body = files.get(prefix + "package.json")
    if body is None:
        return missing(p, "manifest_unavailable")
    try:
        manifest = json.loads(body)
        own_mandatory = set(manifest.get("dependencies", {})) - set(manifest.get("optionalDependencies", {}))
        if manager == "pnpm":
            if lock is None:
                return missing(p, "lockfile_unavailable")
            result = pnpm(manifest, lock, p)
        else:
            # Use the precedence of committed shrinkwrap over package-lock.
            target = next((prefix + x for x in ("npm-shrinkwrap.json", "package-lock.json")
                           if prefix + x in record["archive_members"]), None)
            if not target or target not in files:
                return missing(p, "lockfile_unavailable")
            result = npm(body, files[target])
    except (KeyError, subprocess.SubprocessError, ValueError):
        return missing(p, "reader_unavailable")
    return {"importer": p, "manager": manager, "status": result["status"], "witnesses": result["witnesses"],
            "empty_declarations": not own_mandatory}


def trace_project(case, record, files):
    lock = None
    if "pnpm-lock.yaml" in files and record["status"] == "verified_archive":
        try:
            proc = subprocess.run(["ruby", "-rpsych", "-rjson", "-e", YAML_READER], input=files["pnpm-lock.yaml"],
                                  check=True, capture_output=True, timeout=45)
            lock = json.loads(proc.stdout)["project"]
        except (subprocess.SubprocessError, ValueError):
            pass
    sha_commit = record["resolved"].get("commit")
    return {"sample_id": case["sample_id"], "status": record["status"], "recipe_commit": sha_commit,
            "same_as_screened_head": (sha_commit == case["upstream_head"] if sha_commit and case["upstream_head"] else None),
            "root": [trace(case, record, files, ".", lock)],
            "named": [trace(case, record, files, p, lock) for p in case["importers"]]}


def paths():
    assert read(PROTOCOL)["inputs"] == input_hashes()
    rows = [trace_project(c, r, files) for c, r, files in source_rows()]
    PATHS.write_bytes(gzip.compress(json.dumps(rows, separators=(",", ":")).encode(), mtime=0))
    keys = {(w["package"], w["version"]) for r in rows for tr in r["root"] + r["named"] for w in tr["witnesses"]
            if w["public_npm_tarball"] or sha512_values(w.get("registry_integrity_candidate"))}
    entries = [{"package": p, "version": v} for p, v in sorted(keys)]
    for entry in entries:
        url_for("registry", entry)
    write(REGISTRY_QUEUE, {"stage": "registry", "protocol_sha256": sha(PROTOCOL), "paths_sha256": sha(PATHS),
                           "requests": entries})
    for r in rows:
        print(r["sample_id"], r["status"], [(t["importer"], t["status"], len(t["witnesses"])) for t in r["root"] + r["named"]])
    print(len(entries), "shared exact-version registry requests")


def context(traces, index):
    accounts, complete, count = set(), True, 0
    for trace in traces:
        if trace["status"] not in SUPPORTED:
            complete = False
            continue
        observed, paths_count = join(trace, index)
        accounts.update(observed)
        count += paths_count
        complete &= (trace["status"] == "ok" and paths_count == len(trace["witnesses"])
                     and (trace["manager"] == "npm" or (trace["empty_declarations"] and not trace["witnesses"])))
    return accounts, complete, count


def states(context, portfolio):
    accounts, complete, _ = context
    if accounts & portfolio:
        return (1,)
    return (0,) if complete else (0, 1)


def importer_contrast(contexts, portfolio):
    viable = {sid: list(itertools.product(states(root, portfolio), states(named, portfolio)))
              for sid, root, named in contexts}
    return {"resolved_pairs": sum(len(v) == 1 for v in viable.values()),
            "confirmed_gains": sum(v == [(0, 1)] for v in viable.values()),
            "confirmed_losses": sum(v == [(1, 0)] for v in viable.values()),
            "turnover_counts": [sum(all(a != b for a, b in v) for v in viable.values()),
                                sum(any(a != b for a, b in v) for v in viable.values())],
            "possible_by_project": viable}


def registry_index():
    protocol, queue, observed = read(PROTOCOL), read(REGISTRY_QUEUE), read(REGISTRY)
    assert protocol["inputs"] == input_hashes() and queue["protocol_sha256"] == sha(PROTOCOL)
    assert queue["paths_sha256"] == sha(PATHS) and observed["queue_sha256"] == sha(REGISTRY_QUEUE)
    start, end = map(datetime.fromisoformat, (protocol["frozen_utc"], observed["finished_utc"]))
    index = {}
    for request, record in zip(queue["requests"], observed["observations"], strict=True):
        assert record["url"] == url_for("registry", request) and all(record[k] == v for k, v in request.items())
        assert start <= datetime.fromisoformat(record["observed_at_utc"]) <= end
        if record["status"] == "observed":
            index[request["package"], request["version"]] = record
    return queue, index


def score():
    queue, index = registry_index()
    traces = json.loads(gzip.decompress(PATHS.read_bytes()))
    contexts = [(r["sample_id"], context(r["root"], index), context(r["named"], index)) for r in traces]
    members, slots = frozen_portfolios()
    portfolios = {k: {members[i] for i in indices} for k, indices in slots.items()}
    switches = {k: importer_contrast(contexts, ids) for k, ids in portfolios.items()}
    pairs = {}
    for i, label in ((1, "root"), (2, "named")):
        data = [(row[0], *row[i]) for row in contexts]
        pairs[label] = {k: paired(data, portfolios["name"], ids) for k, ids in portfolios.items() if k.startswith("version_")}
    summary = [{"sample_id": sid, "root_joined_paths": root[2], "named_joined_paths": named[2],
                "root_complete": root[1], "named_complete": named[1]} for sid, root, named in contexts]
    write(RESULT, {"recipes_sampled": len(read(RUN / "recipes.json")["projects"]), "named_candidates": len(traces),
                   "artifact_status": dict(Counter(r["status"] for r in traces)),
                   "root_and_named_readable": sum(all(t["status"] in SUPPORTED for t in r["root"] + r["named"]) for r in traces),
                   "registry_requests": len(queue["requests"]), "registry_observed": len(index),
                   "source_receipts_sha256": sha(SOURCES), "source_retry_sha256": sha(RETRY),
                   "registry_receipts_sha256": sha(REGISTRY),
                   "paths_sha256": sha(PATHS), "contexts": summary, "importer_contrasts": switches,
                   "representation_contrasts": pairs})
    print(json.dumps(summary, indent=2))
    print({k: [v["confirmed_gains"], v["confirmed_losses"], v["resolved_pairs"]] for k, v in switches.items()})


if __name__ == "__main__":
    methods = {"freeze": freeze, "paths": paths, "score": score}
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("stage", choices=methods)
    methods[cli.parse_args().stage]()
