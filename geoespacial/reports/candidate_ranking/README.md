# Ordenação multicritério preliminar

Este gate ordena os 131 candidatos de capitais e aeroportos em três cenários,
sem selecionar locais para implantação:

- `balanced`: 40% altitude, 25% logística urbana, 24% contexto RF e 11%
  conectividade geométrica;
- `altitude_priority`: 60% altitude, 18% logística urbana, 12% contexto RF e
  10% conectividade;
- `logistics_rf_priority`: 25% altitude, 35% logística urbana, 30% contexto RF
  e 10% conectividade.

Logística urbana combina quantidade de cidades e ocupação de oito setores
azimutais. SMP, radiodifusão e endpoints são transformados com `log1p` e
normalizados separadamente, evitando que a classe mais numerosa domine as
demais. A classificação robusta ordena a média das posições nos três cenários,
usando a amplitude das posições como primeiro desempate.

O Aeroporto Embaixador Walther Moreira Salles ficou em primeiro nos três
cenários. Anápolis, São Paulo, Belo Horizonte e Brasília completam os cinco
primeiros robustos. O resultado é sensível à concentração urbana do Sudeste e
não mede cobertura nacional, obstrução do terreno, iluminadores efetivamente
recebidos, restrições fundiárias ou viabilidade de implantação.

Execução, a partir de `geoespacial/`:

```bash
/usr/bin/python3 rank_candidate_sites.py \
  --graphml outputs/unified_candidate_context/graph.graphml \
  --bc250 data/raw/ibge/bc250/bc250_2026-03-03.gpkg \
  --output-dir outputs/candidate_ranking \
  --report reports/candidate_ranking/summary.json
```

O GraphML, o GeoJSON e a tabela gzip reproduziram byte a byte em duas execuções.
