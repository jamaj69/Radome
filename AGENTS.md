# RADOME Project Agent Guide

This repository contains the bilingual technical project for a distributed multiband passive electromagnetic sensing network. The main article is assembled from modular LaTeX chapters in `projeto/`.

## Project Layout

- `projeto/projetov1.tex`: master LaTeX document;
- `projeto/chapters/`: bilingual chapter files included by the master;
- `projeto/figures/`: technical figures, Blender scenes and render scripts;
- `projeto/references.bib`: bibliography used by the master document;
- `projeto/projetov1.pdf`: compiled technical article;
- `projeto/figures/radome_v1_3d.blend`: current Blender scene;
- `projeto/figures/baseline_35S_concrete_base/`: preserved 3D baseline before later scene expansions.

## LaTeX Article Commands

Run these commands from `projeto/`:

```bash
cd /home/jamaj/src/Radome/projeto
pdflatex -interaction=nonstopmode -halt-on-error projetov1.tex
bibtex projetov1
pdflatex -interaction=nonstopmode -halt-on-error projetov1.tex
pdflatex -interaction=nonstopmode -halt-on-error projetov1.tex
```

The final LaTeX pass is the authoritative pass for undefined references and citations. Intermediate citation warnings are expected before BibTeX and subsequent LaTeX passes.

Useful validation command:

```bash
grep -E '^!|Fatal error|undefined|multiply defined' /tmp/projetov1_*log /tmp/projetov1_*.log 2>/dev/null || true
```

The master document uses the bibliography copied from `radome_antenna_literature_review/references.bib`. Do not replace it with an unrelated bibliography without updating the literature-review chapter.

## Regenerating Project Figures

The current generated figures are produced by:

```bash
cd /home/jamaj/src/Radome/projeto/figures
python3 generate_updated_figures.py
```

This regenerates the current zoning, spectral partition and polarimetry figures:

- `fig02_zonamento_radome.png`;
- `fig04_particionamento_espectro.png`;
- `fig05_polarimetria.png`;
- `fig07_sincronizacao.png`, including GNSS timing reference, atomic clock, White Rabbit and RF-delay calibration.

The SVG face diagram is converted to PDF with Chromium because ImageMagick may block SVG through its security policy:

```bash
cd /home/jamaj/src/Radome/projeto/figures
chromium --headless --no-sandbox --disable-gpu \
  --print-to-pdf=fig11_face_yagi_camadas.pdf \
  file:///home/jamaj/src/Radome/projeto/figures/fig11_face_yagi_camadas.svg
```

## Blender Rendering

The main radome scene uses Blender Eevee for fast technical renders:

```bash
cd /home/jamaj/src/Radome/projeto/figures
blender -b --python render_radome_blender.py
```

Outputs:

- `fig13_radome_blender.png`: external perspective;
- `fig14_radome_interior_blender.png`: internal inspection perspective;
- `radome_v1_3d.blend`: saved Blender scene.

The current geometry includes an upper radome cut at 35 degrees south, a reinforced-concrete base of approximately 4 m x 4 m x 3 m, an access opening, an inward triangular pyramid and crossed external VHF/UHF Yagis sharing the apex support axis.

The Yagi arrangement is:

- larger VHF antenna;
- smaller UHF antenna;
- common support/boom axis;
- transverse elements in orthogonal planes;
- independent RF chains, ADCs and ASICs.

Blender may print `libGL` or Nouveau messages in headless mode. If the Eevee render completes and writes the PNG, those messages did not prevent the render.

## Aircraft and Illuminator Scenario

The two-node aircraft validation scene uses a nominal 100 km baseline:

```bash
cd /home/jamaj/src/Radome/projeto/figures
blender -b --python render_aircraft_two_radomes_blender.py
```

Outputs:

- `fig15_aircraft_two_radomes_100km.png`;
- `radome_two_nodes_aircraft_100km.blend`.

The scenario models ADS-B 1090ES at 1090 MHz, with 978 MHz UAT as contextual alternative, and independent UHF television and cellular illuminators. Observables include received power, AOA, hardware timestamps, TDOA and Doppler/FDOA. Direct-emitter checks and bistatic-reflection checks must remain separate models.

## Reproducibility and Editing Rules

- Preserve the bilingual structure: English content followed by Portuguese content in each chapter.
- Keep figures and scripts in `projeto/figures/`.
- Use the existing measured/calibrated terminology; do not claim operational performance from a conceptual diagram.
- Distinguish architectural solutions from parameters still requiring simulation or measurement.
- Do not commit Blender backup files such as `*.blend1`.
- After changing a figure or chapter, compile `projetov1.tex` before claiming completion.
- Keep the baseline scene untouched; create a new named baseline or branch of the scene for major 3D expansions.

## GitHub Workflow

Check the workspace before committing:

```bash
cd /home/jamaj/src/Radome
git status --short
git diff --stat
```

Commit and publish focused changes:

```bash
git add <files>
git commit -m "Describe the focused project change"
git push
```

After publishing:

```bash
git status --short
git log -1 --oneline
```

The repository remote is `git@github.com:jamaj69/Radome.git`.
