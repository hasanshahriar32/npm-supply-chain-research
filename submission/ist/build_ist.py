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


def outputs():
    canonical = text("main_q1.tex")
    preamble = latex_preamble()
    title, data, status, contributions = authors()
    abstract = text("sections/00_abstract.tex")
    keywords = re.search(r"\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}", canonical, re.S)[1].strip().rstrip(".")
    keywords = r" \sep ".join(keywords.split(", "))
    disclosure = text("sections/04a_ai_assistance.tex").split("\n", 1)[1].strip()
    manuscript = "\n".join([
        r"\documentclass[3p]{elsarticle}", preamble, r"\begin{document}", r"\begin{frontmatter}",
        r"\title{\PaperTitle}", title, abstract, r"\begin{keyword}" + keywords + r"\end{keyword}",
        r"\end{frontmatter}", main_body(canonical),
        r"\section*{Author contributions}", contributions,
        r"\section*{Declaration of generative AI and AI-assisted technologies in the manuscript preparation process}",
        disclosure, r"\bibliographystyle{elsarticle-num}", r"\bibliography{references_q1}", r"\end{document}", "",
    ])
    appendix = expand(canonical.split(r"\appendices", 1)[1].split(r"\end{document}", 1)[0])
    appendix = appendix.replace(r"\onecolumn", "").replace(r"Equation~\ref{eq:strict_quorum}", "The strict threshold rule")
    appendix = re.sub(r"(\\begin\{tabular\}.*?\\end\{tabular\})",
                      r"\\begin{adjustbox}{max width=\\linewidth}\n\1\n\\end{adjustbox}", appendix, flags=re.S)
    supplement = "\n".join([r"\documentclass[11pt,a4paper]{article}",
                             r"\usepackage[margin=24mm]{geometry}", r"\usepackage{adjustbox}",
                             preamble, r"\begin{document}",
                             r"\title{Supplementary material for \PaperTitle}", r"\author{}", r"\date{}", r"\maketitle",
                             appendix, r"\end{document}", ""])
    return {"IST_Manuscript.tex": manuscript, "IST_Supplement.tex": supplement}, data, status


def main():
    texts, people, status = outputs()
    with tempfile.TemporaryDirectory(prefix="ist-review-") as work:
        folder = Path(work)
        archive_path = folder / "IST_LaTeX_Source.zip"
        # This archive is the actual source of both checked builds.
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, content in texts.items():
                archive.writestr(name, content)
            for name in ("elsarticle.cls", "elsarticle-num.bst", "README"):
                archive.write(HERE / "template" / name, "elsarticle-README.txt" if name == "README" else name)
            archive.write(Q1 / "bibliography/references_q1.bib", "references_q1.bib")
            figures = set(re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", "\n".join(texts.values())))
            for figure in sorted(figures):
                archive.write(Q1 / "figures" / figure, figure)
        sources = folder / "source"
        with zipfile.ZipFile(archive_path) as archive:
            assert archive.testzip() is None
            archive.extractall(sources)
        checks = {}
        for name in texts:
            stem = Path(name).stem
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
        for name in ("IST_Manuscript.pdf", "IST_Supplement.pdf", "IST_LaTeX_Source.zip"):
            shutil.copy2(folder / name, HERE / name)
        shutil.copy2(HERE.parent / "emse/EMSE_Consumer_Replication.zip", HERE / "IST_Consumer_Replication.zip")
    manifest = {
        "builds": checks,
        "author_roles_confirmed_by_both": status["contribution_roles_confirmed_by_both_authors"],
        "all_authors_approved": status["all_authors_reviewed_and_approved"],
        "sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob("IST_*")) if p.is_file()},
    }
    (HERE / "validation.json").write_text(json.dumps(manifest, indent=2) + "\n")
    subprocess.run([sys.executable, str(HERE / "check_readiness.py")], check=True)
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
