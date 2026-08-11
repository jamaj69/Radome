# Rede municipal de radiodifusão

O pacote oficial da Anatel contém 35.126 registros com coordenadas válidas.
Somente os 18.285 registros `C4 — Canal Licenciado` entram no grafo preliminar
de iluminadores ativos. Canais vagos, suspensos, pendentes ou aguardando atos e
licenciamento permanecem no inventário, sem serem interpretados como fontes RF
operacionais.

Os registros licenciados foram agregados em 11.921 coordenadas. Todos os sítios
receberam código IBGE: 18.253 registros foram conciliados por nome e UF e 32 por
junção espacial com a BC250. Há 117 sítios com mais de um código municipal nos
registros co-localizados; o código modal foi usado e o conflito preservado para
revisão.

Os produtos completos estão em `outputs/broadcast_network/`:

- `broadcast_site_nodes.csv`;
- `broadcast_municipal_network.graphml`;
- `summary.json`.

Serviço licenciado não garante iluminação útil ao radar passivo. O refinamento
deverá considerar ERP, frequência, canal, polarização, altura, diagrama,
orientação, ocupação temporal, relevo e geometria biestática.
