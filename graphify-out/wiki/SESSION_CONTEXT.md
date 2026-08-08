# RADOME session context log

**Updated:** 2026-08-08, America/Belem
**Purpose:** preserve the user-visible chat context across account/session switches. The repository startup protocol in `AGENTS.md` requires reading this file when present.

## Recovery protocol completed in this session

The following required files were read before project work:

1. `AGENTS.md`
2. `README.md`
3. `SUMARIO_E_ROADMAP.md`
4. `ROADMAP_CORRECOES.md`
5. `graphify-out/wiki/SESSION_CONTEXT.md` was absent at startup.

Graphify was available through `/home/python/pyenv/bin/python -m graphify` and was used for focused retrieval and updates.

## User-visible message log

This is a durable log of the chat content visible to the agent. It is not a verbatim dump of hidden system/developer instructions or command outputs.

1. User provided the repository `AGENTS.md` operating instructions and environment context for `/home/jamaj/src/Radome`.
2. User: "Prossiga agora usando a conta do copilot."
3. Assistant recovered mandatory context, inspected the workspace, found pending polarimetry/mast changes, validated LaTeX, updated Graphify and committed with author `github-copilot[bot]`.
4. Assistant advanced into C2 geometry, added a preliminary geodesic verifier, and temporarily paused when the user reported: "O artigo está de lado."
5. Assistant checked `projeto/projetov1.pdf` with `pdfinfo` and page renders; the PDF itself was A4 portrait with page rotation 0. User clarified: "Era so no visualisador do vs code que está girado".
6. User asked how to fix the VS Code extension viewer rotation. Assistant suggested using the PDF viewer rotate command or shortcuts such as `Ctrl+]` / `Ctrl+[`.
7. User: "Funcionou".
8. User: "Prossiga".
9. Assistant resumed C2 geometry work, closing three focused commits:
   - `602f8e5 Add preliminary C2 geodesic geometry verifier`
   - `417bf0f Verify C2 cut geometry topology`
   - `af72037 Complete C2 support geometry checks`
10. User: "Tem como você colocar em um log todas as mensagens do chat? Por que quando troco de uso da conta do git hub para a conta da openia perde todo contexto."
11. Assistant answered that the durable location should be `graphify-out/wiki/SESSION_CONTEXT.md`, because the repository startup protocol already requires future agents to read it.
12. User asked the assistant to continue into C3. The assistant recovered the current roadmap and closed three focused increments: aviation receiver paths, independent experiment protocols, and a reproducible acquisition/horizon screening budget.
13. During the first C3 increment, the assistant detected and prevented a regression to obsolete cross-band polarimetry; the approved C1 same-band restriction and corrected Figure 5 were preserved.
14. A Graphify command was briefly started from `/home/jamaj/src` instead of the repository root. It was terminated, rerun correctly from `/home/jamaj/src/Radome`, and the orphan `/home/jamaj/src/graphify-out/.rebuild.lock` was removed.
15. User: "Grave o status da sessão e atualize a documentação, escpecialmente o roadmap".

## Commits created in this session

All commits below used author `github-copilot[bot] <198982749+github-copilot[bot]@users.noreply.github.com>` as requested. The committer remained the local Git identity.

- `d557c15 Define four-channel polarimetric mast proposal`
- `602f8e5 Add preliminary C2 geodesic geometry verifier`
- `417bf0f Verify C2 cut geometry topology`
- `af72037 Complete C2 support geometry checks`
- `660ad44 Define C3 aviation receiver paths`
- `8e15f3a Separate C3 experiment protocols`
- `f498055 Add C3 acquisition screening budget`

## Current technical state

- C0 baseline was already approved with explicit blockers.
- C1 polarimetry is approved at the architectural level.
- C2 is now marked approved at the parametric level in `ROADMAP_CORRECOES.md`.
- C3 is in progress. Its spectral architecture, aviation paths, experiment separation and acquisition/horizon screening are complete; RF cascade, link and site budgets remain open.
- Deliberate first-demonstrator gaps are `323–470 MHz` and `860–960 MHz`.
- A dedicated `960–1215 MHz` aviation aperture supplies independent UAT 978 MHz and 1090ES paths; neither service is assigned to the `470–860 MHz` UHF Yagi.
- `EXP-006`, `EXP-007` and `EXP-008` separately control cooperative direct ADS-B, known-transmitter calibration and bistatic reflection.
- `projeto/spectral/verify_c3_acquisition_budget.py` reproduces:
  - aviation direct paths: `512 Mbit/s/node`, `0.64 GB/node/10 s`;
  - known UHF transmitter: `800 Mbit/s/node`, `1.00 GB/node/10 s`;
  - bistatic reference plus surveillance: `1600 Mbit/s/node`, `2.00 GB/node/10 s`;
  - screening mutual horizon: `542.3 km` for a 1000 m station and 10000 m aircraft.
- NF, IP3 and usable dynamic range are intentionally unassigned until measured site RFI and a cascaded component budget exist.
- The C2 geometry source is `projeto/geometry/verify_radome_geometry.py`.
- The C2 verifier currently reports:
  - base icosahedron: `V=12`, `E=30`, `F=20`;
  - class-I frequency-2 closed mesh: `V=42`, `E=120`, `F=80`, Euler `2`;
  - chord classes at reference scale: `2.0000 m` and `2.2617 m`;
  - macroface chord: `3.8478 m`;
  - radius: `3.6594 m`;
  - diameter: `7.3189 m`;
  - cut coordinate: `z/R=-0.573576`, polar angle `125 deg`;
  - cut segment: `V=51`, `E=124`, `F=74`, Euler `1`;
  - support ring diameter: `5.9953 m`;
  - direct 4 m x 4 m base support: false;
  - proposed transition square: `6.60 m`, minimum with margin `6.5953 m`, transition ok true.

## Validation already run

For the C2 and C3 changes:

- `python3 projeto/geometry/verify_radome_geometry.py`
- `python3 projeto/spectral/verify_c3_acquisition_budget.py`
- Full LaTeX sequence from `projeto/`:
  - `pdflatex -interaction=nonstopmode -halt-on-error projetov1.tex`
  - `bibtex projetov1`
  - `pdflatex -interaction=nonstopmode -halt-on-error projetov1.tex`
  - `pdflatex -interaction=nonstopmode -halt-on-error projetov1.tex`
- Log scan:
  - `grep -E '^!|Fatal error|undefined|multiply defined' projetov1.log || true`
- Graphify update:
  - `/home/python/pyenv/bin/python -m graphify update .`

Known remaining LaTeX warnings are pre-existing C6 items: duplicate page anchors from front matter, one overfull hbox in the appendix, and bibliography underfull boxes. No fatal errors or undefined references were found in the final scans.

## Next roadmap focus

Complete the remaining C3 evidence before releasing C4:

1. select the actual UHF and aviation waveforms and receiver components;
2. measure site RFI and close cascaded NF, IP3, usable dynamic range and ENOB;
3. close link margin, terrain, common visibility, GDOP, site coordinates and spectrum authorization for the nominal baseline;
4. convert the three experiment protocols into a versioned three-node dataset and acceptance plan;
5. only then synchronize Blender and figures to the approved C2/C3 parameters in C4.

## Operational notes

- `gh auth status` showed the `jamaj69` token as invalid during this session. Local commits worked; pushing may require re-authentication.
- The PDF orientation issue was only in the VS Code viewer state. The PDF metadata reported A4 portrait and page rotation 0.
- Do not assume C2 Blender synchronization is done. C4 still needs Blender and figures to consume the approved C2 parameters.
