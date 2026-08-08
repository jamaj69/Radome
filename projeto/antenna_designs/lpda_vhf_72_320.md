# Preliminary 72–320 MHz LPDA / LPDA preliminar de 72–320 MHz

**Status:** proposed simulation baseline; not approved for fabrication
**Constraint:** maximum transverse element length of 2.000 m
**Application:** receive-only VHF discovery and direction-sensitive channel

## English

### Design objective

This preliminary log-periodic dipole array (LPDA) replaces the assumption that one narrowband Yagi can cover all VHF. It is sized for approximately 72–320 MHz while respecting a 2 m maximum full element length. The upper limit deliberately extends beyond 300 MHz to provide optimization margin at the nominal VHF boundary. Gain, impedance and pattern values remain unverified until full-wave simulation and measurement.

### Selected Carrel parameters

| Parameter | Symbol | Proposed value |
|---|---:|---:|
| Geometric scale factor | τ | 0.86 |
| Relative spacing factor | σ | 0.16 |
| Number of elements | N | 11 |
| Maximum full element length | L₁ | 2.000 m |
| Approximate active-region range | — | 71.5–323 MHz |
| Calculated inter-element boom length | — | 1.780 m |
| Full apex angle | 2α | 24.68° |

The initial dimensions use:

\[
L_n=L_1\tau^{n-1},\qquad
f_n\approx\frac{143}{L_n}\;\text{MHz},\qquad
d_n=\sigma L_n.
\]

Here, `L_n` is the full tip-to-tip dipole length and `d_n` is the boom spacing from element `n` to `n+1`. The constant 143 MHz·m is an initial thin-element half-wave approximation, not a substitute for electromagnetic optimization.

### Element schedule

Elements are numbered from the largest/rear element toward the smallest/feed-end element.

| Element | Full length (m) | Half-length per side (m) | Approx. resonance (MHz) | Spacing to next (m) | Boom position (m) |
|---:|---:|---:|---:|---:|---:|
| 1 | 2.000 | 1.000 | 71.5 | 0.320 | 0.000 |
| 2 | 1.720 | 0.860 | 83.1 | 0.275 | 0.320 |
| 3 | 1.479 | 0.739 | 96.7 | 0.237 | 0.595 |
| 4 | 1.272 | 0.636 | 112.4 | 0.204 | 0.832 |
| 5 | 1.094 | 0.547 | 130.7 | 0.175 | 1.036 |
| 6 | 0.941 | 0.470 | 152.0 | 0.151 | 1.211 |
| 7 | 0.809 | 0.405 | 176.7 | 0.129 | 1.362 |
| 8 | 0.696 | 0.348 | 205.5 | 0.111 | 1.491 |
| 9 | 0.598 | 0.299 | 239.0 | 0.096 | 1.602 |
| 10 | 0.515 | 0.258 | 277.9 | 0.082 | 1.698 |
| 11 | 0.443 | 0.222 | 323.1 | — | 1.780 |

Manufacturing dimensions should initially retain at least ±2 mm element-length and ±2 mm position control, then be revised from sensitivity analysis. Element diameter, end caps, clamps and the conductive boom alter electrical length and are not yet frozen.

### Feed and construction concept

- Use a balanced two-conductor boom; connect successive dipoles alternately to opposite conductors.
- Locate the feed at the smallest-element end and terminate the rear end according to the validated LPDA model.
- Optimize the balanced boom impedance and a wideband current balun for a 50 Ω receiver interface; do not select a fixed transformer ratio before simulation.
- Include the coax transition, common-mode choke, support mast, lightning protection and bonding in the model.
- Treat the present 1.780 m value as inter-element length; allow additional feed, termination and structural margins, producing an overall boom near 2.0–2.2 m.
- The 2 m rear element exactly consumes the nominal face width and therefore requires edge clearance review or an offset/external mount.

### Expected—not guaranteed—performance

A design with τ = 0.86 and σ = 0.16 is intended for moderate broadband directivity rather than maximum gain. A reasonable simulation target is 6–8 dBi realized gain over the useful band, VSWR ≤ 2.5:1, front-to-back ratio ≥ 10 dB and a stable single main lobe. These are acceptance targets, not predicted or measured results.

### Required validation

1. Model thin-wire and finite-diameter versions in NEC/openEMS.
2. Sweep at least 60–350 MHz with ≤1 MHz resolution around discontinuities.
3. Report S11, realized gain, radiation efficiency, front-to-back ratio, HPBW, cross-polarization and 3D patterns.
4. Repeat with boom, balun, coax, mast, adjacent UHF antenna, face frame, dielectric panel and concrete-base environment.
5. Perform tolerance and temperature sweeps.
6. Build a prototype and validate with VNA plus calibrated OTA measurements.

## Português

### Objetivo do projeto

Esta matriz log-periódica de dipolos (LPDA) preliminar substitui a hipótese de que uma única Yagi estreita possa cobrir todo o VHF. Ela é dimensionada para aproximadamente 72–320 MHz, respeitando o comprimento transversal máximo de 2 m. O limite superior ultrapassa deliberadamente 300 MHz para fornecer margem de otimização na fronteira nominal de VHF. Ganho, impedância e diagramas permanecem não verificados até simulação de onda completa e medição.

### Parâmetros de Carrel selecionados

| Parâmetro | Símbolo | Valor proposto |
|---|---:|---:|
| Fator de escala geométrica | τ | 0,86 |
| Fator de espaçamento relativo | σ | 0,16 |
| Número de elementos | N | 11 |
| Comprimento total máximo | L₁ | 2,000 m |
| Região ativa aproximada | — | 71,5–323 MHz |
| Comprimento calculado entre elementos no boom | — | 1,780 m |
| Ângulo total do vértice | 2α | 24,68° |

As dimensões iniciais empregam as mesmas equações apresentadas na seção em inglês. `L_n` é o comprimento total ponta a ponta do dipolo e `d_n` é o espaçamento no boom entre os elementos `n` e `n+1`. A constante de 143 MHz·m é apenas uma aproximação inicial de meia onda para elemento fino.

### Tabela de elementos

A tabela dimensional da seção em inglês é normativa para esta baseline e evita arredondamentos divergentes entre idiomas. Os elementos são numerados do maior, na traseira, para o menor, junto à alimentação.

As dimensões de fabricação devem manter inicialmente pelo menos ±2 mm no comprimento e ±2 mm na posição, sendo posteriormente revistas pela análise de sensibilidade. Diâmetro dos elementos, tampas, grampos e boom condutor alteram o comprimento elétrico e ainda não estão congelados.

### Conceito de alimentação e construção

- Usar boom balanceado de dois condutores, ligando dipolos sucessivos alternadamente aos condutores opostos.
- Posicionar a alimentação no lado do menor elemento e terminar a extremidade traseira conforme o modelo validado.
- Otimizar a impedância do boom balanceado e um balun de corrente de banda larga para interface de 50 Ω; não fixar relação de transformação antes da simulação.
- Incluir transição coaxial, choque de modo comum, mastro, proteção contra descargas e equipotencialização no modelo.
- Tratar 1,780 m como comprimento entre elementos; margens de alimentação, terminação e estrutura levam o boom total para aproximadamente 2,0–2,2 m.
- O elemento traseiro de 2 m consome toda a largura nominal da face, exigindo revisão de folga ou montagem externa deslocada.

### Desempenho esperado, não garantido

Os parâmetros τ = 0,86 e σ = 0,16 visam diretividade moderada de banda larga, não ganho máximo. A meta razoável de simulação é ganho realizado de 6–8 dBi na faixa útil, VSWR ≤ 2,5:1, relação frente-costas ≥ 10 dB e lóbulo principal único e estável. São metas de aceitação, não resultados previstos ou medidos.

### Validação obrigatória

1. Modelar versões de fio fino e diâmetro finito em NEC/openEMS.
2. Varrer pelo menos 60–350 MHz, com resolução ≤1 MHz nas descontinuidades.
3. Relatar S11, ganho realizado, eficiência, relação frente-costas, HPBW, polarização cruzada e diagramas 3D.
4. Repetir com boom, balun, coaxial, mastro, antena UHF adjacente, moldura, painel dielétrico e ambiente da base.
5. Executar varreduras de tolerância e temperatura.
6. Construir protótipo e validar com VNA e medição OTA calibrada.
