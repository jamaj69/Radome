# TOPODATA por caminho cadastral de radioenlace

Este gate substitui o antigo limite otimista — menor frequência recíproca e
maior altura de cada estação — pelo trio exato frequência--altura de origem--
altura de destino de cada caminho cadastral não ambíguo.

Foram avaliados 971 caminhos em 325 candidatos; 22 caminhos com altura ausente
ou ambígua foram excluídos de forma explícita.

| Classe por caminho | `k=1` | `k=4/3` |
|---|---:|---:|
| Fresnel 60% livre | 780 | 812 |
| somente visada | 114 | 86 |
| obstruído | 69 | 65 |
| terreno ausente | 8 | 8 |

| Melhor classe por candidato | `k=1` | `k=4/3` |
|---|---:|---:|
| ao menos um caminho Fresnel 60% livre | 246 | 256 |
| ao menos um caminho somente com visada | 57 | 48 |
| todos os caminhos avaliáveis obstruídos | 21 | 20 |
| terreno ausente em todos os caminhos | 1 | 1 |

O candidato é agregado pela existência de um caminho compatível, mas continua
com `pairing_status=not_performed`. A altura é cadastral e ainda precisa ser
comparada à geometria vertical/ângulo de elevação e confirmada fisicamente.

Duas execuções consecutivas produziram os mesmos SHA-256:

- caminhos: `8fd9341548c6b482c7155cba98e884a98a6008421a4deb4a0157c7c052b3596d`;
- candidatos: `e688642c655334c9cd8f2bec69d60ce4b5aa42581e7452fe6d2fd46564871595`;
- resumo: `8123c8c33f1b3eb085bfcba0b3b5781f28e4494b0a8e16a74d7f923b324c6f43`.
