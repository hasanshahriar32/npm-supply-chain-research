#!/usr/bin/env python3
"""Package the clean Q1 journal source tree into NPM_Supply_Chain_Q1_Journal_Source.zip at the workspace root."""
from __future__ import annotations

import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]
Q1_DIR = ROOT / "manuscript_q1"
ZIP_OUT = ROOT / "NPM_Supply_Chain_Q1_Journal_Source.zip"

EXCLUDE_DIRS = {"build", "__pycache__", ".git"}
EXCLUDE_EXTS = {".aux", ".log", ".out", ".xdv", ".fls", ".fdb_latexmk", ".synctex.gz"}


def should_include(rel_path: Path) -> bool:
    for part in rel_path.parts:
        if part in EXCLUDE_DIRS:
            return False
    if rel_path.suffix.lower() in EXCLUDE_EXTS:
        return False
    if rel_path.name.startswith("."):
        return False
    return True


def main():
    print(f"Packaging Q1 Journal Source from {Q1_DIR} to {ZIP_OUT}...")
    files_to_pack = []
    for p in sorted(Q1_DIR.rglob("*")):
        if p.is_file() and should_include(p.relative_to(Q1_DIR)):
            files_to_pack.append(p)

    with zipfile.ZipFile(ZIP_OUT, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in files_to_pack:
            arcname = Path("manuscript_q1") / p.relative_to(Q1_DIR)
            zf.write(p, arcname=str(arcname))
            print(f"  + {arcname}")

    zip_bytes = ZIP_OUT.stat().st_size
    sha = hashlib.sha256(ZIP_OUT.read_bytes()).hexdigest()
    print("=" * 80)
    print(f"PACKAGED: {ZIP_OUT}")
    print(f"Files included: {len(files_to_pack)}")
    print(f"Archive size: {zip_bytes:,} bytes")
    print(f"SHA-256: {sha}")
    print("=" * 80)


if __name__ == "__main__":
    main()
