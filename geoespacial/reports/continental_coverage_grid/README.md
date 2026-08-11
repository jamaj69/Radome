# Grade continental e lacunas geométricas

A grade usa resolução de 0,25° e conserva centros de célula contidos nos 27
polígonos de UF da BC250, limitados ao território continental a oeste de 34°W.
Cada célula registra os candidatos cujo raio geométrico preliminar contém seu
centro. A fração nacional também é ponderada pela área esférica aproximada das
células.

Dos 11.363 centros continentais, 9.631 estão dentro de ao menos um raio e 1.732
estão fora de todos. A cobertura ponderada por área é 84,46%. Há 1.863 células
com cobertura única e 7.768 com redundância de dois ou mais candidatos.

As maiores quantidades de células descobertas são:

- Pará: 817;
- Amazonas: 337;
- Mato Grosso: 330;
- Amapá e Piauí: 73 cada;
- Roraima: 44.

O arquivo `coverage_instance.json` é compatível com `optimize_sites.py`, mas
preserva deliberadamente todas as células requeridas. Portanto, o otimizador
deve rejeitar a instância enquanto existirem as 1.732 células sem candidato —
isso é uma constatação de insuficiência, não erro do solver.

Execução, a partir de `geoespacial/`:

```bash
/usr/bin/python3 build_continental_coverage_grid.py \
  --graphml outputs/candidate_ranking/graph.graphml \
  --bc250 data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
  --output-dir outputs/continental_coverage_grid \
  --report reports/continental_coverage_grid/summary.json \
  --resolution-deg 0.25
```

Tabela gzip, GeoJSON e instância discreta reproduziram byte a byte em duas
execuções. Incidência do centro no raio não representa *viewshed*, cobertura RF,
continuidade espacial dentro da célula ou viabilidade operacional.
