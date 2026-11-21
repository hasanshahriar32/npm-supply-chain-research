"""Regression checks for the paired estimand and pinned consumer evidence."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import consumer_holdout as study


class ConsumerHoldoutTests(unittest.TestCase):
    def test_partial_witness_and_incomplete_membership(self):
        trace = {"status": "compared", "custom_status": "ok", "sample_id": "H001",
                 "custom_locations": 1, "arborist_locations": 1, "corroborated_paths": 1,
                 "witnesses": [{"package": "dep", "version": "1.0.0", "public_npm_tarball": True}]}
        index = {("dep", "1.0.0"): {"v"}}
        hits, feasible = study.classify(trace, index, {"n"}, {"v"})
        self.assertEqual((hits, feasible), ([False, True], [[0, 1]]))
        self.assertEqual(study.classify(trace, {}, {"n"}, {"v"})[1],
                         [[0, 0], [0, 1], [1, 0], [1, 1]])
        trace["custom_status"] = "partial"
        self.assertEqual(study.classify(trace, index, {"n"}, {"v"})[1], [[0, 1], [1, 1]])

    def test_same_portfolio_has_identically_zero_bounds(self):
        trace = {"sample_id": "H001", "status": "no_root_manifest"}
        result = study.compare_portfolios([trace], {}, {"a"}, {"a"})
        self.assertEqual(result["documented_cells"]["00"], 1)
        self.assertEqual(result["complete_reference_net_bounds"], [0, 0])
        self.assertEqual(result["complete_reference_turnover_bounds"], [0, 0])
        self.assertEqual(result["resolved_pairs"], 0)

    def test_equal_net_can_hide_two_coverage_changes(self):
        def trace(sample_id, package):
            return {"status": "compared", "sample_id": sample_id, "custom_status": "ok",
                    "custom_locations": 1, "arborist_locations": 1, "corroborated_paths": 1,
                    "witnesses": [{"package": package, "version": "1.0.0", "public_npm_tarball": True}]}

        projects = [trace("H001", "first"), trace("H002", "second"),
                    {"sample_id": "H003", "status": "unresolved_head"}]
        memberships = {("first", "1.0.0"): {"n"}, ("second", "1.0.0"): {"v"}}
        result = study.compare_portfolios(projects, memberships, {"n"}, {"v"})
        self.assertEqual(result["documented_cells"], {"00": 1, "01": 1, "10": 1, "11": 0})
        self.assertEqual(result["documented_net"], 0)
        self.assertEqual(result["complete_reference_net_bounds"], [-1/3, 1/3])
        self.assertEqual(result["complete_reference_turnover_bounds"], [2/3, 1])

    def test_missing_paths_and_changed_origin_rejected(self):
        stamp = study.now()
        protocol = {"frozen_utc": stamp, "window_hours": 24}
        row = {"sample_id": "H001", "repository": "unit/test"}
        rec = {**row, "git_url": "https://github.com/unit/test.git",
               "pin_observed_at_utc": stamp, "commit_sha": "a" * 40, "files": {}}
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "incomplete file ledger"):
                study.check_observation(Path(tmp), rec, row, protocol)
            rec["files"] = {name: {"url": study.file_url(rec, name), "observed_at_utc": stamp,
                                   "status": "http_error", "http_status": 404} for name in study.PATHS}
            study.check_observation(Path(tmp), rec, row, protocol)
            rec["files"]["package.json"]["url"] = rec["files"]["package.json"]["url"].replace("unit/test", "unit/other")
            with self.assertRaisesRegex(ValueError, "URL or time"):
                study.check_observation(Path(tmp), rec, row, protocol)

    def test_hash_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp)
            (run / "private").mkdir()
            (run / "paths.json").write_text("{}")
            reference = run / "private/memberships.json"
            reference.write_text("[]")
            (run / "registry_manifest.json").write_text(json.dumps({
                "paths_sha256": study.sha(run / "paths.json"),
                "memberships_sha256": study.sha(reference)}))
            self.assertEqual(study.membership_index(run, [], {}), {})
            reference.write_text("[{}]")
            with self.assertRaisesRegex(ValueError, "checksum"):
                study.membership_index(run, [], {})

    def test_additive_boundary_ties(self):
        self.assertEqual(study.optimal_sets(["0xf", "0x7", "0xb", "0x1"], 2), [[0, 1], [0, 2]])


if __name__ == "__main__":
    unittest.main()
