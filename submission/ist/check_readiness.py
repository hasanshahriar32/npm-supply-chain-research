#!/usr/bin/env python3
"""Verify the local IST deliverables against the current source and data."""
import hashlib
import json
import platform
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from build_ist import HERE, Q1, ROOT, outputs


def check():
    manifest = json.loads((HERE / "validation.json").read_text())
    expected_source, authors, status = outputs()
    assert all(record["passed"] for record in manifest["builds"].values())
    assert manifest["all_authors_approved"] == status["all_authors_reviewed_and_approved"]
    assert manifest["author_roles_confirmed_by_both"] == status["contribution_roles_confirmed_by_both_authors"]
    for filename, digest in manifest["sha256"].items():
        assert hashlib.sha256((HERE / filename).read_bytes()).hexdigest() == digest, filename

    with ZipFile(HERE / "IST_LaTeX_Source.zip") as source:
        assert source.testzip() is None
        for name, content in expected_source.items():
            assert source.read(name).decode() == content, f"{name} export is stale"
        assert source.read("references_q1.bib") == (Q1 / "bibliography/references_q1.bib").read_bytes()

    article = subprocess.check_output(["pdftotext", str(HERE / "IST_Manuscript.pdf"), "-"], text=True)
    article = " ".join(article.split())
    runs = ROOT / "research/consumer_holdout/runs"
    result_path = runs / "selfhosted-lockfile-followup/extension_results.json"
    extension = json.loads(result_path.read_text())
    yarn = json.loads((runs / "selfhosted-modern-yarn-roots/results.json").read_text())
    paired = yarn["comparisons"]["version_1"]
    resolved = f"{paired['resolved_pairs']} of 155 pairs"
    bound = f"{100 * paired['turnover_bounds'][1]:.1f}%"
    for term in ("164", "72.9", resolved, bound, "Y051", "Author contributions",
                 "OpenAI Codex assisted with development and checking of the analysis scripts",
                 "Declaration of generative AI and AI-assisted technologies",
                 *(row["name"] for row in authors["authors_in_supplied_order"])):
        assert term in article, f"Missing from rendered article: {term}"
    supplement = subprocess.check_output(["pdftotext", str(HERE / "IST_Supplement.pdf"), "-"], text=True)
    overlap = extension["retained_registry_overlap"]["canonical_keys_in_both_captures"]
    assert f"{overlap} canonical package/version keys" in " ".join(supplement.split())
    highlights = (HERE / "IST_Highlights.txt").read_text().splitlines()
    assert 3 <= len(highlights) <= 5 and all(line.startswith("- ") and len(line[2:]) <= 85 for line in highlights)

    with TemporaryDirectory(prefix="ist-readiness-replay-") as extracted:
        with ZipFile(HERE / "IST_Consumer_Replication.zip") as replication:
            assert replication.testzip() is None
            replication.extractall(extracted)
        commands = (
            ("replay_yunohost_consumer_results",),
            ("replay_yunohost_budgets",),
            ("replay_selfhosted_comparison",),
            ("study_selfhosted_registry_extension", "verify"),
            ("study_selfhosted_yarn_evidence", "verify"),
            ("check_consumer_pair_support", "verify"),
            ("check_selfhosted_modern_yarn_roots", "verify"),
        )
        for script, *args in commands:
            subprocess.run([sys.executable, f"scripts/{script}.py", *args], cwd=extracted, check=True)
    print(f"IST source, binaries and both-frame replays passed on Python {platform.python_version()}")


if __name__ == "__main__":
    check()
