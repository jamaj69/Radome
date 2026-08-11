# Malha triangular aumentada

A triangulação Delaunay usa os 1.615 candidatos, incluindo os 1.484 derivados
das folhas TOPODATA. Foram geradas 3.209 faces: 2.724 com três arestas de
curvatura pendentes, 27 com duas e 458 esparsas. Nenhuma face tem visada
confirmada.

A envoltória contém 11.174 das 11.363 células continentais, ou 98,41% da área
ponderada. Dentro das faces há 101.500 sítios SMP, 11.703 radiodifusores e 481
endpoints cadastrais; 629/411/135 faces contêm ao menos um objeto de cada classe,
respectivamente. Essas relações são pertença geométrica, não `illuminates`,
visada nem detectabilidade.

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/analyze_triangular_mesh_baseline.py \
  --graphml geoespacial/outputs/augmented_candidate_graph/graph.graphml \
  --grid geoespacial/outputs/augmented_continental_coverage_grid/continental_grid.csv.gz \
  --output-dir geoespacial/outputs/augmented_triangular_mesh \
  --report geoespacial/reports/augmented_triangular_mesh/summary.json
```

CSV gzip, GeoJSON e resumo reproduziram byte a byte.
