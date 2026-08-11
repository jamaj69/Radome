# Auditoria inicial do pacote geral da Anatel

Esta etapa lê diretamente o ZIP oficial, sem extrair seus 10,45 GB, e audita os
seis membros priorizados pelo gate M2E:

- `Estacoes_SARC.csv`;
- `Estacoes_Banda_Larga_Fixa.csv`;
- `Estacoes_Telefonia_Fixa.csv`;
- `Estacoes_SLE.csv`;
- `Estacoes_SLP.csv`;
- `Estacoes_Mosaico_STEL.csv`.

O relatório versionado está em `summary.json`; os registros normalizados e
reproduzíveis ficam em `outputs/anatel_general_audit/`.

## Regra de classificação RF

A direção explícita `Transmissão` ou `Recepção` tem precedência. Quando ela não
existe, somente classes exclusivamente transmissoras, exclusivamente receptoras
ou repetidoras fornecem evidência secundária. Classes fixas/base sem direção e
valores `N/I` ou `Usuário informou errado` permanecem desconhecidos. Portanto,
`active_potential_emitter_records` é um conjunto conservador de candidatos, não
uma confirmação de operação radioelétrica atual.

## Resultado

- SARC: 8.774 registros, todos com coordenadas e código IBGE; 5.926 ativos e
  4.228 ativos com evidência de transmissão/repetição. Há 4.583 frequências
  utilizáveis entre 153,02 e 12.751 MHz, mas nenhuma potência ou designação de
  emissão utilizável nessa versão.
- Banda larga fixa/SCM: 7.513 registros, todos com coordenadas e código IBGE;
  3.703 ativos e 1.850 ativos com direção de transmissão. Há 3.706 frequências
  e potências utilizáveis e 3.514 designações com largura decodificável. Os
  3.799 registros sem direção permanecem desconhecidos.
- Telefonia fixa/STFC: 589 registros, 75 ativos, todos georreferenciados, porém
  sem frequência, potência, classe ou direção utilizável; essa camada ainda não
  pode fornecer iluminadores RF.
- SLE: 119.058 registros, 118.968 ativos e 59.484 ativos com direção explícita
  de transmissão. A camada tem 115.458 coordenadas válidas e código IBGE em
  todos os registros; 118.968 linhas possuem designação decodificável, potência
  e altura, com frequências úteis entre 148 e 927,77 MHz. As 118.490 estações
  móveis e a simetria entre 59.484 linhas de recepção e 59.484 de transmissão
  exigem preservar o papel cadastral sem transformar cada registro em sítio
  fixo ou inferir automaticamente uma ponta de enlace.
- SLP: 10.580.778 registros, 10.542.118 ativos, 5.271.059 ativos com direção
  Tx e 10.451.584 coordenadas válidas. As direções são simétricas, com
  5.290.389 linhas Tx e 5.290.389 Rx, e 9.495.200 linhas são estações móveis.
  O intervalo cadastral de 0,01 a 4.699.875 MHz contém valores que exigem
  validação de unidade e outliers antes de qualquer uso quantitativo.
- Mosaico-STEL: 10.817.122 registros. Ele não constitui uma camada independente:
  reproduz a contagem SLP de 10.580.778 e também agrega as contagens completas
  de SLE, SARC, SCM e STFC, além de
  64.948 registros de radioenlaces STFC, 35.424 SCM e 38 SMP. Portanto, não pode
  ser somado aos arquivos específicos. A equivalência linha a linha será testada
  no próximo gate antes de definir a regra de deduplicação.

Nenhum radioenlace foi pareado nesta etapa. O próximo gate separa as três
famílias explícitas de enlaces presentes no consolidado, identifica quais chaves
cadastrais podem relacionar as pontas e valida geometria e reciprocidade de
frequência antes de criar qualquer aresta.

## Reprodução

```bash
/home/python/pyenv/bin/python audit_anatel_general.py \
  --source data/raw/anatel/estacoes_licenciadas.zip \
  --output-dir outputs/anatel_general_audit \
  --report reports/anatel_general_audit/summary.json
```
