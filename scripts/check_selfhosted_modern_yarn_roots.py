#!/usr/bin/env python3
"""Recheck structurally empty modern Yarn roots using the YunoHost rule."""
import argparse
import json
import subprocess

import check_consumer_pair_support as support
import study_selfhosted_yarn_evidence as selfhost
from study_yunohost_empty_declared_roots import GROUPS, eligible, read_lockfile
from study_yunohost_empty_pnpm_roots import declaration_count, unique_object

RUN = selfhost.RUN.with_name("selfhosted-modern-yarn-roots")
RESULT = RUN / "results.json"
GROUP_KEYS = ("version_1", "version_2", "version_3", "identical_control")


def candidates():
    unsupported = {row["sample_id"] for row in selfhost.read_graphs(selfhost.TRACES)
                   if row["status"] == "unsupported_yarn_format"}
    return [row for row in selfhost.read(selfhost.locks.FILES) if row["sample_id"] in unsupported]


def bindings():
    paths = (selfhost.RESULTS, selfhost.TRACES, selfhost.locks.FILES,
             selfhost.ROOT / "scripts/check_consumer_pair_support.py",
             selfhost.ROOT / "scripts/study_yunohost_empty_declared_roots.py",
             selfhost.ROOT / "scripts/check_selfhosted_modern_yarn_roots.py")
    return {str(path.relative_to(selfhost.ROOT)): selfhost.sha(path) for path in paths}


def inspect(capture, frame, protocol):
    sid = capture["sample_id"]
    folder = selfhost.locks.selfhost.heldout.check_observation(selfhost.SOURCE, capture, frame[sid], protocol)
    manifest = json.loads((folder / "package.json").read_text(), object_pairs_hook=unique_object)
    row = {"sample_id": sid, "stratum": "modern_yarn", "commit_sha": capture["commit_sha"],
           "file_sha256": {key: capture["files"][key]["sha256"] for key in ("package.json", "yarn.lock")},
           "counts": {key: declaration_count(manifest, key) for key in GROUPS},
           "bundled": bool(manifest.get("bundledDependencies") or manifest.get("bundleDependencies")),
           "workspaces": bool(manifest.get("workspaces")),
           "yarn_declared": str(manifest.get("packageManager")).startswith(("yarn@3.", "yarn@4."))}
    row["lock"] = {}
    if row["yarn_declared"] and not row["bundled"] and not any(row["counts"][k] for k in GROUPS[:-1]):
        try:
            row["lock"] = read_lockfile(folder / "yarn.lock", manifest)
        except (subprocess.SubprocessError, ValueError, KeyError, TypeError):
            row["lock"] = {"parse_unresolved": True}
    return row


def summarize(rows):
    zeros = {row["sample_id"] for row in rows if eligible(row)}
    comparisons = {}
    captures = selfhost.read(selfhost.locks.FILES)
    strata = {row["sample_id"]: support.selfhost_stratum(row) for row in captures}
    for group in GROUP_KEYS:
        pairs = support.selfhosted_pairs(group)
        for sid in zeros:
            assert len(pairs[sid]) > 1 and [0, 0] in pairs[sid]
            pairs[sid] = [[0, 0]]
        comparisons[group] = selfhost.summary(pairs)
        if group == "version_1":
            selfhost_support = support.classify(strata, pairs)
    return {"confirmed_empty_roots": sorted(zeros), "comparisons": comparisons,
            "selfhosted_support": selfhost_support}


def score():
    protocol = selfhost.locks.selfhost.heldout.protocol_for(selfhost.SOURCE)
    frame = {row["sample_id"]: row for row in protocol["projects"]}
    rows = [inspect(capture, frame, protocol) for capture in candidates()]
    RUN.mkdir(exist_ok=True)
    selfhost.write(RESULT, {"design": "Post hoc check of all newer-format roots declined by the Yarn Classic "
                                      "reader. Apply the matching YunoHost manifest and importer rule. "
                                      "Count only empty regular production roots at the pinned commit.",
                           "input_sha256": bindings(), "observations": rows, **summarize(rows)})


def verify():
    result = selfhost.read(RESULT)
    assert result["input_sha256"] == bindings()
    for capture, row in zip(candidates(), result["observations"], strict=True):
        assert all(capture[key] == row[key] for key in ("sample_id", "commit_sha"))
        assert row["file_sha256"] == {key: capture["files"][key]["sha256"] for key in ("package.json", "yarn.lock")}
    for key, value in summarize(result["observations"]).items():
        assert result[key] == value, key
    print("Reproduced the Awesome-Selfhosted modern Yarn empty roots")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("score", "verify"))
    {"score": score, "verify": verify}[parser.parse_args().action]()
