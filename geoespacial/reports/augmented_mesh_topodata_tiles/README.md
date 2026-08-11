# Folhas TOPODATA das arestas priorizadas

As 4.262 arestas com limite de curvatura foram amostradas geodesicamente a no
máximo 1 km, totalizando 166.474 amostras. Elas requerem 214 folhas presentes
no inventário oficial, com 13.311.672.320 bytes listados. Destas, 199 já estão
locais e 15 novas somam 945.815.552 bytes listados.

`03N66_ZN.zip` é requerida, mas não consta no inventário oficial congelado. A
ausência afeta 159 amostras de duas arestas e deve falhar de modo conservador.
Nenhum download ocorreu neste gate.

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/select_augmented_mesh_topodata_tiles.py \
  --graph geoespacial/outputs/augmented_candidate_graph/graph.graphml \
  --edges geoespacial/outputs/augmented_mesh_edge_priority/edges.csv.gz \
  --manifest geoespacial/data/manifests/topodata_altitude_tiles.json \
  --existing-dir geoespacial/data/raw/topodata/radio_link_routes \
  --output geoespacial/reports/augmented_mesh_topodata_tiles/selection.json \
  --spacing-km 1
```

A seleção reproduziu byte a byte e não constitui evidência de visada ou RF.
