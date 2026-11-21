#!/usr/bin/env python3
"""Reconcile the release asset, subject and archive audit denominators."""
from collections import Counter
from datetime import datetime

from collect_yunohost_release_metadata import url_for
from study_yunohost_release_delivery import (
    PRIVATE, RELEASES, RESULT, RUN, SUBJECT_QUEUE, SUBJECTS,
    evidence_index, read, read_collection, sha, write,
)


def archive_rows(queue_name, receipt_name):
    q, p = RUN / queue_name, RUN / receipt_name
    queue, receipt = read(q), read(p)
    assert receipt["queue_sha256"] == sha(q)
    lower, upper = map(datetime.fromisoformat, (queue["frozen_utc"], receipt["finished_utc"]))
    for request, row in zip(queue["requests"], receipt["rows"], strict=True):
        assert row["request"] == request
        assert lower <= datetime.fromisoformat(row["observed_at_utc"]) <= upper
    return queue, receipt["rows"]


def verify():
    queue, releases, assets = evidence_index()
    result = read(RESULT)
    assert len(queue["projects"]) == result["recipes"] == 39
    assert sum(bool(r["assets"]) for r in queue["projects"]) == result["recipes_with_direct_assets"] == 37
    assert len(assets) == 38
    assert all(r["receipt"]["url"] == url_for("release", r["request"]) for r in releases)
    assert result["asset_states"] == dict(Counter(a["asset_status"] for a in assets))
    assert result["asset_states"] == {"digest_agrees": 30, "digest_unavailable": 6,
                                      "digest_differs": 1, "http_error_301": 1}
    scope, subjects = read_collection(SUBJECT_QUEUE, SUBJECTS)
    assert scope["release_receipts_sha256"] == sha(RELEASES)
    assert all(r["receipt"]["url"] == url_for("subject", r["request"]) for r in subjects)
    assert len(subjects) == 30
    assert result["subject_states"] == {"digest_bound_statement": 6, "http_error_404": 24}
    predicates = Counter(stmt["class"] for row in subjects for stmt in row.get("matching_statements", []))
    assert predicates == {"provenance": 3, "other": 5} and sum(predicates.values()) == result["digest_bound_statements"]

    q, claims = read_collection(RUN / "source_claim_queue.json", PRIVATE / "source_claims.json")
    assert q["subject_receipts_sha256"] == sha(SUBJECTS)
    assert {tuple(r["request"].values()) for r in claims} == {
        tuple(r["request"].values()) for r in subjects
        if any(p["class"] == "provenance" for p in r.get("matching_statements", []))
    }
    assert all(r["receipt"]["url"] == url_for("subject", r["request"]) for r in claims)
    assert len(claims) == 3 and all(len(r["declared_commits"]) == 1 for r in claims)

    q, archived = archive_rows("archive_queue.json", "archive_results.json")
    assert q["release_receipts_sha256"] == sha(RELEASES)
    assert len(archived) == 15 and all(row["http_status"] == 200 for row in archived)
    agree = [r for r in archived if r["agrees_with_recipe"]]
    assert len(agree) == 14 and all(r["sha256"] == r["request"]["recipe_sha256"] for r in agree)
    assert sum(r["agrees_with_api"] is None for r in agree) == 5
    [mismatch] = [r for r in archived if not r["agrees_with_recipe"]]
    assert mismatch["agrees_with_api"] is True
    assert sum(bool(r.get("inventory")) for r in agree) == 11

    q, details = archive_rows("embedded_queue.json", "embedded_results.json")
    assert q["archive_results_sha256"] == sha(RUN / "archive_results.json")
    assert len(details) == 2 and all(r["sha256"] == r["request"]["recipe_sha256"] for r in details)
    bundled, lock = details
    assert bundled["counts"]["bundled_manifests"] == 198 and bundled["counts"]["bundled_named_versions"] == 190
    assert not bundled["lockfiles"] and not bundled["counts"].get("bundled_sha512_indicators")
    assert not bundled["counts"].get("bundled_public_resolved_urls")
    assert len(lock["lockfiles"]) == 1 and lock["lockfiles"][0]["yarn_classic_header"]
    assert not lock["counts"].get("bundled_manifests")

    q, sidecars = archive_rows("sidecar_queue.json", "sidecar_binding.json")
    assert q["release_receipts_sha256"] == sha(RELEASES)
    [sbom] = [r for r in sidecars if r["format"] == "CycloneDX"]
    assert sbom["matching_name_and_hash_objects"] == 1 and sbom["npm_purl_strings"] == 0
    write(RUN / "evidence_summary.json", {
        "release_results_sha256": sha(RESULT), "source_claims_receipts_sha256": sha(PRIVATE / "source_claims.json"),
        "unverified_source_claims": [{"repository": r["request"]["repo"], "asset_sha256": r["request"]["digest"],
                                      "source_commit": r["declared_commits"][0]} for r in claims],
        "archive_results_sha256": sha(RUN / "archive_results.json"), "sidecar_binding_sha256": sha(RUN / "sidecar_binding.json"),
        "embedded_results_sha256": sha(RUN / "embedded_results.json"),
    })
    print("Verified 39 recipes, 30 exact-digest lookups, 3 declared source commits, 15 downloads and 1 bound SBOM entry")


if __name__ == "__main__":
    verify()
