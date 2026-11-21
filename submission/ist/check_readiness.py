#!/usr/bin/env python3
"""Verify the local IST deliverables against the current source and data."""
import gzip
import hashlib
import json
import platform
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from build_ist import (ATTACHMENTS, HERE, PORTAL_METADATA, ROOT, SOURCE_ARCHIVES,
                       bibliography, form_metadata, outputs)


def visible_text(name):
    return " ".join(subprocess.check_output(["pdftotext", str(HERE / name), "-"], text=True).split())


def check():
    manifest = json.loads((HERE / "validation.json").read_text())
    expected_source, authors, status = outputs()
    assert all(record["passed"] for record in manifest["builds"].values())
    assert manifest["all_authors_approved"] == status["all_authors_reviewed_and_approved"]
    assert manifest["author_roles_confirmed_by_both"] == status["contribution_roles_confirmed_by_both_authors"]
    for filename, digest in manifest["sha256"].items():
        assert hashlib.sha256((HERE / filename).read_bytes()).hexdigest() == digest, filename

    identities = [authors["institution"]]
    for row in authors["authors_in_supplied_order"]:
        identities.extend(row[key] for key in ("name", "email", "orcid"))
        identities.append(row["email"].split("@", 1)[0])
    for name, archive_name in SOURCE_ARCHIVES.items():
        content = expected_source[name]
        with ZipFile(HERE / archive_name) as source:
            assert source.testzip() is None
            assert [path for path in source.namelist() if path.endswith(".tex")] == [name]
            assert all("/" not in path for path in source.namelist())
            assert source.read(name).decode() == content, f"{name} export is stale"
            if r"\bibliography{" in content:
                assert source.read("references_q1.bib").decode() == bibliography(content)
            if name != "IST_Manuscript.tex":
                for path in (p for p in source.namelist() if p.endswith((".tex", ".bib"))):
                    data = source.read(path).decode().casefold()
                    assert all(identity.casefold() not in data for identity in identities), path
    assert (HERE / PORTAL_METADATA).read_text() == form_metadata(authors, status)

    article = visible_text("IST_Manuscript.pdf")
    blind = visible_text("IST_Anonymous_Manuscript.pdf")
    title_page = visible_text("IST_Title_Page.pdf")
    for row in authors["authors_in_supplied_order"]:
        assert all(row[key] in title_page for key in ("name", "email", "orcid"))
        assert row["name"] in article
    assert "Author contributions" in article
    for name in ("IST_Anonymous_Manuscript.pdf", "IST_Supplement.pdf"):
        path = str(HERE / name)
        surfaces = [visible_text(name), *(subprocess.check_output(["pdfinfo", flag, path], text=True)
                                         for flag in ("-url", "-meta", "-custom"))]
        for surface in surfaces:
            assert all(identity.casefold() not in surface.casefold() for identity in identities), name
    runs = ROOT / "research/consumer_holdout/runs"
    result_path = runs / "selfhosted-lockfile-followup/extension_results.json"
    extension = json.loads(result_path.read_text())
    yarn = json.loads((runs / "selfhosted-modern-yarn-roots/results.json").read_text())
    paired = yarn["comparisons"]["version_1"]
    resolved = f"{paired['resolved_pairs']} of 155 pairs"
    bound = f"{100 * paired['turnover_bounds'][1]:.1f}%"
    for term in ("164", "72.9", resolved, bound, "Y051",
                 "OpenAI Codex assisted with development and checking of the analysis scripts",
                 "Declaration of generative AI and AI-assisted technologies"):
        assert term in article and term in blind, f"Missing from rendered article: {term}"
    yunohost = json.loads((runs / "yunohost-npm-unresolved/results.json").read_text())["comparisons"]["version_1"]
    for pdf in (article, blind):
        conclusion = pdf.split("Statements and Declarations", 1)[0].rsplit("Conclusion", 1)[1]
        assert resolved in conclusion and f"{yunohost['resolved_pairs']} of 215 pairs" in conclusion
        for result in (paired, yunohost):
            lo, hi = ("0" if value == 0 else f"{100 * value:.1f}" for value in result["turnover_bounds"])
            assert re.search(rf"\b{re.escape(lo)}\s*[–-]\s*{re.escape(hi)}%", conclusion), conclusion
    supplement = visible_text("IST_Supplement.pdf")
    overlap = extension["retained_registry_overlap"]["canonical_keys_in_both_captures"]
    assert f"{overlap} canonical package/version keys" in " ".join(supplement.split())
    highlights = (HERE / "IST_Highlights.txt").read_text().splitlines()
    assert 3 <= len(highlights) <= 5 and all(line.startswith("- ") and len(line[2:]) <= 85 for line in highlights)

    with TemporaryDirectory(prefix="ist-readiness-replay-") as extracted:
        with ZipFile(HERE / ATTACHMENTS[0]) as replication:
            assert replication.testzip() is None
            for member in replication.namelist():
                payload = replication.read(member)
                if member.endswith(".gz"):
                    payload = gzip.decompress(payload)
                content = payload.decode(errors="ignore").casefold()
                assert all(identity.casefold() not in content for identity in identities), member
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
