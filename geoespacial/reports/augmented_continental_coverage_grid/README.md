# Cobertura geométrica continental aumentada

Com os 131 candidatos originais e 1.484 candidatos TOPODATA, todos os 11.363
centros da grade continental de 0,25° ficam dentro de ao menos um raio
geométrico preliminar. Há 64 células em cobertura única e 11.299 em cobertura
redundante; a fração ponderada por área é 100%.

Esse fechamento é somente incidência do centro da célula em discos limitados
por curvatura. Não comprova continuidade dentro da célula, terreno livre,
*viewshed*, Fresnel, iluminação RF ou serviço operacional. A instância preserva
separadamente o ranking dos 131 candidatos originais e a pontuação de terreno
dos candidatos TOPODATA, sem fingir equivalência entre essas escalas.

```bash
cd /home/jamaj/src/Radome
PYTHONPATH=geoespacial /usr/bin/python3 geoespacial/build_continental_coverage_grid.py \
  --graphml geoespacial/outputs/augmented_candidate_graph/graph.graphml \
  --bc250 geoespacial/data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
  --output-dir geoespacial/outputs/augmented_continental_coverage_grid \
  --report geoespacial/reports/augmented_continental_coverage_grid/summary.json \
  --resolution-deg 0.25
```

Duas execuções produziram tabela gzip, GeoJSON, instância e resumo byte a byte
idênticos.
