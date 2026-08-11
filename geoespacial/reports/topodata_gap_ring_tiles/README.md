# Folhas TOPODATA dos anéis das lacunas

`selection.json` registra a seleção reproduzível das folhas que contêm os
centros das 1.732 sementes e 36 amostras geodésicas em cada anel de 5, 10 e
25 km. A seleção avalia 188.788 pontos e requer 175 folhas presentes no
inventário oficial: 143 já estavam no diretório bruto compartilhado e 32 são
novas, com 1.945.108.480 bytes listados.

O nome `05N51_ZN.zip` é requerido geometricamente, mas não consta no inventário
oficial congelado. A ausência afeta três pontos de anel da única semente
`gap-seed:cell:+003.8750:-0051.1250`. Esses pontos devem continuar incompletos e
falhar de modo conservador até que uma fonte oficial equivalente seja integrada;
não se deve interpolá-los silenciosamente nem atribuir clareza positiva.

Comando:

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/select_topodata_gap_ring_tiles.py \
  --seeds geoespacial/outputs/topodata_gap_seeds/gap_seeds.csv.gz \
  --manifest geoespacial/data/manifests/topodata_altitude_tiles.json \
  --existing-dir geoespacial/data/raw/topodata/radio_link_routes \
  --output geoespacial/reports/topodata_gap_ring_tiles/selection.json \
  --azimuth-count 36
```

Esta seleção apenas fecha a disponibilidade de amostragem do terreno. Ela não
confirma sítio, proeminência topográfica, visada, cobertura ou iluminação RF.

## Aquisição

`acquisition.json` registra 175 ZIPs validados por CRC e SHA-256, totalizando
10.819.492.567 bytes reais, sem falhas ou pendências. Depois do download das 32
folhas novas, uma segunda execução revalidou e marcou todos os 175 arquivos
como `reused`, demonstrando a retomabilidade sem nova transferência.

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/acquire_topodata_route_tiles.py \
  --selection geoespacial/reports/topodata_gap_ring_tiles/selection.json \
  --output-dir geoespacial/data/raw/topodata/radio_link_routes \
  --report geoespacial/reports/topodata_gap_ring_tiles/acquisition.json
```

A ausência externa `05N51_ZN.zip` continua registrada em
`missing_archive_names_from_selection`; ela não é contada entre os 175 arquivos
disponíveis solicitados pelo recibo.
