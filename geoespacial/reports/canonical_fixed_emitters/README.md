# Emissores fixos SARC/SCM no esquema canônico

Esta etapa migra ao modelo `sitio_fisico`--`antena`--`emissao` somente registros
ativos de SARC e banda larga fixa/SCM com evidência cadastral de transmissão ou
repetição. A partição é exaustiva: cada linha auditada é selecionada ou recebe
um motivo exclusivo de exclusão (`not_active`, `receiver_only`,
`unknown_rf_role` ou `invalid_coordinates`).

## Resultado

- 16.287 registros de entrada particionados sem perdas;
- 6.078 emissões selecionadas: 4.228 SARC e 1.850 SCM;
- 3.335 sítios aproximados e 3.995 proxies cadastrais de antena;
- 1 conflito de código municipal preservado;
- SARC: 2.362 sítios e 2.743 proxies de antena; nenhuma emissão
  quantitativamente pronta, pois potência é ausente e
  2.762 selecionadas também não possuem frequência;
- SCM: 973 sítios e 1.252 proxies de antena; 1.849 das 1.850 emissões
  selecionadas têm frequência, potência e altura;
  duas não têm designação de emissão, mas isso não elimina o registro.

O marcador `quantitative_rf_ready` significa apenas presença de frequência,
potência e altura de antena. Não autoriza criar `illuminates`: ainda faltam
validação regulatória, máscara espectral, geometria e propagação.

O nível `antena` é um proxy formado por estação e atributos de antena no sítio
arredondado. Ele não comprova a identidade física da estrutura radiante.

## Reprodução

```bash
/home/python/pyenv/bin/python build_canonical_fixed_emitters.py \
  --sarc outputs/anatel_general_audit/sarc.csv.gz \
  --fixed-broadband outputs/anatel_general_audit/fixed_broadband.csv.gz \
  --output-dir outputs/canonical_fixed_emitters \
  --report reports/canonical_fixed_emitters/summary.json
```
