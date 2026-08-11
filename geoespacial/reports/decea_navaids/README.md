# Auxílios de navegação DECEA/ICA

## Resultado da aquisição

As camadas oficiais `ICA:vor`, `ICA:ndb`, `ICA:dme` e `ICA:navaids` foram
baixadas diretamente do WFS GEOAISWEB em 10 de agosto de 2026. As feições
declaram emenda `2026-08-06` e emenda futura `2026-09-03`; por isso o conjunto
deve ser tratado como recorte de informação aeronáutica sujeito a atualização,
não como cadastro permanente.

| Camada | Feições | Coordenadas | Elevação | Informação RF |
|---|---:|---:|---:|---|
| VOR | 77 | 77 | 76 | frequência em 77; 112–117,7 MHz |
| NDB | 24 | 24 | 19 | frequência em 24; 114,3–407 kHz |
| DME | 173 | 173 | 158 | canal em 173; canal 24–124 |
| `navaids` agregada | 124 | 124 | 30 | tipo/relação, sem frequência |

A camada VOR contém 59 VOR convencionais e 18 DVOR. A camada agregada contém
73 `VOR_DME`, 45 `ILS_DME`, quatro `ILS` e dois `LOC_DME`.

## Interpretação dos campos

- VOR: `latitude`, `longitude`, `elevation`, `elevationu`, `frequency` e
  `frequnits` fornecem posição, elevação e portadora diretamente.
- NDB: `geolat`, `geolong`, `valelev`, `elevationu`, `valfreq` e `uomfreq`
  fornecem posição, elevação parcial e portadora diretamente.
- DME: `geolat`, `geolong`, `valelev` e `valchannel` fornecem posição, elevação
  parcial e canal. `valghostfr` é a frequência VOR/ILS pareada, não a portadora
  UHF transmitida pelo DME; a frequência DME deverá ser derivada por uma tabela
  oficial canal--frequência versionada.
- `navaids`: localiza conjuntos ILS/VOR/DME, mas não substitui as camadas
  específicas para espectro.

Os campos de potência e altura de antena existem no esquema VOR, porém estão
vazios em todas as 77 feições atuais. A banda/designação de emissão NDB está
preenchida em apenas uma das 24 feições. Assim, temos posição, elevação quase
completa e portadora/canal, mas ainda não potência, diagrama, altura radiante ou
largura ocupada suficientes para um modelo de iluminação RF completo.

## Limites e próxima integração

O WFS inclui feições próximas fora do território brasileiro, como auxílios de
FIRs vizinhas. Antes de criar nós definitivos, as camadas devem ser recortadas
pela máscara continental, associadas ao código IBGE por interseção espacial e
reconciliadas entre `navaids`, VOR, NDB e DME por identificador, nome e
proximidade.

Elevações ausentes serão preenchidas provisoriamente pelo MDE e marcadas com
proveniência distinta; não serão confundidas com altitude aeronáutica oficial.
O inventário reprodutível e os hashes estão em
`data/manifests/decea_navaids_inventory.json`.

```bash
/home/python/pyenv/bin/python inventory_decea_navaids.py \
  --input-dir data/raw/decea/navaids \
  --output data/manifests/decea_navaids_inventory.json
```

