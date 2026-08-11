# Seleção TOPODATA para lacunas continentais

O seletor cruza as 1.732 células cujo centro não está em nenhum raio geométrico
preliminar com o inventário oficial TOPODATA. Centro e quatro cantos internos de
cada célula de 0,25° evitam perder uma folha atravessada pela célula.

Resultado: 141 arquivos disponíveis, 8.737.783.808 bytes listados e nenhuma
folha requerida ausente do índice oficial. Todos foram adquiridos e validados:
8.743.661.110 bytes reais, CRC ZIP íntegro e SHA-256 individual no recibo
`acquisition.json`. Uma segunda passagem local reutilizou e revalidou as 141
folhas sem tráfego de rede. Isso ainda não comprova relevo favorável, *viewshed*
ou cobertura RF.

Os 141 GeoTIFFs foram extraídos e inspecionados, totalizando 10.964.218.374
bytes. O índice `index.geojson` registra extensão, resolução e hash de cada
folha sob o nome `topodata_gap_tiles`. Uma segunda passagem revalidou todos os
GeoTIFFs como reutilizados.

```bash
/home/python/pyenv/bin/python select_topodata_gap_tiles.py \
  --grid outputs/continental_coverage_grid/continental_grid.csv.gz \
  --manifest data/manifests/topodata_altitude_tiles.json \
  --output reports/topodata_gap_tiles/selection.json

/home/python/pyenv/bin/python acquire_topodata_route_tiles.py \
  --selection reports/topodata_gap_tiles/selection.json \
  --output-dir data/raw/topodata/radio_link_routes \
  --report reports/topodata_gap_tiles/acquisition.json

/home/python/pyenv/bin/python extract_topodata_route_tiles.py \
  --receipt reports/topodata_gap_tiles/acquisition.json \
  --archive-dir data/raw/topodata/radio_link_routes \
  --target-dir data/processed/topodata/radio_link_routes \
  --report reports/topodata_gap_tiles/extraction.json \
  --index reports/topodata_gap_tiles/index.geojson \
  --index-name topodata_gap_tiles
```
