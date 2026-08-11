# Seleção geoespacial de sítios RADOME

Este diretório é o subprojeto geoespacial do artigo técnico bilíngue RADOME e
contém o fluxo reproduzível para selecionar o menor conjunto de
sítios que satisfaça uma meta explícita de cobertura do espaço aéreo brasileiro.
O resultado é uma triagem de engenharia, não uma autorização de implantação.

A vinculação, os entregáveis e o gate para incorporar resultados às edições em
português e inglês estão definidos em `SUBPROJETO.md`. Os marcos ativos são M2E,
para emissões oficiais, e M3, para infraestrutura aeronáutica e estratégica.

O escopo ativo é somente o território continental. Arquipélagos e ilhas
oceânicas ficam fora da otimização nacional: cada grupo próximo será estudado
depois como um caso independente, com um único radome em seu ótimo local.

A especificação destinada à futura incorporação no artigo está em
`METODOLOGIA_ARTIGO.md`. A política obrigatória de manipulação das bases está em
`POLITICA_REPRODUTIBILIDADE.md`. `run_pipeline.py` reproduz testes, pré-seleção e
grafo com os dados locais verificados; `run_pipeline.sh` é apenas um wrapper de
compatibilidade e não transforma dados.

A reprodução byte a byte é verificada executando o pipeline duas vezes com
`verify_reproducibility.py`. O último resultado e os hashes ficam em
`reports/reproducibility.json`.

O diagnóstico das fontes de torres celulares, aeroportos, bases aéreas e
comandos está em `FONTES_INFRAESTRUTURA.md`.

O plano completo de aquisição, integração, validação e otimização está em
`ROADMAP_GEOESPACIAL.md`. As instruções normativas fornecidas pelo usuário estão
preservadas em `REQUISITOS_GEOLOCALIZACAO.md`; esses requisitos devem ser
consultados antes de alterar critérios ou preparar o texto metodológico.
O checkpoint compacto para retomar o trabalho está em `STATUS_ATUAL.md`.

O inventário dos cadastros já obtidos é reproduzido com:

```bash
/home/python/pyenv/bin/python inventory_infrastructure.py \
  --anac-dir data/raw/anac/aerodromos \
  --anatel-zip data/raw/anatel/estacoes_licenciadas.zip \
  --decea-capabilities data/raw/decea/wfs-get-capabilities.xml \
  --output data/manifests/infrastructure_inventory.json
```

O WFS do DECEA é um catálogo vivo; o `GetCapabilities` usado em cada execução
deve ser preservado em `data/raw/` para que a seleção de camadas seja auditável.
Camadas WFS são adquiridas de forma atômica e recebem hashes com
`acquire_decea_wfs.py`.

O cadastro SMP dedicado da Anatel é resumido sem extrair o CSV de quase 1 GB:

```bash
/home/python/pyenv/bin/python inventory_smp.py \
  data/raw/anatel/estacoes_smp.zip \
  --output data/manifests/smp_inventory.json
```

O total de coordenadas distintas é apenas uma aproximação inicial de sítios
físicos. A camada de torres deve consolidar co-localizações por distância,
número de estação e operadora, preservando tecnologias e frequências associadas.

O cadastro SMP é normalizado sem perdas no esquema canônico com:

```bash
/home/python/pyenv/bin/python build_canonical_smp.py \
  --smp data/raw/anatel/estacoes_smp.zip \
  --output-dir outputs/canonical_smp \
  --report reports/canonical_smp/summary.json
```

A entidade `antena` é um proxy cadastral de estação, setor e sítio, não uma
contagem física comprovada. O método, as cardinalidades e o gate estão em
`reports/canonical_smp/README.md`.

Os arquivos menores do pacote geral Anatel são auditados sem extração com:

```bash
/home/python/pyenv/bin/python audit_anatel_general.py \
  --source data/raw/anatel/estacoes_licenciadas.zip \
  --output-dir outputs/anatel_general_audit \
  --report reports/anatel_general_audit/summary.json
```

Os resultados SARC, banda larga fixa, telefonia fixa, SLE, SLP e Mosaico-STEL
estão documentados em `reports/anatel_general_audit/README.md`.

As famílias explicitamente denominadas radioenlace são extraídas, ainda sem
pareamento, por `extract_anatel_radio_links.py`; resultados e limites estão em
`reports/anatel_radio_links/README.md`.

Transmissores/repetidores ativos de SARC e SCM são migrados ao esquema canônico
com partição exaustiva das exclusões:

```bash
/home/python/pyenv/bin/python build_canonical_fixed_emitters.py \
  --sarc outputs/anatel_general_audit/sarc.csv.gz \
  --fixed-broadband outputs/anatel_general_audit/fixed_broadband.csv.gz \
  --output-dir outputs/canonical_fixed_emitters \
  --report reports/canonical_fixed_emitters/summary.json
```

O resultado e suas limitações estão em `reports/canonical_fixed_emitters/`.

A auditoria registro a registro de geração, tecnologia, frequência e designação
de emissão está em `reports/ANATEL_SPECTRUM_AUDIT.md`. Ela também documenta a
limitação da base de radiodifusão, que fornece canal e frequência central, mas
não largura/designação de emissão.

A matriz consolidada do que existe e do que ainda falta em todas as camadas
oficiais de emissões está em `CAMADAS_EMISSOES_OFICIAIS.md`. Ela define o gate
M2E e impede que uma camada apenas georreferenciada seja considerada pronta
para modelagem RF quantitativa.

A rede município--emissor é construída com o código IBGE como chave:

```bash
/usr/bin/python3 build_municipal_emitter_network.py \
  --bc250 data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
  --population data/raw/ibge/municipios/populacao_censo_2022.json \
  --smp data/raw/anatel/estacoes_smp.zip \
  --terrain-cache data/raw/mapzen/terrarium \
  --output-dir outputs/municipal_emitter_network
```

Os nós `municipio` recebem longitude, latitude, altitude da sede, população e
área. Os nós `torre_smp` preservam estações, operadoras e tecnologias agregadas
e são ligados ao município por `located_in`. O GraphML e os CSVs produzidos são
arquivos derivados volumosos e permanecem em `outputs/`.

## Hipóteses controladas

- a cobertura é avaliada a 150 m, 3 000 m e 10 000 m acima do terreno;
- cada sítio continental deve ter visada direta para pelo menos outro sítio;
- ilhas oceânicas são componentes independentes e estão dispensadas da
  conectividade visual com a rede continental;
- candidatos são extraídos primeiro de cumeadas, máximos locais e pontos de
  grande proeminência relativa;
- altitude absoluta não basta: área visível, população/cidades visíveis em
  vários azimutes e quantidade de enlaces também entram na pontuação;
- proximidade logística é um peso positivo, sem distância máxima eliminatória;
- curvatura terrestre e refração padrão devem ser incluídas nos testes de
  horizonte; a zona de Fresnel depende da faixa e será avaliada separadamente;
- cobertura geométrica não implica desempenho de detecção. Potência do
  iluminador, RCS, ruído, RFI, ganho e perdas pertencem a uma etapa posterior.

As hipóteses numéricas ficam em `site_selection.json`. Alterações que mudem o
número ótimo de sítios devem modificar esse arquivo, registrar a justificativa e
produzir uma nova execução identificada.

## Fontes previstas

| Dado | Fonte principal | Uso |
|---|---|---|
| Elevação nacional | TOPODATA/INPE, GeoTIFF | cumeadas, horizonte e *viewshed* |
| Cartografia nacional | IBGE BC250, GeoPackage | cidades, vias, limites e hidrografia |
| MDE detalhado | IBGE 1:25.000/1:50.000 | refinamento onde houver cobertura |
| Altitudes de controle | IBGE BDG/RAAP | verificação vertical local |
| Ilhas oceânicas | IBGE, SGB e DHN | máscara e refinamento insular |

Arquivos originais volumosos pertencem a `data/raw/` e não devem ser
versionados. Metadados, URLs, hashes e licenças pertencem a
`data/manifests/` e devem ser versionados. Produtos intermediários ficam em
`data/processed/`; tabelas e mapas finais, em `outputs/`.

O inventário oficial atual contém 556 arquivos TOPODATA de altitude numérica,
com aproximadamente 32,19 GiB compactados. Por isso a seleção continental de
folhas deve preceder o download; baixar todo o índice sem máscara desperdiçaria
armazenamento e tempo de processamento.

As folhas selecionadas para as rotas candidatas são adquiridas separadamente,
com retomada por arquivo, validação integral do ZIP e recibo incremental:

```bash
python acquire_topodata_route_tiles.py \
  --selection reports/topodata_radio_link_tiles/selection.json \
  --output-dir data/raw/topodata/radio_link_routes \
  --report reports/topodata_radio_link_tiles/acquisition.json
```

O arquivo somente recebe o nome definitivo depois da validação de CRC e da
confirmação de que contém um GeoTIFF. Uma nova execução reutiliza arquivos já
válidos; falhas e folhas ainda pendentes permanecem explícitas no recibo.
Em 2026-08-11, o lote das rotas foi concluído com 154 arquivos, zero falhas e
9.743.140.443 bytes reais; os hashes individuais estão em
`reports/topodata_radio_link_tiles/acquisition.json`.

Os GeoTIFFs são extraídos sem GDAL externo e indexados espacialmente por Python:

```bash
python extract_topodata_route_tiles.py \
  --receipt reports/topodata_radio_link_tiles/acquisition.json \
  --archive-dir data/raw/topodata/radio_link_routes \
  --target-dir data/processed/topodata/radio_link_routes \
  --report reports/topodata_radio_link_tiles/extraction.json \
  --index reports/topodata_radio_link_tiles/index.geojson
```

O extrator compara cada ZIP com o SHA-256 do recibo, exige exatamente um
GeoTIFF georreferenciado, publica-o atomicamente e registra resolução, extensão,
tamanho e hash. O índice GeoJSON pode ser aberto diretamente no QGIS.

O recálculo TOPODATA preserva as mesmas equações e amostragem da triagem z8 e
publica as transições de classe por candidato:

```bash
python evaluate_anatel_radio_link_topodata.py \
  --geometry outputs/anatel_radio_link_geometry/groups.csv.gz \
  --keys outputs/anatel_radio_link_keys/records.csv.gz \
  --emissions outputs/anatel_radio_links/emissions.csv.gz \
  --terrain-root data/processed/topodata/radio_link_routes \
  --terrain-index reports/topodata_radio_link_tiles/index.geojson \
  --preliminary outputs/anatel_radio_link_terrain/groups.csv.gz \
  --output outputs/anatel_radio_link_topodata/groups.csv.gz \
  --report reports/anatel_radio_link_topodata/summary.json
```

Antes de usar as alturas no perfil definitivo, a auditoria as associa a cada
direção e frequência recíproca, mantendo também os códigos de produto:

```bash
python audit_anatel_radio_link_heights.py \
  --geometry outputs/anatel_radio_link_geometry/groups.csv.gz \
  --keys outputs/anatel_radio_link_keys/records.csv.gz \
  --emissions outputs/anatel_radio_links/emissions.csv.gz \
  --terrain outputs/anatel_radio_link_topodata/groups.csv.gz \
  --paths-output outputs/anatel_radio_link_heights/paths.csv.gz \
  --candidates-output outputs/anatel_radio_link_heights/candidates.csv.gz \
  --report reports/anatel_radio_link_heights/summary.json
```

Uma altura única em cada ponta é apenas não ambígua internamente no cadastro;
não equivale a medição física. Ausência ou múltiplas alturas para o mesmo caminho
permanecem bloqueios explícitos e nenhuma aresta é criada.

O perfil definitivo desta fase é então repetido por caminho não ambíguo:

```bash
python evaluate_anatel_radio_link_paths_topodata.py \
  --geometry outputs/anatel_radio_link_geometry/groups.csv.gz \
  --audited-paths outputs/anatel_radio_link_heights/paths.csv.gz \
  --terrain-root data/processed/topodata/radio_link_routes \
  --terrain-index reports/topodata_radio_link_tiles/index.geojson \
  --paths-output outputs/anatel_radio_link_path_terrain/paths.csv.gz \
  --candidates-output outputs/anatel_radio_link_path_terrain/candidates.csv.gz \
  --report reports/anatel_radio_link_path_terrain/summary.json
```

A consistência vertical confronta os ângulos de elevação cadastrados nas duas
pontas com a geometria esférica derivada do TOPODATA e das alturas:

```bash
python validate_anatel_radio_link_vertical_geometry.py \
  --paths outputs/anatel_radio_link_path_terrain/paths.csv.gz \
  --keys outputs/anatel_radio_link_keys/records.csv.gz \
  --emissions outputs/anatel_radio_links/emissions.csv.gz \
  --terrain-root data/processed/topodata/radio_link_routes \
  --terrain-index reports/topodata_radio_link_tiles/index.geojson \
  --output outputs/anatel_radio_link_vertical/paths.csv.gz \
  --report reports/anatel_radio_link_vertical/summary.json
```

Por fim, todos os gates são consolidados numa partição cadastral sem arestas:

```bash
python consolidate_anatel_radio_link_prequalification.py \
  --audited-paths outputs/anatel_radio_link_heights/paths.csv.gz \
  --terrain-paths outputs/anatel_radio_link_path_terrain/paths.csv.gz \
  --vertical-paths outputs/anatel_radio_link_vertical/paths.csv.gz \
  --keys outputs/anatel_radio_link_keys/records.csv.gz \
  --emissions outputs/anatel_radio_links/emissions.csv.gz \
  --output outputs/anatel_radio_link_prequalification/paths.csv.gz \
  --candidates-output outputs/anatel_radio_link_prequalification/candidates.csv.gz \
  --report reports/anatel_radio_link_prequalification/summary.json
```

O grafo resultante contém somente hipóteses cadastrais, nunca enlaces operacionais:

```bash
python build_anatel_radio_link_hypothesis_graph.py \
  --prequalification outputs/anatel_radio_link_prequalification/paths.csv.gz \
  --terrain outputs/anatel_radio_link_path_terrain/paths.csv.gz \
  --vertical outputs/anatel_radio_link_vertical/paths.csv.gz \
  --output outputs/anatel_radio_link_hypothesis_graph/graph.graphml \
  --report reports/anatel_radio_link_hypothesis_graph/summary.json
```

O enriquecimento liga cada ponta aos municípios canônicos e preserva conjuntos
de estações, entidades e códigos IBGE:

```bash
python enrich_anatel_radio_link_hypothesis_graph.py \
  --graphml outputs/anatel_radio_link_hypothesis_graph/graph.graphml \
  --prequalification outputs/anatel_radio_link_prequalification/paths.csv.gz \
  --keys outputs/anatel_radio_link_keys/records.csv.gz \
  --emissions outputs/anatel_radio_links/emissions.csv.gz \
  --municipality-graphml outputs/municipal_emitter_network/municipal_emitter_network.graphml \
  --output outputs/anatel_radio_link_hypothesis_graph/enriched.graphml \
  --report reports/anatel_radio_link_hypothesis_graph/enrichment.json
```

O grafo unificado compõe SMP, radiodifusão, candidatos e hipóteses RF:

```bash
python build_unified_geospatial_graph.py \
  --municipal outputs/municipal_emitter_network/municipal_emitter_network.graphml \
  --broadcast outputs/broadcast_network/broadcast_municipal_network.graphml \
  --candidates reports/candidate_graph/candidate_graph.graphml \
  --hypotheses outputs/anatel_radio_link_hypothesis_graph/enriched.graphml \
  --output outputs/unified_geospatial_graph/graph.graphml \
  --report reports/unified_geospatial_graph/summary.json
```

Como GraphML não mistura arestas dirigidas e não dirigidas no mesmo grafo, cada
visibilidade geométrica de candidato é armazenada como dois arcos com
`bidirectional_semantics=true`; isso não altera a contagem lógica nem remove o
marcador de terreno pendente.

O contexto municipal e a densidade geométrica de infraestrutura por candidato
são calculados sem criar arestas RF ou alegar visibilidade:

```bash
/usr/bin/python3 enrich_candidate_geospatial_context.py \
  --graphml outputs/unified_geospatial_graph/graph.graphml \
  --bc250 data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
  --output outputs/unified_candidate_context/graph.graphml \
  --table outputs/unified_candidate_context/candidates.csv.gz \
  --report reports/unified_candidate_context/summary.json
```

## Etapas

1. baixar e verificar as fontes registradas no manifesto;
2. reprojetar cada região para um sistema métrico apropriado;
3. gerar cumeadas, máximos locais e proeminência em múltiplas escalas;
4. calcular cobertura nas três altitudes de referência;
5. calcular cidades visíveis e sua distribuição azimutal;
6. construir o grafo de visada entre candidatos continentais;
7. resolver cobertura mínima com conectividade local obrigatória;
8. refinar candidatos com MDE de maior resolução e restrições territoriais;
9. exportar GeoPackage para QGIS e malhas locais para Blender.

O núcleo discreto já pode ser executado independentemente do QGIS:

```bash
/home/python/pyenv/bin/python optimize_sites.py instancia.json --output solucao.json
```

A instância contém células obrigatórias e candidatos com as células cobertas,
arestas de visada, condição de exceção insular e pontuação secundária. O modelo
MILP minimiza primeiro a quantidade de sítios e usa a pontuação apenas para
desempatar soluções com a mesma cardinalidade.

## Pré-seleção BC250

A triagem inicial pode ser reproduzida com o Python do sistema, que fornece os
bindings GDAL/OGR:

```bash
/usr/bin/python3 preselect_bc250.py \
  data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
  --output-dir reports/preselection_bc250
```

Essa etapa parte dos pontos cotados, agrega pontos separados por menos de 10 km
e calcula uma pontuação com 60% de altitude, 25% de quantidade de cidades em
250 km e 15% de ocupação de oito setores azimutais. “Cidade em 250 km” é apenas
um indicador logístico: somente o MDE permitirá substituir esse indicador por
cidades efetivamente visíveis.

## Grafo de capitais e aeroportos

```bash
/home/python/pyenv/bin/python build_candidate_graph.py \
  data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
  --terrain-cache data/raw/mapzen/terrarium \
  --output-dir reports/candidate_graph
```

O grafo usa as 27 capitais brasileiras e os 104 complexos aeroportuários da
BC250. O raio inicial alcança uma superfície aérea de 3.000 m e considera
curvatura com raio terrestre efetivo 4/3. Até o *viewshed* no TOPODATA, raios e
arestas são limites superiores geométricos, não visada confirmada.

## Critério de parada

Não se declarará “cobertura nacional” sem informar, para cada altitude de
referência, a fração coberta, as lacunas, a resolução do MDE e as hipóteses de
propagação. Se 100% não for alcançável, o resultado será uma curva entre número
de sítios e cobertura, em vez de ocultar a lacuna.
