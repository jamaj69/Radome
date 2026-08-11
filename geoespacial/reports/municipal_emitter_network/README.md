# Rede municipal e emissores SMP

A execução inicial gerou 5.571 nós `municipio`, 105.726 nós agregados
`torre_smp` e 105.726 arestas `located_in`. Todos os sítios SMP receberam um
código municipal; 23 coordenadas continham mais de um código nos registros de
origem e foram associadas ao código modal, mantendo a marca de conflito.

O Censo 2022 fornece população para 5.570 municípios. Boa Esperança do Norte
(MT, código 5101837), instalada depois do Censo, aparece na BC250 atual e fica
com população desconhecida, não zero. Qualquer população atribuída a esse novo
município exigirá uma fonte e um ano posteriores explicitamente registrados.

As coordenadas `x` e `y` são longitude e latitude da sede municipal em SIRGAS
2000. A coordenada `z` é uma amostra preliminar do terreno na sede usando
Terrarium, devendo ser substituída pelo TOPODATA. O tamanho visual é a área
calculada da geometria BC250; a população é mantida separadamente.

Os produtos completos permanecem em `outputs/` por terem aproximadamente 64 MB
no total. Este relatório, os scripts, os hashes das fontes e os testes são os
artefatos versionados necessários para reproduzi-los.
