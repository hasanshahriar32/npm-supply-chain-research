#!/usr/bin/env python3
"""Package a standalone typesetting project without raw data or build debris."""
from pathlib import Path
import zipfile

PAPER = Path(__file__).resolve().parents[1]
target = PAPER.parent / "NPM_Supply_Chain_IEEE_Overleaf.zip"
if not (PAPER / "main.pdf").exists():
    raise SystemExit("Compile the manuscript before packaging so the delivered PDF is included.")
allowed_roots = {"config", "sections", "bibliography", "figures", "tables", "results", "research", "scripts", "submission_files"}
allowed_top = {"main.tex", "main.pdf", "README.md", "compile.sh", "Makefile", "requirements-figures.txt"}
paths = sorted(p for p in PAPER.rglob("*") if p.is_file() and "__pycache__" not in p.parts
    and (p.relative_to(PAPER).parts[0] in allowed_roots or p.relative_to(PAPER).as_posix() in allowed_top))
with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in paths:
        archive.write(path, path.relative_to(PAPER).as_posix())
print(f"Wrote {target.name}: {len(paths)} files, {target.stat().st_size:,} bytes")
