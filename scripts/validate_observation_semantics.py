#!/usr/bin/env python3
"""Regression checks for real parsing defects and lost observation states."""
from research_observations import classify_workflow_response, parse_github_repository

cases = {
    "git+https://github.com/tj/commander.js.git": ("tj", "commander.js"),
    "https://github.com/isaacs/fs.realpath": ("isaacs", "fs.realpath"),
    "git@github.com:Owner/Repo.With.Dots.git#ref": ("owner", "repo.with.dots"),
    "ssh://git@github.com/Owner/Repo.git": ("owner", "repo"),
    "github:Owner/Repo": ("owner", "repo"),
    "git://github.com/Owner/Repo.git": ("owner", "repo"),
    "https://github.com/Owner/Repo/tree/main/packages/a": ("owner", "repo"),
    "https://github.com/Owner/Repo.git?ref=main": ("owner", "repo"),
    "https://github.com.evil.example/Owner/Repo": (None, None),
    "https://evil.example/github.com/Owner/Repo": (None, None),
    "https://github.com/Owner/Repo%2Fother": (None, None),
    "https://gitlab.com/Owner/Repo": (None, None),
    "https://github.com/Owner": (None, None),
}
for value, expected in cases.items():
    assert parse_github_repository(value) == expected, value
assert parse_github_repository({"url": "git+https://github.com/tj/commander.js.git"}) == ("tj", "commander.js")
for value in [None, 4, {}, {"url": None}, ""]:
    assert parse_github_repository(value) == (None, None)
for status in [401, 403, 404, 429, 500, 0]:
    assert classify_workflow_response(status, {})[1] is None
assert classify_workflow_response(200, {"errors": [{"message": "unavailable"}]})[1] is None
assert classify_workflow_response(200, {"data": {"repository": None}})[1] is None
assert classify_workflow_response(200, {"data": {"repository": {"object": None}}})[:2] == ("directory_not_observed", 0)
assert classify_workflow_response(200, {"data": {"repository": {"object": {"__typename": "Tree", "entries": [{"name": "ci.yml"}]}}}})[:2] == ("directory_observed", 1)
assert classify_workflow_response(200, {"data": {"repository": {"object": {"__typename": "Blob"}}}})[1] is None
print("Repository URL regression cases and positive/absent/unavailable/error observation checks passed.")
