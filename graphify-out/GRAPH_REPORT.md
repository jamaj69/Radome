# Graph Report - Radome  (2026-08-10)

## Corpus Check
- 32 files · ~416,458 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 573 nodes · 614 edges · 42 communities (40 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `24d2be7c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- RADOME V3.md
- Plano Diretor de Infraestrutura Tática
- Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos
- projeto_tecnico_radome_consolidado.md
- RADOME V3 — Arquitetura Eletrônica Distribuída Revisada.md
- Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos
- RADOME — Geodetic Multiband Passive Electromagnetic Sensing Network
- Conceptual and theoretical gaps
- Conceptual and theoretical gaps
- RADOME — Roadmap de correções técnicas e documentais
- RADOME Project Agent Guide
- RADOME — Sumário executivo e roadmap de pesquisa e engenharia
- radome_antenna_literature_review/review.md
- review.md
- Start here: priority reading order
- RADOME — Registro central de parâmetros
- verify_radome_geometry.py
- render_tetrahedral_face_cluster_blender.py
- RADOME Project / Projeto RADOME
- English
- RADOME — Registro de decisões de arquitetura
- Build instructions
- English
- Start here: priority reading order
- Key research groups
- verify_c3_acquisition_budget.py
- Sub-area guide 1: broadband antenna architectures and radome-face placement
- Sub-area guide 2: electromagnetic effects and functional radome technologies
- Sub-area guide 3: passive emitter detection, direction finding, and localization
- Sub-area guide 4: clandestine, anomalous, and deviated-signal identification
- Sub-area guide 5: integration, calibration, and operational validation
- Blender Baseline: 35S Radome and Concrete Base
- 17. Recalibração constante do relógio
- RADOME V3
- 24. Dois planos de comunicação
- 5. Casco externo e estrutura interna
- build.sh
- 2. Geometria fundamental
- Cross-search signals
- verify_tetrahedral_face_geometry.py
- localize_figures.py

## God Nodes (most connected - your core abstractions)
1. `Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos` - 29 edges
2. `Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos` - 29 edges
3. `RADOME — Registro de decisões de arquitetura` - 20 edges
4. `Plano Diretor de Infraestrutura Tática` - 13 edges
5. `RADOME Project Agent Guide` - 12 edges
6. `RADOME — Geodetic Multiband Passive Electromagnetic Sensing Network` - 12 edges
7. `RADOME — Roadmap de correções técnicas e documentais` - 11 edges
8. `tetrahedral_modules()` - 10 edges
9. `RADOME — Sumário executivo e roadmap de pesquisa e engenharia` - 9 edges
10. `27. Exemplo operacional` - 8 edges

## Surprising Connections (you probably didn't know these)
- `select_contiguous_cluster()` --calls--> `face_edge_key()`  [INFERRED]
  projeto/figures/render_tetrahedral_face_cluster_blender.py → projeto/geometry/verify_tetrahedral_face_geometry.py
- `save()` --calls--> `build_output()`  [INFERRED]
  projeto/figures/generate_updated_figures.py → projeto/figures/build_paths.py

## Import Cycles
- None detected.

## Communities (42 total, 2 thin omitted)

### Community 0 - "RADOME V3.md"
Cohesion: 0.05
Nodes (36): 10. Processamento local, 11. Memória circular de RF, 12. Evento e pré-trigger, 13. Nova interpretação da largura de banda, 14. Trigger distribuído, 15. Separação entre tempo do evento e tempo de transporte, 16. Núcleo temporal atômico, 18. Distribuição do tempo às 60 faces (+28 more)

### Community 1 - "Plano Diretor de Infraestrutura Tática"
Cohesion: 0.06
Nodes (34): 1. Visão Geral das Instalações Estratégicas, 2.1 Painel ATS — Chave de Transferência Automática, 2.2 Módulo UPS e banco LiFePO₄, 2.3 Minigerador autônomo, 2. Infraestrutura do Sistema de Energia Híbrido (Alta Disponibilidade), 3.1 Segregação eletromagnética, 3.2 Recuperação térmica, 3. Logística e Integração Térmica do Heliponto (+26 more)

### Community 2 - "Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos"
Cohesion: 0.06
Nodes (32): 10. Polarizacao: aquisicao vetorial e sintese digital, 11. Front-end RF, conversao e digitalizacao, 12. Sincronizacao, coerencia e holdover, 13. Calibracao ponta a ponta, 14. Geometria de sensoriamento e localizacao, 15. Processamento de radar passivo, 16. Rede de dados e arquitetura computacional, 17. Desempenho e limites fisicos (+24 more)

### Community 3 - "projeto_tecnico_radome_consolidado.md"
Cohesion: 0.06
Nodes (31): 1. Introdução, 2.1 Conceito operacional, 2.2 Arquitetura em alto nível, 2. Visão geral do sistema, 3.1 Topologia da rede, 3.2 Componentes principais, 3.3 Diagrama funcional da arquitetura, 3. Arquitetura técnica proposta (+23 more)

### Community 4 - "RADOME V3 — Arquitetura Eletrônica Distribuída Revisada.md"
Cohesion: 0.05
Nodes (38): 10. Controle individual das bandas, 11. Timestamping centralmente referenciado, 12. Relógio atômico central, 13. Processamento dentro do ASIC de banda, 14. Memória local e gravação dos sinais, 15. Trigger local por banda, 16. ASIC Central da Face — Face Fusion ASIC, 17. Fusão local de informações (+30 more)

### Community 5 - "Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos"
Cohesion: 0.07
Nodes (29): 10. Polarizacao: aquisicao vetorial e sintese digital, 11. Front-end RF, conversao e digitalizacao, 12. Sincronizacao, coerencia e holdover, 13. Calibracao ponta a ponta, 14. Geometria de sensoriamento e localizacao, 15. Processamento de radar passivo, 16. Rede de dados e arquitetura computacional, 17. Desempenho e limites fisicos (+21 more)

### Community 6 - "RADOME — Geodetic Multiband Passive Electromagnetic Sensing Network"
Cohesion: 0.09
Nodes (20): Apendice A - Formato minimo de registro de deteccao, Apendice B - Equacoes de referencia, Referencias, 1. Passive multistatic sensing, 2. Multiband and polarimetric reception, 3. Distributed synchronization and calibration, 4. Edge processing and event-oriented operation, 5. Resilience and deployment realism (+12 more)

### Community 7 - "Conceptual and theoretical gaps"
Cohesion: 0.12
Nodes (16): Airborne and curved-platform field datasets, Antenna bandwidth versus receiver observability, Closed-set and dataset-leakage risks, Conceptual and theoretical gaps, Emitter identity versus signal deviation, Environmental and structural aging, Inconsistent metrics, Insufficient adversarial testing (+8 more)

### Community 8 - "Conceptual and theoretical gaps"
Cohesion: 0.12
Nodes (16): Airborne and curved-platform field datasets, Antenna bandwidth versus receiver observability, Closed-set and dataset-leakage risks, Conceptual and theoretical gaps, Emitter identity versus signal deviation, Environmental and structural aging, Inconsistent metrics, Insufficient adversarial testing (+8 more)

### Community 9 - "RADOME — Roadmap de correções técnicas e documentais"
Cohesion: 0.14
Nodes (13): Definição de concluído, Estado dos gates, Evidência C3 já produzida, Onda 0 — congelar a baseline, Onda 1 — corrigir a polarimetria, Onda 2 — reconstruir a geometria paramétrica, Onda 3 — fechar o plano espectral e os experimentos, Onda 4 — sincronizar Blender, figuras e texto (+5 more)

### Community 10 - "RADOME Project Agent Guide"
Cohesion: 0.15
Nodes (12): Aircraft and Illuminator Scenario, Blender Rendering, GitHub Workflow, Graphify, graphify, LaTeX Article Commands, Mandatory Commit Per Change, Mandatory Startup Context Recovery (+4 more)

### Community 11 - "RADOME — Sumário executivo e roadmap de pesquisa e engenharia"
Cohesion: 0.20
Nodes (9): 1. Síntese executiva, 2. Mapa compacto do sistema, 3. Linha de evolução documental, 4. Verificação da revisão de literatura via Consensus, 5. Estado técnico e lacunas decisivas, 6. Roadmap orientado por gates, 7. Próximas ações prioritárias, 8. Critério de sucesso do programa (+1 more)

### Community 12 - "radome_antenna_literature_review/review.md"
Cohesion: 0.22
Nodes (8): Broadband Antennas Integrated with Radome Faces for Passive Detection of Clandestine or Anomalous RF Signals, How the field got here, Limitations of this review, Recommended research architecture, References, Search method, Terminology shifts, Topic overview

### Community 13 - "review.md"
Cohesion: 0.05
Nodes (42): Boolean searches, Boolean searches, Boolean searches, Boolean searches, Boolean searches, Broadband Antennas Integrated with Radome Faces for Passive Detection of Clandestine or Anomalous RF Signals, Citation velocity, Cross-search signals (+34 more)

### Community 14 - "Start here: priority reading order"
Cohesion: 0.25
Nodes (8): 1. Closest review to the complete antenna problem, 2. Seminal functional-radome paper, 3. Foundational integrated conformal direction finder, 4. Broad orientation for emitter identity, 5. Current radome frontier, 6. Current open-set detection frontier, 7. Key controversy and vulnerability, Start here: priority reading order

### Community 15 - "RADOME — Registro central de parâmetros"
Cohesion: 0.22
Nodes (8): Controle documental e arquitetura, Estados permitidos, Geometria e estrutura, Plano espectral e antenas, RADOME — Registro central de parâmetros, Regras de manutenção, Resultado da revisão C0, Tempo, cenário e validação

### Community 16 - "verify_radome_geometry.py"
Cohesion: 0.38
Nodes (10): clip_polygon_to_cut(), clip_segment_to_cut(), clipped_mesh(), distance(), face_edges(), grouped_lengths(), main(), normalize() (+2 more)

### Community 17 - "render_tetrahedral_face_cluster_blender.py"
Cohesion: 0.24
Nodes (5): arrow(), cylinder_between(), dot(), Render a contiguous cluster of 2 m tetrahedral radome face modules., select_contiguous_cluster()

### Community 20 - "RADOME Project / Projeto RADOME"
Cohesion: 0.33
Nodes (5): 3D baseline / Linha de base 3D, Compilation / Compilação, Independent editions / Edições independentes, RADOME Project / Projeto RADOME, Structure / Estrutura

### Community 21 - "English"
Cohesion: 0.12
Nodes (15): Conceito de alimentação e construção, Desempenho esperado, não garantido, Design objective, Element schedule, English, Expected—not guaranteed—performance, Feed and construction concept, Objetivo do projeto (+7 more)

### Community 22 - "RADOME — Registro de decisões de arquitetura"
Cohesion: 0.10
Nodes (20): ADR-001 — Fonte técnica autoritativa, ADR-002 — Versionamento independente, ADR-003 — Registro central de parâmetros, ADR-004 — Conflitos não são requisitos, ADR-005 — Aprovação condicionada da baseline C0, ADR-006 — Polarimetria restrita à mesma faixa, ADR-007 — LPDA VHF como candidata de banda larga, ADR-008 — Mastro polarimétrico de quatro canais (+12 more)

### Community 23 - "Build instructions"
Cohesion: 0.40
Nodes (4): Automated build, Build instructions, Manual build, Required tools

### Community 24 - "English"
Cohesion: 0.22
Nodes (8): Calibration model, Dual-band four-channel mast / Mastro de quatro canais em duas faixas, English, Ferramentas recomendadas, Português, Recommended simulation stack, Resultados obrigatórios da simulação, Simulation outputs required

### Community 25 - "Start here: priority reading order"
Cohesion: 0.25
Nodes (8): 1. Closest review to the complete antenna problem, 2. Seminal functional-radome paper, 3. Foundational integrated conformal direction finder, 4. Broad orientation for emitter identity, 5. Current radome frontier, 6. Current open-set detection frontier, 7. Key controversy and vulnerability, Start here: priority reading order

### Community 26 - "Key research groups"
Cohesion: 0.33
Nodes (6): F. Costa, A. Monorchio, and G. Manara, I. Liberal, D. Caratelli, and A. Yarovoy, Key research groups, M. Sorecau, E. Sorecau, P. Bechet, and collaborators, X. Sheng, Ning Liu, and collaborators, Zhongxiang Shen and collaborators

### Community 27 - "verify_c3_acquisition_budget.py"
Cohesion: 0.43
Nodes (4): CapturePath, main(), mutual_horizon_km(), radio_horizon_km()

### Community 28 - "Sub-area guide 1: broadband antenna architectures and radome-face placement"
Cohesion: 0.40
Nodes (5): Boolean searches, Key papers, Search terms, Sub-area guide 1: broadband antenna architectures and radome-face placement, What the research shows

### Community 29 - "Sub-area guide 2: electromagnetic effects and functional radome technologies"
Cohesion: 0.40
Nodes (5): Boolean searches, Key papers, Search terms, Sub-area guide 2: electromagnetic effects and functional radome technologies, What the research shows

### Community 30 - "Sub-area guide 3: passive emitter detection, direction finding, and localization"
Cohesion: 0.40
Nodes (5): Boolean searches, Key papers, Search terms, Sub-area guide 3: passive emitter detection, direction finding, and localization, What the research shows

### Community 31 - "Sub-area guide 4: clandestine, anomalous, and deviated-signal identification"
Cohesion: 0.40
Nodes (5): Boolean searches, Key papers, Search terms, Sub-area guide 4: clandestine, anomalous, and deviated-signal identification, What the research shows

### Community 32 - "Sub-area guide 5: integration, calibration, and operational validation"
Cohesion: 0.40
Nodes (5): Boolean searches, Key papers, Search terms, Sub-area guide 5: integration, calibration, and operational validation, What the research shows

### Community 34 - "Blender Baseline: 35S Radome and Concrete Base"
Cohesion: 0.50
Nodes (3): Blender Baseline: 35S Radome and Concrete Base, Geometry, Known presentation issues for the next revision

### Community 37 - "17. Recalibração constante do relógio"
Cohesion: 0.67
Nodes (3): 17. Recalibração constante do relógio, Nível 1 — estabilidade atômica local, Nível 2 — disciplina absoluta

### Community 38 - "RADOME V3"
Cohesion: 0.67
Nodes (3): 1. Objetivo do sistema, Radome Geodésico Multiespectro de 60 Faces com Aquisição Distribuída, Detecção Local e Referência Temporal Atômica, RADOME V3

### Community 39 - "24. Dois planos de comunicação"
Cohesion: 0.67
Nodes (3): 24. Dois planos de comunicação, Capture Plane, Control/Event Plane

### Community 40 - "5. Casco externo e estrutura interna"
Cohesion: 0.67
Nodes (3): 5. Casco externo e estrutura interna, Estrutura mecânica, Superfície aerodinâmica

### Community 47 - "Cross-search signals"
Cohesion: 0.67
Nodes (3): Citation velocity, Cross-search signals, Repeat-hit papers

### Community 50 - "verify_tetrahedral_face_geometry.py"
Cohesion: 0.34
Nodes (17): add(), centroid(), cross(), dot(), face_edge_key(), length(), main(), midpoint() (+9 more)

### Community 52 - "localize_figures.py"
Cohesion: 0.07
Nodes (19): Path, build_output(), ensure_build_dir(), Shared paths for temporary figure-master build artifacts., Generate a language-neutral exploded 3D face illustration., Generate the shared, language-neutral technical figures 01--10.  Permanent publi, save(), draw_label() (+11 more)

## Knowledge Gaps
- **393 isolated node(s):** `build.sh script`, `Mandatory Startup Context Recovery`, `Graphify`, `Project Layout`, `LaTeX Article Commands` (+388 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Plano Diretor de Infraestrutura Tática` connect `Plano Diretor de Infraestrutura Tática` to `RADOME — Geodetic Multiband Passive Electromagnetic Sensing Network`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos` connect `Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos` to `RADOME — Geodetic Multiband Passive Electromagnetic Sensing Network`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **What connects `build.sh script`, `Mandatory Startup Context Recovery`, `Graphify` to the rest of the system?**
  _393 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `RADOME V3.md` be split into smaller, more focused modules?**
  _Cohesion score 0.05405405405405406 - nodes in this community are weakly interconnected._
- **Should `Plano Diretor de Infraestrutura Tática` be split into smaller, more focused modules?**
  _Cohesion score 0.058823529411764705 - nodes in this community are weakly interconnected._
- **Should `Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._
- **Should `projeto_tecnico_radome_consolidado.md` be split into smaller, more focused modules?**
  _Cohesion score 0.0625 - nodes in this community are weakly interconnected._