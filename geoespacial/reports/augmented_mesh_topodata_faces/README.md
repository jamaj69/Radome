# Faces da malha reclassificadas por TOPODATA

As 3.209 faces foram reclassificadas pelas três arestas, sem alterar as
incidências geométricas de iluminadores. Em `k=1`, 2.033 faces têm três arestas
com LOS topográfico, 410 têm duas e 766 são esparsas. Em `k=4/3`, os totais são
2.248, 320 e 641. Três faces tocam ao menos uma das duas arestas sem terreno.

`triangle_k3_terrain_los` significa somente três perfis topograficamente livres
sob o modelo indicado. Não inclui frequência, Fresnel, orçamento de enlace,
RF, `illuminates` ou estado operacional.

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/reclassify_augmented_mesh_faces_topodata.py \
  --faces geoespacial/outputs/augmented_triangular_mesh/triangular_faces.csv.gz \
  --mesh-geojson geoespacial/outputs/augmented_triangular_mesh/triangular_mesh.geojson \
  --profiles geoespacial/outputs/augmented_mesh_topodata_profiles/profiles.csv.gz \
  --output-dir geoespacial/outputs/augmented_mesh_topodata_faces \
  --report geoespacial/reports/augmented_mesh_topodata_faces/summary.json
```

Tabela gzip, GeoJSON e resumo reproduziram byte a byte.
