# RADOME — Registro de decisões de arquitetura

## ADR-001 — Fonte técnica autoritativa

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** `projetov1.tex`, seus capítulos incluídos e a bibliografia associada formam o documento técnico autoritativo.
- **Consequência:** documentos anteriores permanecem como histórico e não prevalecem em caso de conflito.
- **Histórico principal:** `Radome2.pdf`, `RadomeBrasil.pdf`, `RADOME V3.md`, `RADOME V3 — Arquitetura Eletrônica Distribuída Revisada.md`, `Projeto_Radomes_Multifaixa_Revisado.md`, `projeto_tecnico_radome_consolidado.md` e seus PDFs derivados.

## ADR-002 — Versionamento independente

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** usar dois identificadores independentes: versão do documento e revisão da arquitetura.
- **Baseline atual:** documento 1.1; arquitetura 3, conceitual.
- **Consequência:** “RADOME V1” deixa de ser usado como identificador ambíguo do sistema completo. Uma nova compilação editorial pode alterar a versão documental sem alterar a arquitetura, e vice-versa.

## ADR-003 — Registro central de parâmetros

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** `PARAMETERS.md` controla valores quantitativos, estado da evidência, fonte, responsabilidade e gate de validação.
- **Consequência:** números copiados de documentos históricos não retornam ao documento vigente sem revisão explícita.

## ADR-004 — Conflitos não são requisitos

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** parâmetros incompatíveis permanecem visíveis com estado `Em conflito` até resolução pelo gate apropriado.
- **Consequência:** raio, lado de face, apoio civil, lacunas espectrais e polarimetria não podem orientar fabricação enquanto seus conflitos estiverem abertos.

## ADR-005 — Aprovação condicionada da baseline C0

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** aprovar a baseline documental para orientar as ondas de correção, preservando bloqueios explícitos sobre parâmetros `Em conflito`.
- **Escopo da aprovação:** hierarquia documental, versionamento, IDs, estados de evidência e responsabilidades.
- **Fora do escopo:** aprovação de fabricação, desempenho ou resolução técnica dos conflitos C1–C3.
- **Distinções obrigatórias:** o cenário aeronáutico ilustrativo usa dois nós, enquanto o demonstrador-alvo usa três; os 90° entre as Yagis VHF e UHF representam orientação mecânica entre faixas diferentes, não duas componentes polarimétricas coerentes do mesmo sinal.

## ADR-006 — Polarimetria restrita à mesma faixa

- **Data:** 8 de agosto de 2026
- **Estado:** aceita
- **Decisão:** Jones, Stokes, RHCP e LHCP somente podem ser calculados a partir de duas portas simultâneas, ortogonais e coerentes na mesma frequência.
- **Aplicação ao demonstrador:** as Yagis VHF e UHF atuais são canais independentes de polarização única; sua montagem a 90° oferece diversidade mecânica/orientacional entre faixas, não polarimetria.
- **Expansão futura:** uma faixa poderá receber antena dual-polarizada ou par cruzado na mesma faixa, com cadeias coerentes e calibração de amplitude/fase.
- **Evidência exigida:** matriz de Jones, isolamento, cross-pol, equilíbrio de amplitude, fase relativa e deriva versus frequência, ângulo e temperatura.

## ADR-007 — LPDA VHF como candidata de banda larga

- **Data:** 8 de agosto de 2026
- **Estado:** proposta para simulação
- **Decisão:** adotar uma LPDA de 11 elementos, τ = 0,86, σ = 0,16 e elemento máximo de 2 m como baseline de simulação para aproximadamente 72–320 MHz.
- **Motivo:** uma Yagi convencional com elemento máximo de 2 m seria predominantemente estreita e centrada na parte baixa de VHF.
- **Limite:** a LPDA não substitui a Yagi no modelo físico atual até que ganho realizado, impedância, padrão, cargas e integração sejam validados.
- **Fonte dimensional:** `antenna_designs/lpda_vhf_72_320.md`.

## ADR-008 — Mastro polarimétrico de quatro canais

- **Data:** 8 de agosto de 2026
- **Estado:** proposta para simulação
- **Decisão:** avaliar dois canais VHF ortogonais a 0°/90° e dois canais UHF ortogonais a 45°/135° em um mastro estrutural comum, mantendo quatro booms e cadeias RF eletricamente independentes.
- **Calibração:** estimar o campo por faixa com a inversão regularizada de uma matriz complexa 2×2 dependente de frequência, direção e temperatura.
- **Limite:** a rotação UHF de 45° não garante isolamento; quatro portas, acoplamento e padrões embarcados devem ser resolvidos como uma única estrutura eletromagnética.
- **Fonte:** `antenna_designs/dual_band_quad_polarization_mast.md`.

## ADR-009 — Malha geodésica C2 preliminar

- **Data:** 8 de agosto de 2026
- **Estado:** proposta para verificação geométrica
- **Decisão:** substituir a subdivisão provisória de 60 faces por uma malha classe I de frequência 2 derivada de um icosaedro regular.
- **Resultado topológico:** o envelope fechado passa a ter 42 vértices, 120 arestas e 80 faces triangulares, com consistência de Euler igual a 2.
- **Limite:** a projeção esférica gera duas classes de corda; portanto, o lado nominal de 2 m não pode ser aplicado simultaneamente a todas as faces sem declarar a regra de escala.
- **Fonte:** `geometry/verify_radome_geometry.py`.
