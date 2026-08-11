# Roadmap geoespacial da rede RADOME

**Projeto pai:** artigo técnico bilíngue RADOME, em `projeto/`.

**Marcos ativos acoplados:** M2E — fechamento das camadas oficiais de emissões;
e M3 — infraestrutura aeronáutica e estratégica. A governança e o gate de
incorporação científica estão em `SUBPROJETO.md`; a matriz de completude RF
está em `CAMADAS_EMISSOES_OFICIAIS.md`.

**Checkpoint de retomada:** `STATUS_ATUAL.md`. Os esquemas canônicos SMP e de
emissores fixos SARC/SCM estão concluídos com partições e cardinalidades
verificadas; SLE, SLP e Mosaico-STEL já foram auditados, e as três famílias
explícitas de radioenlace foram isoladas sem pareamento.

## Objetivo e regra de inventário

O fluxo deve produzir uma seleção continental auditável do menor conjunto de
radomes, respeitando cobertura, conectividade visual, relevo, logística e
disponibilidade de iluminadores. Cada camada recebe um estado controlado:

- `identified`: fonte oficial localizada;
- `downloaded_verified`: arquivo baixado, tamanho e hash verificados;
- `inventoried`: esquema, contagem e qualidade conhecidos;
- `municipally_linked`: objetos etiquetados com código IBGE;
- `integrated`: nós e arestas gerados;
- `validated`: conflitos tratados e amostras verificadas;
- `selection_ready`: adequada à otimização;
- `pending`: trabalho ainda não executado;
- `blocked_public_source`: falta fonte pública oficial suficiente.

Os estados detalhados e hashes ficam em `data/manifests/`; relatórios pequenos
em `reports/`; dados brutos em `data/raw/`; produtos volumosos em `outputs/`.
Toda transição de estado deve ser produzida por script Python conforme
`POLITICA_REPRODUTIBILIDADE.md`; manipulação manual não fecha gate.

## Inventário atual de camadas

| Tema/camada | Fonte autoritativa | Estado atual | Quantidade/observação | Próxima ação |
|---|---|---|---|---|
| Limites municipais | IBGE BC250 2025 | integrated | 5.571 polígonos | validar área contra área territorial oficial |
| Sedes municipais | IBGE BC250 2025 | integrated | 5.571 pontos | substituir altitude preliminar |
| População municipal | IBGE Censo 2022, variável 93 | integrated | 5.570 municípios | incorporar fonte pós-2022 para Boa Esperança do Norte |
| Capitais e cidades | IBGE BC250 2025 | integrated/preliminary | 27 capitais; cidades usadas na logística | calcular cidades realmente visíveis |
| Estados e país | IBGE BC250 2025 | downloaded_verified | polígonos | usar em máscaras e relatórios |
| Relevo pontual | IBGE BC250 2025 | integrated/preliminary | picos e pontos cotados | reconciliar com MDE |
| Elevação preliminar | Mapzen Terrarium | integrated/preliminary | cache z8 | substituir por TOPODATA |
| MDE nacional | TOPODATA/INPE | augmented_mesh_edges_prioritized | 4.823 arestas únicas ordenadas; 4.262 com limite de curvatura, 4.228 incidentes em K3 pendente e 289 com três classes geométricas de infraestrutura | selecionar folhas atravessadas e perfilar terreno em lotes |
| MDE local detalhado | IBGE/SGB/estaduais | pending | cobertura variável | adquirir somente para finalistas |
| Torres celulares SMP | Anatel | canonical_integrated | 3.284.526 emissões, 105.726 sítios e 282.623 proxies cadastrais de antena; perda zero; 23 conflitos municipais preservados | usar junção espacial para revisar conflitos e buscar parâmetros radiométricos físicos |
| Radiodifusão TV/RTV/FM/OM/RTR | Anatel | integrated/spectrum_partial | 35.126 registros; 18.285 licenciados; centro/canal disponíveis, largura ausente | integrar canalização regulatória; revisar 117 conflitos e ERP |
| Grafo geoespacial unificado | IBGE/Anatel/BC250 | composed_nonoperational | 123.846 nós/119.158 arestas; municípios, SMP, radiodifusão, endpoints e candidatos; zero arestas operacionais | vincular candidatos aos municípios e contar infraestrutura RF por raio |
| SARC | Anatel, pacote geral | canonical_spectrum_partial | 4.228 emissões ativas em esquema canônico; nenhuma quantitativamente pronta por ausência de potência; 2.762 sem frequência | buscar complemento oficial e manter fora de `illuminates` quantitativo |
| Banda larga fixa/SCM | Anatel, pacote geral | canonical_integrated | 1.850 emissões Tx ativas; 1.849 com frequência, potência e altura presentes; duas sem designação | validar regulamentação/propagação antes de `illuminates` |
| Telefonia fixa/STFC | Anatel, pacote geral | georeferenced_not_rf_ready | 589 registros, 75 ativos, sem frequência, potência, classe ou direção utilizável | manter apenas como infraestrutura até obter complemento oficial |
| SLE | Anatel, pacote geral | inventoried/unpaired | 119.058 registros; 59.484 Tx ativos; 115.458 coordenadas válidas; 118.490 linhas móveis | decidir integração somente após comparação com SLP/STEL; não criar sítios fixos para móveis |
| SLP | Anatel, pacote geral | inventoried/unpaired | 10.580.778 linhas; 5.271.059 Tx ativos; 9.495.200 linhas móveis | validar unidades/outliers e não promover móveis a sítios fixos |
| Mosaico-STEL | Anatel, pacote geral | inventoried/aggregate_unpaired | 10.817.122 linhas; reproduz a contagem SLP e agrega 64.948 enlaces STFC, 35.424 SCM e 38 SMP | não somar; testar equivalência, extrair famílias e avaliar chaves/reciprocidade/geometria |
| Estações terrenas/VSAT | Anatel | identified/pending | nova base oficial de estações terrenas em bloco | baixar, inventariar e reconciliar com SLP/SCM/STFC |
| Aeródromos públicos | ANAC | downloaded_verified | 496 | conciliar com BC250 e DECEA |
| Aeródromos privados | ANAC | downloaded_verified | 3.856 | conciliar e classificar uso logístico |
| Helipontos | ANAC | downloaded_verified | 1.595 | integrar por município |
| Helideques | ANAC | downloaded_verified | 203; arquivo atual sem coordenadas suficientes | não usar como ponto continental sem complemento |
| Aeroportos e pistas BC250 | IBGE | integrated/preliminary | 104 complexos; 3.492 pontos de pouso | validar códigos, elevação e status setorial |
| Informação aeronáutica WFS | DECEA/ICA GEOAISWEB | partially_downloaded | 421 tipos; 14 selecionados; VOR/NDB/DME/navaids baixados | baixar as dez camadas restantes e congelar versão |
| Obstáculos OPEA | DECEA/ICA | identified | camada `ICA:opea` | baixar, etiquetar e avaliar alturas |
| VOR/NDB/DME/navaids | DECEA/ICA | downloaded_verified | 77 VOR, 24 NDB, 173 DME e 124 relações agregadas; coordenadas completas, elevação parcial | recortar Brasil, etiquetar município e derivar portadora DME por fonte oficial |
| CTR/TMA/ZIDA | DECEA/ICA | identified | espaço aéreo, não emissores | usar como contexto e restrição |
| Radares aeronáuticos | DECEA/FAB, quando públicos | pending | não inferir de aeródromos | localizar fonte oficial e parâmetros publicáveis |
| Radares meteorológicos | Cemaden/SIPAM/INMET e parceiros | identified/pending | inventário oficial com coordenadas e bandas localizado | extrair tabela, verificar versão e integrar como emissores ativos separados |
| Bases aéreas | FAB/DECEA | blocked_public_source | nomes parciais não bastam | classificar somente com fonte oficial |
| Comandos aéreos | FAB | blocked_public_source | ausentes na BC250 | localizar cadastro público oficial |
| Energia elétrica | IBGE BC250 | downloaded_verified | linhas, usinas e subestações | integrar como logística e viabilidade |
| Rodovias/ferrovias/hidrovias | IBGE BC250 | downloaded_verified | redes nacionais | calcular acessibilidade e custo logístico |
| Portos/terminais | IBGE BC250 | downloaded_verified | pontos e linhas | integrar onde relevante |
| Hidrografia/inundação | IBGE BC250 | downloaded_verified | rios, massas d'água, ilhas e áreas inundáveis | aplicar restrições territoriais |
| Mineração e alterações antrópicas | IBGE BC250 | downloaded_verified | polígonos/pontos | avaliar restrições e acessos |
| Unidades de conservação e terras protegidas | MMA/ICMBio/Funai | pending | ainda não adquiridas | baixar e aplicar restrições legais |
| Uso/cobertura do solo | MapBiomas/IBGE | pending | ainda não adquirido | avaliar implantação e obstrução local |
| Clima, vento e descargas | INMET/INPE | pending | ainda não adquirido | usar no refinamento estrutural e operacional |
| Ilhas oceânicas | IBGE/SGB/DHN | deferred | fora da otimização continental | estudo independente por arquipélago |

## Modelo canônico do grafo

### Tipos de nó

- `municipio`: código IBGE, nome, UF, sede `x/y/z`, área e população;
- `candidato_radome`: relevo, altura, proeminência, horizonte, *viewshed*,
  cidades visíveis, logística, restrições e pontuação;
- `sitio_fisico`: coordenada, código municipal, conflitos e proveniência;
- `antena`: proxy cadastral por estação, setor e sítio, com confiança explícita;
- `emissao`: uma linha SMP preservada, com tecnologia, espectro e proveniência;
- `radiodifusao`: serviço, canal, frequência, ERP, entidade, classe, categoria e
  finalidade;
- `aerodromo`, `heliporto`, `navaid`, `radar`, `energia`, `porto` e outros tipos
  setoriais, sempre com fonte e confiança.

### Tipos de aresta

- `located_in`: objeto contido em município;
- `line_of_sight`: visada topográfica confirmada entre candidatos;
- `curvature_candidate`: ligação limitada por horizonte, ainda sem relevo;
- `covers`: candidato cobre célula, município ou volume aéreo sob hipótese dada;
- `illuminates`: emissor pode iluminar região/candidato após análise RF;
- `accessible_by`: relação logística com infraestrutura de transporte;
- `powered_by`: proximidade/viabilidade de energia;
- `same_physical_site`: co-localização reconciliada entre cadastros.

Toda aresta analítica deve registrar método, parâmetros, data e estado de
validação. `located_in` não implica visibilidade; `illuminates` não implica eco
detectável; `curvature_candidate` não implica visada.

## Fases e gates

### Fase 0 — requisitos e proveniência — concluída

Entregas:

- escopo continental e exceção insular documentados;
- critérios de mínimo número, altitude, cidades e conectividade registrados;
- diretório `geoespacial/`, manifestos e documentação criados.

Gate: requisitos recuperáveis do Git e fontes com URL, estado e hash quando
baixadas.

### Fase 1 — base territorial municipal — concluída preliminarmente

Entregas:

- municípios, sedes, população, área e altitude preliminar;
- código IBGE como chave canônica;
- nós municipais e produtos GraphML/CSV.

Gate pendente para validação: substituir `z` por TOPODATA, validar áreas e
resolver população do município criado após o Censo 2022.

### Fase 2 — inventário de iluminadores — em andamento

Concluído:

- SMP agregado e ligado a municípios;
- TV/RTV/FM/OM/RTR filtrados por status, agregados e ligados a municípios.

Pendente:

- identificar e parear radioenlaces no pacote geral Anatel;
- incorporar ao grafo SMP geração, tecnologia, centro Tx e largura necessária;
- radiodifusão: integrar largura canalizada por ato técnico, revisar conflitos e
  interpretar unidades de ERP/HCI;
- cruzar co-localizações SMP–radiodifusão;
- adquirir outros serviços RF relevantes sem confundi-los com fontes ativas.

Reanálise: o pacote geral Anatel já disponível deve ser auditado antes de se
procurar um arquivo isolado de radioenlaces. SLP/STEL provavelmente contém
pontas licenciadas de enlace e oferece potência/antena, mas a seleção deve ser
demonstrada por serviço, classe e direção. O gate detalhado M2E está em
`CAMADAS_EMISSOES_OFICIAIS.md`.

Gate: cada sítio com código IBGE, status operacional explícito, registros de
origem preservados e conflitos quantificados.

### Fase 3 — infraestrutura aeronáutica e estratégica — ativa

Passos:

1. importar ANAC e WFS DECEA congelado por ciclo AIRAC;
2. reconciliar ICAO/CIAD, nome, coordenada e proximidade;
3. integrar pistas, helipontos, OPEA, VOR, NDB e navaids;
4. buscar fontes públicas de radares, bases e comandos;
5. impedir classificação militar baseada apenas em nome.

Gate: proveniência oficial por objeto e separação entre aeródromo, auxílio RF,
radar e instalação militar.

### Fase 4 — relevo nacional e candidatos — pendente

Passos:

1. selecionar folhas TOPODATA pela máscara continental;
2. baixar, verificar e mosaicar por regiões;
3. derivar cumeadas, máximos locais, declividade e proeminência;
4. remover áreas inviáveis ou legalmente restritas;
5. produzir candidatos multi-escala com altitude e acesso.

Gate: MDE versionado, resolução declarada e candidatos reproduzíveis.

### Fase 5 — visada e cobertura 3D — pendente

Passos:

1. calcular *viewshed* para 150 m, 3.000 m e 10.000 m;
2. gerar perfis entre candidatos e confirmar `line_of_sight`;
3. considerar curvatura e `k=4/3`, com análise de sensibilidade;
4. calcular zona de Fresnel por faixa;
5. contar municípios/cidades realmente visíveis por azimute;
6. separar cobertura territorial de detectabilidade RF.

Gate: mapas de lacunas e matriz de visada confirmada, com parâmetros completos.

### Fase 6 — iluminação RF passiva — pendente

Passos:

1. associar emissores às faixas do receptor;
2. modelar ERP/EIRP, altura, polarização, diagrama e terreno;
3. estimar disponibilidade temporal e densidade espectral;
4. construir geometria bistática emissor–alvo–radome;
5. manter testes de emissor direto separados de reflexões;
6. produzir uma pontuação de diversidade e qualidade de iluminadores.

Gate: `illuminates` sustentado por modelo RF documentado, sem alegar detecção
operacional antes de simulação ou medição.

### Fase 7 — logística, energia e restrições — pendente

Passos:

- integrar vias, energia, cidades, portos e restrições ambientais/territoriais;
- calcular acessibilidade sem impor distância máxima arbitrária;
- pontuar cidades ao redor e abaixo dos candidatos;
- registrar disponibilidade de manutenção, segurança e comunicação.

Gate: cada candidato com vetor de custos e restrições auditável.

### Fase 8 — otimização mínima e análise de sensibilidade — pendente

Passos:

1. montar células/volumes obrigatórios por altitude;
2. resolver mínimo número de sítios com conectividade;
3. desempatar por relevo, visibilidade, iluminadores e logística;
4. variar MDE, refração, pesos e resolução;
5. publicar alternativas de mesma cardinalidade e causas das lacunas.
6. testar em paralelo a heurística de malha triangular cooperativa definida em
   `HEURISTICA_MALHA_TRIANGULAR.md`;
7. comparar discos e tesselação por cardinalidade, lacunas, redundância 2/3,
   faces `K3`, robustez e diversidade de iluminadores.

Gate: solução reproduzível, cobertura quantificada e nenhum sítio continental
isolado; a heurística triangular permanece experimental até superar ou esclarecer
os compromissos da linha de base por discos.

### Fase 9 — refinamento, QGIS, Blender e artigo — pendente

Passos:

- refinar finalistas com MDE e cartografia de maior resolução;
- exportar GeoPackage/QGIS com simbologia e metadados;
- gerar terrenos locais e cenas 3D no Blender;
- realizar inspeção local e levantamento geodésico;
- redigir método, resultados, limitações e sensibilidade em português e inglês.

Gate: todos os números do artigo ligados a commit, configuração, fonte e
relatório reproduzível.

### Fase 10 — arquipélagos e ilhas oceânicas — adiada

Cada grupo próximo será otimizado separadamente para um único radome local,
sem exigir visada com a rede continental. A integração nacional ocorrerá apenas
depois da validação de cada estudo insular.

## Próxima sequência recomendada

1. **concluído:** definir o esquema canônico sítio--antena--emissão e incorporar
   as portadoras SMP já auditadas;
2. **concluído:** auditar os arquivos menores SARC, banda larga fixa e telefonia
   fixa antes de SLE/SLP/STEL;
3. **concluído:** migrar ao esquema canônico os registros ativos SARC/SCM com
   evidência de transmissão ou repetição, preservando as lacunas RF;
4. **concluído:** auditar SLE sem parear enlaces;
5. **concluído:** auditar SLP/STEL e demonstrar a sobreposição do consolidado;
6. **concluído:** extrair enlaces explícitos STFC/SCM/SMP sem pareá-los;
7. **concluído:** recuperar chaves, testar reciprocidade, azimute e terreno z8
   sem criar arestas;
8. **concluído:** 154 folhas TOPODATA selecionadas, baixadas, extraídas e
   indexadas; 328 rotas recalculadas, mantendo a folha ausente explícita;
9. **concluído:** associar os 131 candidatos aos municípios BC250 e contar SMP,
   radiodifusão e endpoints dentro do raio geométrico, sem alegar visibilidade;
10. **concluído:** ordenar candidatos em três cenários normalizados e registrar
    a amplitude de posições como análise de sensibilidade;
11. **concluído:** construir grade continental de 0,25°, matriz candidato--célula
    e diagnóstico de 1.732 células descobertas;
12. **em andamento:** selecionar, adquirir e extrair TOPODATA para as lacunas
    continentais foi concluído (141 GeoTIFFs, 10.964.218.374 bytes, nenhuma
    falha); 1.732 sementes máximas por célula foram geradas sem ausência e
    reproduzem byte a byte; a triagem a 5/10/25 km reteve preliminarmente 1.484
    candidatos, mas 69 sementes exigem folhas de borda para completar os anéis;
    completar a aquisição e depois repetir a triangulação e medir faces `K3`;
13. normalizar radiodifusão e integrar VOR/NDB/DME por município;
14. baixar e congelar as dez camadas DECEA ainda pendentes e reconciliar ANAC,
   BC250 e DECEA;
15. adquirir VSAT e o inventário oficial de radares meteorológicos;
16. selecionar e baixar TOPODATA continental por região;
17. reconstruir o grafo unificado município--sítio--antena--emissão--aeródromo--
   candidato;
18. integrar restrições territoriais e iniciar *viewshed* regional.

## Artefatos obrigatórios por execução

Cada fase quantitativa deve produzir:

- manifesto de entrada com hashes e datas;
- configuração congelada;
- comando ou script reexecutável;
- resumo JSON legível por máquina;
- tabela CSV/GeoPackage com proveniência por objeto;
- mapa ou grafo de inspeção;
- contagem de ausências, conflitos e descartes;
- versão do software e commit Git;
- texto de limitações pronto para adaptação ao artigo.

Aquisição e transformação também devem indicar o script Python autoritativo.
Arquivos shell, projetos QGIS e cenas Blender podem orquestrar ou visualizar,
mas não podem ser a única implementação de qualquer operação sobre as bases.
