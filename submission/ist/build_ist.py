#!/usr/bin/env python3
"""Compile the focused journal article and supporting material for IST."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
Q1 = ROOT / "manuscript_q1"
SOURCE_ARCHIVES = {
    "IST_Manuscript.tex": "IST_LaTeX_Source.zip",
    "IST_Anonymous_Manuscript.tex": "IST_Anonymous_LaTeX_Source.zip",
    "IST_Supplement.tex": "IST_Supplement_Source.zip",
}
PORTAL_METADATA = "IST_Form_Metadata.txt"
ATTACHMENTS = ("IST_Consumer_Replication.zip", "IST_Cover_Letter.txt", "IST_Highlights.txt")
BUNDLE = "IST_Submission_Package.zip"
sys.path.insert(0, str(HERE.parent / "emse"))
from build_emse import compile_pdf, expand, pdf_checks


def text(path):
    return (Q1 / path).read_text()


def latex_preamble():
    preamble = expand(text("config/preamble_q1.tex"))
    preamble = preamble.replace(r"\usepackage{cite}", "").replace(r"\graphicspath{{figures/}}", "")
    macros = [
        expand(text(f"config/{name}.tex"))
        for name in ("research_numbers", "research_method_rows", "reconciliation_numbers", "revision_numbers")
    ]
    return "\n".join([r"\usepackage{amsthm,rotating}", preamble,
                      r"\setlength{\emergencystretch}{1em}", *macros])


def main_body(canonical):
    sections = canonical.split(r"\input{sections/01_introduction}", 1)[1].split(r"\section*{Acknowledgment}", 1)[0]
    sections = sections.replace(r"\input{sections/04a_ai_assistance}", "")
    body = expand(r"\input{sections/01_introduction}" + sections)
    body = body.replace("IEEEproof", "proof")
    for label in ("objective_supplement", "consumer_evidence_details", "consumer_packaging"):
        body = body.replace(r"Appendix~\ref{sec:" + label + "}", "the supplementary material")
    # Use the page's full horizontal extent for the two wide evidence tables.
    for label in ("lit_positioning", "q1_incident_case_study"):
        anchor = body.index(r"\label{tab:" + label + "}")
        start = body.rindex(r"\begin{table*}", 0, anchor)
        end = body.index(r"\end{table*}", anchor) + len(r"\end{table*}")
        block = body[start:end]
        block = block.replace(r"\begin{table*}[t]", r"\begin{sidewaystable}[p]")
        block = block.replace(r"\end{table*}", r"\end{sidewaystable}")
        block = block.replace(r"\begin{tabularx}{\textwidth}{lYYYY}", r"\begin{tabularx}{\linewidth}{p{0.16\linewidth}YYYY}")
        block = block.replace(r"0.98\textwidth", r"0.98\linewidth")
        body = body[:start] + block + body[end:]
    return body


def authors():
    data = json.loads((ROOT / "manuscript/submission_files/authors.json").read_text())
    lines = []
    for i, author in enumerate(data["authors_in_supplied_order"], 1):
        corresponding = r"\corref{corresponding}" if author["name"] == data["corresponding_author"] else ""
        lines.extend([rf"\author[author{i}]{{{author['name']}{corresponding}}}", rf"\ead{{{author['email']}}}"])
    lines.append(r"\cortext[corresponding]{Corresponding author}")
    for i, author in enumerate(data["authors_in_supplied_order"], 1):
        address = author["address"]
        lines.append(rf"\affiliation[author{i}]{{organization={{{author['department']}, {data['institution']}}},"
                     rf"addressline={{{address['street_address']}}},city={{{address['city']}}},"
                     rf"postcode={{{address['postal_code']}}},country={{{address['country']}}}}}")
    status = json.loads((HERE.parent / "emse/submission_status.json").read_text())
    roles = status["individual_contribution_roles"]
    assert list(roles) == [author["name"] for author in data["authors_in_supplied_order"]]
    contributions = " ".join(f"{name} {role}." for name, role in roles.items())
    return "\n".join(lines), data, status, contributions


def paper_metadata(canonical, preamble):
    title = re.search(r"\\newcommand\{\\PaperTitle\}\{([^}]+)\}", preamble)[1]
    abstract = text("sections/00_abstract.tex").strip()
    keywords = re.search(r"\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}", canonical, re.S)[1]
    return title, abstract, keywords.strip().rstrip(".").split(", ")


def contact_block(people):
    blocks = []
    for author in people["authors_in_supplied_order"]:
        addr = author["address"]
        name = author["name"]
        if name == people["corresponding_author"]:
            name += " (corresponding author)"
        blocks.append((name, author["department"], people["institution"],
                       f"{addr['street_address']}, {addr['city']} {addr['postal_code']}, {addr['country']}",
                       author["email"], author["orcid_url"]))
    return blocks


def form_metadata(people, status):
    title, abstract, keywords = paper_metadata(text("main_q1.tex"), text("config/preamble_q1.tex"))
    abstract = re.sub(r"\\(?:begin|end)\{abstract\}|\\textbf\{([^}]+)\}",
                      lambda match: match[1] or "", abstract)
    abstract = abstract.replace(r"\%", "%").replace("--", "–").strip()
    return "\n\n".join([
        "TITLE\n" + title, "ABSTRACT\n" + abstract, "KEYWORDS\n" + "; ".join(keywords),
        "AUTHORS IN ORDER\n" + "\n\n".join("\n".join(block) for block in contact_block(people)),
        "EARLIER GRAPH VALIDATION\n" + status["public_release_url"],
        "CURRENT CONSUMER EVIDENCE\n" + ATTACHMENTS[0],
        "FUNDING\nThis research received no external funding.",
        "COMPETING INTERESTS\nThe authors declare no competing interests relevant to this work.",
    ]) + "\n"


def outputs():
    canonical = text("main_q1.tex")
    preamble = latex_preamble()
    title, data, status, contributions = authors()
    _, abstract, keywords = paper_metadata(canonical, preamble)
    keywords = r" \sep ".join(keywords)
    disclosure = text("sections/04a_ai_assistance.tex").split("\n", 1)[1].strip()
    body = main_body(canonical)
    acknowledgments = canonical.split(r"\section*{Acknowledgment}", 1)[1].split(r"\bibliographystyle", 1)[0].strip()
    named_back = "\n".join([r"\section*{Author contributions}", contributions,
                            r"\section*{Acknowledgments}", acknowledgments])
    blind_access = (r"\providecommand{\ArtifactAccessStatement}{The original graph inputs, derived audit observations, "
                    "protocols and checksums are in a versioned public archive. The editorial office can provide "
                    "access to the earlier archive. The consumer replication archive accompanies this submission.}")
    blind_body, edits = re.subn(r"(?m)^\\providecommand\{\\ArtifactAccessStatement\}.*$",
                               lambda _: blind_access, body)
    assert edits == 1

    def article(front, content, back):
        return "\n".join([
            r"\documentclass[3p]{elsarticle}", preamble, r"\begin{document}", r"\begin{frontmatter}",
            r"\title{\PaperTitle}", front, abstract, r"\begin{keyword}" + keywords + r"\end{keyword}",
            r"\end{frontmatter}", content, back,
            r"\section*{Declaration of generative AI and AI-assisted technologies in the manuscript preparation process}",
            disclosure, r"\bibliographystyle{elsarticle-num}", r"\bibliography{references_q1}", r"\end{document}", "",
        ])

    manuscript = article(title, body, named_back)
    anonymous = article(r"\author{Anonymous authors}", blind_body, "")
    appendix = expand(canonical.split(r"\appendices", 1)[1].split(r"\end{document}", 1)[0])
    appendix = appendix.replace(r"\onecolumn", "").replace(r"Equation~\ref{eq:strict_quorum}", "The strict threshold rule")
    appendix = re.sub(r"(\\begin\{tabular\}.*?\\end\{tabular\})",
                      r"\\begin{adjustbox}{max width=\\linewidth}\n\1\n\\end{adjustbox}", appendix, flags=re.S)
    supplement = "\n".join([r"\documentclass[11pt,a4paper]{article}",
                             r"\usepackage[margin=24mm]{geometry}", r"\usepackage{adjustbox}",
                             preamble, r"\begin{document}",
                             r"\title{Supplementary material for \PaperTitle}", r"\author{}", r"\date{}", r"\maketitle",
                             appendix, r"\end{document}", ""])
    contacts = "\n\n".join(r"\\".join([name, department, university, address,
                                       rf"\nolinkurl{{{email}}}", rf"\url{{{orcid}}}"])
                           for name, department, university, address, email, orcid in contact_block(data))
    title_page = "\n".join([r"\documentclass[11pt,a4paper]{article}", preamble, r"\begin{document}",
                            r"\section*{\PaperTitle}", contacts, named_back, r"\end{document}", ""])
    return {"IST_Manuscript.tex": manuscript, "IST_Anonymous_Manuscript.tex": anonymous,
            "IST_Supplement.tex": supplement, "IST_Title_Page.tex": title_page}, data, status


def bibliography(source):
    active = {key for citation in re.findall(r"\\cite\{([^}]+)\}", source)
              for key in re.split(r"\s*,\s*", citation)}
    full = text("bibliography/references_q1.bib")
    entries = re.findall(r"(?ms)^(@\w+\{([^,]+),.*?^\})", full)
    cited = {key: entry for entry, key in entries if key in active}
    assert set(cited) == active
    return "\n\n".join(cited.values()) + "\n"


def source_archive(path, entry, source):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(entry, source)
        if r"\bibliography{" in source:
            for name in ("elsarticle.cls", "elsarticle-num.bst"):
                archive.write(HERE / "template" / name, name)
            archive.writestr("references_q1.bib", bibliography(source))
        figures = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", source)
        for figure in sorted(set(figures)):
            archive.write(Q1 / "figures" / figure, figure)


def package_members():
    return {
        "README.md": "README.md",
        "IST_Manuscript.pdf": "named/IST_Manuscript.pdf",
        "IST_LaTeX_Source.zip": "named/IST_LaTeX_Source.zip",
        "IST_Anonymous_Manuscript.pdf": "anonymous/IST_Anonymous_Manuscript.pdf",
        "IST_Anonymous_LaTeX_Source.zip": "anonymous/IST_Anonymous_LaTeX_Source.zip",
        "IST_Title_Page.pdf": "editor-only/IST_Title_Page.pdf",
        "IST_Cover_Letter.txt": "editor-only/IST_Cover_Letter.txt",
        "IST_Supplement.pdf": "common/IST_Supplement.pdf",
        "IST_Supplement_Source.zip": "common/IST_Supplement_Source.zip",
        "IST_Consumer_Replication.zip": "common/IST_Consumer_Replication.zip",
        "IST_Highlights.txt": "common/IST_Highlights.txt",
        PORTAL_METADATA: f"author-only/{PORTAL_METADATA}",
        "validation.json": "author-only/validation.json",
    }


def main():
    texts, people, status = outputs()
    with tempfile.TemporaryDirectory(prefix="ist-review-") as work:
        folder = Path(work)
        checks = {}
        for name, source in texts.items():
            stem = Path(name).stem
            sources = folder / stem
            sources.mkdir()
            if archive_name := SOURCE_ARCHIVES.get(name):
                archive_path = folder / archive_name
                source_archive(archive_path, name, source)
                with zipfile.ZipFile(archive_path) as archive:
                    assert archive.testzip() is None
                    archive.extractall(sources)
            else:
                (sources / name).write_text(source)
            compile_pdf(sources / name, folder)
            checks[stem] = pdf_checks(folder / f"{stem}.pdf", folder / f"{stem}.log")
        assert all(item["passed"] for item in checks.values()), checks
        extracted = subprocess.check_output(["pdftotext", str(folder / "IST_Manuscript.pdf"), "-"], text=True)
        words = " ".join(extracted.split())
        words = re.sub(r"(?<=\d)\s*–\s*(?=\d)", "–", words)
        for item in ("Context.", "Objective.", "Method.", "Results.", "Conclusion.", "Y051", "Y473", "2.3–26.0",
                     *(row["name"] for row in people["authors_in_supplied_order"])):
            assert item in words, item
        assert status.get("contribution_roles_confirmed_by_both_authors") in (True, False)
        generated = [*(f"{stem}.pdf" for stem in checks), *SOURCE_ARCHIVES.values()]
        for name in generated:
            shutil.copy2(folder / name, HERE / name)
        shutil.copy2(HERE.parent / "emse/EMSE_Consumer_Replication.zip", HERE / ATTACHMENTS[0])
    (HERE / PORTAL_METADATA).write_text(form_metadata(people, status))
    manifest = {
        "builds": checks,
        "author_roles_confirmed_by_both": status["contribution_roles_confirmed_by_both_authors"],
        "all_authors_approved": status["all_authors_reviewed_and_approved"],
        "sha256": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                   for name in sorted((*generated, *ATTACHMENTS, PORTAL_METADATA))},
    }
    (HERE / "validation.json").write_text(json.dumps(manifest, indent=2) + "\n")
    subprocess.run([sys.executable, str(HERE / "check_readiness.py")], check=True)
    with zipfile.ZipFile(HERE / BUNDLE, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name, location in package_members().items():
            bundle.write(HERE / name, location)
    with zipfile.ZipFile(HERE / BUNDLE) as bundle:
        assert bundle.testzip() is None
        assert all(bundle.read(location) == (HERE / name).read_bytes()
                   for name, location in package_members().items())
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
