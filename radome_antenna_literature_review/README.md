# Build instructions

The package contains:

- `main.tex` — standalone LaTeX source using `natbib` and `plainnat`;
- `references.bib` — BibTeX database containing every cited Consensus paper;
- `review.md` — consolidated Markdown version with rendered numeric citations and bibliography;
- `review.pdf` — compiled PDF;
- `build.sh` — reproducible build script.

## Required tools

- `pdflatex`
- `bibtex` (or `bibtex.original` on systems where the `bibtex` alternative is broken)

## Manual build

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Automated build

```bash
chmod +x build.sh
./build.sh
```

The source was tested with pdfTeX 3.141592653-2.6-1.40.26 and BibTeX 0.99d.
