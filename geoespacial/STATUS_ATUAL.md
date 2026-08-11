# Estado atual do subprojeto geoespacial

**Checkpoint:** 11 de agosto de 2026, após a normalização canônica SMP.

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
  conhecido, ainda não classificado por serviço/emissor.

## Validação reproduzível

- 30 testes automatizados aprovados;
- `run_pipeline.py` executado integralmente;
- duas execuções consecutivas comparadas por `verify_reproducibility.py`;
- 12 produtos CSV, GeoJSON, GraphML, JSON, PNG e gzip com SHA-256 idênticos;
- resultado registrado em `reports/reproducibility.json` com
  `byte_reproducible: true` e `differences: {}`.

## Lacunas controladas

- a entidade SMP `antena` é proxy cadastral de estação/setor/sítio e ainda não
  representa uma estrutura radiante fisicamente confirmada;
- SLP/SLE/SARC/STEL ainda não foram classificados nem pareados como
  radioenlaces;
- radiodifusão ainda requer normalização regulatória de largura, ERP e HCI;
- VOR/NDB/DME precisam de recorte brasileiro e vínculo municipal; DME exige
  tabela canal--frequência;
- potência, altura radiante e diagramas permanecem incompletos em várias fontes;
- dez das 14 camadas DECEA selecionadas ainda não foram congeladas;
- TOPODATA continental ainda não foi selecionado e baixado por região;
- radares aeronáuticos/militares não possuem camada pública estruturada
  confirmada; VSAT e radares meteorológicos estão apenas identificados.

## Próxima ação executável

Auditar por streaming os arquivos menores do pacote geral Anatel, começando por
SARC, banda larga fixa e telefonia fixa. A entrega deve inventariar serviço,
classe, direção, coordenadas, frequência, potência e atributos de antena, sem
ainda inferir radioenlaces. Depois, os emissores fixos aprovados serão migrados
ao mesmo esquema canônico usado pela SMP.

## Comando de retomada

```bash
cd /home/jamaj/src/Radome/geoespacial
/home/python/pyenv/bin/python -m unittest discover -s tests -v
/home/python/pyenv/bin/python verify_reproducibility.py
```
