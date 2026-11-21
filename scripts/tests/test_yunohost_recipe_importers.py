import base64
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from study_yunohost_recipe_importers import join


class RecipePathTests(unittest.TestCase):
    def test_unverified_ancestor_blocks_the_whole_path(self):
        integrity = "sha512-" + base64.b64encode(bytes(64)).decode()
        parent = {"package": "parent", "version": "1.0.0", "snapshot": "parent@1.0.0"}
        child = {"package": "child", "version": "1.0.0", "snapshot": "child@1.0.0"}
        trace = {"manager": "pnpm", "witnesses": [
            {"package": step["package"], "version": step["version"], "path": path, "public_npm_tarball": False,
             "registry_integrity_candidate": integrity}
            for step, path in [(parent, [parent]), (child, [parent, child])]
        ]}
        observations = {("child", "1.0.0"): {"accounts": ["child_account"], "integrity": integrity}}
        self.assertEqual(join(trace, observations), (set(), 0))
        observations[("parent", "1.0.0")] = {"accounts": ["parent_account"], "integrity": integrity}
        self.assertEqual(join(trace, observations), ({"parent_account", "child_account"}, 2))
