# Contexto municipal e RF dos candidatos

O gate associa por contenção espacial na camada `lml_municipio_a` da BC250
cada um dos 131 candidatos do grafo unificado e contabiliza três classes de
infraestrutura dentro do respectivo `coverage_radius_km`:

- sítios SMP;
- sítios licenciados de radiodifusão;
- endpoints cadastrais presentes nas hipóteses de radioenlace.

Todos os 131 candidatos tiveram correspondência municipal. Foram acrescentadas
131 arestas administrativas `located_in`, sem criar arestas operacionais. As
contagens acumuladas sobre todos os candidatos são 790.026 incidências SMP,
80.682 de radiodifusão e 3.623 de endpoints. Essas somas **não são contagens de
objetos únicos**: um mesmo objeto pode estar no raio de vários candidatos.

O raio é um limite geométrico preliminar de curvatura. Distância dentro dele não
comprova visada de terreno, disponibilidade do transmissor, potência recebida ou
iluminação útil. O produto serve para priorização e precisa de *viewshed*, perfil
de terreno e orçamento RF antes de sustentar qualquer afirmação operacional.

Execução reproduzível, a partir de `geoespacial/`:

```bash
/usr/bin/python3 enrich_candidate_geospatial_context.py \
  --graphml outputs/unified_geospatial_graph/graph.graphml \
  --bc250 data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
  --output outputs/unified_candidate_context/graph.graphml \
  --table outputs/unified_candidate_context/candidates.csv.gz \
  --report reports/unified_candidate_context/summary.json
```

Duas execuções consecutivas produziram o mesmo SHA-256 para o GraphML e para a
tabela gzip; os hashes estão em `summary.json`.
