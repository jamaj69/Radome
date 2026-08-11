# Graph Report - Radome  (2026-08-11)

## Corpus Check
- 131 files · ~482,772 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1026 nodes · 1336 edges · 97 communities (84 shown, 13 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 96 edges (avg confidence: 0.79)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cc0aa779`
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
- Seleção geoespacial de sítios RADOME
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
- Key research groups
- Blender Baseline: 35S Radome and Concrete Base
- Sub-area guide 1: broadband antenna architectures and radome-face placement
- Sub-area guide 2: electromagnetic effects and functional radome technologies
- 17. Recalibração constante do relógio
- RADOME V3
- 24. Dois planos de comunicação
- 5. Casco externo e estrutura interna
- Sub-area guide 3: passive emitter detection, direction finding, and localization
- build.sh
- 2. Geometria fundamental
- Sub-area guide 4: clandestine, anomalous, and deviated-signal identification
- Sub-area guide 5: integration, calibration, and operational validation
- Cross-search signals
- Cross-search signals
- localize_figures.py
- Seleção geoespacial de sítios RADOME
- verify_tetrahedral_face_geometry.py
- inventory_topodata.py
- localize_figures.py
- Pré-seleção continental baseada na BC250
- Grafo preliminar de capitais e aeroportos
- run_pipeline.sh
- localize_figures.py
- Fontes de infraestrutura para o grafo de candidatos
- inventory_infrastructure.py
- inventory
- municipal_emitter_network/README.md
- build
- broadcast_network/README.md
- Requisitos preservados para geolocalização dos radomes
- localize_figures.py
- Subprojeto de seleção geoespacial
- inventory
- Auditoria de tecnologia e espectro das estações Anatel
- Auxílios de navegação DECEA/ICA
- Inventário de camadas oficiais de emissões
- acquire
- acquire_decea_wfs.py
- Política de manipulação reproduzível das bases geoespaciais
- main
- verify_reproducibility.py
- Estado atual do subprojeto geoespacial
- build_municipal_emitter_network.py
- canonical_smp/README.md
- Emissores fixos SARC/SCM no esquema canônico
- Famílias explícitas de radioenlaces Anatel
- write_fixture
- anatel_radio_link_keys/README.md
- anatel_radio_link_candidates/README.md
- evaluate_anatel_radio_link_terrain.py
- extract_topodata_route_tiles.py
- test_build_canonical_fixed_emitters.py
- build_canonical_smp.py
- inventory_infrastructure.py
- build_municipal_emitter_network.py
- ZipFile
- write_fixture
- validate
- anatel_radio_link_terrain/README.md
- analyze
- topodata_radio_link_tiles/README.md
- inventory
- build_canonical_fixed_emitters.py

## God Nodes (most connected - your core abstractions)
1. `Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos` - 29 edges
2. `Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos` - 29 edges
3. `RADOME — Registro de decisões de arquitetura` - 20 edges
4. `deterministic_gzip_csv()` - 17 edges
5. `number()` - 13 edges
6. `build()` - 13 edges
7. `Plano Diretor de Infraestrutura Tática` - 13 edges
8. `RADOME Project Agent Guide` - 12 edges
9. `RADOME — Geodetic Multiband Passive Electromagnetic Sensing Network` - 12 edges
10. `Fases e gates` - 12 edges

## Surprising Connections (you probably didn't know these)
- `analyze()` --calls--> `number()`  [INFERRED]
  geoespacial/analyze_anatel_radio_link_candidates.py → geoespacial/audit_anatel_spectrum.py
- `analyze()` --calls--> `deterministic_gzip_csv()`  [INFERRED]
  geoespacial/analyze_anatel_radio_link_candidates.py → geoespacial/build_canonical_smp.py
- `analyze()` --calls--> `stable_identifier()`  [INFERRED]
  geoespacial/analyze_anatel_radio_link_candidates.py → geoespacial/build_canonical_smp.py
- `audit_member()` --calls--> `emission_bandwidth_hz()`  [INFERRED]
  geoespacial/audit_anatel_general.py → geoespacial/audit_anatel_spectrum.py
- `audit_member()` --calls--> `number()`  [INFERRED]
  geoespacial/audit_anatel_general.py → geoespacial/audit_anatel_spectrum.py

## Import Cycles
- None detected.

## Communities (97 total, 13 thin omitted)

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
Cohesion: 0.18
Nodes (10): 1. Síntese executiva, 2. Mapa compacto do sistema, 3. Linha de evolução documental, 4. Verificação da revisão de literatura via Consensus, 5. Estado técnico e lacunas decisivas, 6. Roadmap orientado por gates, 7. Próximas ações prioritárias, 8. Critério de sucesso do programa (+2 more)

### Community 12 - "radome_antenna_literature_review/review.md"
Cohesion: 0.22
Nodes (8): Broadband Antennas Integrated with Radome Faces for Passive Detection of Clandestine or Anomalous RF Signals, How the field got here, Limitations of this review, Recommended research architecture, References, Search method, Terminology shifts, Topic overview

### Community 13 - "review.md"
Cohesion: 0.22
Nodes (8): Broadband Antennas Integrated with Radome Faces for Passive Detection of Clandestine or Anomalous RF Signals, How the field got here, Limitations of this review, Recommended research architecture, References, Search method, Terminology shifts, Topic overview

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
Cohesion: 0.27
Nodes (9): Any, Candidate, load_instance(), main(), Path, Minimize site count, using candidate score only as a tie-breaker., solve(), candidate() (+1 more)

### Community 18 - "Seleção geoespacial de sítios RADOME"
Cohesion: 0.13
Nodes (21): horizon_km(), main(), node_id(), Path, Lê uma camada com os bindings GDAL, sem conversão externa por shell., read_layer(), terrain_elevation(), tile_pixel() (+13 more)

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

### Community 33 - "Key research groups"
Cohesion: 0.33
Nodes (6): F. Costa, A. Monorchio, and G. Manara, I. Liberal, D. Caratelli, and A. Yarovoy, Key research groups, M. Sorecau, E. Sorecau, P. Bechet, and collaborators, X. Sheng, Ning Liu, and collaborators, Zhongxiang Shen and collaborators

### Community 34 - "Blender Baseline: 35S Radome and Concrete Base"
Cohesion: 0.50
Nodes (3): Blender Baseline: 35S Radome and Concrete Base, Geometry, Known presentation issues for the next revision

### Community 35 - "Sub-area guide 1: broadband antenna architectures and radome-face placement"
Cohesion: 0.40
Nodes (5): Boolean searches, Key papers, Search terms, Sub-area guide 1: broadband antenna architectures and radome-face placement, What the research shows

### Community 36 - "Sub-area guide 2: electromagnetic effects and functional radome technologies"
Cohesion: 0.40
Nodes (5): Boolean searches, Key papers, Search terms, Sub-area guide 2: electromagnetic effects and functional radome technologies, What the research shows

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

### Community 41 - "Sub-area guide 3: passive emitter detection, direction finding, and localization"
Cohesion: 0.40
Nodes (5): Boolean searches, Key papers, Search terms, Sub-area guide 3: passive emitter detection, direction finding, and localization, What the research shows

### Community 44 - "Sub-area guide 4: clandestine, anomalous, and deviated-signal identification"
Cohesion: 0.40
Nodes (5): Boolean searches, Key papers, Search terms, Sub-area guide 4: clandestine, anomalous, and deviated-signal identification, What the research shows

### Community 45 - "Sub-area guide 5: integration, calibration, and operational validation"
Cohesion: 0.40
Nodes (5): Boolean searches, Key papers, Search terms, Sub-area guide 5: integration, calibration, and operational validation, What the research shows

### Community 46 - "Cross-search signals"
Cohesion: 0.67
Nodes (3): Citation velocity, Cross-search signals, Repeat-hit papers

### Community 47 - "Cross-search signals"
Cohesion: 0.67
Nodes (3): Citation velocity, Cross-search signals, Repeat-hit papers

### Community 48 - "localize_figures.py"
Cohesion: 0.18
Nodes (10): Camada municipal e integração de emissores, Construção dos candidatos, Fontes e proveniência, Grafo, Hipóteses controladas, Metodologia reproduzível para seleção geoespacial de sítios, Objetivo, Otimização (+2 more)

### Community 49 - "Seleção geoespacial de sítios RADOME"
Cohesion: 0.25
Nodes (7): Critério de parada, Etapas, Fontes previstas, Grafo de capitais e aeroportos, Hipóteses controladas, Pré-seleção BC250, Seleção geoespacial de sítios RADOME

### Community 50 - "verify_tetrahedral_face_geometry.py"
Cohesion: 0.17
Nodes (22): arrow(), cylinder_between(), dot(), Render a contiguous cluster of 2 m tetrahedral radome face modules., select_contiguous_cluster(), add(), centroid(), cross() (+14 more)

### Community 51 - "inventory_topodata.py"
Cohesion: 0.47
Nodes (3): main(), parse_index(), InventoryTopodataTest

### Community 52 - "localize_figures.py"
Cohesion: 0.07
Nodes (18): build_output(), ensure_build_dir(), Path, Shared paths for temporary figure-master build artifacts., Generate a language-neutral exploded 3D face illustration., Generate the shared, language-neutral technical figures 01--11.  Permanent publi, save(), draw_label() (+10 more)

### Community 56 - "localize_figures.py"
Cohesion: 0.10
Nodes (20): Artefatos obrigatórios por execução, Fase 0 — requisitos e proveniência — concluída, Fase 10 — arquipélagos e ilhas oceânicas — adiada, Fase 1 — base territorial municipal — concluída preliminarmente, Fase 2 — inventário de iluminadores — em andamento, Fase 3 — infraestrutura aeronáutica e estratégica — ativa, Fase 4 — relevo nacional e candidatos — pendente, Fase 5 — visada e cobertura 3D — pendente (+12 more)

### Community 57 - "Fontes de infraestrutura para o grafo de candidatos"
Cohesion: 0.22
Nodes (8): ANAC e DECEA, Anatel, Comunicação nas bases históricas do IBGE, Fontes de infraestrutura para o grafo de candidatos, IBGE BC250 2025, Ordem de integração, Radiodifusão, Resultado por tema

### Community 58 - "inventory_infrastructure.py"
Cohesion: 0.21
Nodes (11): audit(), audit_member(), main(), Counter, Path, rf_role(), sorted_counter(), usable_text() (+3 more)

### Community 59 - "inventory"
Cohesion: 0.25
Nodes (10): audit_broadcast(), audit_smp(), emission_bandwidth_hz(), main(), number(), positive_frequency(), Path, Decodifica a largura necessária no início da designação ITU. (+2 more)

### Community 61 - "build"
Cohesion: 0.35
Nodes (8): build(), main(), municipality_index(), normalize_name(), Path, sha256(), spatial_code(), BroadcastNetworkTest

### Community 63 - "Requisitos preservados para geolocalização dos radomes"
Cohesion: 0.22
Nodes (8): Cidades, municípios e logística, Decisões operacionais derivadas, Escopo territorial, Grafo de infraestrutura e iluminadores, Objetivo primário, Relevo, visada e conectividade, Reprodutibilidade e publicação, Requisitos preservados para geolocalização dos radomes

### Community 64 - "localize_figures.py"
Cohesion: 0.33
Nodes (6): inventory_layer(), main(), present(), Path, sha256(), DeceaNavaidInventoryTest

### Community 65 - "Subprojeto de seleção geoespacial"
Cohesion: 0.29
Nodes (6): Documentos de controle, Gate de integração com o artigo, Marcos ativos: M2E e M3, Missão e limites, Subprojeto de seleção geoespacial, Vinculação ao projeto principal

### Community 66 - "inventory"
Cohesion: 0.40
Nodes (4): Auditoria inicial do pacote geral da Anatel, Regra de classificação RF, Reprodução, Resultado

### Community 67 - "Auditoria de tecnologia e espectro das estações Anatel"
Cohesion: 0.29
Nodes (6): Auditoria de tecnologia e espectro das estações Anatel, Conclusão, Produtos e reprodução, Referências regulatórias para o próximo gate, Rádio e televisão, SMP

### Community 68 - "Auxílios de navegação DECEA/ICA"
Cohesion: 0.40
Nodes (4): Auxílios de navegação DECEA/ICA, Interpretação dos campos, Limites e próxima integração, Resultado da aquisição

### Community 69 - "Inventário de camadas oficiais de emissões"
Cohesion: 0.25
Nodes (7): Critério de prontidão, Fontes oficiais adicionais identificadas, Inventário de camadas oficiais de emissões, Matriz reavaliada, Novo gate de emissões oficiais — M2E, Principal descoberta da reanálise, Sequência revisada

### Community 70 - "acquire"
Cohesion: 0.23
Nodes (9): acquire(), file_sha256(), main(), Path, extract(), main(), Path, safe_destination() (+1 more)

### Community 71 - "acquire_decea_wfs.py"
Cohesion: 0.36
Nodes (6): download_atomic(), main(), Path, request_url(), sha256(), DeceaAcquisitionTest

### Community 72 - "Política de manipulação reproduzível das bases geoespaciais"
Cohesion: 0.33
Nodes (5): Contrato de cada script, Gates futuros, Política de manipulação reproduzível das bases geoespaciais, Pontos de entrada atuais, Regra obrigatória

### Community 73 - "main"
Cohesion: 0.83
Nodes (3): main(), Path, run()

### Community 74 - "verify_reproducibility.py"
Cohesion: 0.39
Nodes (5): ReproducibilityTest, main(), Path, sha256(), snapshot()

### Community 75 - "Estado atual do subprojeto geoespacial"
Cohesion: 0.25
Nodes (7): Comando de retomada, Dados e integrações concluídos, Estado atual do subprojeto geoespacial, Lacunas controladas, Próxima ação executável, Validação reproduzível, Vinculação e governança

### Community 76 - "build_municipal_emitter_network.py"
Cohesion: 0.20
Nodes (11): acquire_archive(), acquire_selection(), atomic_json(), main(), Path, Valida estrutura, CRC e presenca do GeoTIFF de altitude., Reutiliza um ZIP valido ou o baixa para arquivo temporario atomico., sha256_file() (+3 more)

### Community 78 - "Emissores fixos SARC/SCM no esquema canônico"
Cohesion: 0.50
Nodes (3): Emissores fixos SARC/SCM no esquema canônico, Reprodução, Resultado

### Community 79 - "Famílias explícitas de radioenlaces Anatel"
Cohesion: 0.50
Nodes (3): Famílias explícitas de radioenlaces Anatel, Reprodução, Resultado

### Community 83 - "evaluate_anatel_radio_link_terrain.py"
Cohesion: 0.09
Nodes (21): classify(), evaluate(), interpolate(), main(), profile(), Path, Terrarium, evaluate() (+13 more)

### Community 84 - "extract_topodata_route_tiles.py"
Cohesion: 0.24
Nodes (10): atomic_json(), extract_archive(), extract_receipt(), feature(), inspect_geotiff(), main(), Path, sha256_file() (+2 more)

### Community 85 - "test_build_canonical_fixed_emitters.py"
Cohesion: 0.47
Nodes (5): CanonicalFixedEmittersTest, Path, read_rows(), record(), write_input()

### Community 86 - "build_canonical_smp.py"
Cohesion: 0.25
Nodes (11): build(), canonical_coordinate(), deterministic_gzip_csv(), dominant_code(), main(), Counter, Path, Abre CSV gzip reproduzível, sem nome ou horário variável no cabeçalho. (+3 more)

### Community 87 - "inventory_infrastructure.py"
Cohesion: 0.27
Nodes (9): main(), parse_args(), Path, read_anac_csv(), read_anatel_zip(), read_decea_capabilities(), sha256(), InfrastructureInventoryTest (+1 more)

### Community 88 - "build_municipal_emitter_network.py"
Cohesion: 0.27
Nodes (9): dominant_code(), main(), municipal_features(), Counter, Path, read_population(), read_smp_sites(), write_network() (+1 more)

### Community 89 - "ZipFile"
Cohesion: 0.24
Nodes (9): clean(), extract(), main(), Path, extract(), main(), Path, RawLinkKeysTest (+1 more)

### Community 90 - "write_fixture"
Cohesion: 0.47
Nodes (4): CanonicalSmpTest, Path, read_gzip_csv(), write_fixture()

### Community 91 - "validate"
Cohesion: 0.33
Nodes (6): GeometryTest, angular_error(), bearing(), main(), Path, validate()

### Community 93 - "analyze"
Cohesion: 0.36
Nodes (5): analyze(), distance(), main(), Path, CandidateTest

### Community 95 - "inventory"
Cohesion: 0.39
Nodes (5): file_sha256(), inventory(), main(), Path, SmpInventoryTest

### Community 96 - "build_canonical_fixed_emitters.py"
Cohesion: 0.48
Nodes (6): antenna_signature(), build(), canonical_number(), exclusion_reason(), main(), Path

## Knowledge Gaps
- **486 isolated node(s):** `run_pipeline.sh script`, `build.sh script`, `Mandatory Startup Context Recovery`, `Graphify`, `Project Layout` (+481 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `deterministic_gzip_csv()` connect `build_canonical_smp.py` to `build_canonical_fixed_emitters.py`, `evaluate_anatel_radio_link_terrain.py`, `test_build_canonical_fixed_emitters.py`, `ZipFile`, `inventory_infrastructure.py`, `validate`, `analyze`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Why does `Plano Diretor de Infraestrutura Tática` connect `Plano Diretor de Infraestrutura Tática` to `RADOME — Geodetic Multiband Passive Electromagnetic Sensing Network`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Why does `Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos` connect `Rede Distribuida de Radomes Conformais Multifaixa e Polarimetricos` to `RADOME — Geodetic Multiband Passive Electromagnetic Sensing Network`?**
  _High betweenness centrality (0.006) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ZipFile` (e.g. with `audit_broadcast()` and `audit_smp()`) actually correct?**
  _`ZipFile` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `deterministic_gzip_csv()` (e.g. with `analyze()` and `audit_member()`) actually correct?**
  _`deterministic_gzip_csv()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **What connects `run_pipeline.sh script`, `build.sh script`, `Mandatory Startup Context Recovery` to the rest of the system?**
  _486 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `RADOME V3.md` be split into smaller, more focused modules?**
  _Cohesion score 0.05405405405405406 - nodes in this community are weakly interconnected._