# Seleção TOPODATA para lacunas continentais

O seletor cruza as 1.732 células cujo centro não está em nenhum raio geométrico
preliminar com o inventário oficial TOPODATA. Centro e quatro cantos internos de
cada célula de 0,25° evitam perder uma folha atravessada pela célula.

Resultado: 141 arquivos disponíveis, 8.737.783.808 bytes listados e nenhuma
folha requerida ausente do índice oficial. A seleção é apenas um plano de
aquisição; não comprova relevo favorável, *viewshed* ou cobertura RF.

```bash
/home/python/pyenv/bin/python select_topodata_gap_tiles.py \
  --grid outputs/continental_coverage_grid/continental_grid.csv.gz \
  --manifest data/manifests/topodata_altitude_tiles.json \
  --output reports/topodata_gap_tiles/selection.json
```
