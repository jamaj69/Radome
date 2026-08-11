# Auditoria cadastral de alturas dos radioenlaces

A auditoria associa altura, direção, frequência recíproca e código de produto
da antena antes de qualquer pareamento. Isso evita tratar várias antenas de uma
mesma estação como um único campo contraditório.

Foram encontrados 993 caminhos dirigidos por frequência:

| Estado da altura por caminho | Quantidade |
|---|---:|
| uma altura cadastral em cada ponta | 971 |
| múltiplas alturas em pelo menos uma ponta | 12 |
| altura ausente em pelo menos uma ponta | 10 |

Dos 328 candidatos, 325 têm pelo menos um caminho com alturas cadastrais não
ambíguas, um possui somente caminhos ambíguos e dois possuem somente caminhos
com altura ausente. Entre os 325 utilizáveis cadastralmente, a classificação
TOPODATA `k=1` é 245 com 60% de Fresnel livre, 58 somente com visada, 21
obstruídos e um sem terreno.

“Não ambígua” significa apenas que o cadastro fornece um único valor na
combinação ponta--direção--frequência. Não demonstra a altura física instalada,
o datum vertical, a referência da medição ou a correspondência atual em campo.
Por isso nenhum candidato recebeu `pairing_status` diferente de `not_performed`.

Duas execuções consecutivas produziram os mesmos hashes:

- caminhos: `a3259963a48d2bef7c489806f95c18de0963eb64b9859fce7d0aaec479c5636a`;
- candidatos: `6749a7b0c22f47988b5c70b62d7e7fa901ccf100dba743916a6f69990721b139`;
- resumo: `046617b3b677a929ee2000e11eabd48bc5a8a302ffafa8a56f47e59eab396c74`.
