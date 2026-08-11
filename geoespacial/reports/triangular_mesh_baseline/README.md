# Linha de base da malha triangular

O primeiro experimento aplica Delaunay aos 131 candidatos atuais depois de
projetá-los numa Lambert azimutal equivalente esférica centrada em 54°W, 15°S.
Ele produz 244 faces e cruza cada uma com a grade continental e os inventários
de SMP, radiodifusão e endpoints cadastrais de radioenlace.

As arestas disponíveis ainda são somente os limites geométricos por curvatura
do grafo de candidatos. Portanto, as classes são deliberadamente:

- 22 `triangle_k3_curvature_pending`;
- 6 `triangle_two_edge_curvature_pending`;
- 216 `triangle_sparse_curvature_pending`.

Não há ainda qualquer face `triangle_k3_confirmed`. A envoltória Delaunay contém
10.567 das 11.363 células e aproximadamente 92,92% da área amostrada, mas isso
representa pertença à malha, não cobertura por radar ou visada.

Dentro da envoltória ficaram 100.967 sítios SMP, 11.608 radiodifusores e 480
endpoints. Quase todas as faces possuem SMP (243) e 237 possuem radiodifusão,
enquanto somente 118 possuem endpoints. São associações geométricas, não arestas
`illuminates`.

A face Belo Horizonte--Aeroporto Elias Breder--Aeroporto Doutor Saulo Vilela é
um exemplo `K3` preliminar relativamente regular: ângulo mínimo 52,3°, razão
entre arestas 1,17 e 1.023/130/10 objetos SMP/radiodifusão/endpoints. Já a face
São Paulo--Congonhas--Jundiaí, embora densa, tem ângulo mínimo 4,9° e razão 8,22,
mostrando por que qualidade geométrica deve ser restrição independente.

Execução, a partir de `geoespacial/`:

```bash
/home/python/pyenv/bin/python analyze_triangular_mesh_baseline.py \
  --graphml outputs/candidate_ranking/graph.graphml \
  --grid outputs/continental_coverage_grid/continental_grid.csv.gz \
  --output-dir outputs/triangular_mesh_baseline \
  --report reports/triangular_mesh_baseline/summary.json
```

CSV gzip e GeoJSON reproduziram byte a byte em duas execuções.
