# Consistência da geometria vertical dos radioenlaces

Os 971 caminhos com alturas cadastrais não ambíguas foram confrontados com os
ângulos de elevação cadastrados nas duas pontas. O ângulo esperado usa uma Terra
esférica efetiva e as altitudes de topo obtidas por cota TOPODATA mais altura
cadastral da antena.

Oito caminhos não puderam ser avaliados por falta de terreno. Nos 963 restantes:

| Erro máximo nas duas pontas | caminhos consistentes `k=1` | candidatos com caminho consistente | caminhos consistentes `k=4/3` | candidatos com caminho consistente |
|---:|---:|---:|---:|---:|
| 0,5° | 860 | 286 | 884 | 292 |
| 1,0° | 933 | 311 | 933 | 311 |
| 2,0° | 941 | 315 | 943 | 316 |
| 5,0° | 955 | 322 | 957 | 323 |

O limiar de 1° é provisório e serve à triagem, não à certificação física. A
concordância cadastral não confirma a instalação atual, a referência vertical,
a calibração mecânica ou o estado do equipamento. `pairing_status` permanece
`not_performed`.

Duas execuções consecutivas produziram os mesmos SHA-256:

- caminhos: `1742c7c287e2f040530be083f1366996d9eda34344e5f6349376f22c6f75a068`;
- resumo: `e190344cfa6727d58e9ff8dc4f83b99d366a9ce1c8f2c3695997b6a6a7cf16c9`.
