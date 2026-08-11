# Visualização Blender: Terra curva e três candidatos RADOME

Este subprojeto cria uma cena de comunicação, não uma análise operacional. A Terra é esférica e cada marcador é colocado em latitude, longitude e cota; os três sítios são escolhidos da classificação reproduzível com cota mínima de 1.000 m e pelo menos 500 incidências geométricas combinadas de SMP, radiodifusão e pontas de enlace.

Essas incidências não demonstram iluminação RF, visada, Fresnel, licenciamento ou viabilidade. A esfera fornece o contexto de curvatura terrestre; uma superfície TOPODATA contínua nacional permanece uma extensão futura, pois as folhas atualmente extraídas foram selecionadas para rotas, não para um mosaico nacional de renderização.

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/blender_topografia_radomes/select_visual_sites.py --ranking geoespacial/outputs/candidate_ranking/candidate_ranking.csv.gz --output geoespacial/blender_topografia_radomes/build/selected_sites.json
blender -b --python geoespacial/blender_topografia_radomes/render_curved_earth_radomes.py -- --selection geoespacial/blender_topografia_radomes/build/selected_sites.json --blend geoespacial/blender_topografia_radomes/build/earth_radomes.blend --render geoespacial/blender_topografia_radomes/build/earth_radomes.png
```
