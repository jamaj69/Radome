# Metodologia reproduzível para seleção geoespacial de sítios

Este documento é a fonte intermediária para a futura seção metodológica do
artigo RADOME. Nenhum resultado exploratório deve ser transcrito para o artigo
sem manter a ligação com o script, a configuração e o artefato que o produziu.

## Objetivo

Selecionar o menor conjunto de sítios continentais capaz de satisfazer metas
de cobertura aérea, favorecendo grandes altitudes e proeminência, cidades
visíveis ao redor do sítio e conectividade visual entre radomes. Arquipélagos e
ilhas oceânicas estão fora desta otimização e terão estudos locais separados.

## Fontes e proveniência

As fontes, URLs, tamanhos, hashes e estados de aquisição estão em
`data/manifests/sources.json`. A lista de folhas TOPODATA está congelada em
`data/manifests/topodata_altitude_tiles.json`.

- IBGE BC250 2025: capitais, aeroportos, cidades, vias, energia, limites e
  pontos de relevo;
- TOPODATA/INPE: MDE e refinamento de cumeadas, perfis e *viewsheds*;
- Mapzen Terrain Tiles: somente cotas preliminares dos nós antes do TOPODATA;
- IBGE BDG/RAAP: futura verificação vertical dos finalistas.

Dados brutos ficam em `data/raw/`, são ignorados pelo Git e podem ser
reconstituídos pelos manifestos. Resultados usados no texto devem permanecer em
`reports/` e ser versionados.

## Hipóteses controladas

Os parâmetros numéricos autoritativos estão em `site_selection.json`. A
configuração inicial usa superfícies a 150 m, 3.000 m e 10.000 m acima do
terreno, centro de fase 15 m acima do sítio e fator de raio terrestre efetivo
`k = 4/3`.

O horizonte geométrico de uma altura `h` é aproximado por:

```text
d(h) = sqrt(2 k R h + h²)
```

Para um sítio e uma superfície-alvo, o raio preliminar é:

```text
r = d(h_sítio + h_radome) + d(h_alvo)
```

Essa expressão considera curvatura e refração padrão, mas não bloqueio por
relevo. Por isso todo raio produzido antes do *viewshed* recebe o estado
`geometric_upper_bound_topographic_occlusion_pending`.

## Construção dos candidatos

1. A triagem BC250 lê 127 pontos cotados.
2. Pontos separados por menos de 10 km são agregados, preservando a maior cota.
3. A pontuação exploratória usa 60% de altitude, 25% de quantidade de cidades
   em 250 km e 15% de ocupação de oito setores azimutais.
4. Capitais brasileiras e complexos aeroportuários são adicionados como nós de
   infraestrutura, sem substituir os candidatos de cumeada.
5. Comandos aéreos só serão adicionados após registro de fonte oficial.

Proximidade de cidade é um indicador logístico. No refinamento, a contagem deve
ser substituída por cidades contidas no polígono de visibilidade calculado.

## Grafo

Cada nó armazena:

- identificador estável, nome, tipo e coordenadas;
- cota e fonte da cota;
- altura do radome e altitude-alvo;
- raio ou polígono de cobertura;
- número de cidades cobertas;
- grau, componente conexo e estado de validação.

Uma aresta preliminar existe quando a distância geodésica entre dois sítios é
menor ou igual à soma de seus horizontes geométricos terrestres. A aresta é
marcada `curvature_only_terrain_pending`. O perfil TOPODATA deverá confirmar ou
remover a aresta, considerando relevo e posteriormente a zona de Fresnel da
faixa analisada.

## Otimização

`optimize_sites.py` resolve um problema binário de cobertura mínima. Cada célula
obrigatória deve ser coberta por ao menos um sítio. Cada sítio continental
selecionado deve possuir ao menos um vizinho selecionado com visada confirmada.
O número de sítios é o objetivo primário; a pontuação técnica apenas desempata
soluções de mesma cardinalidade.

O artigo deve publicar, para cada altitude-alvo:

- número de sítios;
- fração territorial coberta;
- lacunas e sua área;
- quantidade de cidades cobertas;
- componentes e nós isolados;
- resolução e versão do MDE;
- hipóteses de propagação e data da execução.

## Sequência reproduzível atual

```bash
/home/python/pyenv/bin/python -m unittest discover -s tests -v
/usr/bin/python3 preselect_bc250.py \
  data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
  --output-dir reports/preselection_bc250
/home/python/pyenv/bin/python build_candidate_graph.py \
  data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
  --terrain-cache data/raw/mapzen/terrarium \
  --output-dir reports/candidate_graph
```

O comando agregado equivalente é `run_pipeline.sh`.

## Regras para incorporação no artigo

- não chamar raio geométrico de cobertura confirmada;
- não afirmar visada a partir de uma aresta preliminar;
- não confundir cidades próximas com cidades visíveis;
- não usar o grafo de infraestrutura para eliminar regiões pouco urbanizadas;
- citar a versão do manifesto, o commit Git e os parâmetros da execução;
- regenerar os resultados após qualquer mudança de fonte ou configuração;
- incorporar metodologia e resultados nas duas árvores linguísticas do artigo.

## Camada municipal e integração de emissores

O município é representado como um tipo próprio de nó, identificado pelo código
IBGE de sete dígitos. Não existe uma única tabela oficial que reúna todos os
atributos necessários; a camada canônica é uma composição rastreável:

- limite, área e coordenadas da sede municipal: BC250/IBGE;
- população residente: Censo Demográfico 2022, variável 93 da API de Agregados;
- altitude da sede: amostra do modelo de elevação na coordenada da sede;
- emissores e instalações: cadastros setoriais da Anatel, ANAC e DECEA.

Para o nó municipal, `x` é a longitude da sede, `y` é a latitude da sede e `z`
é a altitude do terreno na sede. Longitude e latitude usam SIRGAS 2000
(EPSG:4674); a altitude deve registrar fonte, resolução e referência vertical.
Enquanto o TOPODATA não estiver integrado, a amostra Terrarium é explicitamente
preliminar e não pode fundamentar uma decisão final de sítio.

O tamanho visual do nó municipal é proporcional à área territorial em
quilômetros quadrados. A população permanece como atributo independente para
permitir uma visualização alternativa por população e para ponderar logística,
manutenção e quantidade potencial de iluminadores. Área e população não devem
ser combinadas implicitamente em um único indicador.

Torres e demais objetos recebem `ibge_code` e são ligados ao município por uma
aresta `located_in`. Quando o cadastro setorial contém o código apenas em parte
dos registros, ele é propagado entre setores, frequências e tecnologias que
compartilham a mesma instalação. Ausências e conflitos são resolvidos por
junção espacial com a malha municipal, mantendo uma marca de revisão.

Uma linha do cadastro SMP não equivale a uma torre. O mesmo sítio pode aparecer
repetidamente por estação, setor, frequência, geração e operadora. A camada de
sítios físicos agrega coordenadas próximas e preserva conjuntos de estações,
operadoras, tecnologias e faixas. O limiar espacial e os casos conflitantes
devem ser informados junto com qualquer contagem de “torres”.

O grafo municipal-emissor serve para analisar disponibilidade geométrica de
iluminadores celulares, rádio e televisão, bem como infraestrutura
aeronáutica. A presença de um emissor não demonstra que seu sinal produz eco
detectável no radome: frequência, potência irradiada, diagrama, polarização,
ocupação temporal, perdas, geometria biestática, RCS e ruído pertencem à etapa
radioelétrica posterior.

Para radiodifusão, o universo cadastral é separado do conjunto de iluminadores
ativos. Apenas `C4 — Canal Licenciado` entra no grafo operacional preliminar.
O cadastro fornece serviço, canal e frequência central, mas não a designação ou
largura necessária de emissão. Esses limites espectrais só serão adicionados
após integração de canalização regulatória versionada por serviço.

No SMP, cada registro preserva `Geração`, `Tecnologia`, tipo 5G, faixa/subfaixa,
`FreqTxMHz`, `FreqRxMHz` e `Designação Emissão`. A largura necessária é
decodificada do prefixo da designação ITU e o intervalo preliminar transmitido é
o centro Tx mais ou menos metade dessa largura. `FreqRxMHz` não é tratado como
emissão da ERB, e o cálculo não substitui a máscara espectral regulamentar.
Canais vagos, suspensos, pendentes ou aguardando outorga, dados, ato de RF ou
licenciamento permanecem no inventário. Registros licenciados co-localizados
são agregados por coordenada, preservando serviço, canal, frequência, entidade,
classe, categoria, finalidade e ERP.
