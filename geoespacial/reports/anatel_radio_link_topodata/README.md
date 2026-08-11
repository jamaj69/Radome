# Perfis TOPODATA dos candidatos de radioenlace

O recálculo aplica aos 328 candidatos alinhados a mesma interpolação geodésica,
passo máximo de 1 km, modelos de curvatura (`k=1` e `k=4/3`) e requisito de 60%
da primeira zona de Fresnel usados na triagem Terrarium. Somente o provedor de
elevação foi substituído pelos GeoTIFFs TOPODATA/INPE.

| Classe | Terrarium k=1 | TOPODATA k=1 | TOPODATA k=4/3 |
|---|---:|---:|---:|
| Fresnel 60% livre | 218 | 247 | 257 |
| somente visada geométrica | 69 | 59 | 50 |
| terreno/curvatura obstruídos | 40 | 21 | 20 |
| terreno ausente | 1 | 1 | 1 |

A rota ausente é `anatel_link_group:4558a672e5ede6fe58a0c97d`, com 137 de 218
amostras sem cobertura devido à folha `26S48_ZN.zip`, que não consta no índice
oficial. Nenhum valor foi interpolado através dessa lacuna.

As alturas são o máximo cadastral por ponta e constituem limite superior
otimista, não altura física verificada. Portanto, `pairing_status` continua
`not_performed`: estes resultados não criam arestas no grafo.

Produtos:

- `summary.json`: contagens, parâmetros, proveniência e transições por classe;
- `../../outputs/anatel_radio_link_topodata/groups.csv.gz`: métricas por candidato
  (o diretório `outputs/` é local e reproduzível pelo script versionado).

Duas execuções consecutivas produziram os mesmos SHA-256:

- CSV gzip: `1d437ab8c04e82c2c53abfc7afd203a56416dbee4770ef9cdda1b93944520aa5`;
- resumo JSON: `689fce99ea265401c8c93a543c42ccc8489a731853f9e2df30e710f79ceb2803`.
