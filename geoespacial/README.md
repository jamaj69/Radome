# Seleção geoespacial de sítios RADOME

Este diretório é o subprojeto geoespacial do artigo técnico bilíngue RADOME e
contém o fluxo reproduzível para selecionar o menor conjunto de
sítios que satisfaça uma meta explícita de cobertura do espaço aéreo brasileiro.
O resultado é uma triagem de engenharia, não uma autorização de implantação.

A vinculação, os entregáveis e o gate para incorporar resultados às edições em
português e inglês estão definidos em `SUBPROJETO.md`. O marco ativo é a Fase 3:
infraestrutura aeronáutica e estratégica.

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
