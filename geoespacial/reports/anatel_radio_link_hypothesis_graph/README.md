# Grafo de hipóteses cadastrais de radioenlace

O GraphML é um multigrafo dirigido: cada coordenada cadastral é um nó e cada
frequência pré-qualificada é uma aresta própria. Frequências paralelas entre o
mesmo par de coordenadas não são colapsadas.

| Métrica | União | `k=1` | `k=4/3` |
|---|---:|---:|---:|
| nós | 497 | 477 | 497 |
| arestas de hipótese | 796 | 764 | 796 |
| candidatos | 250 | 240 | 250 |
| componentes | — | 237 | 247 |
| maior componente, em nós | — | 3 | 3 |

O grafo contém 135 frequências distintas. A pequena diferença entre número de
pares e componentes decorre de poucas coordenadas compartilhadas; a maioria dos
candidatos forma um componente próprio de duas pontas.

Todas as arestas carregam frequência, alturas, distância, folgas de Fresnel,
erros horizontal/vertical e aprovação por modelo de Terra. Todos os nós e
arestas declaram `physical_verification=false` e `pairing_status=not_performed`;
cada aresta também declara `operational_edge=false` e
`edge_type=cadastral_prequalified_hypothesis`.

O GraphML foi recarregado pelo NetworkX, preservando 497 nós, 796 arestas e os
marcadores de segurança. Duas gerações consecutivas produziram:

- GraphML: `d984ee5119369fbbfb00af663d41ff4743adb02ea8fb2e0523b6482c718278f7`;
- resumo: `3ee67beef2347e5524c4f05a673bacf5584f45fe98aaa610925b004919c54a27`.

## Enriquecimento municipal

O grafo enriquecido acrescenta somente os municípios referenciados, em vez de
copiar os 5.571 municípios e 105.726 sítios SMP do grafo canônico completo:

- 497 pontas com contexto cadastral completo;
- 365 municípios canônicos referenciados;
- 497 vínculos `located_in_cadastral`;
- nenhum código municipal ausente ou conflitante;
- 494 pontas ligadas a uma estação e três a duas estações;
- 496 pontas ligadas a uma entidade e uma a duas entidades.

O produto contém 862 nós e 1.293 arestas: 796 hipóteses de radioenlace e 497
vínculos administrativos. Continua com zero arestas operacionais. Duas gerações
consecutivas produziram:

- GraphML enriquecido: `82d68f59ef015ee4d3cfc97ebca2b736463e7fd0e019a1ff3c3eca67b6621319`;
- recibo: `ab357a57451203b968e3e3e262b73db95082a413d38d6b5f1b4132afbda5a750`.
