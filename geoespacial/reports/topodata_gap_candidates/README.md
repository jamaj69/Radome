# Triagem multiescala dos candidatos de lacuna

As 1.732 sementes foram avaliadas em 36 azimutes, nos anéis de 5, 10 e 25 km.
A clareza de anel é a cota da semente menos a maior cota amostrada no anel; não
é proeminência topográfica. A pontuação preliminar combina 50% de altitude, 30%
de relevo relativo celular e 20% de clareza positiva normalizada.

A consolidação gulosa a 10 km preservou 1.484 candidatos e atribuiu todas as
1.732 células a um candidato. Após adquirir e indexar as folhas de borda, há
1.732/1.732/1.731 sementes com anel completo a 5/10/25 km. A única semente
incompleta é `gap-seed:cell:+003.8750:-0051.1250`: ela tem 33/36 amostras no
anel de 25 km porque `05N51_ZN.zip` não consta no inventário oficial. Ela
permanece explicitamente marcada e não recebe contribuição otimista desse anel.

Duas execuções produziram CSV gzip e GeoJSON byte a byte idênticos. O resultado
é triagem preliminar, não *viewshed*, visada, proeminência, cobertura RF ou
aprovação de sítio.

```bash
/home/python/pyenv/bin/python consolidate_topodata_gap_candidates.py \
  --seeds outputs/topodata_gap_seeds/gap_seeds.csv.gz \
  --terrain-root data/processed/topodata/radio_link_routes \
  --terrain-index reports/topodata_gap_ring_tiles/index.geojson \
  --output-dir outputs/topodata_gap_candidates \
  --report reports/topodata_gap_candidates/summary.json \
  --minimum-distance-km 10 --azimuth-count 36
```
