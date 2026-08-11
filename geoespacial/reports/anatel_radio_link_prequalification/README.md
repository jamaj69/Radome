# Pré-qualificação cadastral dos radioenlaces

Este produto consolida, por caminho dirigido e frequência, todos os gates já
calculados:

1. reciprocidade espectral;
2. azimute nas duas pontas, com limiar provisório de 15°;
3. uma altura cadastral por ponta;
4. 60% da primeira zona de Fresnel livre no TOPODATA;
5. geometria vertical nas duas pontas, com limiar provisório de 1°.

| Resultado | `k=1` | `k=4/3` |
|---|---:|---:|
| caminhos pré-qualificados | 764 | 796 |
| caminhos bloqueados | 229 | 197 |
| candidatos com ao menos um caminho pré-qualificado | 240 | 250 |
| candidatos sem caminho pré-qualificado | 88 | 78 |

No gate horizontal, 977 caminhos são consistentes a 15°, 12 possuem azimute
ambíguo e quatro são inconsistentes. Os bloqueadores permanecem concatenados
em cada linha, permitindo distinguir ausência, ambiguidade, obstrução e erro
angular sem perda de informação.

“Pré-qualificado” significa somente que os registros oficiais são mutuamente
compatíveis sob as hipóteses publicadas. Não confirma localização física,
instalação, operação atual, calibração, datum de altura nem desempenho medido.
Todos os registros preservam `pairing_status=not_performed` e não constituem
arestas operacionais.

Duas execuções consecutivas produziram os mesmos SHA-256:

- caminhos: `3ce9ec53519aceb9e6762a6dd2ed0fac8135a4f032d58bd6bdc56fdb076dab8b`;
- candidatos: `6b6dac10a8ab6399684b2a37bcb7721d71fd9f3026c7f2fd45d80b4341c5247b`;
- resumo: `874b7885018832a6ce718e22b4a3054dc0ab48c3f94b1b57fc2d6e0198f54fd1`.
