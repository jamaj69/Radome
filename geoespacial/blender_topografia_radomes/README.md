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
subamostragem: cada célula vira um vértice, e cada quadrícula recebe uma face
quadrilateral. A coordenada Z de cada vértice é derivada diretamente da cota
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

A câmera zenital enquadra somente a região central da janela DEM, deixando uma
margem de superfície TOPODATA real ao redor da área visível. Não há extensão
plana ou extrapolação de cotas além da folha disponível.

### Visão regional dos três sítios

Para enquadrar Juiz de Fora, Anápolis e Brasília em uma única superfície, use a
grade regional subamostrada. Ela consulta as folhas disponíveis, preserva a
cota TOPODATA mais próxima em cada vértice e cria uma cena com margem, os três
radomes e as divisas BC250. Caso uma folha não esteja no acervo local, a cena
mantém uma lacuna sem faces; nunca interpola ou inventa cotas. A resolução padrão de 0,02° é deliberadamente
cartográfica (~2 km), pois uma união desses sítios em 30 m seria grande demais
para uma cena única.

A aparência da superfície é a NASA Blue Marble global já versionada. Seus UVs
são calculados de longitude/latitude pela projeção equiretangular (``u=(lon+
180)/360``, ``v=(lat+90)/180``), portanto o render usa o recorte geográfico
correto da imagem, enquanto as elevações continuam vindas do TOPODATA.

```bash
bash geoespacial/blender_topografia_radomes/render_on_host.sh --regional-terrain
```

Os parâmetros opcionais são espaçamento e margem em graus, por exemplo
`--regional-terrain 0.01 0.25`. A saída é
`build/topodata_regional_radomes.blend` e `build/topodata_regional_radomes.png`.

Para controlar integralmente o corte, informe uma moldura WGS84 explícita na
ordem `oeste sul leste norte`. Ela determina a extensão da malha, o recorte das
divisas, a câmera e os UVs da Blue Marble; assim, ampliar oeste/leste preenche
mais a largura da figura sem esticar a textura:

```bash
bash geoespacial/blender_topografia_radomes/render_on_host.sh \
  --regional-terrain 0.02 0.25 -50.0 -22.2 -45.5 -15.5
```

As folhas que cubram a moldura precisam existir localmente. Se a moldura maior
introduzir lacunas, rode primeiro o fluxo de aquisição regional e confirme as
folhas indicadas pelo relatório.

Antes desse render, complete de forma auditável as folhas ZN eventualmente
ausentes da moldura — no acervo atual, são quatro folhas oficiais ao norte da
folha `18S48_ZN`, que já estava presente:

```bash
bash geoespacial/blender_topografia_radomes/render_on_host.sh --acquire-regional-terrain
```

O comando escreve seleção, recibo com SHA-256, extração e índice em
`geoespacial/reports/topodata_regional_scene/`, preservando ZIPs e GeoTIFFs nas
áreas ignoradas de dados. ZIPs já presentes são revalidados e reutilizados; toda
folha necessária passa novamente pela extração. Em seguida, inicia o render
regional sem lacunas de dados locais.

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

Para a alternativa acelerada por `foreach_set`, que preserva o renderizador
original como referência, execute:

```bash
bash geoespacial/blender_topografia_radomes/render_on_host.sh --topodata-rs-batched 0
```

Ela grava `topodata_rs_batched.blend` e `topodata_rs_batched.png`.

Para não inicializar dois processos gráficos, o wrapper renderiza diretamente.
Durante o render, acompanhe `nvidia-smi` em outro terminal para confirmar o uso
e a memória da RTX.

## Varredura nacional por blocos TOPODATA nativos

Uma cena nacional com cada vértice a aproximadamente 30 m excede com folga a
memória de uma estação de trabalho e a VRAM da GPU. Em vez disso, o fluxo de
varredura divide **cada folha** TOPODATA em blocos adjacentes de 720×720
quadrículas (721×721 vértices), compartilhando uma borda entre blocos vizinhos.
O manifesto é leve: contém apenas os recortes e a proveniência. A ferramenta lê
uma única janela do GeoTIFF, monta sua malha no Blender com `foreach_set`,
renderiza-a e encerra o processo; o próximo bloco só é aberto em uma nova
execução. Assim, a resolução nativa é preservada localmente sem somar folhas em
RAM ou VRAM.

Exemplo: gerar o manifesto e renderizar o primeiro bloco com 720 quadrículas por
lado:

```bash
cd /home/jamaj/src/Radome
bash geoespacial/blender_topografia_radomes/render_on_host.sh --topodata-tile 720 0
```

O segundo argumento é o tamanho do bloco em quadrículas; o terceiro é seu índice
no manifesto, que é ordenado por nome de folha, linha e coluna. As saídas são
`build/topodata_tile_manifest.json`, `build/topodata_tile_<índice>.blend` e
`build/topodata_tile_<índice>.png`. Para avançar, altere apenas o índice; cada
render é independente e libera a memória ao terminar. Este mecanismo é de
visualização topográfica e não faz alegações de cobertura RF, visada ou
viabilidade de implantação.

Para percorrer uma faixa finita sem manter duas malhas abertas, informe também a
quantidade. O Blender é iniciado e finalizado uma vez por bloco:

```bash
bash geoespacial/blender_topografia_radomes/render_on_host.sh --topodata-tile-range 720 0 3
```

O comando acima renderiza somente os índices 0, 1 e 2. O lote é deliberadamente
finito: varrer as 13 mil janelas do subconjunto atualmente extraído gera muitos
arquivos e deve ser agendado por faixa, folha ou área de interesse.
