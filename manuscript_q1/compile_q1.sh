#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

paper_entry=${1:-main_q1.tex}
paper_job=${paper_entry%.tex}
mkdir -p build

TECTONIC_BIN="${TECTONIC:-$HOME/.local/bin/tectonic}"
if [[ ! -x "$TECTONIC_BIN" ]] && command -v tectonic >/dev/null 2>&1; then
  TECTONIC_BIN=$(command -v tectonic)
fi

if [[ -x "$TECTONIC_BIN" ]]; then
  echo "Compiling with Tectonic ($TECTONIC_BIN)..."
  "$TECTONIC_BIN" --keep-logs --keep-intermediates --outdir build "$paper_entry"
elif command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build "$paper_entry"
elif command -v pdflatex >/dev/null 2>&1 && command -v bibtex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build "$paper_entry"
  bibtex "build/$paper_job"
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build "$paper_entry"
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build "$paper_entry"
else
  echo 'Install a LaTeX distribution with IEEEtran, or Tectonic.' >&2
  exit 1
fi

cp "build/$paper_job.pdf" "$paper_job.pdf"
echo "Successfully built manuscript_q1/$paper_job.pdf"
