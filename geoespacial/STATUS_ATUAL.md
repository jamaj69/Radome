# Estado atual do subprojeto geoespacial

**Checkpoint:** 11 de agosto de 2026, após a auditoria streaming de SLP e Mosaico-STEL.

## Vinculação e governança

O projeto principal é o artigo técnico bilíngue em `projeto/`. Este diretório é
o subprojeto que produz evidência reproduzível para a metodologia de seleção de
sítios. Os marcos ativos são:

- M2E: fechamento das camadas oficiais de emissões;
- M3: infraestrutura aeronáutica e estratégica.

Toda manipulação autoritativa das bases é feita por Python conforme
`POLITICA_REPRODUTIBILIDADE.md`. Dados brutos são imutáveis; QGIS, Blender,
planilhas e comandos avulsos são ferramentas de inspeção ou apresentação.

## Dados e integrações concluídos

- IBGE BC250 2025 baixado, verificado e usado na triagem continental;
- 5.571 municípios e sedes no modelo territorial preliminar;
- população do Censo 2022 integrada, com Boa Esperança do Norte marcada sem
  população censitária em vez de receber zero;
- Anatel SMP: 3.284.526 registros, 105.726 sítios aproximados, gerações
  2G/3G/4G/5G e espectro individual auditado;
- esquema SMP canônico: 105.726 sítios, 282.623 proxies cadastrais de antena e
  3.284.526 emissões, todas ligadas e sem perda de linha da fonte;
- Anatel radiodifusão: 35.126 registros, 18.285 licenciados C4, agregados em
  11.921 sítios municipais;
- ANAC: aeródromos públicos/privados, helipontos e helideques baixados e
  inventariados;
- DECEA/ICA: VOR, NDB, DME e `navaids` baixados, verificados e inventariados;
- pacote geral Anatel de 10,45 GB descompactados disponível e com esquema
  conhecido; SARC, banda larga fixa, telefonia fixa e SLE auditados por streaming;
- SARC: 8.774 registros, 4.228 ativos potencialmente emissores e 4.583
  frequências utilizáveis, mas sem potência/designação utilizável;
- banda larga fixa: 7.513 registros, 1.850 ativos com direção Tx, 3.706 com
  frequência/potência e 3.514 com largura decodificada;
- telefonia fixa: 589 registros georreferenciados, mas sem parâmetros RF úteis.
- SLE: 119.058 registros, 118.968 ativos, 59.484 ativos com direção Tx,
  115.458 coordenadas válidas e 118.968 designações, potências e alturas
  utilizáveis; 118.490 linhas representam estações móveis e não sítios fixos;
- SLP: 10.580.778 linhas, das quais 10.542.118 ativas e 5.271.059 Tx ativas;
  9.495.200 linhas móveis e 10.451.584 coordenadas válidas;
- Mosaico-STEL: consolidado de 10.817.122 linhas que reproduz a contagem SLP e
  agrega as contagens de SLE, SARC, SCM, STFC e radioenlaces explícitos; não é
  camada independente e não deve ser somado aos membros específicos;
- radioenlaces explícitos extraídos sem pareamento: 64.948 STFC, 35.424 SCM e
  38 SMP, totalizando 100.410 registros e 17.214 números de estação por família;
- chaves brutas recuperadas para as 100.410 linhas: Fistel, ato de RF e códigos
  homologados de antena/transmissor completos; equivalência linha a linha confirmada;
- 928 grupos família--Fistel--ato particionados: 340 candidatos recíprocos de
  duas coordenadas, 40 não recíprocos, 175 locais e 373 ambíguos;
- nos 340 recíprocos, 328 têm caminho alinhado a até 15 graus e 12 não; a
  sensibilidade é 326/328/328/329 grupos a 5/10/15/30 graus;
- triagem Terrarium z8 dos 328 alinhados: em `k=1`, 218 têm 60% de Fresnel livre,
  69 apenas visada, 40 obstruídos e 1 sem terreno; em `k=4/3`, 228/66/33/1;
- seleção TOPODATA das 328 rotas: 154 arquivos, cerca de 9,07 GiB listados;
  `26S48_ZN.zip` ausente do índice oficial e preservado como lacuna;
- aquisição TOPODATA concluída: 154 ZIPs validados, 9.743.140.443 bytes reais,
  zero falhas e SHA-256 individual registrado no recibo incremental;
- extração TOPODATA concluída: 154 GeoTIFFs georreferenciados, 12.013.983.756
  bytes, zero falhas e índice GeoJSON com extensão e resolução de cada folha;
- perfis TOPODATA das 328 rotas: em `k=1`, 247 têm 60% de Fresnel livre, 59
  apenas visada, 21 são obstruídos e 1 permanece sem terreno; em `k=4/3`,
  257/50/20/1; nenhuma aresta foi criada;
- auditoria de alturas por direção e frequência: 993 caminhos recíprocos, sendo
  971 com uma altura cadastral em cada ponta, 12 ambíguos e 10 incompletos;
  325 candidatos têm ao menos um caminho utilizável, 1 só ambíguos e 2 só ausentes;
- recálculo TOPODATA dos 971 caminhos não ambíguos: em `k=1`, 780 têm Fresnel
  livre, 114 somente visada, 69 são obstruídos e 8 não têm terreno; por candidato,
  246/57/21/1 têm, respectivamente, ao menos um Fresnel, ao menos um LOS, somente
  caminhos obstruídos ou somente terreno ausente;
- geometria vertical: 963 caminhos avaliáveis e 8 sem terreno; no limiar
  provisório de 1°, 933 caminhos em 311 candidatos concordam nas duas pontas
  para `k=1` e também para `k=4/3`;
- pré-qualificação consolidada: em `k=1`, 764 caminhos de 240 candidatos passam
  simultaneamente reciprocidade, azimute, altura, Fresnel e geometria vertical;
  em `k=4/3`, são 796 caminhos de 250 candidatos; continuam sem pareamento;
- GraphML de hipóteses: multigrafo dirigido com 497 nós, 796 arestas cadastrais,
  250 candidatos e 135 frequências; zero arestas operacionais, com 237 componentes
  em `k=1` e 247 em `k=4/3`, maior componente com três nós;
- enriquecimento do GraphML: 497 pontas vinculadas a 365 municípios por 497
  arestas administrativas, sem código ausente ou conflito municipal; grafo total
  com 862 nós e 1.293 arestas, das quais nenhuma é operacional;
- grafo geoespacial unificado: 123.846 nós e 119.158 registros de aresta, reunindo
  5.571 municípios, 105.726 sítios SMP, 11.921 radiodifusores, 497 endpoints e
  131 candidatos; zero colisões de atributo e zero arestas operacionais;
- contexto dos candidatos: os 131 candidatos foram associados por contenção
  BC250 a municípios canônicos, sem ausências; o grafo enriquecido tem 119.289
  arestas, incluindo 131 novos vínculos administrativos, e continua com zero
  arestas operacionais;
- dentro dos raios geométricos preliminares há 790.026 incidências candidato--SMP,
  80.682 candidato--radiodifusor e 3.623 candidato--endpoint; são incidências
  sobrepostas, não objetos únicos nem confirmação de visada/iluminação;
- ordenação preliminar: três cenários preservam separadamente altitude, cidades,
  oito setores azimutais, SMP, radiodifusão, endpoints e conectividade; Aeroporto
  Embaixador Walther Moreira Salles lidera os três, seguido na ordenação robusta
  por Anápolis, São Paulo, Belo Horizonte e Brasília;
- grade continental de 0,25°: 11.363 centros dentro das UFs, dos quais 9.631
  estão em ao menos um raio geométrico e 1.732 permanecem descobertos; a fração
  ponderada por área é 84,46%, com 1.863 células em cobertura única e 7.768 em
  cobertura redundante;
- lacunas dominantes: PA 817 células, AM 337, MT 330, AP/PI 73 cada e RR 44;
  a instância do otimizador preserva essas impossibilidades e não pode produzir
  uma falsa solução de cobertura nacional;
- heurística alternativa registrada: tesselação triangular com vértices em
  candidatos, preferência por faces de visada completa `K3`, caso degradado de
  duas arestas e pontuação de iluminadores internos; implementação pendente e
  comparação obrigatória com a cobertura por discos;
- linha de base triangular executada: 131 vértices e 244 faces Delaunay; somente
  22 faces têm três arestas de curvatura pendentes, 6 têm duas e 216 são
  esparsas; 92,92% da área da grade está dentro da envoltória da malha, sem que
  isso represente cobertura ou visada;
- dentro da envoltória há 100.967 sítios SMP, 11.608 radiodifusores e 480
  endpoints; associações são apenas geométricas e nenhuma é `illuminates`;
- seleção TOPODATA das lacunas continentais concluída: as 1.732 células
  descobertas intersectam 141 arquivos disponíveis, com 8.737.783.808 bytes
  listados e nenhuma folha requerida ausente do índice oficial;
- aquisição dessas lacunas concluída: 141 ZIPs validados por CRC, totalizando
  8.743.661.110 bytes reais, com SHA-256 individual; uma segunda passagem local
  marcou e revalidou os 141 como reutilizados, sem falhas;
- extração das lacunas concluída: 141 GeoTIFFs georreferenciados, com
  10.964.218.374 bytes, SHA-256 individual e índice GeoJSON próprio; a segunda
  passagem revalidou todos como reutilizados;
- sementes de terreno alto geradas para as 1.732 células descobertas: uma
  semente por célula no centro do pixel TOPODATA de maior cota, sem ausência;
  cotas de 29,389--2.131,380 m e relevo relativo celular de
  24,169--2.062,120 m; CSV gzip e GeoJSON reproduziram byte a byte;
- triagem multiescala consolidada: anéis de 5/10/25 km com 36 azimutes estão
  completos para 1.732/1.732/1.731 sementes; consolidação a 10 km reteve 1.484
  candidatos representando todas as 1.732 células; somente a semente
  `gap-seed:cell:+003.8750:-0051.1250` permanece com 33/36 amostras no anel de
  25 km e não recebe pontuação otimista para esse anel;
- grafo aumentado de candidatos: os 1.484 candidatos TOPODATA foram ligados aos
  131 originais, totalizando 1.615 candidatos; 45.137 pares satisfazem somente
  o limite geométrico de curvatura e geram 90.274 arcos dirigidos, todos não
  operacionais e pendentes de terreno intermediário, visada e Fresnel;
- cobertura geométrica aumentada: os 1.615 candidatos incidem sobre todos os
  11.363 centros da grade continental; 64 células têm cobertura única e 11.299
  redundante, mas o resultado por discos não comprova terreno, visada ou RF;
- malha triangular aumentada: 1.615 vértices geram 3.209 faces Delaunay, sendo
  2.724 `K3` somente por curvatura pendente; a envoltória contém 98,41% da área
  da grade e associa geometricamente 101.500 SMP, 11.703 radiodifusores e 481
  endpoints, sem criar `illuminates` ou visada confirmada;
- prioridade de perfis: as 3.209 faces contêm 4.823 arestas únicas; 4.262 têm
  limite de curvatura disponível, 4.228 incidem em ao menos uma face `K3`
  pendente e 289 combinam geometricamente as três classes de infraestrutura;
- seleção TOPODATA das arestas: 4.262 rotas e 166.474 amostras requerem 214
  folhas oficiais; 199 já estão locais e 15 novas somam 945.815.552 bytes
  listados; `03N66_ZN.zip` está ausente do inventário e afeta duas arestas;
- aquisição TOPODATA das arestas concluída: 214 ZIPs validados por CRC e
  SHA-256, totalizando 13.317.509.748 bytes reais, sem falhas; uma segunda
  passagem revalidou todos como reutilizados;
- extração TOPODATA das arestas concluída: 214 GeoTIFFs em EPSG:4326,
  totalizando 16.660.168.596 bytes, sem falhas e com índice GeoJSON próprio;
  uma segunda passagem revalidou todos como reutilizados;
- perfis TOPODATA da malha: em `k=1`, 3.653 das 4.262 arestas têm visada
  topográfica, 607 são obstruídas e 2 não têm terreno completo; em `k=4/3`,
  são 3.849/411/2; não há teste de Fresnel sem frequência selecionada e nenhuma
  aresta foi promovida a operacional;
- faces TOPODATA: em `k=1`, 2.033 das 3.209 faces têm três arestas LOS, 410
  têm duas e 766 são esparsas; em `k=4/3`, são 2.248/320/641; três faces tocam
  arestas sem terreno e nenhuma classificação inclui Fresnel ou RF;
- comparação malha--discos: embora os discos incidam nos 11.363 centros, faces
  `K3` LOS contêm só 1.149 centros em `k=1` (10,11%) e 1.299 em `k=4/3`
  (11,43%); os grafos têm 129/122 componentes, maiores componentes com
  1.174/1.325 vértices e 47/23 vértices de articulação; o gate confere a
  paridade candidato--vértice, que cada perfil pertence à malha e que as
  células `K3` não excedem a grade antes de publicar o resultado;
- seleção das folhas de borda concluída: os 188.788 centros e pontos dos anéis
  requerem 175 folhas TOPODATA disponíveis, das quais 143 já são locais e 32
  novas somam 1.945.108.480 bytes listados; `05N51_ZN.zip` não consta no
  inventário oficial e afeta somente três pontos de uma semente, mantidos como
  incompletos de forma conservadora;
- aquisição das folhas de borda concluída: 175 ZIPs validados por CRC e
  SHA-256, totalizando 10.819.492.567 bytes reais, sem falhas; uma segunda
  passagem marcou e revalidou todos como reutilizados, sem nova transferência;
- extração das folhas de borda concluída: 175 GeoTIFFs georreferenciados,
  totalizando 13.608.072.450 bytes, sem falhas, com índice GeoJSON próprio; uma
  segunda passagem marcou e revalidou todos como reutilizados;
- emissores fixos canônicos: 6.078 emissões, 3.335 sítios e 3.995 proxies de
  antena; 4.228 SARC e 1.850 SCM selecionados com partição sem perdas;
- 1.849 emissões SCM têm frequência, potência e altura presentes; nenhuma SARC
  atende esse mínimo devido à ausência de potência.

## Validação reproduzível

- 102 testes automatizados aprovados na descoberta completa com
  `PYTHONPATH=geoespacial`;
- `run_pipeline.py` executado integralmente;
- duas execuções consecutivas comparadas por `verify_reproducibility.py`;
- 25 produtos CSV, GeoJSON, GraphML, JSON, PNG e gzip com SHA-256 idênticos;
- resultado registrado em `reports/reproducibility.json` com
  `byte_reproducible: true` e `differences: {}`.
- o novo extrato e seu relatório foram reproduzidos separadamente com hashes
  idênticos; sua inclusão na prova integral ocorrerá após o gate de chaves brutas.

## Lacunas controladas

- a entidade SMP `antena` é proxy cadastral de estação/setor/sítio e ainda não
  representa uma estrutura radiante fisicamente confirmada;
- SLP/Mosaico-STEL foram classificados, mas nenhum radioenlace foi pareado;
- o consolidado Mosaico-STEL apresenta sobreposição estrutural com SLP e outras
  camadas; a equivalência linha a linha ainda precisa ser demonstrada;
- radiodifusão ainda requer normalização regulatória de largura, ERP e HCI;
- VOR/NDB/DME precisam de recorte brasileiro e vínculo municipal; DME exige
  tabela canal--frequência;
- potência, altura radiante e diagramas permanecem incompletos em várias fontes;
- dez das 14 camadas DECEA selecionadas ainda não foram congeladas;
- o subconjunto TOPODATA das rotas foi extraído, mas a lacuna `26S48_ZN.zip`
  requer tratamento explícito nos perfis afetados;
- radares aeronáuticos/militares não possuem camada pública estruturada
  confirmada; VSAT e radares meteorológicos estão apenas identificados.

## Próxima ação executável

Diagnosticar as células fora de faces `K3`, identificar os gargalos responsáveis
e formular a próxima expansão/seleção de candidatos, mantendo iluminadores
separados do futuro modelo RF/Fresnel.

## Comando de retomada

```bash
cd /home/jamaj/src/Radome/geoespacial
/home/python/pyenv/bin/python -m unittest discover -s tests -v
/home/python/pyenv/bin/python verify_reproducibility.py
```
