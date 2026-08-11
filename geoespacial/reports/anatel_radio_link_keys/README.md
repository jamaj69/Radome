# Chaves cadastrais brutas dos radioenlaces

O extrato bruto recupera as chaves omitidas pelo normalizador geral para as
100.410 linhas STFC/SCM/SMP previamente selecionadas. A correspondência usa o
número original da linha e compara campos cadastrais e valores numéricos.

Todas as 100.410 linhas foram equivalentes, sem divergências. Fistel, ato de RF,
códigos de homologação e de produto da antena e do transmissor estão presentes
em todas elas. Presença não implica unicidade nem identifica automaticamente a
contraponta; `pairing_status` permanece `not_performed`.

```bash
/home/python/pyenv/bin/python extract_anatel_radio_link_keys.py \
  --source data/raw/anatel/estacoes_licenciadas.zip \
  --normalized outputs/anatel_radio_links/emissions.csv.gz \
  --output outputs/anatel_radio_link_keys/records.csv.gz \
  --report reports/anatel_radio_link_keys/summary.json
```
