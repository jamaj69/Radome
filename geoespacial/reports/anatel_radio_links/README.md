# Famílias explícitas de radioenlaces Anatel

O extrator percorre o produto normalizado Mosaico-STEL e conserva somente os
serviços explicitamente denominados radioenlace. Nenhuma ponta é pareada.

## Resultado

| Família | Registros | Estações | Coordenadas | Tx | Rx |
|---|---:|---:|---:|---:|---:|
| STFC | 64.948 | 10.020 | 9.983 | 32.474 | 32.474 |
| SCM | 35.424 | 7.190 | 6.954 | 17.712 | 17.712 |
| SMP | 38 | 4 | 4 | 19 | 19 |

Todos os números de estação aparecem com registros Tx e Rx. Isso é evidência de
estrutura cadastral bidirecional, mas não identifica por si só a estação remota:
uma mesma estação pode ter várias frequências, antenas e destinos. O produto
mantém `pairing_status: not_performed` até que sejam recuperadas do membro bruto
as chaves cadastrais adicionais e verificadas reciprocidade espectral e geometria.

## Reprodução

```bash
/home/python/pyenv/bin/python extract_anatel_radio_links.py \
  --source outputs/anatel_general_audit/mosaico_stel.csv.gz \
  --output outputs/anatel_radio_links/emissions.csv.gz \
  --report reports/anatel_radio_links/summary.json
```
