# Seleção geoespacial de sítios RADOME

Este diretório contém o fluxo reproduzível para selecionar o menor conjunto de
sítios que satisfaça uma meta explícita de cobertura do espaço aéreo brasileiro.
O resultado é uma triagem de engenharia, não uma autorização de implantação.

O escopo ativo é somente o território continental. Arquipélagos e ilhas
oceânicas ficam fora da otimização nacional: cada grupo próximo será estudado
depois como um caso independente, com um único radome em seu ótimo local.

## Hipóteses controladas

- a cobertura é avaliada a 150 m, 3 000 m e 10 000 m acima do terreno;
- cada sítio continental deve ter visada direta para pelo menos outro sítio;
- ilhas oceânicas são componentes independentes e estão dispensadas da
  conectividade visual com a rede continental;
- candidatos são extraídos primeiro de cumeadas, máximos locais e pontos de
  grande proeminência relativa;
- altitude absoluta não basta: área visível, população/cidades visíveis em
  vários azimutes e quantidade de enlaces também entram na pontuação;
- proximidade logística é um peso positivo, sem distância máxima eliminatória;
- curvatura terrestre e refração padrão devem ser incluídas nos testes de
  horizonte; a zona de Fresnel depende da faixa e será avaliada separadamente;
- cobertura geométrica não implica desempenho de detecção. Potência do
  iluminador, RCS, ruído, RFI, ganho e perdas pertencem a uma etapa posterior.

As hipóteses numéricas ficam em `site_selection.json`. Alterações que mudem o
número ótimo de sítios devem modificar esse arquivo, registrar a justificativa e
produzir uma nova execução identificada.

## Fontes previstas

| Dado | Fonte principal | Uso |
|---|---|---|
| Elevação nacional | TOPODATA/INPE, GeoTIFF | cumeadas, horizonte e *viewshed* |
| Cartografia nacional | IBGE BC250, GeoPackage | cidades, vias, limites e hidrografia |
| MDE detalhado | IBGE 1:25.000/1:50.000 | refinamento onde houver cobertura |
| Altitudes de controle | IBGE BDG/RAAP | verificação vertical local |
| Ilhas oceânicas | IBGE, SGB e DHN | máscara e refinamento insular |

Arquivos originais volumosos pertencem a `data/raw/` e não devem ser
versionados. Metadados, URLs, hashes e licenças pertencem a
`data/manifests/` e devem ser versionados. Produtos intermediários ficam em
`data/processed/`; tabelas e mapas finais, em `outputs/`.

O inventário oficial atual contém 556 arquivos TOPODATA de altitude numérica,
com aproximadamente 32,19 GiB compactados. Por isso a seleção continental de
folhas deve preceder o download; baixar todo o índice sem máscara desperdiçaria
armazenamento e tempo de processamento.

## Etapas

1. baixar e verificar as fontes registradas no manifesto;
2. reprojetar cada região para um sistema métrico apropriado;
3. gerar cumeadas, máximos locais e proeminência em múltiplas escalas;
4. calcular cobertura nas três altitudes de referência;
5. calcular cidades visíveis e sua distribuição azimutal;
6. construir o grafo de visada entre candidatos continentais;
7. resolver cobertura mínima com conectividade local obrigatória;
8. refinar candidatos com MDE de maior resolução e restrições territoriais;
9. exportar GeoPackage para QGIS e malhas locais para Blender.

O núcleo discreto já pode ser executado independentemente do QGIS:

```bash
/home/python/pyenv/bin/python optimize_sites.py instancia.json --output solucao.json
```

A instância contém células obrigatórias e candidatos com as células cobertas,
arestas de visada, condição de exceção insular e pontuação secundária. O modelo
MILP minimiza primeiro a quantidade de sítios e usa a pontuação apenas para
desempatar soluções com a mesma cardinalidade.

## Critério de parada

Não se declarará “cobertura nacional” sem informar, para cada altitude de
referência, a fração coberta, as lacunas, a resolução do MDE e as hipóteses de
propagação. Se 100% não for alcançável, o resultado será uma curva entre número
de sítios e cobertura, em vez de ocultar a lacuna.
