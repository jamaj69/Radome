# Cobertura e resiliência da malha TOPODATA

Os discos geométricos incidem em 11.363/11.363 centros, mas as faces `K3` com
LOS TOPODATA contêm somente 1.149 centros em `k=1` (10,11%) e 1.299 em `k=4/3`
(11,43%). A pertença usa a atribuição exclusiva de cada centro à sua face
Delaunay; não é cobertura RF.

O grafo LOS `k=1` tem 3.653 arestas, 129 componentes, maior componente com
1.174 dos 1.615 vértices, 97 isolados e 47 vértices de articulação. Em `k=4/3`,
são 3.849 arestas, 122 componentes, maior componente com 1.325 vértices, 96
isolados e 23 articulações.

`vertex_sensitivity.csv.gz` registra grau, articulação e quantas células/área
de faces `K3` deixam de ser qualificadas quando cada vértice falha. Essa perda
é topológica e territorial; não estima disponibilidade operacional.

O script falha se o número de candidatos do relatório de discos não coincidir
com os vértices da malha, se um perfil não corresponder a uma aresta da malha ou
se as células `K3` excederem a grade declarada. Essas travas evitam comparar
artefatos de execuções incompatíveis.

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/analyze_augmented_mesh_resilience.py \
  --faces geoespacial/outputs/augmented_mesh_topodata_faces/triangular_faces_topodata.csv.gz \
  --profiles geoespacial/outputs/augmented_mesh_topodata_profiles/profiles.csv.gz \
  --disk-report geoespacial/reports/augmented_continental_coverage_grid/summary.json \
  --output geoespacial/outputs/augmented_mesh_resilience/vertex_sensitivity.csv.gz \
  --report geoespacial/reports/augmented_mesh_resilience/summary.json
```

Tabela e resumo reproduziram byte a byte.
