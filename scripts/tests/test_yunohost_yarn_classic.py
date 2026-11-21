import base64
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from study_yunohost_yarn_classic import witnesses


def integrity(byte):
    return "sha512-" + base64.b64encode(bytes([byte]) * 64).decode()


def node(name, origin, children):
    return {"package": name, "version": "1.0.0", "origin": origin, "integrity": integrity(1), "children": children}


def observation(account, deps=None, conditional=False, digest=1):
    return {"integrity": integrity(digest), "conditional": conditional, "accounts": [account],
            "dependencies": deps or {}, "optional_dependencies": {}, "bundles_dependencies": False}


class YarnPathTests(unittest.TestCase):
    def test_positive_only_evidence_requires_all_ancestors(self):
        graph = {"sample_id": "fixture", "roots": [["parent", "^1"]], "nodes": {
            "parent@^1": node("parent", "npm", [["child", "^1"]]),
            "child@^1": node("child", "yarn_mirror", []),
        }}
        parent = observation("parent_account", {"child": "^1"})
        child = observation("child_account")
        index = {("parent", "1.0.0"): parent, ("child", "1.0.0"): child}
        row, issues = witnesses(graph, index)
        self.assertEqual(row, ("fixture", {"parent_account", "child_account"}, False, 2))
        self.assertFalse(issues)

        parent["conditional"] = True
        self.assertEqual(witnesses(graph, index)[0], ("fixture", set(), False, 0))
        parent["conditional"] = False
        child["integrity"] = integrity(2)
        self.assertEqual(witnesses(graph, index)[0], ("fixture", {"parent_account"}, False, 1))
        child["integrity"] = integrity(1)
        parent["dependencies"] = {"child": "^2"}
        self.assertEqual(witnesses(graph, index)[0], ("fixture", {"parent_account"}, False, 1))
