# RADOME session context log

**Updated:** 2026-08-10, America/Sao_Paulo
**Purpose:** preserve the user-visible chat context across account/session switches. The repository startup protocol in `AGENTS.md` requires reading this file when present.

## Recovery protocol completed in this session

The following required files were read before project work:

1. `AGENTS.md`
2. `README.md`
3. `SUMARIO_E_ROADMAP.md`
4. `ROADMAP_CORRECOES.md`
5. `graphify-out/wiki/SESSION_CONTEXT.md`

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
16. User asked to reinterpret every external face as a 2 m triangular tetrahedral cell, with Faraday shielding on the three inward faces, independently shielded ADC/ASIC preprocessing modules and a Blender scene showing tangent vectors on contiguous faces.
17. The first verifier showed that regular tetrahedra with all six edges equal to 2 m produce 120 interpenetrations. A planar frequency-2 icosahedral subdivision preserves 80 equilateral external faces and 120 shared external edges.
18. Assistant created the reproducible tetrahedral verifier, a Blender scene with seven contiguous faces and tangent/normal vectors, updated the article, parameters, ADRs and roadmaps, recompiled the PDF, updated Graphify and committed `c26bd56 Model tetrahedral radome face assembly`.
19. User required shorter inward pyramids to reserve internal space for shielding, power cabling and optical fibres.
20. A depth sweep from 0.20 m to 1.00 m found no collisions for shallow full-face cells. The adopted baseline uses a 0.75 m normal height, 240 independent Faraday walls, 120 inter-cell service corridors and a minimum free-core radius of 2.2730 m.
21. Assistant regenerated the Blender scene and `.blend`, updated the controlled documents and PDF, updated Graphify and committed `e0889e5 Reserve service core with shallow face cells`.
22. User asked whether the session, Graphify and roadmap updates had been persisted. Audit confirmed Graphify and roadmap commits, but found this session log stale and one obsolete “hub” word in the C2 summary; both were corrected in the present increment.
23. User requested replacing the single bilingual article with independent Brazilian Portuguese and English editions. The refactoring introduced `radome-pt-br.tex` with ABNTEX2/ABNT citations, `radome-en.tex` with English language settings, separate chapter trees, shared configuration, language-specific chapter manifests and independently compiled PDFs.
24. User required the project to preserve explicitly that associated reception of the same echo by multiple antennas/faces of one radome and by other integrated radomes reduces measurement uncertainty through timestamped, calibrated fusion. The wording was strengthened in both editions: valid additional information cannot increase weighted-least-squares covariance and strictly reduces it along non-redundant observable directions; experiments quantify the magnitude rather than establish the principle. The timing chapter now states that face channels share the node's central time base and that radomes use a common network epoch continuously checked through simultaneous GNSS, frequency-reference, White Rabbit, holdover and RF-delay calibration techniques.
25. User rejected any remaining modal wording such as “may reduce” and pointed to the ISO GUM Part II treatment. The authoritative editions contained no remaining modal statement after commit `69170fc`; the project then added the official JCGM 102:2011 (GUM Supplement 2) reference and cited its multivariate treatment of input quantities, covariances and output quantities directly in the uncertainty-reduction argument.
26. User clarified that receive-only operation using echoes of perfectly known external emissions makes the station much less visible. The project separated two signatures: emission detectability is necessarily lower than for an equivalent active radar because RADOME generates no illumination or RF scan, and any externally observed contribution is secondary scattering; the magnitude of structural scattering/RCS reduction from geometry and absorbers remains a measurable hypothesis. Both editions preserve the emission-discretion claim without asserting absolute invisibility.
27. User required a permanent assumption that potential rivals with remote-sensing capability will map every deployed radome. ADR-016 now treats site coordinates, silhouette and physical presence as eventually known through optical/SAR observation. Security no longer depends on geographic secrecy or visual invisibility; it relies on receive-only operation, distribution, redundancy, physical/cyber protection, modular recovery and continuity after node loss. Passivity remains valuable because a mapped station still does not reveal activity or operating mode through dedicated radar emissions.
28. User required incorporation of advanced-aircraft jamming: emissions intended to obscure active air-defence radars make their source more observable to passive radomes and can support position/vector estimation. ADR-017 and `EXP-011` now treat jamming as a non-cooperative direct emitter observed through power, spectrum, AOA, timestamps and FDOA/Doppler. The controlled claim preserves the advantage while distinguishing the radiation source from the aircraft when jammers are directional, coherent, towed, expendable, distributed or stand-off.
29. User requested similar pagination for the two editions. The Brazilian ABNTEX2 master changed from 12 pt/openright/twoside to 11 pt/openany/oneside, removing blank recto-alignment and pre-textual verso pages without altering technical content, margins or figures. The Portuguese edition decreased from 53 to 36 pages, while English remains at 35; ADR-018 accepts the single residual page rather than distort the layout.
30. User asked for a full render pass including Blender on a machine with a better GPU and requested verification that Blender works well there. Assistant recovered repository context, used Graphify for focused retrieval, ran the figure generators, Chromium SVG-to-PDF export, Blender scene renders and both authoritative LaTeX builds, and confirmed that the real headless Blender render workloads completed successfully despite non-blocking EGL fallback, PulseAudio and thumbnail-cache warnings.
31. During the render pass, `generate_fig12_3d.py` exposed that the default `python3` resolved to `/usr/bin/python3` with a mismatched Matplotlib installation from `~/.local`, where `mpl_toolkits.mplot3d` failed. The shared interpreter `/home/python/pyenv/bin/python` already had working Matplotlib and `mplot3d`.
32. User clarified that the default Python environment is `/home/python/pyenv` and requested that `PYTHONENV` point there and that Matplotlib be corrected. Assistant updated workspace defaults and project references to prefer `/home/python/pyenv/bin/python`, added a writable `MPLCONFIGDIR`, and changed the executable shebangs for the geometry and spectral verification scripts.
33. Assistant updated the tracked workspace file `Radome.code-workspace` to set `python.defaultInterpreterPath` to `/home/python/pyenv/bin/python` and to export `PYTHONENV`, `VIRTUAL_ENV`, `MPLCONFIGDIR` and a `PATH` preferring `/home/python/pyenv/bin`. It also updated the ignored `.vscode/settings.json` locally with matching values for the current machine.
34. User showed `env | grep PYTHONPATH` returning `PYTHONPATH=/home/python/pyenv/bin`. Assistant identified that as wrong because `PYTHONPATH` should not point to a `bin` directory, then added `PYTHONPATH=""` to the tracked workspace terminal environment and committed that focused follow-up separately.
35. User requested rerunning all programs. Assistant reran the three Python verification scripts under `/home/python/pyenv/bin/python`, regenerated the common and localized figures, reran Chromium headless SVG export, reran all Blender scripts and rebuilt `radome-en.pdf` and `radome-pt-br.pdf`. The final log scan again found no fatal errors, undefined references or multiply defined labels.
36. User corrected shell startup files and asked for a final sanity check in a fresh login shell with `env | grep PYTHONPATH` and a Matplotlib `mplot3d` import. Assistant found that the login shell still reported `PYTHONPATH=/home/python/pyenv/bin` and did not have `python` on `PATH`, suggesting another login-shell startup file was still overriding the environment. User then reported an interactive shell prompt showing `(pyenv)` and `PYTHONPATH=/home/python/pyenv`, and stated an intention to restart.
37. User requested that this session be logged before restarting. Assistant updated this durable context file so the next agent can recover the Python-environment fixes, the full rerun results and the remaining shell-environment caveat.
38. User required a stricter repository-hygiene rule: if the Git tree is not clean after a completed change, remaining files must either be committed in a coherent focused change or explicitly ignored. Future agents should not leave a dirty tree as “expected”.
39. User clarified that `SESSION_CONTEXT.md` should indeed be committed, and strengthened the durability rule: everything needed to recover context and reproduce the build must be present in local Git and intended to exist in the remote repository as well.
40. User observed that Portuguese and English figure text differs substantially in width and requested language-specific generation. The figure localizer retained common geometry masters but gained independent English and Portuguese composition profiles, multiline fitting constrained by block width and height, language-specific title/key widths and annotation offsets. Both localized sets and authoritative PDFs were regenerated and visually audited.
41. User rejected the resulting Figure 1 as visually poor. Its common geometry master was redesigned as a compact hierarchy with a wide external-source card, three aligned receiving-node cards carrying radome glyphs, separated illumination and calibrated-observation paths, and a central association/fusion card. Localized labels now sit directly inside the functional blocks in both editions.
42. User required the three Figure 1 cards to identify actual stations as `Radome A`, `Radome B` and `Radome C`, and the lower block as `Central de comando` / `Command center`. The localized key and both LaTeX captions were updated consistently; the caption preserves that the command center performs association and fusion.
43. User reported that Figure 11 labels were completely misaligned. The root cause was a Chromium date header in the Letter-size intermediate PDF: the localizer cropped the header together with the horizontal SVG, producing a vertical canvas incompatible with normalized coordinates. The documented export now disables PDF headers/footers; the clean horizontal master was regenerated, and stack/channel labels are centred directly inside their coloured elements while only free-form geometry labels remain callouts.
44. User rejected Figure 11 again and asked for a simpler workflow without Chrome. The SVG/PDF/browser path was removed. `generate_updated_figures.py` now creates the common Figure 11 master directly with Matplotlib as a wide two-part diagram: face-normal crossed Yagis at left and large independent shielded VHF/UHF receive-chain blocks at right, converging on common timing and optical-fibre service. Both localized editions derive from that PNG master.
45. User initiated national geospatial optimization of radome sites. The objective is the smallest network covering Brazil at controlled flight-height surfaces, prioritizing ridgelines, prominence, visible area and cities visible around each site. Continental sites require line of sight to at least one peer; oceanic islands are explicitly exempt. The initial contract uses 150 m, 3,000 m and 10,000 m AGL surfaces, records propagation assumptions in JSON and separates versioned source manifests from ignored raw geospatial data.
46. The discrete site optimizer is implemented independently of GIS dependencies. It solves a binary mixed-integer coverage model, minimizes selected-site cardinality, uses engineering score only as a tie-breaker, enforces a selected visible peer for every continental site and permits explicitly exempt oceanic candidates to remain isolated. Synthetic tests cover the continental pair, island exemption, isolated-site rejection and missing coverage reporting.
47. User narrowed the active optimization to continental Brazil only. Each oceanic archipelago or nearby island group will be a separate future case with exactly one locally optimized radome; these sites do not participate in the current national minimum or continental line-of-sight graph.
48. User required a dedicated root `geoespacial/` directory. The site-selection module, tests, configuration, source manifests and ignored raw-data tree were moved out of `projeto/` into that directory. The official IBGE BC250 2025 GeoPackage archive was downloaded, ZIP-tested and SHA-256 verified; its extracted 71-layer GeoPackage exposes the required city, boundary, relief-point, road and energy layers.
49. The official TOPODATA GeoTIFF directory was inventoried reproducibly. It lists 556 numeric-altitude `ZN` archives totalling about 32.19 GiB at the directory's rounded advertised sizes. The project will intersect tile footprints with the continental mask before download instead of blindly acquiring the entire index.
50. A first continental BC250 screening was generated as CSV and QGIS-ready GeoJSON. It reduces 127 quoted-height points to 75 candidates at 10 km spacing and ranks them with an explicitly provisional 60% elevation, 25% nearby-city count and 15% eight-sector city-balance score. Pico da Bandeira, Pedra da Mina and Agulhas Negras lead this logistics-aware screen; Pico da Neblina and Monte Roraima remain retained but score lower because nearby-city density is sparse. The report states that proximity is not visibility and that the sparse, Southeast-biased BC250 points cannot establish national coverage.
51. User requested graph analysis with radius-scaled nodes at every Brazilian capital, airport or air command and nearby-city count as a node attribute. The preliminary graph contains 27 Brazilian capitals and 104 BC250 airport complexes. Local elevation is sampled from cached Mapzen Terrain Tiles; coverage radius reaches a 3,000 m altitude surface with effective-Earth-radius factor 4/3. The 131-node GraphML has 109 curvature-only candidate edges, 68 components and 39 isolates. Radius and edges are explicitly geometric upper bounds pending TOPODATA terrain occlusion. Air commands remain pending because no corresponding official BC250 layer exists.
52. User required sufficient scripts and documentation to support later incorporation of the site-selection process into the bilingual article. `geoespacial/METODOLOGIA_ARTIGO.md` now defines objective, provenance, equations, candidate construction, graph semantics, MILP optimization, required report fields, reproducibility commands and publication safeguards. `run_pipeline.sh` provides one-command validation and regeneration from the verified local BC250.
53. User requested an official-source search for cellular towers, airports, air bases and related infrastructure. BC250 2025 supplies airport complexes and runways but its jurisdiction/classification/altitude fields are mostly null or unknown. The historical BC250 2015 Energy and Communication ZIP was downloaded and verified; it contains communication lines, not tower points. Current licensed cellular ERB locations must come from Anatel's SMP station dataset. Civil aerodromes should be reconciled with ANAC; public military/aeronautical classification should use AISWEB/DECEA AIP/ROTAER/WFS. Air commands remain pending an official public dataset.
54. The current ANAC CSVs were downloaded and inventoried: 496 public aerodromes, 3,856 private aerodromes, 1,595 heliports and 203 helidecks. DECEA GEOAISWEB exposes 421 WFS feature types; 13 aerodrome, runway, obstacle, navigation-aid and controlled/defense-airspace layers were selected. Anatel's 2026-08-10 general licensed-stations ZIP was downloaded and verified (223,059,863 compressed bytes; SHA-256 `b77abb225b4ad03bc8b8c6a27913e0b6d851873bab3bd483e66d86712dd5eec1`), but it does not contain the catalog's dedicated SMP resource. The dedicated “Estações do Serviço Móvel Pessoal - SMP” CSV remains a separate acquisition target.
55. The dedicated Anatel SMP resource URL was recovered from the catalog's loaded resource metadata and downloaded. `estacoes_smp.zip` has SHA-256 `6a032a50d842c32f1f2a7d7e052cf82cd383bbeccc7a55d651dd02b5bee3eab8` and contains a 981,622,204-byte CSV with 3,284,526 licensed coordinate-bearing records, 112,934 station numbers and 105,726 distinct coordinates rounded to five decimals. The coordinate count is an approximate physical-site count pending spatial co-location consolidation.
56. User requested municipality nodes with x/y/z, population, visual size and IBGE-code links from cellular towers and later emitters. The canonical layer is composed from BC250 municipal geometry and seats, Censo 2022 population and preliminary terrain elevation. The first network has 5,571 municipality nodes, 105,726 aggregated SMP-site nodes and 105,726 `located_in` edges. Every SMP site received an IBGE municipality code by propagation across co-located records; 23 sites retain a conflict flag. Boa Esperança do Norte (5101837), created after the 2022 Census, has unknown rather than zero population. The methodology and article caveats are documented in `geoespacial/METODOLOGIA_ARTIGO.md`.
57. User ordered acquisition and municipal integration of broadcast and repeater stations. The official Anatel broadcast ZIP was downloaded and verified (SHA-256 `c921e2d34d8fa4f6f76273d6bc2ce14a8b936cb5700a2a895274c5c72c517cb8`). It contains 35,126 coordinate-bearing TV/RTV/FM/OM/RTR-related records; only 18,285 `C4 — Canal Licenciado` records enter the active-illuminator graph, aggregated into 11,921 sites. All sites received an IBGE code; 117 retain a municipal-code conflict flag. Vacant, suspended, pending and awaiting-licensing channels remain inventory-only.
58. User requested a detailed geospatial roadmap and durable preservation of all phase instructions for later methodology writing. `geoespacial/REQUISITOS_GEOLOCALIZACAO.md` now records the continental scope, separate island studies, minimum-site objective, altitude/city/logistics criteria, LOS/connectivity, municipality-node semantics, emitter integration and reproducibility rules. `geoespacial/ROADMAP_GEOESPACIAL.md` inventories acquired, integrated, identified, pending and public-source-blocked layers; defines graph node/edge types; and specifies phases 0–10 with gates, deliverables and the recommended next sequence.
59. User requested that the geospatial work be made an explicit subproject of the main project, which is the bilingual article, and asked Graphify to identify the next phase. `geoespacial/SUBPROJETO.md` now defines the parent relationship, controlled documents, deliverables and article-integration gate. The active milestone is M3/Fase 3: freeze the 13 selected DECEA layers by AIRAC cycle, reconcile DECEA with ANAC and BC250, link objects to municipalities and preserve official provenance. Remaining Phase 2 radio-link, conflict and co-location work stays mandatory as a parallel closure track.
60. User requested verification of technology and emission spectrum in Anatel SMP and broadcast data. The SMP source explicitly provides generation, technology, 5G type, Tx/Rx centres, band/subband and emission designation for 3,284,526 records; all designation bandwidth prefixes were decoded into per-record preliminary Tx intervals. The broadcast source provides service, channel and centre frequency for 35,126 records but no per-record emission designation or occupied bandwidth, so exact limits require a versioned regulatory channelization table. The audit preserves OM source values as kHz and normalizes them to MHz, marks nonphysical Rx values unavailable and keeps `FreqRxMHz` separate from ERB emissions.
61. User asked whether DECEA/ICA or FAB sources provide coordinates and altitudes for VOR, NDB and related RF emitters. The official GEOAISWEB WFS layers `ICA:vor`, `ICA:ndb`, `ICA:dme` and `ICA:navaids` were downloaded and hashed. They contain complete coordinates for 77 VOR, 24 NDB, 173 DME and 124 aggregate relations; official elevations are present for 76, 19, 158 and 30 respectively. VOR and NDB carry explicit frequencies, DME carries its channel and paired VOR/ILS frequency, and the aggregate layer carries no frequency. VOR power and antenna-height fields are entirely empty, and DME RF carriers require an official channel-pairing table. The selected DECEA inventory expanded from 13 to 14 layers when the specific DME layer was added.
62. User ordered durable registration of the DECEA findings, a new geospatial-roadmap analysis and a review of missing official emission layers. `geoespacial/CAMADAS_EMISSOES_OFICIAIS.md` now defines completeness across location, altitude/antenna height, spectrum, power/diagram, municipality and provenance, and establishes gate M2E. The key reprioritization is that the already downloaded 10.45 GB general Anatel package exposes frequency, emission designation, power and antenna fields for SLP/SLE/SARC/STEL and fixed services; it must be classified before assuming that a separate SMP-radio-link file is required. VSAT earth stations and an official interinstitutional weather-radar inventory were added as identified acquisition targets. M2E and M3 are now coupled active tracks before quantitative `illuminates` edges.
63. User required every manipulation of geospatial databases to be performed by Python scripts for repeatability. `geoespacial/POLITICA_REPRODUTIBILIDADE.md` now makes raw inputs immutable and requires versioned Python for acquisition, extraction, cleaning, joins, aggregation and export. `run_pipeline.py` replaces shell orchestration as the authoritative entry point; the shell file is only a compatibility wrapper. `build_candidate_graph.py` now reads GeoPackage layers through Python GDAL bindings instead of invoking `ogr2ogr`, and `acquire_decea_wfs.py` provides atomic WFS downloads with per-layer hashes and manifests. The rule was added to `AGENTS.md` and the normative geolocation requirements.
64. User asked whether reproduction had actually been tested. `verify_reproducibility.py` now executes the authoritative Python pipeline twice over unchanged inputs and compares SHA-256 for seven CSV, GeoJSON, GraphML, JSON and PNG products, writing a versioned machine-readable report and failing if any byte differs.
65. User requested a documentation checkpoint so work can continue without context loss. `geoespacial/STATUS_ATUAL.md` now consolidates parent-project linkage, M2E/M3 status, acquired and integrated layers, 26-test and seven-product byte-reproducibility evidence, controlled gaps and the exact next implementation: a canonical `sitio_fisico`--`antena`--`emissao` model populated first from the audited SMP records with zero-loss/cardinality tests.
66. User ordered continuation of the next M2E gate. `build_canonical_smp.py` now streams the official SMP ZIP into deterministic gzip tables for 105,726 sites, 282,623 antenna proxies and all 3,284,526 source emissions. The intermediate antenna identity is explicitly low-confidence and means station plus sector at a five-decimal rounded site, not a physically verified radiator. Thirty tests pass, no source row or relation was lost, all records have valid site/antenna links, 23 municipal conflicts remain explicit, and 12 pipeline products reproduce byte for byte. The next M2E action is the streaming audit of smaller general-Anatel files, beginning with SARC, fixed broadband and fixed telephony.
67. User ordered continuation. `audit_anatel_general.py` now streams the general Anatel ZIP without extracting 10.45 GB and normalizes 16,876 records from SARC, fixed broadband/SCM and fixed telephony/STFC. Direction is authoritative when explicit; exclusive Tx/Rx and repeater classes are secondary evidence; unknown records are not inferred as emitters. SARC has 4,228 active potential emitters but no usable power/designation, SCM has 1,850 active explicit Tx records with substantially better RF fields, and STFC has no usable RF parameters. No link endpoints were paired. Thirty-three tests pass and 17 products reproduce byte for byte. The next gate migrates only sufficiently evidenced active transmitters/repeaters into the canonical schema.

## Commits created in this session

All commits below used author `github-copilot[bot] <198982749+github-copilot[bot]@users.noreply.github.com>` as requested. The committer remained the local Git identity.

- `d557c15 Define four-channel polarimetric mast proposal`
- `602f8e5 Add preliminary C2 geodesic geometry verifier`
- `417bf0f Verify C2 cut geometry topology`
- `af72037 Complete C2 support geometry checks`
- `660ad44 Define C3 aviation receiver paths`
- `8e15f3a Separate C3 experiment protocols`
- `f498055 Add C3 acquisition screening budget`
- `e0d1e01 Record C3 session and roadmap status`
- `c26bd56 Model tetrahedral radome face assembly`
- `e0889e5 Reserve service core with shallow face cells`

Later environment-fix commits in this session used the local Git identity:

- `962239c Use pyenv Python for project scripts and docs`
- `5eaf1d4 Clear PYTHONPATH in workspace terminal env`

Recent geospatial commits used the local Git identity:

- `d7b0ee5 Documenta roadmap geoespacial e requisitos`
- `a7093e6 Integra estacoes licenciadas de radiodifusao`
- `4241a00 Formaliza subprojeto geoespacial do artigo`
- `52272c7 Audita espectro das estacoes Anatel`
- `b1b10ca Adquire auxilios de navegacao do DECEA`
- `6f292e3 Reavalia camadas oficiais de emissoes`
- `457ddd5 Padroniza manipulacao geoespacial em Python`
- `3b83061 Verifica reproducao byte a byte do pipeline`

## Current technical state

- C0 baseline was already approved with explicit blockers.
- C1 polarimetry is approved at the architectural level.
- C2 was approved for the projected frequency-2 candidate, then reopened by ADR-012 when the external faces were required to be uniformly equilateral with 2 m edges.
- The current C2 candidate has 80 planar-subdivision external faces, 120 shared external edges and no projected midpoint vertices.
- A regular all-edges-at-2 m tetrahedral interpretation is blocked because it produces 120 volumetric interpenetrations.
- The adopted shallow cells have a 0.75 m normal height from external-face centre to local inward apex, zero volumetric collisions, 1.3769 m lateral edges, 240 independent Faraday side walls and 120 inter-cell service corridors.
- Adjacent local apexes are separated by 0.5435–1.1547 m, reserving a minimum internal free-core radius of 2.2730 m for power, optical fibre, bonding, cooling and maintenance distribution.
- C2 remains open for a lower boundary made of complete modules, real wall/joint thicknesses, corridor accessibility, Faraday continuity and a recalculated civil interface.
- C3 is in progress. Its spectral architecture, aviation paths, experiment separation and acquisition/horizon screening are complete; RF cascade, link and site budgets remain open.
- The technical publication now has two authoritative editions: `projeto/radome-pt-br.tex`/`.pdf` and `projeto/radome-en.tex`/`.pdf`. The former bilingual chapters are preserved under `projeto/chapters/legacy-bilingual/` only for traceability.
- ADR-013 fixes the combined VHF/UHF Yagi boom on the outward normal of each external triangular face. The mutually orthogonal transverse directions are 45° and 135° in the local tangent basis.
- Each language edition now uses a localized figure set under `projeto/figures/en/` or `projeto/figures/pt-BR/`. Both sets derive from common geometry masters but carry titles, labels and visual keys in the edition language; this supersedes the short-lived text-free publication rule.
- `projeto/figures/localize_figures.py` now separates common geometry from language-specific composition. English and Portuguese profiles independently control title/key width, font scaling, floating-label width and per-figure offsets; functional-block labels use bounded multiline fitting instead of indiscriminate single-line font reduction.
- The localized figure generator uses figure-specific label coordinates derived from the real centres of the geometry-master blocks. Functional block diagrams place text directly inside the coloured block, reduce the font only when needed to preserve internal margins, and compensate font bearings so the visible glyphs are centred horizontally and vertically. Floating callouts alone use adaptive white boxes sized from the rendered glyph bounds. Nested label boxes and approximate anchor-only placement are not acceptable for publication.
- The two-node aircraft Blender scene uses a bright technical background, enlarged symbolic radomes and aircraft, thick coloured paths, visible AOA cones and localized callouts. The 100 km baseline remains nominal; object enlargement is diagrammatic rather than a physical scale claim.
- The introduction and literature review explicitly define radome as “radar dome” while separating the enclosure from active transmission. RADOME nodes are receive-only: direct emitters are located by AOA triangulation or TDOA/FDOA multilateration, while non-emitting targets require external illuminators and bistatic/multistatic reference-surveillance processing. The primary local source is Qamar, Salazar-Cerreno and Aboserwal (2020), DOI 10.1109/ACCESS.2020.3032881.
- ADR-014 records a candidate architectural innovation: exposed VHF/UHF receiving Yagis combined with individually shielded, absorber-lined pyramidal cells. The hypothesis is lower shell loss on reception plus lower self-interference, coupling and aperture reradiation. Conductive shielding alone is reflective; invisibility is not claimed, and absorber selection, power balance, shielding effectiveness, OTA patterns and angular RCS remain mandatory evidence.
- Four additional local sources were integrated into both literature-review editions on 2026-08-09. Oh et al. (2026, DOI 10.3390/aerospace13030227) experimentally demonstrate package-level integration of a UHF antenna, metallic isolation wall and low-loss GFRP radome, so generic antenna--metal-wall--radome integration is not claimed as novel. Ramanamurthy and Krishna (2016) support coupled mechanical/RF validation but their 15 kHz--18 GHz/75 bar claim is not transferred without reproduction. Abotalebi (2023) and the locally available Tandel (2024) preview support comparison against compact monocone, bicone and planar/FSS alternatives. The candidate novelty is narrowed to the specific external orthogonal different-band Yagis, face-normal boom, shielded/absorber-lined pyramidal cell and distributed receive-only operation.
- ADR-015 controls the cost--performance and localization argument. Exposed antennas, no dedicated transmitter and face-level replacement may reduce shell, RF-power and maintenance costs, but wind/corrosion/lightning/sealing exposure and multiplied channels remain counter-costs; lower life-cycle cost requires a traceable normalized comparison. Bistatic excess delay defines an iso-range ellipsoid, while calibrated AOA, per-face power, Doppler/FDOA and coherent same-band polarization constrain a probabilistic state. Associated valid observations of the same echo from multiple antennas/faces and synchronized radomes add information: weighted-least-squares covariance cannot increase and decreases strictly along non-redundant observable directions. The principle is an architectural/model property; field evidence must quantify the achieved reduction and validate covariance consistency.
- Deliberate first-demonstrator gaps are `323–470 MHz` and `860–960 MHz`.
- A dedicated `960–1215 MHz` aviation aperture supplies independent UAT 978 MHz and 1090ES paths; neither service is assigned to the `470–860 MHz` UHF Yagi.
- `EXP-006`, `EXP-007` and `EXP-008` separately control cooperative direct ADS-B, known-transmitter calibration and bistatic reflection.
- `projeto/spectral/verify_c3_acquisition_budget.py` reproduces:
  - aviation direct paths: `512 Mbit/s/node`, `0.64 GB/node/10 s`;
  - known UHF transmitter: `800 Mbit/s/node`, `1.00 GB/node/10 s`;
  - bistatic reference plus surveillance: `1600 Mbit/s/node`, `2.00 GB/node/10 s`;
  - screening mutual horizon: `542.3 km` for a 1000 m station and 10000 m aircraft.
- NF, IP3 and usable dynamic range are intentionally unassigned until measured site RFI and a cascaded component budget exist.
- The intended shared Python environment for this repository is `/home/python/pyenv`. Project documentation, the tracked workspace file and the executable verification scripts were updated to prefer that interpreter explicitly rather than relying on the system `python3`.
- The workspace terminal defaults now set `PYTHONENV=/home/python/pyenv`, `VIRTUAL_ENV=/home/python/pyenv`, `MPLCONFIGDIR=/tmp/matplotlib-radome` and a `PATH` preferring `/home/python/pyenv/bin`. `PYTHONPATH` is explicitly cleared in the tracked workspace configuration because the previous values `/home/python/pyenv/bin` and `/home/python/pyenv` were both inappropriate import paths.
- The superseded projected C2 geometry remains reproducible in `projeto/geometry/verify_radome_geometry.py` for historical comparison.
- The current ADR-012 source is `projeto/geometry/verify_tetrahedral_face_geometry.py`, which reports:
  - base icosahedron: `V=12`, `E=30`, `F=20`;
  - planar class-I frequency-2 envelope: `V=42`, `E=120`, `F=80`, Euler `2`;
  - all external receiver-face edges: `2.0000 m`;
  - macroface edge: `4.0000 m`;
  - circumradius/inradius: `3.8042 m / 3.0230 m`;
  - shallow-cell height: `0.7500 m`;
  - lateral edges: `1.3769 m`;
  - adjacent-apex separation: `0.5435–1.1547 m`;
  - minimum free-core radius: `2.2730 m`;
  - volumetric collisions: `0`.

## Validation already run

For the C2 and C3 changes:

- `/home/python/pyenv/bin/python projeto/geometry/verify_radome_geometry.py`
- `/home/python/pyenv/bin/python projeto/geometry/verify_tetrahedral_face_geometry.py`
- `/home/python/pyenv/bin/python projeto/spectral/verify_c3_acquisition_budget.py`
- `blender -b --python render_tetrahedral_face_cluster_blender.py` (run from `projeto/figures/`)
- Full LaTeX sequence from `projeto/`:
  - `pdflatex -interaction=nonstopmode -halt-on-error projetov1.tex`
  - `bibtex projetov1`
  - `pdflatex -interaction=nonstopmode -halt-on-error projetov1.tex`
  - `pdflatex -interaction=nonstopmode -halt-on-error projetov1.tex`
- Log scan:
  - `grep -E '^!|Fatal error|undefined|multiply defined' projetov1.log || true`
- Graphify update:
  - `/home/python/pyenv/bin/python -m graphify update .`

For the environment-correction and render-verification follow-up:

- `MPLCONFIGDIR=/tmp/matplotlib-radome /home/python/pyenv/bin/python projeto/geometry/verify_radome_geometry.py`
- `MPLCONFIGDIR=/tmp/matplotlib-radome /home/python/pyenv/bin/python projeto/geometry/verify_tetrahedral_face_geometry.py`
- `MPLCONFIGDIR=/tmp/matplotlib-radome /home/python/pyenv/bin/python projeto/spectral/verify_c3_acquisition_budget.py`
- `MPLCONFIGDIR=/tmp/matplotlib-radome /home/python/pyenv/bin/python generate_updated_figures.py` (from `projeto/figures/`)
- `MPLCONFIGDIR=/tmp/matplotlib-radome /home/python/pyenv/bin/python generate_fig12_3d.py` (from `projeto/figures/`)
- `chromium --headless --no-sandbox --user-data-dir=/tmp/chromium-radome --print-to-pdf=fig11_face_yagi_camadas.pdf file:///home/jamaj/src/Radome/projeto/figures/fig11_face_yagi_camadas.svg`
- `MPLCONFIGDIR=/tmp/matplotlib-radome /home/python/pyenv/bin/python localize_figures.py` (from `projeto/figures/`)
- `blender -b --python render_radome_blender.py`
- `blender -b --python render_aircraft_two_radomes_blender.py`
- `blender -b --python render_tetrahedral_face_cluster_blender.py`
- `blender -b --python render_radome_blender_35S.py` (from `projeto/figures/baseline_35S_concrete_base/`)
- Full authoritative LaTeX sequences from `projeto/`:
  - `pdflatex -interaction=nonstopmode -halt-on-error radome-en.tex`
  - `bibtex radome-en`
  - `pdflatex -interaction=nonstopmode -halt-on-error radome-en.tex`
  - `pdflatex -interaction=nonstopmode -halt-on-error radome-en.tex`
  - `pdflatex -interaction=nonstopmode -halt-on-error radome-pt-br.tex`
  - `bibtex radome-pt-br`
  - `pdflatex -interaction=nonstopmode -halt-on-error radome-pt-br.tex`
  - `pdflatex -interaction=nonstopmode -halt-on-error radome-pt-br.tex`
- Final log scan:
  - `grep -E '^!|Fatal error|undefined|multiply defined' radome-en.log radome-pt-br.log`
- PDF metadata checks:
  - `pdfinfo radome-en.pdf`
  - `pdfinfo radome-pt-br.pdf`
- Graphify update:
  - `/home/python/pyenv/bin/python -m graphify update .`

Known remaining LaTeX warnings are pre-existing C6 items: duplicate page anchors from front matter, one overfull hbox in the appendix, and bibliography underfull boxes. No fatal errors or undefined references were found in the final scans.

## Next roadmap focus

For the geospatial subproject, execute M2E before quantitative RF edges:

1. migrate sufficiently evidenced active SARC/SCM transmitters or repeaters into the canonical schema;
2. classify SLE/SLP/STEL and pair radio links only with explicit keys and geometry;
3. continue M3 reconciliation.

The compact restart checkpoint is `geoespacial/STATUS_ATUAL.md`.

For the article hardware track, complete the remaining C3 evidence before releasing C4:

1. select the actual UHF and aviation waveforms and receiver components;
2. measure site RFI and close cascaded NF, IP3, usable dynamic range and ENOB;
3. close link margin, terrain, common visibility, GDOP, site coordinates and spectrum authorization for the nominal baseline;
4. convert the three experiment protocols into a versioned three-node dataset and acceptance plan;
5. only then synchronize Blender and figures to the approved C2/C3 parameters in C4.

In parallel, close the reopened C2 tetrahedral candidate before treating the current Blender scene as fabrication geometry:

1. select a lower boundary composed of complete face modules;
2. replace zero-thickness walls with structural and conductive thicknesses plus assembly tolerances;
3. size power/fibre corridors, bend radii, segregation, thermal paths and maintenance access;
4. verify Faraday continuity, filtered penetrations, bonding and lightning-current paths;
5. recalculate the support transition and foundation for the selected modular boundary.

## Operational notes

- `gh auth status` showed the `jamaj69` token as invalid during this session. Local commits worked; pushing may require re-authentication.
- The PDF orientation issue was only in the VS Code viewer state. The PDF metadata reported A4 portrait and page rotation 0.
- On 2026-08-09, `projeto/radome-en.pdf` was found with trailing corrupted data after an interrupted or concurrent write: `pdfinfo` could not read its cross-reference table even though an earlier valid PDF body remained embedded in the file. The English edition was rebuilt under an isolated job name, visually audited across all 31 pages, validated as A4/PDF 1.5 and only then moved over the authoritative artifact. Future diagnosis must distinguish a successful LaTeX log from the integrity of the PDF file currently on disk.
- `fig16_tetrahedral_face_cluster.png` and `radome_tetrahedral_face_cluster.blend` represent the current ADR-012 candidate, including tangent vectors, shallow cells and the reserved service core. They are architectural visualization, not fabrication approval.
- Blender headless renders on this machine consistently reported EGL initialization errors before falling back successfully to surfaceless EGL. The render jobs themselves completed and wrote the expected PNG and `.blend` artifacts; the warnings were non-blocking in this session.
- The preserved baseline Blender script `projeto/figures/baseline_35S_concrete_base/render_radome_blender_35S.py` still writes its outputs to the shared `projeto/figures/fig13_radome_blender.png` and `projeto/figures/fig14_radome_interior_blender.png` paths rather than to the preserved baseline directory, so rerunning it overwrites the main radome outputs.
- A direct headless Blender Python probe of `gpu.platform` crashed and wrote `/tmp/blender.crash.txt`, but the actual project Blender render scripts completed successfully; render success is the more trustworthy health signal for this environment.
- When diagnosing the Python environment, remember that the shell-level state may differ between interactive shells and fresh login shells. A fresh login shell late in this session still showed stale values from startup files (`PYTHONPATH=/home/python/pyenv/bin` and no `python` on `PATH`), while a later user-reported interactive shell showed `(pyenv)` and `PYTHONPATH=/home/python/pyenv`. The preferred final state is to leave `PYTHONPATH` unset and rely on `PATH` plus `VIRTUAL_ENV`.
