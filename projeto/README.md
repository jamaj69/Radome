# RADOME V1 Project / Projeto RADOME V1

## Master document / Documento mestre

The project is organized around [projetov1.tex](projetov1.tex). It is the master LaTeX file and contains the preamble, bilingual abstract and resumo, chapter order, figures path, appendix and bibliography.

O projeto é organizado em torno de [projetov1.tex](projetov1.tex). Ele é o arquivo mestre LaTeX e contém o preâmbulo, abstract e resumo bilíngues, ordem dos capítulos, caminho das figuras, apêndice e bibliografia.

## Structure / Estrutura

- `projetov1.tex`: master file / arquivo mestre;
- `chapters/`: independent bilingual chapters / capítulos bilíngues independentes;
- `figures/`: technical figures / figuras técnicas;
- `references.bib`: bibliography copied from `radome_antenna_literature_review` / bibliografia copiada de `radome_antenna_literature_review`;
- `projetov1.pdf`: compiled version / versão compilada.

## Compilation / Compilação

From this directory / A partir deste diretório:

```bash
pdflatex -interaction=nonstopmode projetov1.tex
bibtex projetov1
pdflatex -interaction=nonstopmode projetov1.tex
pdflatex -interaction=nonstopmode projetov1.tex
```

Each chapter presents the English version followed by the Portuguese version. The literature-review chapter uses the bibliography already developed for the project and identifies the technical gap addressed by the proposed architecture.

Cada capítulo apresenta primeiro a versão em inglês e depois a versão em português. O capítulo de revisão de literatura usa a bibliografia já desenvolvida para o projeto e identifica a lacuna técnica abordada pela arquitetura proposta.
