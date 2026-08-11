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
- emissores fixos canônicos: 6.078 emissões, 3.335 sítios e 3.995 proxies de
  antena; 4.228 SARC e 1.850 SCM selecionados com partição sem perdas;
- 1.849 emissões SCM têm frequência, potência e altura presentes; nenhuma SARC
  atende esse mínimo devido à ausência de potência.

## Validação reproduzível

- 46 testes automatizados aprovados;
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
- o subconjunto TOPODATA das rotas foi baixado, mas os GeoTIFFs ainda precisam
  ser extraídos e a lacuna `26S48_ZN.zip` requer tratamento explícito;
- radares aeronáuticos/militares não possuem camada pública estruturada
  confirmada; VSAT e radares meteorológicos estão apenas identificados.

## Próxima ação executável

Extrair atomicamente os 154 GeoTIFFs TOPODATA, montar o índice espacial e repetir
os 328 perfis de terreno. Não inventar substituto para `26S48_ZN.zip`; as rotas
afetadas devem permanecer com terreno ausente. Alturas físicas continuam pendentes.

## Comando de retomada

```bash
cd /home/jamaj/src/Radome/geoespacial
/home/python/pyenv/bin/python -m unittest discover -s tests -v
/home/python/pyenv/bin/python verify_reproducibility.py
```
