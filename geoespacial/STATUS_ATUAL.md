# Estado atual do subprojeto geoespacial

**Checkpoint:** 10 de agosto de 2026, após o commit de reprodução byte a byte.

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
- Anatel radiodifusão: 35.126 registros, 18.285 licenciados C4, agregados em
  11.921 sítios municipais;
- ANAC: aeródromos públicos/privados, helipontos e helideques baixados e
  inventariados;
- DECEA/ICA: VOR, NDB, DME e `navaids` baixados, verificados e inventariados;
- pacote geral Anatel de 10,45 GB descompactados disponível e com esquema
  conhecido, ainda não classificado por serviço/emissor.

## Validação reproduzível

- 26 testes automatizados aprovados;
- `run_pipeline.py` executado integralmente;
- duas execuções consecutivas comparadas por `verify_reproducibility.py`;
- sete produtos CSV, GeoJSON, GraphML, JSON e PNG com SHA-256 idênticos;
- resultado registrado em `reports/reproducibility.json` com
  `byte_reproducible: true` e `differences: {}`.

## Lacunas controladas

- o grafo SMP por sítio ainda não preserva cada antena e emissão como entidade;
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

Implementar em Python o esquema canônico `sitio_fisico`--`antena`--`emissao` e
migrar primeiro os registros SMP já auditados, mantendo:

- identificador e coordenada do sítio;
- código IBGE e conflitos;
- estação, setor e operadora;
- geração, tecnologia e subtipo 5G;
- faixa/subfaixa, centro Tx/Rx e designação de emissão;
- largura necessária e limites espectrais derivados;
- proveniência do registro e confiança de cada atributo.

O gate dessa próxima mudança exige testes de cardinalidade e perda zero de
registros, um resumo JSON, produtos derivados em `outputs/` e nova comparação
de reprodução. Depois disso, o mesmo esquema será aplicado aos arquivos menores
do pacote geral Anatel: SARC, banda larga fixa e telefonia fixa.

## Comando de retomada

```bash
cd /home/jamaj/src/Radome/geoespacial
/home/python/pyenv/bin/python -m unittest discover -s tests -v
/home/python/pyenv/bin/python verify_reproducibility.py
```
