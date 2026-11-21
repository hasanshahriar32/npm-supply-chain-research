"""Regression coverage for pnpm's split lockfile and integrity observations."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from study_pnpm_parser_development import YAML_READER
from verify_pnpm_registry_integrity import sha512_values


class PnpmDevelopmentTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("ruby"), "Ruby's standard Psych parser is needed")
    def test_boot_document_is_separate_and_duplicate_keys_fail(self):
        source = """---
lockfileVersion: '9.0'
importers:
  .:
    packageManagerDependencies:
      pnpm: {specifier: '12.0.0', version: '12.0.0'}
---
lockfileVersion: '9.0'
importers:
  .:
    dependencies:
      leaf: {specifier: ^1, version: '1.0.0'}
"""
        args = ["ruby", "-rpsych", "-rjson", "-e", YAML_READER]
        proc = subprocess.run(args, input=source, capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout)
        self.assertTrue(data["boot_document"])
        self.assertNotIn("packageManagerDependencies", data["project"]["importers"]["."])
        self.assertEqual(data["project"]["importers"]["."]["dependencies"]["leaf"]["version"], "1.0.0")
        proc = subprocess.run(args, input=source + "lockfileVersion: '8.0'\n",
                              capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)

    def test_integrity_uses_full_sha512_values_only(self):
        full_value = "sha512-" + ("A" * 86) + "=="
        self.assertEqual(sha512_values(full_value + " sha512-YWJjZA== sha256-wrong"), {full_value})
        self.assertEqual(sha512_values("sha512-!"), set())


if __name__ == "__main__":
    unittest.main()
