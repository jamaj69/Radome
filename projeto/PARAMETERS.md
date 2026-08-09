# RADOME — Registro central de parâmetros

**Documento controlado:** `projetov1.tex`, versão 1.1
**Arquitetura:** revisão 3, conceitual
**Atualização inicial:** 8 de agosto de 2026
**Revisão da baseline C0:** aprovada com bloqueios em 8 de agosto de 2026

Este registro é a fonte central para valores quantitativos do projeto. Uma entrada não se torna requisito somente por aparecer aqui: o campo `Estado` informa o nível de evidência e o campo `Validação` define o próximo gate.

## Estados permitidos

| Estado | Significado |
|---|---|
| Proposto | Valor de projeto ainda sem confirmação suficiente por cálculo, simulação ou ensaio |
| Derivado | Calculado a partir de premissas registradas e reproduzíveis, ainda sujeito à validação do modelo |
| Simulado | Obtido em modelo identificado, com configuração e versão preservadas |
| Medido | Obtido em ensaio identificado, com instrumento, incerteza e condições registrados |
| Histórico | Mantido somente para rastreabilidade; não controla o projeto atual |
| Em conflito | Duas ou mais fontes vigentes não podem ser satisfeitas simultaneamente |

## Controle documental e arquitetura

| ID | Parâmetro | Valor | Estado | Fonte vigente | Responsável | Validação |
|---|---|---:|---|---|---|---|
| DOC-001 | Versão do documento técnico | 1.1 | Proposto | `projetov1.tex` | Engenharia de sistemas | Aprovar baseline C0 |
| ARC-001 | Revisão da arquitetura | 3 | Proposto | `projetov1.tex`; `01_scope.tex` | Arquitetura de sistemas | Aprovar baseline C0 |
| ARC-002 | Número-alvo de nós do primeiro demonstrador | 3 | Proposto | `01_scope.tex` | Engenharia de sistemas | SRR do demonstrador |

## Geometria e estrutura

| ID | Parâmetro | Valor | Unidade | Estado | Fonte vigente | Responsável | Validação |
|---|---|---:|---|---|---|---|---|
| GEO-001 | Poliedro base fechado | icosaedro regular | — | Proposto | `03_geometry_radome.tex`; `geometry/verify_radome_geometry.py` | Engenharia geométrica | Malha paramétrica C2 preliminar |
| GEO-002 | Macrofaces do poliedro base | 20 | face | Derivado | `geometry/verify_radome_geometry.py` | Engenharia geométrica | Verificação topológica C2 |
| GEO-003 | Faces receptoras do envelope fechado | 80 | face | Derivado | `geometry/verify_radome_geometry.py` | Engenharia geométrica | Verificador C2; sincronizar figuras e Blender em C4 |
| GEO-004 | Lado da face receptora externa | 2.0 | m | Derivado | `geometry/verify_tetrahedral_face_geometry.py`; ADR-012 | Engenharia geométrica | Confirmar tolerâncias e junta estrutural |
| GEO-005 | Raio da candidata anterior com projeção esférica | 3.6594 | m | Histórico | `geometry/verify_radome_geometry.py`; ADR-009 | Engenharia geométrica | Não controla ADR-012 |
| GEO-006 | Diâmetro da candidata anterior com projeção esférica | 7.3189 | m | Histórico | `geometry/verify_radome_geometry.py`; ADR-009 | Engenharia geométrica | Não controla ADR-012 |
| GEO-007 | Corte inferior da candidata anterior | z/R = -0.573576, ângulo polar 125° | — | Histórico | `geometry/verify_radome_geometry.py`; ADR-009 | Geometria/estruturas | Redefinir por módulos inteiros na ADR-012 |
| GEO-008 | Subdivisão tetraédrica candidata | classe I, frequência 2, sem projeção dos pontos médios | — | Proposto | `geometry/verify_tetrahedral_face_geometry.py`; ADR-012 | Engenharia geométrica | Fechar C2 reaberto e interface civil |
| GEO-009 | Vértices do envelope fechado C2 | 42 | vértice | Derivado | `geometry/verify_radome_geometry.py` | Engenharia geométrica | Verificador C2 |
| GEO-010 | Arestas do envelope fechado C2 | 120 | aresta | Derivado | `geometry/verify_radome_geometry.py` | Engenharia geométrica | Verificador C2 |
| GEO-011 | Diâmetro do anel de apoio da candidata anterior | 5.9953 | m | Histórico | `geometry/verify_radome_geometry.py`; ADR-009 | Engenharia civil | Não reutilizar na ADR-012 |
| GEO-012 | Topologia do segmento cortado da candidata anterior | V=51, E=124, F=74, Euler=1 | — | Histórico | `geometry/verify_radome_geometry.py`; ADR-009 | Engenharia geométrica | Redefinir por módulos inteiros |
| GEO-013 | Borda do segmento cortado da candidata anterior | 16 vértices / 16 arestas | — | Histórico | `geometry/verify_radome_geometry.py`; ADR-009 | Engenharia civil | Redefinir por módulos inteiros |
| GEO-014 | Aresta da macroface icosaédrica tetraédrica | 4.0000 | m | Derivado | `geometry/verify_tetrahedral_face_geometry.py` | Engenharia geométrica | Verificador ADR-012 |
| GEO-015 | Classe de aresta das faces externas | 2.0000 | m | Derivado | `geometry/verify_tetrahedral_face_geometry.py` | Engenharia geométrica | Verificador ADR-012 |
| GEO-016 | Altura do segmento cortado da candidata anterior | 5.7584 | m | Histórico | `geometry/verify_radome_geometry.py`; ADR-009 | Engenharia geométrica | Não controla ADR-012 |
| GEO-017 | Raio circunscrito / inraio do envelope ADR-012 | 3.8042 / 3.0230 | m | Derivado | `geometry/verify_tetrahedral_face_geometry.py` | Engenharia geométrica | Recalcular borda e apoio |
| GEO-018 | Arestas laterais das células tetraédricas rasas | 1.3769 | m | Derivado | `geometry/verify_tetrahedral_face_geometry.py` | Estruturas | Dimensionar painéis, juntas e montagem |
| GEO-019 | Colisões de tetraedros regulares de aresta 2 m | 120 | colisão | Derivado | `geometry/verify_tetrahedral_face_geometry.py` | Engenharia geométrica | Configuração regular bloqueada |
| GEO-020 | Colisões das células tetraédricas com altura de 0,75 m | 0 | colisão | Derivado | `geometry/verify_tetrahedral_face_geometry.py` | Engenharia geométrica | Validar tolerâncias e espessuras reais |
| GEO-021 | Altura normal centro da face–ápice local | 0.7500 | m | Proposto | `geometry/verify_tetrahedral_face_geometry.py`; ADR-012 | Estruturas/EMC | Otimizar volume, rigidez e acessibilidade |
| GEO-022 | Raio mínimo do núcleo interno livre | 2.2730 | m | Derivado | `geometry/verify_tetrahedral_face_geometry.py` | Integração | Reservar distribuição central e manutenção |
| GEO-023 | Separação entre ápices de células vizinhas | 0.5435–1.1547 | m | Derivado | `geometry/verify_tetrahedral_face_geometry.py` | Integração | Dimensionar corredores e raios de curvatura |
| CIV-001 | Planta da base de concreto | 4 × 4 | m | Proposto | `08_infrastructure_validation.tex` | Engenharia civil | Não suporta diretamente o anel C2 sem transição |
| CIV-002 | Altura estrutural livre da base | 3 | m | Proposto | `08_infrastructure_validation.tex` | Engenharia civil | Estudo estrutural e de acesso |
| CIV-003 | Envelope quadrado mínimo da transição de apoio C2 | 6.6 × 6.6 | m | Proposto | `geometry/verify_radome_geometry.py`; `03_geometry_radome.tex` | Engenharia civil | Grade beam ou moldura estrutural a detalhar |
| MEC-001 | Elemento transversal máximo da Yagi VHF | 2 | m | Proposto | `03_geometry_radome.tex` | Antenas/estruturas | Modelo EM e cargas de vento |
| MEC-002 | Ângulo nominal entre os planos das Yagis VHF e UHF | 90 | grau | Proposto | `03_geometry_radome.tex` | Antenas/estruturas | Verificar montagem; não usar como base polarimétrica entre faixas |
| MEC-003 | Paredes laterais Faraday independentes | 240 | parede | Derivado | `geometry/verify_tetrahedral_face_geometry.py`; ADR-012 | EMC/estruturas | Detalhar espessura, juntas RF e bonding |
| MEC-004 | Invólucros ADC/ASIC por face dual-pol | 2 | invólucro | Proposto | `render_tetrahedral_face_cluster_blender.py`; `05_electronics_processing.tex` | EMC/eletrônica | Ensaiar SE, emissões, térmica e acoplamento |
| MEC-005 | Corredores intercelulares de cabos e fibras | 120 | corredor | Derivado | `geometry/verify_tetrahedral_face_geometry.py`; ADR-012 | Integração/EMC | Separar energia de fibra/RF e validar acesso |
| MEC-006 | Ângulo entre o eixo comum dos booms e a normal externa da face | 0 | grau | Proposto | ADR-013; `render_radome_blender.py` | Antenas/estruturas | Verificar tolerância de alinhamento e carga no suporte |
| MEC-007 | Rotação da montagem Yagi cruzada em torno da normal | 45 | grau | Proposto | ADR-013; `render_radome_blender.py` | Antenas/estruturas | Verificar referência da base tangente e tolerância angular |
| MEC-008 | Revestimento absorvedor interno da célula piramidal | material e espessura não selecionados | — | Proposto | ADR-014; `09_literature_review.tex` | EM/estruturas | Otimizar por faixa e medir absorção, reflexão, térmica, inflamabilidade e durabilidade |
| MEC-009 | Baixa observabilidade da célula receptora | não demonstrada | — | Proposto | ADR-014 | EM/ensaios | Medir RCS monoestática/biestática, $S_{11}$ da abertura e reradiação com/sem absorvedor |

## Plano espectral e antenas

| ID | Parâmetro | Valor | Unidade | Estado | Fonte vigente | Responsável | Validação |
|---|---|---:|---|---|---|---|---|
| RF-001 | Faixa HF conceitual | 3–30 | MHz | Proposto | `generate_updated_figures.py` | Engenharia RF | SRR espectral C3 |
| RF-002 | Faixa VHF conceitual | 30–300 | MHz | Proposto | `generate_updated_figures.py` | Engenharia RF | Seleção de subfaixas C3 |
| RF-003 | Faixa da Yagi UHF conceitual | 470–860 | MHz | Proposto | `generate_updated_figures.py` | Engenharia RF | Resolver lacunas e medir banda C3 |
| RF-004 | Faixa L/S/C agregada | 1–8 | GHz | Proposto | `generate_updated_figures.py` | Engenharia RF | Decompor em cadeias realizáveis C3 |
| RF-005 | Faixa X/Ku agregada | 8–18 | GHz | Proposto | `generate_updated_figures.py` | Engenharia RF | Decompor em tiles C3 |
| RF-006 | Faixa K/Ka agregada | 18–40 | GHz | Proposto | `generate_updated_figures.py` | Engenharia RF | Decompor em tiles C3 |
| RF-007 | Faixa 323–470 MHz no primeiro demonstrador | deliberadamente não coberta | — | Proposto | `DECISIONS.md` ADR-010 | Engenharia RF | Reavaliar somente mediante caso de uso e cadeia próprios |
| RF-008 | Faixa 860–960 MHz no primeiro demonstrador | deliberadamente não coberta | — | Proposto | `DECISIONS.md` ADR-010 | Engenharia RF | Não inferir cobertura entre a Yagi UHF e a cadeia aeronáutica |
| RF-009 | Faixa da abertura/array aeronáutico dedicado | 960–1215 | MHz | Proposto | `DECISIONS.md` ADR-010 | Antenas/RF | Selecionar topologia e medir ganho, padrão e acoplamento |
| RF-010 | Caminho receptor UAT | abertura RF-009 → preselector 978 → limitador/LNA → ADC coerente → canal FPGA UAT | — | Proposto | `DECISIONS.md` ADR-010 | RF/eletrônica | Dimensionar largura, NF, IP3, amostragem e faixa dinâmica C3 |
| RF-011 | Caminho receptor 1090ES | abertura RF-009 → preselector 1090 → limitador/LNA → ADC coerente → canal FPGA 1090ES | — | Proposto | `DECISIONS.md` ADR-010 | RF/eletrônica | Dimensionar largura, NF, IP3, amostragem e faixa dinâmica C3 |
| RF-012 | Baseline de captura UAT/1090ES | 8 MS/s, I/Q 16+16 bit, 2 canais por nó | — | Proposto | `spectral/verify_c3_acquisition_budget.py` | RF/dados | Confirmar largura ocupada, aliasing e implementação ADC/DDC |
| RF-013 | Baseline de captura UHF direta | 25 MS/s, I/Q 16+16 bit, 1 canal por nó | — | Proposto | `spectral/verify_c3_acquisition_budget.py` | RF/dados | Ajustar à forma de onda e largura do transmissor selecionado |
| RF-014 | Baseline de captura biestática UHF | 25 MS/s, I/Q 16+16 bit, 2 canais por nó | — | Proposto | `spectral/verify_c3_acquisition_budget.py` | RF/dados | Validar coerência entre referência e vigilância |
| RF-015 | NF, IP3 e faixa dinâmica utilizável | não atribuídos | — | Proposto | `spectral/verify_c3_acquisition_budget.py` | RF/eletrônica | Fechar orçamento em cascata após campanha RFI e seleção de componentes |
| ANT-001 | LPDA VHF candidata: faixa de projeto | 71.5–323 | MHz | Derivado | `antenna_designs/lpda_vhf_72_320.md` | Antenas/RF | Simulação NEC/openEMS e OTA |
| ANT-002 | LPDA VHF candidata: τ / σ | 0.86 / 0.16 | — | Proposto | `antenna_designs/lpda_vhf_72_320.md` | Antenas/RF | Otimização de ganho e impedância |
| ANT-003 | LPDA VHF candidata: elementos | 11 | elemento | Derivado | `antenna_designs/lpda_vhf_72_320.md` | Antenas/RF | Confirmar região ativa por frequência |
| ANT-004 | LPDA VHF candidata: boom entre elementos | 1.780 | m | Derivado | `antenna_designs/lpda_vhf_72_320.md` | Antenas/estruturas | Adicionar margens e verificar cargas |
| ANT-005 | LPDA VHF candidata: ganho realizado alvo | 6–8 | dBi | Proposto | `antenna_designs/lpda_vhf_72_320.md` | Antenas/RF | Não citar como desempenho até simulação e ensaio |
| POL-001 | Polarimetria por faixa | 2 portas simultâneas, ortogonais e coerentes na mesma frequência | Proposto | `04_multiband_polarimetry.tex` | Antenas/RF | Arquitetura corrigida; medir matriz de Jones, isolamento e deriva |
| POL-002 | Polarimetria das Yagis VHF/UHF do primeiro demonstrador | não implementada; dois canais independentes single-pol | Proposto | `04_multiband_polarimetry.tex` | Antenas/RF | Preservar separação entre faixas; não produzir Stokes/RHCP do par |
| POL-003 | Critério mínimo de coerência polarimétrica | amplitude e fase calibradas em frequência, ângulo e temperatura | Proposto | `04_multiband_polarimetry.tex` | Metrologia RF | Plano de ensaio OTA e injeção coerente |
| POL-004 | Par polarimétrico VHF candidato | 0° / 90° | Proposto | `antenna_designs/dual_band_quad_polarization_mast.md` | Antenas/RF | Simulação multiporta e calibração 2×2 |
| POL-005 | Par polarimétrico UHF candidato | 45° / 135° | Proposto | `antenna_designs/dual_band_quad_polarization_mast.md` | Antenas/RF | Rotação para base global e simulação multiporta |
| POL-006 | Canais RF independentes no mastro polarimétrico | 4 | canal | Proposto | `antenna_designs/dual_band_quad_polarization_mast.md` | RF/eletrônica | Quatro portas, clocks coerentes por faixa e isolamento medido |
| POL-007 | Matriz de calibração por faixa | C_b(f,θ,φ,T), complexa 2×2 | Proposto | `antenna_designs/dual_band_quad_polarization_mast.md` | Metrologia RF | Medir condição, incerteza e pseudoinversa regularizada |

## Tempo, cenário e validação

| ID | Parâmetro | Valor | Unidade | Estado | Fonte vigente | Responsável | Validação |
|---|---|---:|---|---|---|---|---|
| TIM-001 | Antenas GNSS externas por estação | ≥2 | antena | Proposto | `06_timing_localization.tex` | Metrologia temporal | Justificar redundância e medir atrasos |
| TIM-002 | Saídas de referência locais | 1 PPS e 10 MHz | — | Proposto | `06_timing_localization.tex` | Metrologia temporal | Orçamento de incerteza |
| EXP-001 | Frequência ADS-B 1090ES | 1090 | MHz | Proposto | `07_passive_radar.tex`; RF-011 | RF/experimentos | Validar o caminho dedicado e a decodificação C3 |
| EXP-002 | Frequência UAT contextual | 978 | MHz | Proposto | `07_passive_radar.tex`; RF-010 | RF/experimentos | Canal incluído para ensaio contextual; validar disponibilidade regulatória e de tráfego |
| EXP-003 | Baseline do cenário aeronáutico | 100 | km | Proposto | `07_passive_radar.tex` | Localização/sistemas | Orçamento de enlace e geometria C3 |
| EXP-004 | Faixa de iluminadores TV UHF | 470–860 | MHz | Proposto | `07_passive_radar.tex` | RF/experimentos | Levantamento regulatório e de sítio |
| EXP-005 | Nós receptores no cenário aeronáutico ilustrativo | 2 | nó | Proposto | `07_passive_radar.tex` | Localização/sistemas | Não confundir com demonstrador de três nós ARC-002 |
| EXP-006 | Protocolo de emissor direto cooperativo | ADS-B 1090ES; UAT contextual | — | Proposto | `07_passive_radar.tex`; `DECISIONS.md` ADR-011 | RF/experimentos | Decodificação, associação e resíduos contra estado GNSS transmitido |
| EXP-007 | Protocolo de calibração por transmissor conhecido | sinal direto UHF com posição e forma de onda conhecidas | — | Proposto | `07_passive_radar.tex`; `DECISIONS.md` ADR-011 | Metrologia/experimentos | Resíduos de AOA, atraso e potência contra levantamento independente |
| EXP-008 | Protocolo de reflexão biestática | canais simultâneos de referência e vigilância | — | Proposto | `07_passive_radar.tex`; `DECISIONS.md` ADR-011 | Radar passivo | Pd/Pfa e erros atraso–Doppler contra alvo controlado ou rastreado |
| EXP-009 | Janela de captura bruta de triagem | 10 | s | Proposto | `spectral/verify_c3_acquisition_budget.py` | Dados/experimentos | Ajustar por protocolo após medir ocupação e taxa de eventos |
| EXP-010 | Alturas de triagem para horizonte | estação 1000; aeronave 10000 | m | Proposto | `spectral/verify_c3_acquisition_budget.py` | Sistemas/sítio | Substituir por terreno, sítios e trajetória reais |
| EXP-011 | Protocolo de emissão não cooperativa/jamming | potência, ocupação espectral, AOA, timestamp e FDOA/Doppler por face/nó | — | Proposto | `07_passive_radar.tex`; `DECISIONS.md` ADR-017 | RF/experimentos | Localizar a fonte de radiação e estimar trajetória; não equiparar automaticamente jammer e aeronave |

## Resultado da revisão C0

- Todos os valores quantitativos atualmente usados como parâmetros de arquitetura no artigo possuem entrada neste registro.
- A baseline documental está aprovada para orientar as correções, não para fabricação.
- Entradas `Em conflito` permanecem bloqueadas até C1, C2 ou C3.
- ARC-002 controla o demonstrador de três nós; EXP-005 controla apenas o cenário aeronáutico ilustrativo de dois nós.
- MEC-002 controla a orientação mecânica entre Yagis de faixas diferentes e não satisfaz POL-001.
- C1 corrige a arquitetura documental: somente módulos que satisfaçam POL-001 e POL-003 podem declarar Jones, Stokes, RHCP ou LHCP.

## Regras de manutenção

1. Novos números técnicos recebem um ID antes de entrar no artigo.
2. Mudanças de valor atualizam fonte, estado, responsável e validação.
3. Resultados simulados ou medidos devem apontar para o artefato reproduzível correspondente.
4. Entradas `Em conflito` não podem fundamentar fabricação ou alegação de desempenho.
5. Decisões que alterem premissas ou precedência documental devem ser registradas em `DECISIONS.md`.
