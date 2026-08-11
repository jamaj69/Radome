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

Fontes:

- <https://dados.gov.br/dados/conjuntos-dados/outorga-e-licenciamento---estaes-licenciadas>
- <https://www.anatel.gov.br/dadosabertos/PDA/Estacoes_Licenciadas/Estacoes_Licenciadas_Glossario_e_Metadados.pdf>

## ANAC e DECEA

O cadastro da ANAC é a referência para aeródromos civis públicos e privados. O
AISWEB/DECEA é a fonte oficial de informação aeronáutica e oferece AIP, ROTAER e
geosserviços WFS/WMS. Esses dados devem validar coordenadas, elevação, operação
e uso militar quando a informação for pública.

Fontes:

- <https://dados.gov.br/dados/conjuntos-dados/aerodromos---lista-de-aerodromos-publicos-v2>
- <https://aisweb.decea.mil.br/?i=publicacoes&p=api>

## Ordem de integração

1. baixar e inventariar Estações SMP da Anatel;
2. agregar registros que representem a mesma instalação física;
3. adicionar ERBs ao GeoPackage como camada de iluminadores;
4. obter aeródromos atualizados da ANAC/DECEA;
5. reconciliar por código ICAO, nome e proximidade com a BC250;
6. classificar bases aéreas somente quando a fonte oficial permitir;
7. reconstruir o grafo mantendo origem, data e confiança de cada atributo.
