# Fontes de infraestrutura para o grafo de candidatos

Levantamento realizado para localizar torres celulares, aeroportos, bases aéreas
e instalações relacionadas. A regra é preferir a fonte oficial responsável pelo
cadastro setorial e usar o IBGE como base cartográfica de integração.

## Resultado por tema

| Tema | IBGE | Fonte autoritativa complementar | Decisão |
|---|---|---|---|
| Capitais e cidades | BC250 2025 | — | usar IBGE |
| Aeroportos | BC250 2025, subsistema AER | ANAC e AISWEB/DECEA | usar IBGE na triagem e validar no cadastro setorial |
| Pistas e pontos de pouso | BC250 2025 | ANAC e AISWEB/DECEA | incorporar apenas os subconjuntos necessários |
| Torres/ERBs celulares | não há camada na BC250 2025 | Anatel, Estações SMP licenciadas | usar Anatel |
| Radioenlaces celulares | não há camada na BC250 2025 | Anatel, radioenlaces SMP | usar Anatel |
| TV, RTV, FM, OM e RTR | não há cadastro setorial completo | Anatel, estações de radiodifusão | baixado e integrado por município |
| Bases/aeródromos militares | aparecem parcialmente como aeroportos, sem classificação confiável | AISWEB/DECEA e AIP/ROTAER | validar e classificar pelo DECEA |
| Comandos aéreos | não há camada nominal | fonte pública oficial da FAB/DECEA, se disponível | manter pendente |

## IBGE BC250 2025

O GeoPackage já verificado contém:

- `aer_complexo_aeroportuario_p`: 104 pontos;
- `aer_pista_ponto_pouso_p`: 3.492 pontos;
- `aer_pista_ponto_pouso_l`: 2.830 linhas;
- `lml_capital_p`: 27 capitais brasileiras após filtro por geocódigo;
- `lml_cidade_p`: cidades usadas na contagem de cobertura.

O manual da base informa que o subsistema aeroportuário usa listas oficiais da
ANAC e dados da INFRAERO como insumos. Contudo, na edição baixada, a maioria dos
atributos de jurisdição, administração, classificação e altitude dos complexos
aeroportuários está vazia ou desconhecida. Nomes como Aeroporto Anápolis e
Aeroporto Santa Maria aparecem, mas isso não é suficiente para classificá-los
automaticamente como bases aéreas.

Fonte: <https://www.ibge.gov.br/geociencias/cartas-e-mapas/bases-cartograficas-continuas/15759-brasil.html>

## Comunicação nas bases históricas do IBGE

A BC250 2015 possuía o pacote `Energia_Comunicacao_v2015.zip`. A inspeção do
arquivo oficial mostrou somente `ENC_Trecho_Comunic_L`, isto é, linhas de
comunicação. Não há camada pontual de torre ou estação celular. O pacote é
antigo e não será usado como cadastro de ERBs.

Fonte: <https://geoftp.ibge.gov.br/cartas_e_mapas/bases_cartograficas_continuas/bc250/versao2015/Shapefile/>

## Anatel

O conjunto “Outorga e Licenciamento — Estações Licenciadas” contém um recurso
específico para Estações do Serviço Móvel Pessoal (SMP), com informações
técnicas e localizações. É a fonte adequada para ERBs e deve ser baixada em CSV,
normalizada por local físico e integrada ao grafo como:

- possível iluminador celular;
- indicador de cobertura e logística de telecomunicações;
- não como candidato automático a radome.

Estações repetidas por frequência, tecnologia ou operadora no mesmo local
devem ser agregadas sem perder os atributos originais.

Em 10 de agosto de 2026 foi também baixado o pacote geral
`estacoes_licenciadas.zip`: 223.059.863 bytes compactados, SHA-256
`b77abb225b4ad03bc8b8c6a27913e0b6d851873bab3bd483e66d86712dd5eec1` e
10.451.254.153 bytes descompactados. Seus 13 arquivos incluem STEL, SLP,
radioamador, SLE e outros serviços, mas **não** incluem um arquivo SMP dedicado.
O pacote geral não deve ser confundido com o recurso separado “Estações do
Serviço Móvel Pessoal - SMP”, que o catálogo informa ter sido atualizado em
21/07/2026. O URL foi recuperado do recurso carregado pelo próprio catálogo e o
ZIP dedicado foi baixado e verificado. Ele contém 3.284.526 registros
licenciados, 112.934 números de estação e 105.726 coordenadas distintas após
arredondamento a cinco casas decimais. A última contagem é uma aproximação de
sítios físicos, não ainda uma contagem definitiva de torres: setores,
frequências, tecnologias e operadoras co-localizadas precisam ser consolidados.

Fontes:

- <https://dados.gov.br/dados/conjuntos-dados/outorga-e-licenciamento---estaes-licenciadas>
- <https://www.anatel.gov.br/dadosabertos/PDA/Estacoes_Licenciadas/Estacoes_Licenciadas_Glossario_e_Metadados.pdf>

## ANAC e DECEA

O cadastro da ANAC é a referência para aeródromos civis públicos e privados. O
AISWEB/DECEA é a fonte oficial de informação aeronáutica e oferece AIP, ROTAER e
geosserviços WFS/WMS. Esses dados devem validar coordenadas, elevação, operação
e uso militar quando a informação for pública.

Os quatro CSV atuais da ANAC foram baixados e verificados. Após remover a linha
de preâmbulo e o cabeçalho, eles contêm 496 aeródromos públicos, 3.856
aeródromos privados, 1.595 helipontos e 203 helideques. A separação deve ser
mantida: helideques não têm coordenadas no arquivo atual e não são candidatos
continentais equivalentes a aeródromos.

O `GetCapabilities` do WFS do GEOAISWEB expõe 421 tipos de feição. A triagem
selecionou 14 camadas diretamente úteis: aeródromos, helipontos, pistas,
cabeceiras, obstáculos OPEA, VOR, NDB, DME, auxílios de navegação, CTR, TMA, ZIDA e
as visões AIXM correlatas. A camada `ICA:zida`, intitulada “Zona de
Identificação de Defesa Aérea (ZIDA 80nm)”, é contexto de defesa aérea, não uma
lista de bases ou comandos.

VOR, NDB, DME e a visão agregada `navaids` já foram baixados e auditados. As
quatro camadas têm coordenadas completas; elevação está presente em 76/77 VOR,
19/24 NDB, 158/173 DME e 30/124 feições agregadas. VOR e NDB têm frequência;
DME tem canal, enquanto sua portadora exige a tabela oficial de pareamento.

Fontes:

- <https://dados.gov.br/dados/conjuntos-dados/aerodromos---lista-de-aerodromos-publicos-v2>
- <https://aisweb.decea.mil.br/?i=publicacoes&p=api>

## Ordem de integração

1. definir o esquema canônico sítio--antena--emissão;
2. incorporar ao grafo as portadoras SMP já auditadas;
3. classificar o pacote geral Anatel por serviço, classe, direção e situação,
   começando pelos arquivos menores antes de SLP/STEL;
4. parear radioenlaces e reconciliar co-localizações sem perder antenas e
   emissões múltiplas;
5. normalizar radiodifusão e VOR/NDB/DME e associá-los aos municípios;
6. concluir a aquisição DECEA e reconciliar por ICAO, CIAD, nome e proximidade
   com ANAC e BC250;
7. classificar bases e radares somente quando fonte oficial permitir;
8. reconstruir o grafo mantendo origem, data e confiança de cada atributo.

O inventário reproduzível está em
`data/manifests/infrastructure_inventory.json` e é regenerado por
`inventory_infrastructure.py`. Arquivos brutos continuam fora do Git.

## Radiodifusão

O recurso `estacoes_radiodifusao.zip` da Anatel foi baixado e verificado. Seus
35.126 registros incluem TV, televisão digital e retransmissoras, FM,
retransmissoras de FM e ondas médias. Todos possuem coordenadas válidas, mas o
cadastro mistura estados regulatórios diferentes. O grafo de iluminadores usa
somente 18.285 registros `C4 — Canal Licenciado`, agregados em 11.921 sítios.

Os 11.647 canais vagos e os canais pendentes, suspensos ou aguardando
licenciamento não são fontes ativas. Essa separação deve permanecer explícita
no artigo e nos scripts. Todos os sítios licenciados receberam código IBGE; 117
coordenadas com códigos conflitantes foram marcadas para revisão.
