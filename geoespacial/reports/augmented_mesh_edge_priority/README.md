# Prioridade de perfis da malha aumentada

As 3.209 faces produzem 4.823 arestas únicas. A fila coloca primeiro os limites
de curvatura, a incidência em faces `K3`, a presença das três classes
geométricas de infraestrutura, a qualidade angular e a menor distância.

Há 4.262 arestas com limite de curvatura disponível, 4.228 incidentes em ao
menos uma face `K3` pendente e 289 com as três classes SMP, radiodifusão e
endpoint nas faces adjacentes. Esses valores só priorizam o perfilamento; não
confirmam visada, iluminação RF ou aresta operacional.

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/prioritize_augmented_mesh_edges.py \
  --graph geoespacial/outputs/augmented_candidate_graph/graph.graphml \
  --faces geoespacial/outputs/augmented_triangular_mesh/triangular_faces.csv.gz \
  --output geoespacial/outputs/augmented_mesh_edge_priority/edges.csv.gz \
  --report geoespacial/reports/augmented_mesh_edge_priority/summary.json
```

A fila e o resumo reproduziram byte a byte.
