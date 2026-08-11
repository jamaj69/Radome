# Heurística de malha triangular cooperativa

## Origem e objetivo

Esta heurística registra a instrução do usuário de testar uma organização
alternativa à cobertura por discos independentes. O território continental é
representado por uma tesselação triangular cujos vértices são possíveis locais
de radomes. Cada face da malha deve favorecer observação cooperativa por três
radomes e concentração de iluminadores de oportunidade em seu interior.

Ela será comparada à otimização de cobertura mínima já existente. Não a
substitui antes da avaliação quantitativa e não altera o tratamento separado
dos arquipélagos e ilhas oceânicas.

## Construção proposta

1. Gerar vértices candidatos em terreno alto, cumeadas e máximos locais,
   acrescentando capitais, aeroportos e infraestrutura estratégica quando a
   fonte oficial permitir.
2. Remover locais inviáveis por restrições territoriais, fundiárias, ambientais
   ou de acesso, sem usar urbanização baixa como critério eliminatório.
3. Construir uma triangulação geodésica restrita, inicialmente por Delaunay em
   projeções métricas regionais, respeitando fronteira continental, vazios e
   descontinuidades territoriais.
4. Validar cada aresta por curvatura, perfil TOPODATA e, depois, zona de Fresnel
   por faixa. Distância ou vizinhança na triangulação não comprova visada.
5. Classificar as faces:
   - `triangle_k3_confirmed`: os três pares de vértices possuem visada confirmada;
   - `triangle_two_edge_degraded`: somente duas arestas são confirmadas;
   - `triangle_invalid`: menos de duas arestas, território fora da face útil ou
     outra restrição eliminatória.
6. Associar municípios, células territoriais, iluminadores e atributos de
   logística a cada triângulo por operações espaciais reproduzíveis.

Triângulos `K3` são preferidos porque os três radomes formam um subgrafo completo
e podem compartilhar observações. A categoria degradada permite estudar a
exigência do usuário de detecção por pelo menos dois radomes, mas não deve ser
confundida com equivalência técnica ao caso de três receptores.

## Iluminadores dentro dos triângulos

Cada face deve registrar, separadamente por classe e faixa:

- número de sítios SMP, emissoras/repetidoras e auxílios ou enlaces aeronáuticos;
- número de entidades, frequências, tecnologias e direções de emissão distintas;
- distribuição espacial e azimutal dos iluminadores dentro da face;
- distância de cada iluminador aos três vértices;
- estado cadastral, atividade conhecida, ERP/EIRP, altura, polarização e diagrama;
- disponibilidade temporal e compatibilidade com as faixas receptoras;
- geometria emissor--célula/alvo--radome e diversidade biestática/multiestática.

Um emissor cadastrado dentro do triângulo não demonstra eco detectável. O escore
inicial poderá usar densidade e diversidade apenas como proxies. A promoção a
`illuminates` exigirá modelo RF, terreno, orçamento de enlace e, posteriormente,
simulação ou medição.

## Objetivos e restrições a testar

A comparação deve usar objetivos lexicográficos ou uma formulação multiobjetivo
auditável, preservando cada componente:

1. minimizar área/células continentais fora da união das faces válidas;
2. minimizar o número total de vértices/radomes;
3. maximizar a fração territorial coberta por triângulos `K3`;
4. maximizar a área com recepção potencial por pelo menos dois vértices;
5. maximizar diversidade e qualidade preliminar de iluminadores dentro das faces;
6. favorecer altitude, proeminência, cidades ao redor, acesso e manutenção;
7. penalizar triângulos excessivamente alongados, arestas frágeis e concentração
   desnecessária de vértices numa mesma região.

Os pesos, quando usados, terão análise de sensibilidade. A cardinalidade mínima
continua prioritária, mas deverá ser publicada a curva entre número de radomes,
área coberta, redundância de recepção, quantidade de triângulos `K3` e qualidade
dos iluminadores.

## Métricas mínimas

- vértices, arestas e faces selecionados;
- distribuição de comprimentos de aresta e qualidade dos triângulos;
- faces `K3`, degradadas e inválidas;
- área e população dentro da malha, fora dela e com redundância 2/3;
- componentes conexos, articulações e vulnerabilidade à perda de um vértice;
- iluminadores únicos e incidências por face, classe e banda;
- fração das faces com iluminadores distribuídos, não apenas concentrados num
  único canto;
- comparação com a cobertura mínima por discos sob as mesmas fontes, MDE,
  resolução territorial e hipóteses de propagação.

## Experimentos previstos

1. **Concluído:** triangulação dos 131 candidatos atuais para estabelecer uma
   linha de base; 244 faces, sendo 22 `K3` por curvatura ainda pendentes de
   terreno, 6 degradadas e 216 esparsas.
2. Inclusão dos novos candidatos altos gerados nas 1.732 células atualmente
   descobertas.
3. Triangulação Delaunay não restrita versus triangulação restrita por visada.
4. Otimização estrita `K3` versus solução que admite faces degradadas.
5. Sensibilidade a MDE, `k`, altura-alvo, resolução da grade e pesos de
   iluminadores/logística.
6. Teste de robustez removendo um vértice por vez.
7. Comparação final com o modelo de cobertura mínima por discos.

## Estado

Heurística registrada em 2026-08-11. A linha de base Delaunay foi implementada
em `analyze_triangular_mesh_baseline.py`; validação de terreno, otimização e os
demais experimentos permanecem pendentes. Nenhum resultado operacional ou
número de radomes decorre ainda desta formulação.
