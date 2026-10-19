#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
mkdir -p build
if [[ -n "${TECTONIC:-}" ]]; then
  "$TECTONIC" --keep-logs --keep-intermediates --outdir build main.tex
elif command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
elif command -v tectonic >/dev/null 2>&1; then
  tectonic --keep-logs --keep-intermediates --outdir build main.tex
elif command -v pdflatex >/dev/null 2>&1 && command -v bibtex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
  bibtex build/main
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
else
  echo 'Install a LaTeX distribution with IEEEtran, or Tectonic; alternatively upload the Overleaf ZIP.' >&2
  exit 1
fi
cp build/main.pdf main.pdf
echo 'Built manuscript/main.pdf'
