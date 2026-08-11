# Grafo geoespacial unificado

O produto compõe quatro GraphMLs reproduzíveis em um `MultiDiGraph`:

- municípios e sítios SMP;
- municípios e radiodifusão;
- capitais/aeroportos candidatos;
- endpoints e hipóteses cadastrais de radioenlace.

| Tipo de nó | Quantidade |
|---|---:|
| município | 5.571 |
| torre/sítio SMP | 105.726 |
| sítio de radiodifusão | 11.921 |
| endpoint cadastral de radioenlace | 497 |
| aeroporto candidato | 104 |
| capital candidata | 27 |
| **total** | **123.846** |

| Relação/hipótese | Registros |
|---|---:|
| `located_in` | 117.647 |
| `located_in_cadastral` | 497 |
| hipótese de radioenlace | 796 |
| visibilidade geométrica preliminar | 218 arcos / 109 relações lógicas |
| **total** | **119.158** |

GraphML não admite mistura de arestas dirigidas e não dirigidas no mesmo grafo.
Por isso cada uma das 109 visibilidades preliminares de candidatos é representada
por dois arcos com `bidirectional_semantics=true`, `terrain_confirmation=false`
e `operational_edge=false`. As 796 hipóteses RF preservam seus próprios marcadores
de ausência de verificação física. Nenhuma colisão de atributos foi encontrada.

O grafo foi recarregado integralmente, confirmando cardinalidades e zero arestas
operacionais. Duas gerações consecutivas produziram:

- GraphML: `ee3d62afade09010dd011ffab01f86288ab44d8d2f7665c67dacacd4ba39d80f`;
- resumo: `935e7c1e573d10cd6f1b70d58123cfe2aac3b665074855dd0c9b2d82ad81db95`.
