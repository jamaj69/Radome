# Modelo canônico das emissões SMP

Este produto normaliza o cadastro oficial de estações SMP da Anatel na relação
`sitio_fisico`--`antena`--`emissao`, sem descartar nenhuma linha da fonte.

A base não fornece um identificador físico inequívoco de antena. Por isso,
`antenna_id` representa explicitamente um **proxy cadastral** formado por
estação, setor e sítio aproximado por coordenadas arredondadas a cinco casas.
Ele não deve ser interpretado como contagem comprovada de estruturas radiantes.

Produtos derivados, regeneráveis e não autoritativos:

- `outputs/canonical_smp/sites.csv.gz`;
- `outputs/canonical_smp/antennas.csv.gz`;
- `outputs/canonical_smp/emissions.csv.gz`;
- `outputs/canonical_smp/summary.json`.

O resumo versionado está em `summary.json`. A reprodução usa:

```bash
/home/python/pyenv/bin/python build_canonical_smp.py \
  --smp data/raw/anatel/estacoes_smp.zip \
  --output-dir outputs/canonical_smp \
  --report reports/canonical_smp/summary.json
```

O gate exige `zero_loss: true`, todas as emissões ligadas a sítio e proxy de
antena, e hashes idênticos em duas execuções consecutivas do pipeline.
