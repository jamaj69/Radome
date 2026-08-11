# Grafo preliminar de capitais e aeroportos

O grafo contém 131 possíveis candidatos continentais: 27 capitais brasileiras
e 104 complexos aeroportuários da BC250. Há 109 arestas candidatas pela
curvatura terrestre, 68 componentes conexos e 39 nós isolados.

Cada nó registra nome, tipo, coordenadas, altitude amostrada, raio de cobertura,
quantidade de cidades dentro do raio e grau no grafo. O tamanho desenhado do nó
é proporcional ao raio. Laranja identifica capitais; azul, aeroportos.

O raio é calculado para um radome com centro de fase 15 m acima do terreno e
uma superfície aérea a 3.000 m, usando raio terrestre efetivo de 4/3. A cota
local vem de Mapzen Terrain Tiles em zoom 8. Este raio é um **limite superior
geométrico**: curvatura é considerada, mas serras intermediárias ainda não.

## Primeiros resultados

| Candidato | Tipo | Cota (m) | Raio (km) | Cidades | Grau |
|---|---|---:|---:|---:|---:|
| Aeroporto Embaixador Walther Moreira Salles | aeroporto | 1.254 | 372,6 | 907 | 7 |
| Belo Horizonte | capital | 855 | 347,4 | 773 | 4 |
| Aeroporto Leite Lopes | aeroporto | 554 | 324,1 | 753 | 2 |
| Aeroporto Pampulha | aeroporto | 788 | 342,6 | 749 | 3 |
| Aeroporto Federal Antônio Correia Pinto de Macedo | aeroporto | 930 | 352,5 | 742 | 2 |
| Aeroporto Internacional Tancredo Neves | aeroporto | 830 | 345,6 | 733 | 3 |
| Aeroporto Internacional de Viracopos | aeroporto | 662 | 333,0 | 682 | 6 |

Entre as capitais, Belo Horizonte, São Paulo e Curitiba têm as maiores
contagens de cidades. Goiânia possui grau 7; Brasília e São Paulo, grau 6.
Esses valores favorecem regiões densas e não eliminam candidatos amazônicos ou
fronteiriços.

Uma aresta significa apenas que a distância entre os nós é menor que a soma dos
horizontes geométricos locais. O refinamento TOPODATA deverá remover arestas
bloqueadas e substituir círculos por polígonos de *viewshed*.

Arquivos: `candidate_graph.graphml` para Gephi/NetworkX, pontos QGIS em
`candidate_nodes.geojson`, tabela em `candidate_nodes.csv`, visualização em
`candidate_graph.png` e auditoria em `summary.json`.

Comandos aéreos ainda não estão incluídos: a BC250 não oferece uma camada
nominal correspondente. Eles serão adicionados quando uma fonte oficial e
publicável for registrada no manifesto.
