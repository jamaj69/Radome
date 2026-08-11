# Sementes TOPODATA nas lacunas continentais

Para cada uma das 1.732 células cujo centro não pertence a nenhum raio
geométrico preliminar, o script seleciona o centro do pixel TOPODATA válido de
maior cota. Também registra mínimo, média e relevo relativo dentro da célula.

Todas as células receberam uma semente. As cotas variam de 29,389 m a
2.131,380 m e o relevo relativo celular de 24,169 m a 2.062,120 m. Duas
execuções produziram CSV gzip e GeoJSON byte a byte idênticos.

`relative_relief_m` é apenas máximo menos mínimo na célula de 0,25°. Não é
proeminência topográfica. As sementes não comprovam acesso, estabilidade,
licenciamento, *viewshed*, visada entre nós ou iluminação RF.

```bash
/home/python/pyenv/bin/python generate_topodata_gap_seeds.py \
  --grid outputs/continental_coverage_grid/continental_grid.csv.gz \
  --terrain-root data/processed/topodata/radio_link_routes \
  --terrain-index reports/topodata_gap_tiles/index.geojson \
  --output-dir outputs/topodata_gap_seeds \
  --report reports/topodata_gap_seeds/summary.json \
  --resolution-deg 0.25
```
