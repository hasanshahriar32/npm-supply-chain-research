import base64
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_yunohost_release_sbom import matches_component
from collect_yunohost_release_metadata import bound_statement
from study_yunohost_release_delivery import asset_key, source_calls


class ReleaseEvidenceTests(unittest.TestCase):
    def test_install_source_and_exact_asset_are_literal(self):
        files = {"scripts/install": 'ynh_setup_source --dest_dir="$install_dir"\n'
                                   'ynh_setup_source --source_id="$variant"\n'
                                   'ynh_setup_source --source_id="runtime"\n'
                                   '# ynh_setup_source --source_id="comment"\n'}
        self.assertEqual(set(source_calls(files)), {"main", "runtime"})
        self.assertEqual(asset_key("https://github.com/Owner/Repo/releases/download/v1%2B2/app.zip"),
                         ("owner/repo", "v1+2", "app.zip"))
        self.assertIsNone(asset_key("https://github.com/Owner/Repo/archive/refs/tags/v1.zip"))

    def test_attestation_claim_uses_exact_subject(self):
        digest = "1" * 64
        statement = {"_type": "https://in-toto.io/Statement/v1", "subject": [{"digest": {"sha256": digest}}],
                     "predicateType": "https://slsa.dev/provenance/v1"}
        bundle = {"dsseEnvelope": {"payloadType": "application/vnd.in-toto+json",
                                   "payload": base64.b64encode(json.dumps(statement).encode()).decode()}}
        self.assertEqual(bound_statement(bundle, digest)["class"], "provenance")
        self.assertIsNone(bound_statement(bundle, "2" * 64))

    def test_sbom_requires_filename_and_digest_in_one_object(self):
        digest = "1" * 64
        record = {"name": "Java runtime", "properties": [{"name": "Filename", "value": "runtime.tar.gz"}],
                  "hashes": [{"alg": "SHA-256", "content": digest}]}
        self.assertTrue(matches_component(record, "runtime.tar.gz", digest))
        self.assertFalse(matches_component(record, "other.tar.gz", digest))
        self.assertFalse(matches_component(record, "runtime.tar.gz", "2" * 64))
