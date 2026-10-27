#!/usr/bin/env python3
"""Export the shared journal text to a flat, named EMSE LaTeX package."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
Q1 = ROOT / "manuscript_q1"
SOURCE = HERE / "source"
BUILD = HERE / "build"


def expand(text: str) -> str:
    def include(match: re.Match) -> str:
        path = Q1 / (match[1] + ".tex")
        return f"\n% Shared source: {path.relative_to(ROOT)}\n" + expand(path.read_text())
    return re.sub(r"\\input\{([^}]+)\}", include, text)


def compiler() -> str:
    candidate = Path(os.environ.get("TECTONIC", Path.home() / ".local/bin/tectonic"))
    executable = str(candidate) if candidate.is_file() else shutil.which("tectonic")
    if not executable:
        raise RuntimeError("Tectonic is required to build and validate this export")
    return executable


def compile_pdf(entry: Path, out: Path) -> None:
    out.mkdir(exist_ok=True, parents=True)
    result = subprocess.run(
        [compiler(), "--keep-logs", "--keep-intermediates", "--outdir", str(out), entry.name],
        cwd=entry.parent, text=True, capture_output=True,
    )
    (out / (entry.stem + ".compiler.txt")).write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-5000:])


def pdf_checks(pdf: Path, log: Path) -> dict:
    content = log.read_text(errors="replace")
    errors = []
    wide = [float(x) for x in re.findall(r"Overfull \\hbox \(([0-9.]+)pt too wide\)", content)]
    if any(x > 1 for x in wide):
        errors.append(f"Overfull boxes greater than 1pt: {wide}")
    if re.search(r"(?:Citation|Reference).*undefined|There were undefined|Missing character:", content):
        errors.append("Undefined citation/reference or missing glyph")
    if "Float too large" in content or re.search(r"Overfull \\vbox", content):
        errors.append("Oversized float or vertical overflow")
    fonts = subprocess.check_output(["pdffonts", str(pdf)], text=True).splitlines()[2:]
    if not fonts or any("Type 3" in line or line.split()[-5] != "yes" for line in fonts):
        errors.append("Unembedded or Type 3 font")
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    pages = int(re.search(r"^Pages:\s+(\d+)", info, re.M)[1])
    return {"pages": pages, "fonts": len(fonts), "errors": errors, "passed": not errors}


def main() -> None:
    SOURCE.mkdir(exist_ok=True)
    BUILD.mkdir(exist_ok=True)
    canonical = (Q1 / "main_q1.tex").read_text()
    preamble = expand((Q1 / "config/preamble_q1.tex").read_text())
    preamble = preamble.replace(r"\usepackage{cite}", "")
    preamble = preamble.replace(r"\usepackage[hidelinks]{hyperref}", r"\hypersetup{hidelinks}")
    preamble = preamble.replace(r"\graphicspath{{figures/}}", "")
    preamble += "\n" + r"\usepackage{adjustbox}" + "\n" + r"\raggedbottom" + "\n"
    macros = "\n".join(expand(r"\input{config/" + name + "}") for name in
                       ["research_numbers", "research_method_rows", "reconciliation_numbers"])
    abstract = (Q1 / "sections/00_abstract.tex").read_text().replace(
        r"\begin{abstract}", "").replace(r"\end{abstract}", "").strip()
    keywords = re.search(r"\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}", canonical, re.S)[1].strip().rstrip(".")
    start = canonical.index(r"\input{sections/01_introduction}")
    end = canonical.index(r"\section*{Acknowledgment}")
    body = expand(canonical[start:end])
    body = body.replace(r"\IEEEPARstart{N}{pm}", "npm")
    body = body.replace("IEEEproof", "proof").replace(r"\cite{", r"\citep{")
    # The five-column literature matrix needs a landscape page at this text width.
    matrix_label = body.index(r"\label{tab:lit_positioning}")
    matrix_start = body.rfind(r"\begin{table*}", 0, matrix_label)
    matrix_end = body.index(r"\end{table*}", matrix_label) + len(r"\end{table*}")
    matrix = body[matrix_start:matrix_end]
    matrix = matrix.replace(r"\begin{table*}[t]", r"\begin{sidewaystable}[p]")
    matrix = matrix.replace(r"\end{table*}", r"\end{sidewaystable}")
    matrix = matrix.replace(r"\begin{tabularx}{\textwidth}{lYYYY}",
                            r"\begin{tabularx}{\linewidth}{p{0.16\linewidth}YYYY}")
    matrix = matrix.replace("This Study (Q1 Journal Expansion)", "This Study")
    body = body[:matrix_start] + matrix + body[matrix_end:]
    # Preserve shared table values while fitting the narrower Springer text block.
    body = re.sub(r"(\\begin\{tabular\})", r"\\begin{adjustbox}{max width=\\linewidth}\n\1", body)
    body = body.replace(r"\end{tabular}", r"\end{tabular}" + "\n" + r"\end{adjustbox}")
    authors = json.loads((ROOT / "manuscript/submission_files/authors.json").read_text())
    author_lines = []
    for i, author in enumerate(authors["authors_in_supplied_order"], 1):
        given, family = author["name"].rsplit(" ", 1)
        star = "*" if author["name"] == authors["corresponding_author"] else ""
        author_lines.append(rf"\author{star}[{i}]{{\fnm{{{given}}} \sur{{{family}}}}}\email{{{author['email']}}}")
    for i, author in enumerate(authors["authors_in_supplied_order"], 1):
        addr = author["address"]
        author_lines.append(rf"\affil[{i}]{{\orgdiv{{{author['department']}}}, \orgname{{{authors['institution']}}}, \orgaddress{{\street{{{addr['street_address']}}}, \city{{{addr['city']}}}, \postcode{{{addr['postal_code']}}}, \country{{{addr['country']}}}}}}}")
    tex = (r"\documentclass[pdflatex,sn-basic]{sn-jnl}" + "\n" + preamble + macros + "\n"
           + r"\begin{document}" + "\n" + r"\title{\PaperTitle}" + "\n"
           + "\n".join(author_lines) + "\n" + r"\abstract{" + abstract + "}\n"
           + r"\keywords{" + keywords + "}\n" + r"\maketitle" + "\n" + body
           + "\n" + r"\bibliography{references_q1}" + "\n" + r"\end{document}" + "\n")
    (SOURCE / "EMSE_Manuscript.tex").write_text(tex)
    shutil.copy2(Q1 / "bibliography/references_q1.bib", SOURCE / "references_q1.bib")
    for name in ["sn-jnl.cls", "sn-basic.bst"]:
        shutil.copy2(HERE / "template" / name, SOURCE / name)
    figures = sorted(set(re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex)))
    assert len(figures) == 12
    for name in figures:
        assert Path(name).name == name
        shutil.copy2(Q1 / "figures" / name, SOURCE / name)
    source_files = ["EMSE_Manuscript.tex", "references_q1.bib", "sn-jnl.cls", "sn-basic.bst", *figures]
    compile_pdf(SOURCE / "EMSE_Manuscript.tex", BUILD)
    shutil.copy2(BUILD / "EMSE_Manuscript.pdf", HERE / "EMSE_Manuscript.pdf")
    shutil.copy2(BUILD / "EMSE_Manuscript.pdf", HERE / "EMSE_Reference_Copy.pdf")
    # Derive the separate title-page declarations from the same shared text.
    title_path = HERE / "EMSE_Title_Page.tex"
    title = title_path.read_text().split("% BEGIN GENERATED DECLARATIONS")[0]
    title = title.replace(r"\end{document}", "").rstrip()
    declarations = (Q1 / "sections/10_declarations.tex").read_text()
    title += "\n% BEGIN GENERATED DECLARATIONS\n" + r"\newpage" + "\n" + declarations
    title += ("\n" + r"\subsection*{Publication Status}" + "\n"
              + "Neither the conference-length draft nor the journal manuscript has been published, accepted, or is under review elsewhere. This manuscript is not an extension of a previously published conference paper.\n\n"
              + r"\subsection*{Acknowledgments}" + "\n"
              + "The authors thank npm package maintainers and the open-source community for the studied public artifacts, and deps.dev and GitHub for data interfaces. AI assistance is disclosed in the manuscript methods.\n"
              + r"\end{document}" + "\n")
    title_path.write_text(title)
    compile_pdf(title_path, BUILD)
    shutil.copy2(BUILD / "EMSE_Title_Page.pdf", HERE / "EMSE_Title_Page.pdf")
    shutil.copy2(BUILD / "EMSE_Title_Page.log", HERE / "EMSE_Title_Page.log")
    package = HERE / "EMSE_LaTeX_Source.zip"
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in source_files:
            archive.write(SOURCE / name, name)
        archive.write(BUILD / "EMSE_Manuscript.bbl", "EMSE_Manuscript.bbl")
    # Verify a clean extraction without access to the repository's source paths.
    with tempfile.TemporaryDirectory(prefix="emse-standalone-") as tmp:
        extracted = Path(tmp)
        with zipfile.ZipFile(package) as archive:
            assert all("/" not in name for name in archive.namelist())
            archive.extractall(extracted)
        compile_pdf(extracted / "EMSE_Manuscript.tex", extracted / "build")
        standalone = pdf_checks(extracted / "build/EMSE_Manuscript.pdf", extracted / "build/EMSE_Manuscript.log")
    manuscript = pdf_checks(HERE / "EMSE_Manuscript.pdf", BUILD / "EMSE_Manuscript.log")
    title_checks = pdf_checks(HERE / "EMSE_Title_Page.pdf", BUILD / "EMSE_Title_Page.log")
    extracted_text = subprocess.check_output(["pdftotext", str(HERE / "EMSE_Manuscript.pdf"), "-"], text=True)
    normalized = " ".join(extracted_text.split())
    required = ["Statements and Declarations", "Data Availability", "Code Availability", "Funding", "Competing Interests", "Use of AI Assistance", "hasanshahriar32@gmail.com", "not yet available"]
    content_checks = all(term in normalized for term in required)
    report = {"date": "2026-10-27", "manuscript": manuscript, "title_page": title_checks,
              "standalone_archive_build": standalone, "required_content_present": content_checks,
              "abstract_words": len(abstract.split()), "keywords": len(keywords.split(",")), "figures": len(figures),
              "data_release_public": False, "author_contributions_confirmed": False,
              "coauthor_submission_approval_confirmed": authors["submission_approval_confirmed"],
              "sha256": {name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() for name in source_files}}
    report["passed"] = all(x["passed"] for x in [manuscript, title_checks, standalone]) and content_checks
    (HERE / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
    (HERE / "title_page_validation.json").write_text(json.dumps(title_checks, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "sha256"}, indent=2))
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
