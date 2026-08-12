# Visualização Blender: Terra curva e três candidatos RADOME

Este subprojeto cria uma cena de comunicação, não uma análise operacional. A Terra é esférica e cada marcador é colocado em latitude, longitude e cota; os três sítios são escolhidos da classificação reproduzível com cota mínima de 1.000 m e pelo menos 500 incidências geométricas combinadas de SMP, radiodifusão e pontas de enlace.

Essas incidências não demonstram iluminação RF, visada, Fresnel, licenciamento ou viabilidade. A esfera fornece o contexto de curvatura terrestre; uma superfície TOPODATA contínua nacional permanece uma extensão futura, pois as folhas atualmente extraídas foram selecionadas para rotas, não para um mosaico nacional de renderização.

A renderização padrão é deliberadamente cartográfica: usa a textura Blue Marble,
limites estaduais discretos, fronteiras terrestres internacionais do Brasil e
somente três marcadores. Os rótulos são texto preto ampliado, voltado para a
câmera, com fino halo branco de contraste e posicionado junto ao marcador. A saída padrão é 2400×1500, com 128 amostras Eevee. Malhas TOPODATA locais e pontos de altitude são
diagnósticos separados, habilitados apenas pelos parâmetros explícitos abaixo;
eles não são adequados à escala continental.

```bash
cd /home/jamaj/src/Radome
/home/python/pyenv/bin/python geoespacial/blender_topografia_radomes/select_visual_sites.py --ranking geoespacial/outputs/candidate_ranking/candidate_ranking.csv.gz --output geoespacial/blender_topografia_radomes/build/selected_sites.json
/usr/bin/python3 geoespacial/blender_topografia_radomes/export_geographic_overlays.py --bc250 geoespacial/data/raw/ibge/bc250/bc250_2026-03-03.gpkg --ranking geoespacial/outputs/candidate_ranking/candidate_ranking.csv.gz --output geoespacial/blender_topografia_radomes/build/overlays.json
blender -b --python geoespacial/blender_topografia_radomes/render_curved_earth_radomes.py -- --selection geoespacial/blender_topografia_radomes/build/selected_sites.json --overlays geoespacial/blender_topografia_radomes/build/overlays.json --terrain geoespacial/blender_topografia_radomes/build/topodata_terrain.json --texture geoespacial/blender_topografia_radomes/assets/nasa_blue_marble_topography_bathymetry_april_5400x2700.jpg --blend geoespacial/blender_topografia_radomes/build/earth_radomes.blend --render geoespacial/blender_topografia_radomes/build/earth_radomes.png --overview
```

No terminal do host — isto é, fora de qualquer sandbox de agente — prefira o
wrapper abaixo. Ele reexporta as entradas e entrega o processo final ao Blender,
permitindo que o Eevee use o contexto gráfico e a GPU disponíveis para o seu
usuário:

```bash
cd /home/jamaj/src/Radome
bash geoespacial/blender_topografia_radomes/render_on_host.sh
```

Para inspeção técnica local, acrescente `--include-local-terrain`. Para depurar
os pontos de cota preliminares, acrescente `--show-altitude-points`; esse último
modo não deve ser usado no render continental de apresentação.

## Superfície 3D TOPODATA

O modo local solicita uma janela de até 721×721 células TOPODATA por sítio, sem
subamostragem: cada célula vira um vértice, e cada quadrícula recebe duas faces
triangulares. A coordenada Z de cada vértice é derivada diretamente da cota
TOPODATA da respectiva célula. A cena usa coordenadas locais em metros e uma
exageração vertical de 1,5×, explicitamente visual; portanto, o relevo é
geométrico, enquanto a escala vertical não é uma medição de engenharia.
Quando o sítio está junto à borda de uma folha, a janela é reduzida ao maior
quadrado centrado disponível, em vez de extrapolar a folha.

Para criar e renderizar a inspeção do sítio de Juiz de Fora (índice 0):

```bash
cd /home/jamaj/src/Radome
bash geoespacial/blender_topografia_radomes/render_on_host.sh --local-terrain 0
```

Use os índices `1` para Anápolis e `2` para Brasília. As saídas são
`build/topodata_local_terrain.blend` e `build/topodata_local_terrain.png`.
O arquivo `.blend` preserva a superfície, a grade e o marcador simbólico de
radome para inspeção e ajustes no Blender.

A vista ampliada também recorta do BC250/IBGE as divisas municipais (linhas
escuras) e estaduais (linhas amarelas). Elas são sobreposições cartográficas
acima do relevo, sem alterar as cotas do DEM.

### Visão zenital com ortoimagem

Por padrão, a visão zenital usa a textura global NASA Blue Marble já versionada
no subprojeto. Ela é livre e fornece cor contextual, mas seus 5.400×2.700 pixels
não têm resolução espacial adequada para uma janela TOPODATA local. Uma
ortoimagem da mesma janela geográfica pode substituí-la por UV sobre a
superfície deformada. Forneça uma imagem que você esteja autorizado a usar e que
cubra exatamente a janela exportada; o programa não baixa nem redistribui
imagens do Google. Para a visão zenital de Anápolis:

```bash
bash geoespacial/blender_topografia_radomes/render_on_host.sh --top-down 1
```

Opcionalmente, substitua a textura NASA por uma ortoimagem local:

```bash
bash geoespacial/blender_topografia_radomes/render_on_host.sh --top-down 1 /caminho/para/ortofoto_anapolis.png
```

O resultado é `build/topodata_top_down.blend` e `build/topodata_top_down.png`.
O radome permanece acima do terreno e a câmera ortográfica fica no zênite.

### Textura TOPODATA RS

O modo `--topodata-rs` baixa de forma validada as folhas oficiais `RS` de relevo
sombreado correspondentes às três folhas `ZN`, extrai os GeoTIFFs e recorta cada
textura à janela exata da malha. Assim, `ZN` determina os vértices e `RS` a
aparência sombreada alinhada, sem alegar cobertura do solo ou imagem de satélite.

```bash
bash geoespacial/blender_topografia_radomes/render_on_host.sh --topodata-rs 0
```

Para não inicializar dois processos gráficos, o wrapper renderiza diretamente.
Durante o render, acompanhe `nvidia-smi` em outro terminal para confirmar o uso
e a memória da RTX.
