#!/usr/bin/env python3
"""Audit the remaining npm roots and test strict additional evidence."""
import argparse
from collections import Counter
import json
import subprocess
from urllib.parse import unquote, urlsplit

import check_yunohost_bun_direct as bun
from study_yunohost_empty_pnpm_roots import declaration_count, unique_object

INITIAL = bun.INITIAL
RUN = INITIAL.RUN.with_name("yunohost-npm-unresolved")
RESULTS = RUN / "results.json"
GROUPS = ("dependencies", "optionalDependencies", "peerDependencies", "devDependencies")


def candidates():
    pairs = INITIAL.read(bun.PAIRS)["comparisons"]["version_1"]["projects"]
    traces = bun.read_graphs(bun.TRACES)
    assert [p["sample_id"] for p in pairs] == [t["sample_id"] for t in traces]
    return [trace for trace, pair in zip(traces, pairs, strict=True)
            if trace["status"].startswith("npm_") and len(pair["feasible"]) > 1]


def same_labels(manifest, record):
    return all(key not in manifest or key not in record or manifest[key] == record[key]
               for key in ("name", "version"))


def semver(witnesses):
    matched = subprocess.check_output(["node", "-e", bun.SEMVER_CHECK],
                                     input=json.dumps(witnesses), text=True, timeout=20)
    return [witness for witness, ok in zip(witnesses, json.loads(matched), strict=True) if ok]


def v1_entry_count(dependencies):
    stack = list(dependencies.values())
    counts = Counter()
    while stack:
        row = stack.pop()
        counts["total"] += 1
        counts["dev"] += row.get("dev") is True
        stack.extend(row.get("dependencies", {}).values())
    return {key: counts[key] for key in ("total", "dev")}


def npm_tarball(url, name, version):
    parts = urlsplit(url)
    return (parts.scheme == "https" and parts.netloc == "registry.npmjs.org"
            and not parts.query and not parts.fragment
            and unquote(parts.path) == f"/{name}/-/{name.split('/')[-1]}-{version}.tgz")


def v1_regular(manifest, lock):
    dependencies = lock.get("dependencies", {})
    accepted = []
    for name, constraint in sorted(manifest.get("dependencies", {}).items()):
        row = dependencies.get(name, {})
        version = row.get("version")
        integrity = row.get("integrity")
        if (isinstance(version, str) and isinstance(row.get("resolved"), str)
                and not any(row.get(flag) for flag in ("dev", "optional", "bundled", "os", "cpu", "libc"))
                and name not in manifest.get("optionalDependencies", {})
                and npm_tarball(row["resolved"], name, version) and INITIAL.sha512_values(integrity)):
            accepted.append({"package": name, "version": version, "range": constraint, "integrity": integrity})
    return semver(accepted)


def inspect(row, trace):
    sid = row["frame_id"]
    folder = INITIAL.CAPTURE / "projects" / sid
    lock_name = INITIAL.choose_npm(row)
    assert lock_name in ("npm-shrinkwrap.json", "package-lock.json")
    manifest = json.loads((folder / "package.json").read_bytes(), object_pairs_hook=unique_object)
    lock = json.loads((folder / lock_name).read_bytes(), object_pairs_hook=unique_object)
    version = lock["lockfileVersion"]
    root = lock.get("packages", {}).get("")
    identity = same_labels(manifest, lock) and (root is None or same_labels(manifest, root))
    guarded = any(manifest.get(key) for key in ("workspaces", "bundleDependencies", "bundledDependencies"))
    result = {
        "sample_id": sid, "repository": row["repository"], "commit_sha": row["commit_sha"],
        "file_sha256": {name: row["files"][name]["sha256"] for name in ("package.json", lock_name)},
        "earlier_status": trace["status"], "lockfile_version": version, "root_labels_agree": identity,
        "workspace_or_bundle": guarded, "witnesses": [],
        "counts": {key: declaration_count(manifest, key) for key in GROUPS},
    }
    if version == 1:
        declarations = manifest.get("devDependencies", {})
        dependencies = lock.get("dependencies", {})
        checks = [{"package": name, "range": constraint, "version": dependencies.get(name, {}).get("version")}
                  for name, constraint in declarations.items()]
        counts = v1_entry_count(dependencies)
        result["v1_entries"] = counts
        result["v1_dev_agrees"] = (len(semver(checks)) == len(checks)
                                   and counts["total"] == counts["dev"])
        if identity and not guarded and not any(manifest.get(key) for key in ("overrides", "resolutions")):
            result["witnesses"] = v1_regular(manifest, lock)
    else:
        result["root_declarations_agree"] = root is not None and all(
            manifest.get(key, {}) == root.get(key, {}) for key in GROUPS
        )
    if trace["complete"]:
        # These records had complete path extraction but incomplete package identity.
        # Count locations with neither a canonical URL nor a usable npm integrity token.
        gaps = 0
        for witness in trace["witnesses"]:
            metadata = lock["packages"][witness["location"]]
            if not metadata.get("resolved") and not INITIAL.sha512_values(metadata.get("integrity")):
                gaps += 1
        result["locations_with_no_url_or_sha512"] = gaps
    return result


def empty(row):
    if row["workspace_or_bundle"] or not row["root_labels_agree"] or any(row["counts"][key] for key in GROUPS[:-1]):
        return False
    return row.get("v1_dev_agrees", False) if row["lockfile_version"] == 1 else (
        row["lockfile_version"] in (2, 3) and row["root_declarations_agree"])


def summarize(observations, joined):
    added_zeros = {row["sample_id"] for row in observations if empty(row)}
    bun_result = INITIAL.read(bun.RESULTS)
    previous_zeros = set(INITIAL.read(bun.EMPTY_RESULTS)["additional_common_negatives"])
    previous_zeros.update(INITIAL.read(bun.PNPM_RESULTS)["verified_empty_roots"])
    assert not previous_zeros & added_zeros
    comparisons = {}
    for variant, result in INITIAL.read(bun.PAIRS)["comparisons"].items():
        required = {"control"} if variant == "identical_control" else {"name", variant}
        positives = {row["sample_id"] for row in [*bun_result["registry_join"], *joined]
                     if required.issubset(row["covered_by"])}
        zeros = previous_zeros | added_zeros
        assert not zeros & positives
        viable = []
        for row in result["projects"]:
            sid, states = row["sample_id"], row["feasible"]
            if sid in zeros or sid in positives:
                confirmed = [1, 1] if sid in positives else [0, 0]
                assert confirmed in states and len(states) > 1
                states = [confirmed]
            viable.append(states)
        n = len(viable)
        deltas = [{v - p for p, v in states} for states in viable]
        comparisons[variant] = {"resolved_pairs": sum(len(states) == 1 for states in viable),
                                "turnover_bounds": [sum(0 not in d for d in deltas) / n,
                                                    sum(d != {0} for d in deltas) / n],
                                "net_bounds": [sum(min(d) for d in deltas) / n, sum(max(d) for d in deltas) / n]}
        for metric in ("net_bounds", "turnover_bounds"):
            old = bun_result["comparisons"][variant][metric]
            lo, hi = comparisons[variant][metric]
            assert old[0] <= lo <= hi <= old[1]
    return {"additional_common_negatives": sorted(added_zeros), "comparisons": comparisons}


def inputs():
    files = (bun.TRACES, bun.PAIRS, bun.REPLAY, bun.RESULTS, bun.EMPTY_RESULTS,
             bun.PNPM_RESULTS, INITIAL.ROOT / "scripts/check_yunohost_npm_unresolved.py")
    return {str(path.relative_to(INITIAL.ROOT)): INITIAL.sha(path) for path in files}


def score():
    RUN.mkdir(exist_ok=True)
    frame = {row["frame_id"]: row for row, _ in INITIAL.inputs()}
    observations = [inspect(frame[trace["sample_id"]], trace) for trace in candidates()]
    joined = bun.evaluate(observations)
    output = {"design": "Post hoc diagnostic of all unresolved npm projects. Compare empty root manifests "
                        "with pinned npm lock declarations and dev-only v1 lock entries. Audit absent artifact "
                        "identity and check v1 direct dependencies against retained exact-version receipts.",
              "input_sha256": inputs(), "observations": observations, "registry_join": joined,
              **summarize(observations, joined)}
    INITIAL.write(RESULTS, output)
    print(output["additional_common_negatives"], output["comparisons"]["version_1"])
    print([(r["sample_id"], len(r["matched_versions"]), r["covered_by"]) for r in joined if r["matched_versions"]])


def verify():
    result = INITIAL.read(RESULTS)
    assert result["input_sha256"] == inputs()
    rows = result["observations"]
    assert [row["sample_id"] for row in rows] == [trace["sample_id"] for trace in candidates()]
    joined = bun.evaluate(rows)
    assert joined == result["registry_join"]
    assert all(result[key] == item for key, item in summarize(rows, joined).items())
    table = (INITIAL.ROOT / "manuscript_q1/tables/yunohost_consumer_holdout_table.tex").read_text()
    columns = [result["comparisons"][f"version_{i}"] for i in range(1, 4)]
    count = " & ".join(str(row["resolved_pairs"]) for row in columns)
    assert f"npm follow-up resolved pairs & {count}" + r"\\" in table
    for label, field in ((r"npm follow-up turnover (\%)", "turnover_bounds"),
                         ("npm follow-up net change (pp)", "net_bounds")):
        expected = [f"$[{100*lo:.1f},{100*hi:.1f}]$" for lo, hi in (r[field] for r in columns)]
        assert " & ".join([label, *expected]) + r"\\" in table
    print("Reproduced the unresolved npm diagnostic and combined bounds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    stages = {"score": score, "verify": verify}
    parser.add_argument("stage", choices=stages)
    stages[parser.parse_args().stage]()
