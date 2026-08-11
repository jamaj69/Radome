# Visualização Blender: Terra curva e três candidatos RADOME

Este subprojeto cria uma cena de comunicação, não uma análise operacional. A Terra é esférica e cada marcador é colocado em latitude, longitude e cota; os três sítios são escolhidos da classificação reproduzível com cota mínima de 1.000 m e pelo menos 500 incidências geométricas combinadas de SMP, radiodifusão e pontas de enlace.

Essas incidências não demonstram iluminação RF, visada, Fresnel, licenciamento ou viabilidade. A esfera fornece o contexto de curvatura terrestre; uma superfície TOPODATA contínua nacional permanece uma extensão futura, pois as folhas atualmente extraídas foram selecionadas para rotas, não para um mosaico nacional de renderização.

A renderização padrão é deliberadamente cartográfica: usa a textura Blue Marble,
limites estaduais discretos, fronteiras terrestres internacionais do Brasil e
somente três marcadores. Os rótulos são painéis claros voltados para a câmera,
com texto preto e linhas-guia. Malhas TOPODATA locais e pontos de altitude são
diagnósticos separados, habilitados apenas pelos parâmetros explícitos abaixo;
eles não são adequados à escala continental.

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/blender_topografia_radomes/select_visual_sites.py --ranking geoespacial/outputs/candidate_ranking/candidate_ranking.csv.gz --output geoespacial/blender_topografia_radomes/build/selected_sites.json
/usr/bin/python3 geoespacial/blender_topografia_radomes/export_geographic_overlays.py --bc250 geoespacial/data/raw/ibge/bc250/bc250_2026-03-03.gpkg --ranking geoespacial/outputs/candidate_ranking/candidate_ranking.csv.gz --output geoespacial/blender_topografia_radomes/build/overlays.json
blender -b --python geoespacial/blender_topografia_radomes/render_curved_earth_radomes.py -- --selection geoespacial/blender_topografia_radomes/build/selected_sites.json --overlays geoespacial/blender_topografia_radomes/build/overlays.json --terrain geoespacial/blender_topografia_radomes/build/topodata_terrain.json --texture geoespacial/blender_topografia_radomes/assets/nasa_blue_marble_topography_bathymetry_april_5400x2700.jpg --blend geoespacial/blender_topografia_radomes/build/earth_radomes.blend --render geoespacial/blender_topografia_radomes/build/earth_radomes.png --overview
```

Para inspeção técnica local, acrescente `--include-local-terrain`. Para depurar
os pontos de cota preliminares, acrescente `--show-altitude-points`; esse último
modo não deve ser usado no render continental de apresentação.
