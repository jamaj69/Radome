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
- emissores fixos canônicos: 6.078 emissões, 3.335 sítios e 3.995 proxies de
  antena; 4.228 SARC e 1.850 SCM selecionados com partição sem perdas;
- 1.849 emissões SCM têm frequência, potência e altura presentes; nenhuma SARC
  atende esse mínimo devido à ausência de potência.

## Validação reproduzível

- 78 testes automatizados aprovados na descoberta completa com
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

Gerar candidatos adicionais nas 1.732 células descobertas, começando por pontos
altos/cumeadas nas regiões de lacuna e mantendo proximidade urbana e distribuição
azimutal como critérios logísticos. Não executar cobertura mínima antes de cada
célula possuir ao menos um candidato; não promover cota BC250 a relevo validado.

## Comando de retomada

```bash
cd /home/jamaj/src/Radome/geoespacial
/home/python/pyenv/bin/python -m unittest discover -s tests -v
/home/python/pyenv/bin/python verify_reproducibility.py
```
