# Perfis TOPODATA das arestas da malha

As 4.262 arestas com limite de curvatura foram perfiladas a no máximo 1 km,
com 15 m AGL em cada ponta. Em `k=1`, 3.653 têm linha de visada topográfica,
607 são obstruídas e 2 não têm terreno completo. Em `k=4/3`, os totais são
3.849, 411 e 2. As duas ausências correspondem às rotas afetadas pela folha
oficial ausente `03N66_ZN.zip` e falham de modo conservador.

Não foi calculada zona de Fresnel porque nenhuma frequência de enlace entre
radomes foi selecionada. Logo, `los_clear` não significa enlace RF utilizável,
`illuminates`, cobertura ou aresta operacional.

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/profile_augmented_mesh_edges_topodata.py \
  --graph geoespacial/outputs/augmented_candidate_graph/graph.graphml \
  --edges geoespacial/outputs/augmented_mesh_edge_priority/edges.csv.gz \
  --terrain-root geoespacial/data/processed/topodata/radio_link_routes \
  --terrain-index geoespacial/reports/augmented_mesh_topodata_tiles/index.geojson \
  --output geoespacial/outputs/augmented_mesh_topodata_profiles/profiles.csv.gz \
  --report geoespacial/reports/augmented_mesh_topodata_profiles/summary.json \
  --height-m 15 --spacing-km 1
```

Duas execuções produziram perfil e resumo byte a byte idênticos.
