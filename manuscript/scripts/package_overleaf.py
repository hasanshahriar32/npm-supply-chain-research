#!/usr/bin/env python3
"""Package a standalone typesetting project without raw data or build debris."""
from pathlib import Path
import json
import zipfile

PAPER = Path(__file__).resolve().parents[1]
target = PAPER.parent / "NPM_Supply_Chain_IEEE_Overleaf.zip"
if not (PAPER / "main.pdf").exists():
    raise SystemExit("Compile the manuscript before packaging so the delivered PDF is included.")
allowed_roots = {"config", "sections", "bibliography", "figures", "tables", "results", "research", "scripts", "submission_files", "guideline"}
allowed_top = {"main.tex", "main.pdf", "main_authors.tex", "main_authors.pdf", "README.md", "compile.sh", "Makefile", "requirements-figures.txt"}
paths = sorted(p for p in PAPER.rglob("*") if p.is_file() and "__pycache__" not in p.parts
    and p.relative_to(PAPER).as_posix() != "results/package_validation.json"
    and (p.relative_to(PAPER).parts[0] in allowed_roots or p.relative_to(PAPER).as_posix() in allowed_top))
with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in paths:
        archive.write(path, path.relative_to(PAPER).as_posix())
print(f"Wrote {target.name}: {len(paths)} files, {target.stat().st_size:,} bytes")

# Separate typesetting-only bundle: no local working notes, source-repository
# hashes, audit metadata, or environment-specific research context.
anonymous_target = PAPER.parent / "NPM_Supply_Chain_IEEE_Anonymous_Source.zip"
anonymous_roots = {"config", "sections", "bibliography", "figures", "tables"}
anonymous_top = {"main.tex", "main.pdf", "compile.sh"}
anonymous_inputs = {"results/numbers.tex", "results/field_rows.tex", "results/reconciliation_numbers.tex",
    "results/research_numbers.tex", "results/research_method_rows.tex"}
private_inputs = {"config/authors.tex"}
anonymous_paths = [p for p in paths if p.relative_to(PAPER).parts[0] in anonymous_roots
    or p.relative_to(PAPER).as_posix() in anonymous_top | anonymous_inputs]
anonymous_paths = [p for p in anonymous_paths if p.relative_to(PAPER).as_posix() not in private_inputs]
author_record = json.loads((PAPER / "submission_files/authors.json").read_text())
private_names = [a["name"] for a in author_record["authors_in_supplied_order"]] + [author_record["institution"]]
for path in anonymous_paths:
    if path.suffix in {".tex", ".md", ".bib", ".sh"}:
        content = path.read_text()
        if any(name in content for name in private_names):
            raise SystemExit(f"Author identity found in anonymous source input: {path.relative_to(PAPER)}")
with zipfile.ZipFile(anonymous_target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in anonymous_paths:
        archive.write(path, path.relative_to(PAPER).as_posix())
    archive.writestr("README.md", """# Anonymous conference typesetting source

Open main.tex in Overleaf or run `bash compile.sh` with a LaTeX compiler.
The paper uses IEEEtran conference mode, A4 paper, and standard 10-point text.
This bundle contains the PDF and typesetting inputs, not the underlying data.
It omits author-side research notes and repository/environment provenance.
Named author configuration, author records, and the named draft are excluded.

The authors must review the scientific claims and the venue's submission
requirements before submitting this draft.
""")
print(f"Wrote {anonymous_target.name}: {len(anonymous_paths)+1} files, {anonymous_target.stat().st_size:,} bytes")
