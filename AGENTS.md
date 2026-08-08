# RADOME Project Agent Guide

This repository contains the bilingual technical project for a distributed multiband passive electromagnetic sensing network. The main article is assembled from modular LaTeX chapters in `projeto/`.

## Mandatory Startup Context Recovery

Every agent that opens or resumes work in this repository must recover the stable project context before declaring itself ready, proposing changes or executing project work.

Read, in this order:

1. `AGENTS.md` — operating, generation and validation rules;
2. `README.md` — mission, scope and repository map;
3. `SUMARIO_E_ROADMAP.md` — consolidated technical context and development path;
4. `ROADMAP_CORRECOES.md` — active inconsistency-remediation plan and current gates;
5. `graphify-out/wiki/SESSION_CONTEXT.md`, when present — compact generated context.

After those reads, use Graphify for focused retrieval when `graphify-out/graph.json` exists. Only then report that context recovery is complete. Do not claim readiness merely because the files exist: their current contents must have been read during the session.

If one of the four required Markdown files is missing or unreadable, report the missing file and do not claim full readiness. Work needed to restore the missing context file is still allowed.

## Graphify

Graphify is installed in the shared Python environment, not necessarily in the shell `PATH`. Invoke it only as:

```bash
/home/python/pyenv/bin/python -m graphify <command>
```

Repository workflow:

- use `query "<question>" --budget 1500` for focused project questions;
- use `path`, `explain`, `affected` and `god-nodes` for relationships and impact;
- use `update .` after relevant document or script changes;
- use `extract . --code-only` only when rebuilding the local graph from scratch without an LLM backend;
- consult `graphify-out/wiki/index.md` for broad navigation when available;
- do not treat generated graph relationships as engineering evidence: requirements and technical claims still require source documents, calculations or measurements.

If Graphify is unavailable, continue with `rg` and the stable context files, state the limitation, and do not fabricate graph results.

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

## Mandatory Commit Per Change

Every completed, coherent project change must be committed before work starts on the next change. This rule exists to preserve an auditable engineering history and applies to technical text, parameters, decisions, figures, scripts, Blender assets, generated PDFs and project workflow files.

Required sequence:

1. make one focused change or roadmap gate;
2. run the focused validation required by the affected files;
3. regenerate dependent figures or PDFs when applicable;
4. update Graphify with `/home/python/pyenv/bin/python -m graphify update .`;
5. inspect `git status`, `git diff --check` and the focused diff;
6. commit the complete focused change with a descriptive message;
7. confirm the commit with `git status --short` and `git log -1 --oneline`;
8. only then begin the next change.

Do not combine unrelated corrections in one commit. Do not leave a completed gate uncommitted while starting another gate. Generated artifacts that are authoritative or required for reproducibility, including `projeto/projetov1.pdf` after a chapter change, belong in the same commit as their source change. Push only when requested by the user or when the active publishing workflow explicitly requires it.

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

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `/home/python/pyenv/bin/python -m graphify query "<question>" --budget 1500` when graphify-out/graph.json exists. Use the same module invocation with `path "<A>" "<B>"` for relationships and `explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code or project documentation, run `/home/python/pyenv/bin/python -m graphify update .` to keep the graph current (AST-only, no API cost).
