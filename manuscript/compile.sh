#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
paper_entry=${1:-main.tex}
if [[ "$paper_entry" == "--both" ]]; then
  bash "$0" main.tex
  bash "$0" main_authors.tex
  exit 0
fi
case "$paper_entry" in
  main.tex|main_authors.tex) ;;
  *) echo 'Usage: bash compile.sh [main.tex|main_authors.tex|--both]' >&2; exit 2 ;;
esac
paper_job=${paper_entry%.tex}
mkdir -p build
if [[ -n "${TECTONIC:-}" ]]; then
  "$TECTONIC" --keep-logs --keep-intermediates --outdir build "$paper_entry"
elif command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build "$paper_entry"
elif command -v tectonic >/dev/null 2>&1; then
  tectonic --keep-logs --keep-intermediates --outdir build "$paper_entry"
elif command -v pdflatex >/dev/null 2>&1 && command -v bibtex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build "$paper_entry"
  bibtex "build/$paper_job"
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build "$paper_entry"
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build "$paper_entry"
else
  echo 'Install a LaTeX distribution with IEEEtran, or Tectonic; alternatively upload the Overleaf ZIP.' >&2
  exit 1
fi
cp "build/$paper_job.pdf" "$paper_job.pdf"
echo "Built manuscript/$paper_job.pdf"
