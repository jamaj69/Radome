# RADOME Project / Projeto RADOME

## Independent editions / Edições independentes

The project has two authoritative and independently compiled editions: [radome-en.tex](radome-en.tex) in English and [radome-pt-br.tex](radome-pt-br.tex) in Brazilian Portuguese. Shared packages live in `config/radome-common.tex`; each master selects its own document class, language and citation conventions. The current controlled identifiers are document version 1.1 and architecture revision 3.

O projeto possui duas edições autoritativas compiladas de forma independente: [radome-pt-br.tex](radome-pt-br.tex), em português brasileiro, e [radome-en.tex](radome-en.tex), em inglês. Os pacotes compartilhados ficam em `config/radome-common.tex`; cada arquivo mestre seleciona sua própria classe, idioma e convenções de citação. Os identificadores controlados atuais são versão do documento 1.1 e revisão da arquitetura 3.

## Structure / Estrutura

- `radome-en.tex`: English master using `report`, English `babel` and `natbib`;
- `radome-pt-br.tex`: mestre brasileiro usando `abntex2`, `babel` e `abntex2cite`;
- `projetov1.tex`: compatibility entry point for the Brazilian edition / entrada de compatibilidade para a edição brasileira;
- `chapters/en/`: English chapters and sections / capítulos e seções em inglês;
- `chapters/pt-BR/`: capítulos e seções em português brasileiro / Brazilian Portuguese chapters and sections;
- `chapters/legacy-bilingual/`: frozen pre-refactoring sources retained for traceability / fontes bilíngues anteriores congeladas para rastreabilidade;
- `config/`: shared preamble and edition-specific chapter manifests / preâmbulo comum e manifestos de capítulos;
- `figures/`: technical figures / figuras técnicas;
- `references.bib`: bibliography copied from `radome_antenna_literature_review` / bibliografia copiada de `radome_antenna_literature_review`;
- `radome-en.pdf` and `radome-pt-br.pdf`: authoritative compiled editions / edições compiladas autoritativas;
- `PARAMETERS.md`: controlled quantitative parameter register / registro controlado de parâmetros quantitativos;
- `DECISIONS.md`: architecture decision record / registro de decisões de arquitetura.
- `antenna_designs/`: proposed antenna baselines awaiting simulation and measurement / baselines propostas de antenas aguardando simulação e medição.

## 3D baseline / Linha de base 3D

The previous Blender scene is preserved in `figures/baseline_35S_concrete_base/`. This historical baseline contains the 35-degree-south radome cut, the 4 m x 4 m x 3 m reinforced-concrete base, the access opening, the internal pyramid and the external VHF Yagi. ADR-012 supersedes its projected face geometry but does not overwrite the preserved scene.

A cena Blender anterior está preservada em `figures/baseline_35S_concrete_base/`. Essa baseline histórica contém o corte do radome em 35 graus sul, a base de concreto armado de 4 m x 4 m x 3 m, a abertura de acesso, a pirâmide interna e a Yagi VHF externa. A ADR-012 substitui sua geometria projetada de faces, mas não sobrescreve a cena preservada.

The tetrahedral candidate is generated separately. It shows seven contiguous 2 m faces with 0.75 m inward depth, independent Faraday side walls, inter-cell power/fibre corridors, a reserved internal core, two shielded ADC/ASIC enclosures per dual-polarized aperture and the local tangent/normal bases.

A candidata tetraédrica é gerada separadamente. Ela mostra sete faces contíguas de 2 m com profundidade interna de 0,75 m, paredes Faraday independentes, corredores intercelulares de energia/fibra, núcleo interno reservado, dois invólucros ADC/ASIC blindados por abertura dual-pol e as bases tangentes/normais locais.

```bash
python3 geometry/verify_tetrahedral_face_geometry.py
cd figures
blender -b --python render_tetrahedral_face_cluster_blender.py
```

Outputs / Saídas:

- `figures/fig16_tetrahedral_face_cluster.png`;
- `figures/radome_tetrahedral_face_cluster.blend`.

## Compilation / Compilação

From this directory / A partir deste diretório:

```bash
pdflatex -interaction=nonstopmode -halt-on-error radome-en.tex
bibtex radome-en
pdflatex -interaction=nonstopmode -halt-on-error radome-en.tex
pdflatex -interaction=nonstopmode -halt-on-error radome-en.tex

pdflatex -interaction=nonstopmode -halt-on-error radome-pt-br.tex
bibtex radome-pt-br
pdflatex -interaction=nonstopmode -halt-on-error radome-pt-br.tex
pdflatex -interaction=nonstopmode -halt-on-error radome-pt-br.tex
```

Add or reorder chapters in the matching manifest under `config/`. Write language-specific content directly in `chapters/en/` or `chapters/pt-BR/`; ordinary `\\chapter`, `\\section` and `\\subsection` commands are supported.

Adicione ou reordene capítulos no manifesto correspondente em `config/`. Edite o conteúdo diretamente em `chapters/en/` ou `chapters/pt-BR/`; os comandos usuais `\\chapter`, `\\section` e `\\subsection` são suportados.

Both editions must reference the same figure files. Figures are language-neutral and contain no embedded text; all verbal explanation belongs in the localized LaTeX captions.

As duas edições devem referenciar os mesmos arquivos de figura. As figuras são independentes de idioma e não contêm texto incorporado; toda explicação verbal pertence às legendas LaTeX localizadas.
