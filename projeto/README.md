# RADOME Project / Projeto RADOME

## Master document / Documento mestre

The project is organized around [projetov1.tex](projetov1.tex). It is the authoritative master LaTeX file and contains the preamble, bilingual abstract and resumo, chapter order, figures path, appendix and bibliography. The current controlled identifiers are document version 1.1 and architecture revision 3.

O projeto é organizado em torno de [projetov1.tex](projetov1.tex). Ele é o arquivo mestre LaTeX autoritativo e contém o preâmbulo, abstract e resumo bilíngues, ordem dos capítulos, caminho das figuras, apêndice e bibliografia. Os identificadores controlados atuais são versão do documento 1.1 e revisão da arquitetura 3.

## Structure / Estrutura

- `projetov1.tex`: master file / arquivo mestre;
- `chapters/`: independent bilingual chapters / capítulos bilíngues independentes;
- `figures/`: technical figures / figuras técnicas;
- `references.bib`: bibliography copied from `radome_antenna_literature_review` / bibliografia copiada de `radome_antenna_literature_review`;
- `projetov1.pdf`: compiled version / versão compilada.
- `PARAMETERS.md`: controlled quantitative parameter register / registro controlado de parâmetros quantitativos;
- `DECISIONS.md`: architecture decision record / registro de decisões de arquitetura.
- `antenna_designs/`: proposed antenna baselines awaiting simulation and measurement / baselines propostas de antenas aguardando simulação e medição.

## 3D baseline / Linha de base 3D

The current Blender scene is preserved in `figures/baseline_35S_concrete_base/`. This baseline contains the 35-degree-south radome cut, the 4 m x 4 m x 3 m reinforced-concrete base, the access opening, the internal pyramid and the external VHF Yagi. It is the reference scene for the next stage, in which identical face modules will be instantiated across the radome.

A cena Blender atual está preservada em `figures/baseline_35S_concrete_base/`. Essa linha de base contém o corte do radome em 35 graus sul, a base de concreto armado de 4 m x 4 m x 3 m, a abertura de acesso, a pirâmide interna e a Yagi VHF externa. Ela é a cena de referência para a próxima etapa, na qual módulos de face idênticos serão instanciados em todo o radome.

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
