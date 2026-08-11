# Política de manipulação reproduzível das bases geoespaciais

## Regra obrigatória

Toda aquisição, extração, leitura, limpeza, normalização, cruzamento espacial,
agregação, classificação, cálculo e exportação de bases deste subprojeto deve
ser implementada por script Python versionado. Dados brutos em `data/raw/` são
imutáveis: uma execução pode criá-los por download atômico, mas nunca corrigi-los
manualmente no lugar.

Comandos interativos de QGIS, planilhas, editores, `curl`, `wget`, `unzip`,
`ogr2ogr`, `jq`, `sed` ou `awk` podem ser usados para diagnóstico, mas não são
etapas autoritativas do pipeline nem podem ser a única forma de produzir um
artefato. Se um diagnóstico alterar a interpretação ou gerar um produto, ele
deve ser convertido em Python antes de fechar o gate.

Arquivos shell só podem preparar ambiente ou chamar um ponto de entrada Python;
não podem transformar dados. `run_pipeline.sh` existe apenas como wrapper de
compatibilidade para `run_pipeline.py`.

## Contrato de cada script

Todo script que manipule bases deve, conforme aplicável:

1. receber caminhos e parâmetros pela linha de comando;
2. falhar explicitamente quando entrada, camada ou coluna obrigatória faltar;
3. preservar a fonte bruta e escrever em `data/processed/`, `outputs/`,
   `reports/` ou `data/manifests/`;
4. gravar codificação, CRS, unidades e semântica dos campos;
5. produzir contagens de entrada, saída, descarte, ausência e conflito;
6. usar escrita atômica para downloads e produtos críticos;
7. registrar URL, data, tamanho e SHA-256 das entradas adquiridas;
8. ser coberto por teste unitário para regras de transformação não triviais;
9. produzir resultados determinísticos quando entradas e configuração forem
   idênticas, salvo metadados temporais explicitamente identificados;
10. evitar chamadas a ferramentas externas para transformação quando houver
    binding Python adequado.

## Pontos de entrada atuais

| Operação | Script Python |
|---|---|
| aquisição HTTP genérica com hash | `acquire_http.py` |
| extração ZIP segura e inventariada | `extract_zip.py` |
| aquisição de camadas WFS DECEA | `acquire_decea_wfs.py` |
| inventário ANAC/Anatel/DECEA | `inventory_infrastructure.py` |
| inventário VOR/NDB/DME | `inventory_decea_navaids.py` |
| inventário SMP | `inventory_smp.py` |
| auditoria espectral Anatel | `audit_anatel_spectrum.py` |
| auditoria streaming do pacote geral Anatel | `audit_anatel_general.py` |
| modelo canônico sítio--antena--emissão SMP | `build_canonical_smp.py` |
| modelo canônico de emissores fixos SARC/SCM | `build_canonical_fixed_emitters.py` |
| rede municipal SMP | `build_municipal_emitter_network.py` |
| rede municipal de radiodifusão | `build_broadcast_network.py` |
| inventário TOPODATA | `inventory_topodata.py` |
| pré-seleção BC250 | `preselect_bc250.py` |
| grafo de candidatos | `build_candidate_graph.py` |
| otimização discreta | `optimize_sites.py` |
| pipeline preliminar | `run_pipeline.py` |
| comparação byte a byte de duas execuções | `verify_reproducibility.py` |

## Gates futuros

Nenhuma nova camada será marcada `downloaded_verified`, `integrated` ou
`selection_ready` se sua aquisição e transformação não puderem ser repetidas
por um desses scripts ou por um novo script Python versionado. Projetos QGIS e
cenas Blender serão saídas de inspeção e comunicação; não serão a fonte única
de nenhuma coordenada, classificação ou resultado quantitativo.
