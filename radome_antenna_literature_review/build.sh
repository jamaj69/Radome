#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

PDFLATEX="${PDFLATEX:-pdflatex}"
if command -v bibtex >/dev/null 2>&1 && bibtex --version >/dev/null 2>&1; then
  BIBTEX="${BIBTEX:-bibtex}"
elif command -v bibtex.original >/dev/null 2>&1; then
  BIBTEX="${BIBTEX:-bibtex.original}"
elif command -v bibtex8 >/dev/null 2>&1; then
  BIBTEX="${BIBTEX:-bibtex8}"
else
  echo "BibTeX executable not found." >&2
  exit 1
fi

"$PDFLATEX" -interaction=nonstopmode -halt-on-error main.tex
"$BIBTEX" main
"$PDFLATEX" -interaction=nonstopmode -halt-on-error main.tex
"$PDFLATEX" -interaction=nonstopmode -halt-on-error main.tex
"$PDFLATEX" -interaction=nonstopmode -halt-on-error main.tex
cp -f main.pdf review.pdf
